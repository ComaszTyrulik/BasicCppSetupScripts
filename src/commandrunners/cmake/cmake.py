from src.commandrunners.command_runner import CommandRunner
from src.config.config_names import BuildConfigNames


class CMake:
    COMMAND_CONFIGURE = 'cmake -S . -B "{}"'
    COMMAND_BUILD = 'cmake --build "{}" --config {}'

    def __init__(self, command_runner: CommandRunner, project_path: str, build_dir_path: str):
        self.command_runner = command_runner

        self.project_path = project_path
        self.build_dir_path = build_dir_path

    def configure(self, parameters=''):
        if parameters != '':
            parameters = ' ' + parameters

        command = CMake.COMMAND_CONFIGURE.format(self.build_dir_path) + parameters
        self.command_runner.run_command(command, self.project_path)

    def build(self, config=None):
        if config is not None:
            command = CMake.COMMAND_BUILD.format(self.build_dir_path, config)
            self.command_runner.run_command(command, self.project_path)
        else:
            for config in BuildConfigNames.all_configs():
                command = CMake.COMMAND_BUILD.format(self.build_dir_path, config)
                self.command_runner.run_command(command, self.project_path)


