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
            self.cmake.configure()
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
