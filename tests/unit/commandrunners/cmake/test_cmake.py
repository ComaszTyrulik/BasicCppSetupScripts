from unittest.mock import MagicMock

from src.commandrunners.cmake import CMake
from src.commandrunners.command_runner import CommandRunner


def test_configure_will_run_valid_command():
    command_runner_mock = MagicMock(CommandRunner)
    command_runner_mock.run_command = MagicMock()

    build_dir = 'build/path'
    project_path = 'project/path'

    expected_command = f'cmake -S . -B "{build_dir}"'

    sut = CMake(command_runner_mock, project_path, build_dir)
    sut.configure()
    command_runner_mock.run_command.assert_called_with(expected_command, project_path)

