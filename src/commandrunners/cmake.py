from src.commandrunners.command_runner import CommandRunner


class CMake:
    COMMAND_CONFIGURE = 'cmake -S . -B {}'

    def __init__(self, command_runner: CommandRunner, project_path: str, build_dir_path: str):
        self.command_runner = command_runner

        self.project_path = project_path
        self.build_dir_path = build_dir_path

    def configure(self):
        self.command_runner.run_command(CMake.COMMAND_CONFIGURE.format(self.build_dir_path), self.project_path)
