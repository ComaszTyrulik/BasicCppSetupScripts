import sys
import argparse

from src.commandrunners.conan import Conan
from src.program.commands.class_commands.class_command import ClassCommand
from src.program.commands.class_commands.source_command import SourceCommand
from src.program.commands.class_commands.header_command import HeaderCommand
from src.functions import create_arguments_parser
from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.target_config_manager import TargetConfigManager
from src.commandrunners.command_runner import CommandRunner
from src.program.program_command_helper import ProgramCommandHelper
from src.commandrunners.cmake import CMake
from src.config.config import Config


class Program:
    PROGRAM_NAME = 'program'
    PROGRAM_USAGE = '''{green}<command> [<args>]

{white}This program let's you manage project's targets' files.{reset}

{purple}Available commands{white}
 {green}{header}{white}     Add/Remove/Rename header files
 {green}{source}{white}     Add/Remove/Rename source files
 {green}{class}{white}      Add/Remove/Rename header and source files at the same time
 {green}{config}{white}     Performs operations on config 
 {green}{conan}{white}      installs project dependency using conan
 {green}{cmake}{white}      runs CMake configuration command

{yellow}Type "<command> --help" for more information on a specific command{white}
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
            prog=self.PROGRAM_NAME,
            usage=ProgramCommandHelper.format_text(self.PROGRAM_USAGE),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        command_choices = [
            ProgramCommandHelper.COMMAND_NAME_HEADER,
            ProgramCommandHelper.COMMAND_NAME_SOURCE,
            ProgramCommandHelper.COMMAND_NAME_CLASS,
            ProgramCommandHelper.COMMAND_NAME_CONFIG,
            ProgramCommandHelper.COMMAND_NAME_CONAN,
            ProgramCommandHelper.COMMAND_NAME_CMAKE,
        ]
        parser.add_argument('command', help='command to execute', metavar='<command>', choices=command_choices)
        command_line_args = parser.parse_args(sys.argv[1:2])
        self.execute_command(command_line_args.command)

    def execute_command(self, command):
        command_class = None
        if command == ProgramCommandHelper.COMMAND_NAME_HEADER:
            command_class = HeaderCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)
        elif command == ProgramCommandHelper.COMMAND_NAME_SOURCE:
            command_class = SourceCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)
        elif command == ProgramCommandHelper.COMMAND_NAME_CLASS:
            command_class = ClassCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)
        elif command == ProgramCommandHelper.COMMAND_NAME_CONFIG:
            self.config_command()
            return
        elif command == ProgramCommandHelper.COMMAND_NAME_CONAN:
            self.conan_command()
            return
        elif command == ProgramCommandHelper.COMMAND_NAME_CMAKE:
            self.cmake.configure()
            return

        usage = command_class.PROGRAM_USAGE
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('target', help='target for which the files should be added', metavar='<target>')
        parser.add_argument(
            'command',
            help='command to execute',
            metavar='<command>',
            choices=[
                ProgramCommandHelper.COMMAND_NAME_CLASS_ADD,
                ProgramCommandHelper.COMMAND_NAME_CLASS_RENAME,
                ProgramCommandHelper.COMMAND_NAME_CLASS_REMOVE,
            ]
        )

        command_line_arguments = parser.parse_args(sys.argv[2:4])
        target_name = command_line_arguments.target
        target = self.config.get_target_config_by_name(target_name)

        command = command_line_arguments.command
        if command == ProgramCommandHelper.COMMAND_NAME_CLASS_ADD:
            command_class.add(target)
        elif command == ProgramCommandHelper.COMMAND_NAME_CLASS_RENAME:
            command_class.rename(target)
        elif command == ProgramCommandHelper.COMMAND_NAME_CLASS_REMOVE:
            command_class.remove(target)

    def config_command(self):
        usage = '''{green}beast config [<args>]

{purple}Available arguments{white}
{green}--list-targets{white}   Shows a list of project's targets. Those targets can be used by {class} commands
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('--list-targets', help='show available config targets', action='store_true')

        command_line_args = parser.parse_args(sys.argv[2:])
        if command_line_args.list_targets:
            print(self.config.list_targets_names())

    def conan_command(self):
        project_path = self.config.project_path
        conan_config = self.config['conan']

        conan_file_path = f'{project_path}/{conan_config["file_path"]}'
        conan_build_dir = f'{project_path}/{conan_config["build_dir"]}'
        self.conan.install(conan_file_path, conan_build_dir)
