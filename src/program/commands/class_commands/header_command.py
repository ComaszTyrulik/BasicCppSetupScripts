import sys

from src.program.commands.class_commands.class_commands_helper import ClassCommandsHelper
from src.program.commands.class_commands.class_renamer import ClassRenamer
from src.program.commands.class_commands.class_remover import ClassRemover
from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.program.commands.class_commands.class_adder import ClassAdder
from src.functions import create_arguments_parser
from src.program.program_command_helper import ProgramCommandHelper
from src.commandrunners.cmake import CMake
from src.config.config import Config
from src.config.target_config_manager import TargetConfigManager


class HeaderCommand:
    FILE_EXTENSION = '.h'

    def __init__(
        self,
        config: Config,
        cmake: CMake,
        target_config_manager: TargetConfigManager,
        class_files_helper: ClassFilesHelper
    ):
        self.config = config
        self.cmake = cmake
        self.target_config_manager = target_config_manager
        self.class_files_helper = class_files_helper

    def get_usage(self):
        return ClassCommandsHelper.get_single_file_program_usage(ProgramCommandHelper.COMMAND_NAME_HEADER)

    def add(self, target):
        program_usage = ClassCommandsHelper.get_add_command_usage(ProgramCommandHelper.COMMAND_NAME_HEADER, self.FILE_EXTENSION)
        parser = create_arguments_parser(usage=program_usage)
        parser.add_argument('header_name', help='header to add', metavar='<header_name>')
        parser.add_argument('-n', '--namespace', help=ProgramCommandHelper.NAMESPACE_PARAM_HELP, type=str)
        parser.add_argument(
            '-i',
            '--interface',
            help='when this argument is present, the header will be created as an interface, using interface template',
            action='store_true'
        )

        command_line_arguments = self.parse_arguments(parser)
        header_name = command_line_arguments.header_name

        namespace = target['namespace']
        if command_line_arguments.namespace:
            namespace = command_line_arguments.namespace

        header_file_content = None
        if command_line_arguments.interface:
            header_file_content = \
                self.class_files_helper.get_header_file_content(
                    header_name, namespace, self.config.interface_template_file_path
                )

        adder = ClassAdder(self.target_config_manager, self.class_files_helper)
        adder.add_header(header_name, target, self.config, namespace, header_file_content)

        self.cmake.configure()

    def rename(self, target):
        program_usage = ClassCommandsHelper.get_rename_command_usage(ProgramCommandHelper.COMMAND_NAME_HEADER)
        parser = create_arguments_parser(usage=program_usage)
        parser.add_argument('old_header_name', help='header location to move from', metavar='<old_header_name>')
        parser.add_argument('new_header_name', help='new header location', metavar='<new_header_name>')

        command_line_arguments = self.parse_arguments(parser)
        old_header_name = command_line_arguments.old_header_name
        new_header_name = command_line_arguments.new_header_name

        renamer = ClassRenamer(self.config, self.target_config_manager, self.class_files_helper)
        renamer.rename_header(old_header_name, new_header_name, target)

        self.cmake.configure()

    def remove(self, target):
        program_usage = ClassCommandsHelper.get_remove_command_usage(ProgramCommandHelper.COMMAND_NAME_HEADER)
        parser = create_arguments_parser(usage=program_usage)
        parser.add_argument('header_name', help='header to remove', metavar='<header_name>')

        command_line_arguments = self.parse_arguments(parser)
        class_name = command_line_arguments.header_name

        remover = ClassRemover(self.config, self.target_config_manager, self.class_files_helper)
        remover.remove_header(class_name, target)

        self.cmake.configure()

    def parse_arguments(self, parser):
        return parser.parse_args(sys.argv[5:])
