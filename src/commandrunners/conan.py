from src.commandrunners.command_runner import CommandRunner
from src.config.config_names import BuildConfigNames


class Conan:
    def __init__(self, command_runner: CommandRunner, project_path):
        self.command_runner = command_runner
        self.project_path = project_path

    def install(self, conan_file_path, conan_build_dir):
        for config in BuildConfigNames.all_configs():
            command = f'conan install "{conan_file_path}" -if="{conan_build_dir}" -g cmake_multi --build=missing -s build_type={config}'
            self.command_runner.run_command(command, self.project_path)
