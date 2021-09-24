import sys

from src.program.commands.class_commands.class_commands_helper import ClassCommandsHelper
from src.program.commands.class_commands.class_renamer import ClassRenamer
from src.program.commands.class_commands.class_remover import ClassRemover
from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.program.commands.class_commands.class_adder import ClassAdder
from src.functions import create_arguments_parser
from src.program.program_command_helper import ProgramCommandHelper
from src.commandrunners.cmake.cmake import CMake
from src.config.config import Config
from src.config.target_config_manager import TargetConfigManager


class ClassCommand:
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
        return ClassCommandsHelper.get_class_file_program_usage()

    def add(self, target):
        parser = create_arguments_parser(usage=ClassCommandsHelper.get_class_add_command_usage())
        parser.add_argument('class_name', help='class to add', metavar='<class_name>')
        parser.add_argument('-n', '--namespace', help=ProgramCommandHelper.NAMESPACE_PARAM_HELP, type=str)

        command_line_arguments = self.parse_arguments(parser)
        class_name = command_line_arguments.class_name

        namespace = target['namespace']
        if command_line_arguments.namespace:
            namespace = command_line_arguments.namespace

        if target['tests'] is True:
            header_file_content = self.class_files_helper.get_header_file_content(class_name, namespace, self.config.test_template_file_path)
        else:
            header_file_content = self.class_files_helper.get_header_file_content(class_name, namespace, self.config.class_template_file_path)

        adder = ClassAdder(self.target_config_manager, self.class_files_helper)
        adder.add_header(class_name, target, self.config, namespace, header_file_content)
        adder.add_source(class_name, target, self.config, namespace)

        self.cmake.configure()

    def rename(self, target):
        parser = create_arguments_parser(usage=ClassCommandsHelper.get_class_rename_command_usage())
        parser.add_argument('old_class_name', help='class files location to move from', metavar='<old_class_name>')
        parser.add_argument('new_class_name', help='new class files location', metavar='<new_class_name>')

        command_line_arguments = self.parse_arguments(parser)
        old_class_name = command_line_arguments.old_class_name
        new_class_name = command_line_arguments.new_class_name

        renamer = ClassRenamer(self.config, self.target_config_manager, self.class_files_helper)
        renamer.rename_header(old_class_name, new_class_name, target)
        renamer.rename_source(old_class_name, new_class_name, target)

        self.cmake.configure()

    def remove(self, target):
        parser = create_arguments_parser(usage=ClassCommandsHelper.get_class_remove_command_usage())
        parser.add_argument('class_name', help='class files to remove', metavar='<class_name>')

        command_line_arguments = self.parse_arguments(parser)
        class_name = command_line_arguments.class_name

        remover = ClassRemover(self.config, self.target_config_manager, self.class_files_helper)
        remover.remove_header(class_name, target)
        remover.remove_source(class_name, target)

        self.cmake.configure()

    def parse_arguments(self, parser):
        return parser.parse_args(sys.argv[5:])
