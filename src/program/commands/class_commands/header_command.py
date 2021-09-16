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


class HeaderCommand:
    PROGRAM_USAGE = '''{green}{header} <target> <command> [<args>]

{white}This command operates on header files relatively to the target's headers directory defined in project config.

{green}For the list of available targets, execute: {yellow}{config} --list_targets

{purple}Available commands{white}
 {green}{class_add}{white}     Adds new header file to the given target
 {green}{class_rename}{white}     Renames existing header file
 {green}{class_remove}{white}     Removes existing header file from the given target

{yellow}Type "{header} <target> <command> --help" for more information on a specific sources related command{white}
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
        program_usage = '''{green}{header} <target> {class_add} <header_name> [<args>]

{white}This command creates single header file under the headers base directories of the given CMake target.
If name contains slashes, it will create subdirectories inside base directory.
Eg. {yellow}{header} {class_add} subDir/myClass{white} will result in creation of the 'myClass.h'
file under the 'baseDirectory/subDir' path.{white}
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(program_usage))
        parser.add_argument('header_name', help='header to add', metavar='<header_name>')
        parser.add_argument('-n', '--namespace', help=ProgramCommandHelper.NAMESPACE_PARAM_HELP, type=str)
        parser.add_argument(
            '-i',
            '--interface',
            help='when this argument is present, the header will be created as an interface, using interface template',
            action='store_true'
        )

        command_line_arguments = parser.parse_args(sys.argv[4:])
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
        usage = '''{green}{header} <target> {class_rename} <old_header_name> <new_header_name> [<args>]

{white}This command renames class' header file.
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('old_header_name', help='header to rename', metavar='<old_header_name>')
        parser.add_argument('new_header_name', help='new header name', metavar='<new_header_name>')

        command_line_arguments = parser.parse_args(sys.argv[4:])
        old_header_name = command_line_arguments.old_header_name
        new_header_name = command_line_arguments.new_header_name

        renamer = ClassRenamer(self.config, self.target_config_manager, self.class_files_helper)
        renamer.rename_header(old_header_name, new_header_name, target)

        self.cmake.configure()

    def remove(self, target):
        usage = '''{green}{header} <target> {class_remove} <header_name> [<args>]

{white}This command removes header file from the headers base directories.
If header name contains slashes, it will also delete empty subdirectories inside base directory.
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('header_name', help='header to remove', metavar='<header_name>')

        command_line_arguments = parser.parse_args(sys.argv[4:])
        class_name = command_line_arguments.header_name

        remover = ClassRemover(self.config, self.target_config_manager, self.class_files_helper)
        remover.remove_header(class_name, target)

        self.cmake.configure()
