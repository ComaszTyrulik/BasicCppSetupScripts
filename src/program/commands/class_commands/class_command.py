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


class ClassCommand:
    PROGRAM_USAGE = '''{green}{class} <target> <command> [<args>]

{white}This command operates on source and header files relatively to the target's sources and headers directory defined in project config.

{green}For the list of available targets, execute: {yellow}{config} --list_targets

{purple}Available commands{white}
 {green}{class_add}{white}     Adds new class file to the given target
 {green}{class_rename}{white}     Renames existing class file
 {green}{class_remove}{white}     Removes existing class file from the given target

{yellow}Type "{class} <target> <command> --help" for more information on a specific class related command{white}
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
        program_usage = '''{green}{class} <target> {class_add} <class_name> [<args>]

{white}This command creates single header and single source files under the headers and sources base directories of the given CMake target.
If class name contains slashes, it will create subdirectories inside base directory.
Eg. {yellow}{class} {class_add} subDir/myClass{white} will result in creation of the 'myClass.h' and 'myClass.cpp'
files under the 'baseDirectory/subDir' path.{white}
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(program_usage))
        parser.add_argument('class_name', help='class to add', metavar='<class_name>')
        parser.add_argument('-n', '--namespace', help=ProgramCommandHelper.NAMESPACE_PARAM_HELP, type=str)

        command_line_arguments = parser.parse_args(sys.argv[4:])
        class_name = command_line_arguments.class_name

        namespace = target['namespace']
        if command_line_arguments.namespace:
            namespace = command_line_arguments.namespace

        header_file_content = None
        if target['tests'] is True:
            header_file_content = self.class_files_helper.get_header_file_content(class_name, namespace, self.config.test_template_file_path)
        else:
            header_file_content = self.class_files_helper.get_header_file_content(class_name, namespace, self.config.class_template_file_path)

        adder = ClassAdder(self.target_config_manager, self.class_files_helper)
        adder.add_header(class_name, target, self.config, namespace, header_file_content)
        adder.add_source(class_name, target, self.config, namespace)

        self.cmake.configure()

    def rename(self, target):
        usage = '''{green}{class} <target> {class_rename} <old_class_name> <new_class_name> [<args>]

{white}This command renames class' header and source files.
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('old_class_name', help='class to rename', metavar='<old_class_name>')
        parser.add_argument('new_class_name', help='new class name', metavar='<new_class_name>')

        command_line_arguments = parser.parse_args(sys.argv[4:])
        old_class_name = command_line_arguments.old_class_name
        new_class_name = command_line_arguments.new_class_name

        renamer = ClassRenamer(self.config, self.target_config_manager, self.class_files_helper)
        renamer.rename_header(old_class_name, new_class_name, target)
        renamer.rename_source(old_class_name, new_class_name, target)

        self.cmake.configure()

    def remove(self, target):
        usage = '''{green}{class} <target> {class_remove} <class_name> [<args>]

{white}This command removes header and source files from the headers and sources base directories.
If class name contains slashes, it will also delete empty subdirectories inside base directory.
'''
        parser = create_arguments_parser(usage=ProgramCommandHelper.format_text(usage))
        parser.add_argument('class_name', help='class to remove', metavar='<class_name>')

        command_line_arguments = parser.parse_args(sys.argv[4:])
        class_name = command_line_arguments.class_name

        remover = ClassRemover(self.config, self.target_config_manager, self.class_files_helper)
        remover.remove_header(class_name, target)
        remover.remove_source(class_name, target)

        self.cmake.configure()
