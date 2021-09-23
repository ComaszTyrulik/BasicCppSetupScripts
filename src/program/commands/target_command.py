import sys
import argparse

from src.program.commands.class_commands.class_command import ClassCommand
from src.program.commands.class_commands.source_command import SourceCommand
from src.program.commands.class_commands.header_command import HeaderCommand
from src.functions import create_arguments_parser
from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.target_config_manager import TargetConfigManager
from src.program.program_command_helper import ProgramCommandHelper
from src.commandrunners.cmake.cmake import CMake
from src.config.config import Config


class TargetCommand:
    PROGRAM_USAGE = '''{green}{program_name} {target} <target> <command> [<args>][-h|--help]

{white}Performs operations on selected target's files.{reset}

{purple}Available commands{white}
 {green}{header}{white}     Add/Remove/Move header files
 {green}{source}{white}     Add/Remove/Move source files
 {green}{class}{white}      Add/Remove/Move header and source files at the same time

{purple}For the list of available targets, execute: {yellow} {program_name} {config} {targets_list} {reset}
'''

    def __init__(
        self,
        config: Config,
        cmake: CMake,
        target_config_manager: TargetConfigManager,
        class_files_helper: ClassFilesHelper,
    ):
        self.config = config
        self.cmake = cmake
        self.class_files_helper = class_files_helper
        self.target_config_manager = target_config_manager

        self.execute()

    def execute(self):
        parser = argparse.ArgumentParser(
            usage=ProgramCommandHelper.format_text(self.PROGRAM_USAGE),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        command_choices = [
            ProgramCommandHelper.COMMAND_NAME_HEADER,
            ProgramCommandHelper.COMMAND_NAME_SOURCE,
            ProgramCommandHelper.COMMAND_NAME_CLASS,
        ]

        parser.add_argument('target', help='target for which the files should be added', metavar='<target>', choices=self.config.list_targets_names())
        parser.add_argument('command', help='command to execute', metavar='<command>', choices=command_choices)
        command_line_args = parser.parse_args(sys.argv[2:4])

        target = self.config.get_target_config_by_name(command_line_args.target)
        self.execute_command(command_line_args.command, target)

    def execute_command(self, command, target):
        command_class = None
        if command == ProgramCommandHelper.COMMAND_NAME_HEADER:
            command_class = HeaderCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)
        elif command == ProgramCommandHelper.COMMAND_NAME_SOURCE:
            command_class = SourceCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)
        elif command == ProgramCommandHelper.COMMAND_NAME_CLASS:
            command_class = ClassCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)

        usage = command_class.get_usage()
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
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

        command_line_arguments = parser.parse_args(sys.argv[4:5])

        command = command_line_arguments.command
        if command == ProgramCommandHelper.COMMAND_NAME_CLASS_ADD:
            command_class.add(target)
        elif command == ProgramCommandHelper.COMMAND_NAME_CLASS_RENAME:
            command_class.rename(target)
        elif command == ProgramCommandHelper.COMMAND_NAME_CLASS_REMOVE:
            command_class.remove(target)
