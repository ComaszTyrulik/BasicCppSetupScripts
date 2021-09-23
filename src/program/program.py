import sys
import argparse

from src.commandrunners.conan import Conan
from src.functions import create_arguments_parser
from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.target_config_manager import TargetConfigManager
from src.commandrunners.command_runner import CommandRunner
from src.program.commands.target_command import TargetCommand
from src.program.program_command_helper import ProgramCommandHelper
from src.commandrunners.cmake import CMake
from src.config.config import Config
from src.config.config_names import BuildConfigNames


class Program:
    PROGRAM_USAGE = '''{green}{program_name} <command> [<args>][-h|--help]

{white}This program let's you manage project's config and targets
as well as running cmake and conan functions.{reset}

{purple}Available commands{white}
 {green}{target}{white}     Performs operations on targets
 {green}{config}{white}     Performs operations on config
 {green}{conan}{white}      Installs project dependency using conan
 {green}{cmake}{white}      Runs CMake configuration command
'''

    def __init__(
        self,
        command_runner: CommandRunner,
        config: Config,
        cmake: CMake,
        target_config_manager: TargetConfigManager,
        class_files_helper: ClassFilesHelper,
        conan: Conan
    ):
        self.config = config
        self.command_runner = command_runner

        self.cmake = cmake
        self.build_dir_path = self.config.build_directory_path

        self.target_config_manager = target_config_manager
        self.class_files_helper = class_files_helper
        self.conan = conan

        self.create_program()

    def create_program(self):
        parser = argparse.ArgumentParser(
            usage=ProgramCommandHelper.format_text(self.PROGRAM_USAGE),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        command_choices = [
            ProgramCommandHelper.COMMAND_NAME_TARGET,
            ProgramCommandHelper.COMMAND_NAME_CONFIG,
            ProgramCommandHelper.COMMAND_NAME_CONAN,
            ProgramCommandHelper.COMMAND_NAME_CMAKE,
        ]
        parser.add_argument('command', help='command to execute', metavar='<command>', choices=command_choices)
        command_line_args = parser.parse_args(sys.argv[1:2])
        self.execute_command(command_line_args.command)

    def execute_command(self, command):
        if command == ProgramCommandHelper.COMMAND_NAME_TARGET:
            TargetCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)
            return
        if command == ProgramCommandHelper.COMMAND_NAME_CONFIG:
            self.config_command()
            return
        if command == ProgramCommandHelper.COMMAND_NAME_CONAN:
            self.conan_command()
            return
        if command == ProgramCommandHelper.COMMAND_NAME_CMAKE:
            self.cmake_command()
            return

    def config_command(self):
        usage = '''{green}{program_name} config [<args>][-h|--help]

{purple}Available arguments{white}
 {green}{targets_list}{white}   Shows a list of project's targets. Those targets can be used by {class} commands
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument(ProgramCommandHelper.PARAM_TARGETS_LIST, help='show available config targets', action='store_true')

        command_line_args = parser.parse_args(sys.argv[2:])
        if command_line_args.targets_list:
            print(self.config.list_targets_names())

    def conan_command(self):
        project_path = self.config.project_path
        conan_config = self.config['conan']

        conan_file_path = f'{project_path}/{conan_config["file_path"]}'
        conan_build_dir = f'{project_path}/{conan_config["build_dir"]}'
        self.conan.install(conan_file_path, conan_build_dir)

    def cmake_command(self):
        usage = '''{green}{program_name} cmake <command> [<args>][-h|--help]

{purple}Available commands{white}
 {green}{cmake_configure}{white}    Configures cmake - this command is executed by default, if no command is provided
 {green}{cmake_build}{white}        Builds cmake project
'''

        command_choices = [
            ProgramCommandHelper.COMMAND_CMAKE_CONFIGURE,
            ProgramCommandHelper.COMMAND_CMAKE_BUILD,
        ]

        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument(
            'command',
            help='command to execute',
            metavar='<command>',
            choices=command_choices,
            nargs='?',
            default=ProgramCommandHelper.COMMAND_CMAKE_CONFIGURE,
        )

        command_line_args = parser.parse_args(sys.argv[2:3])
        if command_line_args.command == ProgramCommandHelper.COMMAND_CMAKE_CONFIGURE:
            self.cmake.configure()
            return

        # CMake Build
        usage = '''{green}{program_name} cmake {cmake_build} [<args>][-h|--help]{white}

Builds CMake project from the `build_dir_path` defined in the project config.
If no configuration is provided via arguments, project is built for all available configurations.

{purple}Available arguments{white}
 {green}{cmake_build_config}{white}     Build configuration, can be one of {available_configs}.
'''

        formatter_map = {'available_configs': BuildConfigNames.available_names()}
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage, formatter_map))
        parser.add_argument(
            ProgramCommandHelper.PARAM_CMAKE_CONFIG,
            help='build configuration',
            metavar='<config>',
            choices=BuildConfigNames.all_configs(),
        )

        command_line_args = parser.parse_args(sys.argv[3:])
        self.cmake.build(command_line_args.config)
