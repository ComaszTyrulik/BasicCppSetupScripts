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


class SourceCommand:
    FILE_EXTENSION = '.cpp'

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
        return ClassCommandsHelper.get_single_file_program_usage(ProgramCommandHelper.COMMAND_NAME_SOURCE)

    def add(self, target):
        program_usage = ClassCommandsHelper.get_add_command_usage(ProgramCommandHelper.COMMAND_NAME_SOURCE, self.FILE_EXTENSION)
        parser = create_arguments_parser(usage=program_usage)
        parser.add_argument('source_name', help='source file to add', metavar='<source_name>')
        parser.add_argument('-n', '--namespace', help=ProgramCommandHelper.NAMESPACE_PARAM_HELP, type=str)

        command_line_arguments = self.parse_arguments(parser)
        source_name = command_line_arguments.source_name

        namespace = target['namespace']
        if command_line_arguments.namespace:
            namespace = command_line_arguments.namespace

        adder = ClassAdder(self.target_config_manager, self.class_files_helper)
        adder.add_source(source_name, target, self.config, namespace)

        self.cmake.configure()

    def rename(self, target):
        program_usage = ClassCommandsHelper.get_rename_command_usage(ProgramCommandHelper.COMMAND_NAME_SOURCE)
        parser = create_arguments_parser(usage=program_usage)
        parser.add_argument('old_source_name', help='source location to move from', metavar='<old_source_name>')
        parser.add_argument('new_source_name', help='new source location', metavar='<new_source_name>')

        command_line_arguments = self.parse_arguments(parser)
        old_source_name = command_line_arguments.old_source_name
        new_source_name = command_line_arguments.new_source_name

        renamer = ClassRenamer(self.config, self.target_config_manager, self.class_files_helper)
        renamer.rename_source(old_source_name, new_source_name, target)

        self.cmake.configure()

    def remove(self, target):
        program_usage = ClassCommandsHelper.get_remove_command_usage(ProgramCommandHelper.COMMAND_NAME_SOURCE)
        parser = create_arguments_parser(usage=program_usage)
        parser.add_argument('source_name', help='source to remove', metavar='<source_name>')

        command_line_arguments = self.parse_arguments(parser)
        class_name = command_line_arguments.source_name

        remover = ClassRemover(self.config, self.target_config_manager, self.class_files_helper)
        remover.remove_source(class_name, target)

        self.cmake.configure()

    def parse_arguments(self, parser):
        return parser.parse_args(sys.argv[5:])
