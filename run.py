from inspect import getframeinfo, currentframe
from pathlib import Path

import colorama
import traceback

from src.commandrunners.conan import Conan
from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.target_config_manager import TargetConfigManager
from src.functions import get_scripts_config_file_path, get_scripts_config_path
from src.commandrunners.cmake import CMake
from src.config.config import Config
from src.commandrunners.command_runner import CommandRunner
from src.files.file_opener import FileOpener
from src.yaml_utils.yaml_manager import YAMLManager
from src.program.program import Program

colorama.init(autoreset=True)

try:
    current_filename = getframeinfo(currentframe()).filename
    cwd = Path(current_filename).resolve().parent.__str__().replace('\\', '/')

    test_file_template_path = f'{get_scripts_config_path(cwd + "/")}/test_template.h'
    interface_template_file_path = f'{get_scripts_config_path(cwd + "/")}/interface_template.h'
    class_template_file_path = f'{get_scripts_config_path(cwd + "/")}/class_template.h'

    file_opener = FileOpener()
    config = Config(
        get_scripts_config_file_path(cwd + '/'),
        YAMLManager(file_opener),
        test_file_template_path,
        interface_template_file_path,
        class_template_file_path
    )
    command_runner = CommandRunner()

    project_working_dir = config.project_path
    build_dir_path = config.build_directory_path

    cmake = CMake(command_runner, project_working_dir, build_dir_path)

    target_config_manager = TargetConfigManager(file_opener)
    class_files_helper = ClassFilesHelper(file_opener)
    conan = Conan(command_runner, project_working_dir)

    Program(command_runner, config, cmake, target_config_manager, class_files_helper, conan)
except Exception as exception:
    print(f'{colorama.Fore.LIGHTYELLOW_EX}An error occurred!\nDetails:{colorama.Fore.LIGHTRED_EX} {exception}')
    print('')
    print('Exception traceback:')
    traceback.print_exc()

colorama.deinit()
