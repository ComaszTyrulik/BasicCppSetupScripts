from inspect import getframeinfo, currentframe
from pathlib import Path

import colorama
import traceback

from src.beastengine.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.target_config_manager import TargetConfigManager
from src.functions import get_scripts_config_path
from src.commandrunners.cmake.cmake import CMake
from src.commandrunners.cmake.cmake_config_files_creator import CMakeConfigFilesCreator
from src.commandrunners.conan import Conan
from src.config.config import Config
from src.commandrunners.command_runner import CommandRunner
from src.files.file_opener import FileOpener
from src.yaml_utils.yaml_manager import YAMLManager
from src.beastengine.beastengine import BeastEngine
from src.beastengine.commands.class_commands.target_cmake_vars_file_opener import TargetCMakeVarsFileOpener

colorama.init(autoreset=True)

try:
    current_filename = getframeinfo(currentframe()).filename
    cwd = Path(current_filename).resolve().parent.__str__().replace('\\', '/')

    file_opener = FileOpener()
    config = Config(get_scripts_config_path(cwd + '/'), YAMLManager(file_opener))
    command_runner = CommandRunner()

    project_working_dir = config.project_path
    build_dir_path = config.build_directory_path

    conan = Conan(command_runner, build_dir_path)
    cmake =\
        CMake(
            command_runner,
            CMakeConfigFilesCreator(command_runner, file_opener),
            config,
            project_working_dir,
            build_dir_path
        )

    target_config_manager = TargetConfigManager(TargetCMakeVarsFileOpener(file_opener))
    class_files_helper = ClassFilesHelper(file_opener)

    BeastEngine(
        command_runner,
        config,
        conan,
        cmake,
        target_config_manager,
        class_files_helper
    )
except Exception as exception:
    print(f'{colorama.Fore.LIGHTYELLOW_EX}An error occurred!\nDetails:{colorama.Fore.LIGHTRED_EX} {exception}')
    traceback.print_exc()

colorama.deinit()
