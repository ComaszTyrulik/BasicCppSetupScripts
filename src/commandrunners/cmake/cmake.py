from src.commandrunners.cmake.cmake_config_files_creator import CMakeConfigFilesCreator
from src.commandrunners.command_runner import CommandRunner
from src.config.config import Config
from src.config.config_names import BuildConfigNames


class CMake:
    COMMAND_INIT = 'cmake -S . -B {}'
    COMMAND_BUILD = 'cmake --build . --config {}'

    FILE_MODE_READ = 'r'
    FILE_MODE_READ_APPEND_WRITE = 'r+'
    FILE_MODE_TRUNCATE_WRITE = 'w'

    def __init__(
            self,
            command_runner: CommandRunner,
            config_files_creator: CMakeConfigFilesCreator,
            config: Config,
            project_path: str,
            build_dir_path: str
    ):
        self.command_runner = command_runner
        self.config_files_creator = config_files_creator

        self.project_path = project_path
        self.build_dir_path = build_dir_path

        self.config = config.cmake
        self.config_dir = f'{self.project_path}/{self.config["directory_name"]}'
        self.targets_config = self.config['targets']

    def configure(self):
        self.command_runner.run_command(CMake.COMMAND_INIT.format(self.build_dir_path), self.project_path)

    def build(self, config_name: BuildConfigNames):
        self.command_runner.run_command(CMake.COMMAND_BUILD.format(config_name), self.build_dir_path)

    def generate_configs(self):
        self.generate_main_config()
        self.generate_targets_configs()

    def generate_main_config(self):
        self.config_files_creator.generate_main_config(self.config, self.config_dir)

    def generate_targets_configs(self):
        for target in self.targets_config:
            self.generate_target_config(self.targets_config[target])

    def generate_target_config(self, target):
        self.config_files_creator.generate_target_config(target, self.config_dir)
