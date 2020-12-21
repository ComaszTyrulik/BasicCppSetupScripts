import os
import shutil
import colorama

from src.commandrunners.cmake.cmake import CMake
from src.commandrunners.conan import Conan


class Init:
    def __init__(self, build_dir_path: str, conan: Conan, cmake: CMake):
        # Remove build directory if exists
        if os.path.isdir(build_dir_path):
            print(f'{colorama.Fore.YELLOW}Removing "{build_dir_path}" directory')
            shutil.rmtree(build_dir_path)

        # Create build directory
        print(f'{colorama.Fore.YELLOW}Recreating "{build_dir_path}" directory{colorama.Fore.WHITE}\n')
        os.mkdir(build_dir_path)

        conan.install()
        cmake.generate_configs()
        cmake.configure()
