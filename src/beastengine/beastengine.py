import sys
import argparse

from src.functions import create_arguments_parser
from src.config.config_names import BuildConfigNames
from src.beastengine.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.target_config_manager import TargetConfigManager
from src.commandrunners.command_runner import CommandRunner
from src.beastengine.commands.class_commands.class_command import ClassCommand
from src.beastengine.commands.init import Init
from src.beastengine.commands.configure import Configure
from src.beastengine.commands.build import Build
from src.beastengine.beast_command_helper import BeastCommandHelper
from src.commandrunners.cmake.cmake import CMake
from src.commandrunners.conan import Conan
from src.config.config import Config


class BeastEngine:
    PROGRAM_NAME = 'beast'
    PROGRAM_USAGE = '''{green}beast <command> [<args>]

{white}This program let's you configure and manage the {project_name} project.
Use it to install all the required dependencies and configure CMake project.
You can also use it for building the project with desired configuration.{reset}

{purple}Configuration commands{white}
 {green}{init}{white}          Installs {project_name}. Creates build ('{build_dir_name}') directory and downloads all necessary dependencies
 {green}{configure}{white}     Configures CMake project inside the build ('{build_dir_name}') directory
 {green}{install_deps}{white}       Installs and/or updates project dependencies 

{purple}Development commands{white}
 {green}{build}{white}         Builds {project_name} project based on given parameters into the build ('{build_dir_name}') directory 
 {green}{class}{white}         Performs operations on classes
 {green}{config}{white}        Performs operations on config

{yellow}Type "beast <command> --help" for more information on a specific command{white}
'''

    def __init__(
            self,
            command_runner: CommandRunner,
            config: Config,
            conan: Conan,
            cmake: CMake,
            target_config_manager: TargetConfigManager,
            class_files_helper: ClassFilesHelper
    ):
        self.config = config
        self.command_runner = command_runner

        self.conan = conan
        self.cmake = cmake

        self.build_dir_path = self.config.build_directory_path

        self.target_config_manager = target_config_manager
        self.class_files_helper = class_files_helper

        self.create_program()

    def create_program(self):
        project_name = self.config.cmake['project']['name']
        substitution_map = {'project_name': project_name, 'build_dir_name': self.build_dir_path}

        parser =\
            argparse.ArgumentParser(
                prog=self.PROGRAM_NAME,
                usage=BeastCommandHelper.format_text(self.PROGRAM_USAGE, substitution_map),
                formatter_class=argparse.RawDescriptionHelpFormatter
            )

        parser.add_argument('command', help='command to execute', metavar='<command>')
        command_line_args = parser.parse_args(sys.argv[1:2])
        self.execute_command(command_line_args.command)

    def execute_command(self, command):
        if command == BeastCommandHelper.COMMAND_NAME_INIT:
            self.init()
        elif command == BeastCommandHelper.COMMAND_NAME_CONFIGURE:
            Configure(self.cmake)
        elif command == BeastCommandHelper.COMMAND_NAME_BUILD:
            self.build()
        elif command == BeastCommandHelper.COMMAND_NAME_CLASS:
            ClassCommand(self.config, self.cmake, self.target_config_manager, self.class_files_helper)
        elif command == BeastCommandHelper.COMMAND_NAME_INSTALL_DEPENDENCIES:
            self.conan.install()
        elif command == BeastCommandHelper.COMMAND_NAME_CONFIG:
            self.config_command()

    def init(self):
        usage = '''{green}beast {init}{white}
        Initializes the project.
        Recreates build ('{build_dir_name}') directory. If it exists, the directory is deleted and a fresh one is created.
        Downloads Conan dependencies based on the 'conanfile.py' file.
        Generates project target's CMake configuration files. Initializes required CMake variables.
        Configures CMake by running {yellow}{cmake_command}{reset}
        '''
        cmake_command = self.cmake.COMMAND_INIT.format(self.build_dir_path)
        substitution_map = {'build_dir_name': self.build_dir_path, 'cmake_command': cmake_command}

        parser = create_arguments_parser(usage=BeastCommandHelper.format_text(usage, substitution_map))
        parser.parse_args(sys.argv[2:])

        Init(self.config.build_directory_path, self.conan, self.cmake)

    def build(self):
        usage = '''{green}beast {build} [-c|--config CONFIG <args>]

{purple}Available arguments{white}
{green}-c --config{white}   Defines the configuration in which the project will be built.
              The available configurations are: {configs}.
              If no config is specified, the build is performed for all configurations at once.
'''
        substitution_map = {'configs': BuildConfigNames.available_names()}

        parser = create_arguments_parser(usage=BeastCommandHelper.format_text(usage, substitution_map))
        parser.add_argument(
            '-c',
            '--config',
            help='what configuration should the project be built for. Leave empty for all at once build '
        )

        command_line_args = parser.parse_args(sys.argv[2:])
        config = None
        if command_line_args.config:
            config = command_line_args.config

        Build(self.cmake, config)

    def config_command(self):
        usage = '''{green}beast config [<args>]

{purple}Available arguments{white}
{green}--list-targets{white}   Shows a list of project's targets. Those targets can be used by {class} commands
'''
        parser = create_arguments_parser(usage=BeastCommandHelper.format_text(usage))
        parser.add_argument('--list-targets', help='show available config targets', action='store_true')

        command_line_args = parser.parse_args(sys.argv[2:])
        if command_line_args.list_targets:
            print(self.config.list_targets_names())
