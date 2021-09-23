from unittest.mock import MagicMock, call

import pytest

from src.commandrunners.cmake import CMake
from src.commandrunners.command_runner import CommandRunner
from src.config.config_names import BuildConfigNames


def test_configure_will_run_valid_command():
    command_runner_mock = MagicMock(CommandRunner)
    command_runner_mock.run_command = MagicMock()

    build_dir = 'build/path'
    project_path = 'project/path'

    expected_command = f'cmake -S . -B "{build_dir}"'

    sut = CMake(command_runner_mock, project_path, build_dir)
    sut.configure()
    command_runner_mock.run_command.assert_called_with(expected_command, project_path)


def test_build_will_run_build_command_for_all_configurations_if_no_config_provided():
    command_runner_mock = MagicMock(CommandRunner)
    command_runner_mock.run_command = MagicMock()

    build_dir = 'build/path'
    project_path = 'project/path'

    expected_debug_command = f'cmake --build "{build_dir}" --config {BuildConfigNames.CONFIG_DEBUG}'
    expected_release_command = f'cmake --build "{build_dir}" --config {BuildConfigNames.CONFIG_RELEASE}'
    expected_rel_with_debug_command = f'cmake --build "{build_dir}" --config {BuildConfigNames.CONFIG_REL_WITH_DEBUG}'
    expected_min_size_rel_command = f'cmake --build "{build_dir}" --config {BuildConfigNames.CONFIG_MIN_SIZE_REL}'

    expected_debug_call = call(expected_debug_command, project_path)
    expected_release_call = call(expected_release_command, project_path)
    expected_rel_with_debug_call = call(expected_rel_with_debug_command, project_path)
    expected_min_size_rel_call = call(expected_min_size_rel_command, project_path)

    sut = CMake(command_runner_mock, project_path, build_dir)
    sut.build()
    command_runner_mock \
        .run_command \
        .assert_has_calls(
            [
                expected_debug_call,
                expected_release_call,
                expected_rel_with_debug_call,
                expected_min_size_rel_call
            ]
        )


@pytest.mark.parametrize("expected_config", BuildConfigNames.all_configs())
def test_build_will_run_build_command_with_given_configuration(expected_config):
    command_runner_mock = MagicMock(CommandRunner)
    command_runner_mock.run_command = MagicMock()

    build_dir = 'build/path'
    project_path = 'project/path'
    expected_command = f'cmake --build "{build_dir}" --config {expected_config}'

    sut = CMake(command_runner_mock, project_path, build_dir)
    sut.build(expected_config)
    command_runner_mock.run_command.assert_called_with(expected_command, project_path)
