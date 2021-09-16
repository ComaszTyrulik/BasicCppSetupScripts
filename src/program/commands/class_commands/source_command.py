import sys

from src.program.commands.class_commands.class_renamer import ClassRenamer
from src.program.commands.class_commands.class_remover import ClassRemover
from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.program.commands.class_commands.class_adder import ClassAdder
from src.functions import create_arguments_parser
from src.program.program_command_helper import ProgramCommandHelper
from src.commandrunners.cmake import CMake
from src.config.config import Config
from src.config.target_config_manager import TargetConfigManager


class SourceCommand:
    PROGRAM_USAGE = '''{green}{source} <target> <command> [<args>]

{white}This command operates on source files relatively to the target's sources directory defined in project config.

{green}For the list of available targets, execute: {yellow}{config} --list_targets

{purple}Available commands{white}
 {green}{class_add}{white}     Adds new source file to the given target
 {green}{class_rename}{white}     Renames existing source file
 {green}{class_remove}{white}     Removes existing source file from the given target

{yellow}Type "{class} <target> <command> --help" for more information on a specific sources related command{white}
'''

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

    def add(self, target):
        program_usage = '''{green}{source} <target> {class_add} <source_name> [<args>]

    {white}This command creates single source file under the sources base directories of the given CMake target.
    If name contains slashes, it will create subdirectories inside base directory.
    Eg. {yellow}{source} {class_add} subDir/myClass{white} will result in creation of the 'myClass.cpp'
    file under the 'baseDirectory/subDir' path.{white}
    '''

        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(program_usage))
        parser.add_argument('source_name', help='source file to add', metavar='<source_name>')
        parser.add_argument('-n', '--namespace', help=ProgramCommandHelper.NAMESPACE_PARAM_HELP, type=str)

        command_line_arguments = parser.parse_args(sys.argv[4:])
        source_name = command_line_arguments.source_name

        namespace = target['namespace']
        if command_line_arguments.namespace:
            namespace = command_line_arguments.namespace

        adder = ClassAdder(self.target_config_manager, self.class_files_helper)
        adder.add_source(source_name, target, self.config, namespace)

        self.cmake.configure()

    def rename(self, target):
        usage = '''{green}{source} <target> {class_rename} <old_source_name> <new_source_name> [<args>]

{white}This command renames class' source file.
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('old_source_name', help='source to rename', metavar='<old_source_name>')
        parser.add_argument('new_source_name', help='new source name', metavar='<new_source_name>')

        command_line_arguments = parser.parse_args(sys.argv[4:])
        old_source_name = command_line_arguments.old_source_name
        new_source_name = command_line_arguments.new_source_name

        renamer = ClassRenamer(self.config, self.target_config_manager, self.class_files_helper)
        renamer.rename_source(old_source_name, new_source_name, target)

        self.cmake.configure()

    def remove(self, target):
        usage = '''{green}{source} <target> {class_remove} <source_name> [<args>]

{white}This command removes source file from the sources base directories.
If source name contains slashes, it will also delete empty subdirectories inside base directory.
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('source_name', help='source to remove', metavar='<source_name>')

        command_line_arguments = parser.parse_args(sys.argv[4:])
        class_name = command_line_arguments.source_name

        remover = ClassRemover(self.config, self.target_config_manager, self.class_files_helper)
        remover.remove_source(class_name, target)

        self.cmake.configure()
