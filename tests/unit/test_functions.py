import argparse
import pytest
import src.functions as functions

from mock import MagicMock


@pytest.mark.parametrize('project_path', ['./', '', None])
def test_get_scripts_config_path_will_return_valid_scripts_config_file_path_when_different_project_paths_provided(project_path):
    expected_config_path = f'{project_path}config/scripts_config.yaml'
    assert expected_config_path == functions.get_scripts_config_path(project_path)


@pytest.mark.parametrize('project_path', ['./', '', None])
def test_get_scripts_dist_config_path_will_return_valid_scripts_dist_config_file_path_when_different_project_paths_provided(project_path):
    expected_config_path = f'{project_path}config/scripts_config.yaml.dist'
    assert expected_config_path == functions.get_scripts_dist_config_path(project_path)


def test_create_arguments_parser_will_create_empty_parser_when_no_data_passed():
    expected_program = None
    expected_usage = None
    expected_description = None

    argument_parser_mock = MagicMock(argparse.ArgumentParser)
    functions.ArgumentParser = argument_parser_mock

    functions.create_arguments_parser()
    argument_parser_mock.assert_called_with(
        prog=expected_program,
        usage=expected_usage,
        description=expected_description,
    )


def test_create_arguments_parser_will_create_parser_with_given_program():
    expected_program = 'Program'

    argument_parser_mock = MagicMock(argparse.ArgumentParser)
    functions.ArgumentParser = argument_parser_mock

    functions.create_arguments_parser(program=expected_program)
    argument_parser_mock.assert_called_with(
        prog=expected_program,
        usage=None,
        description=None,
    )


def test_create_arguments_parser_will_create_parser_with_given_usage():
    expected_usage = 'Program Usage'

    argument_parser_mock = MagicMock(argparse.ArgumentParser)
    functions.ArgumentParser = argument_parser_mock

    functions.create_arguments_parser(usage=expected_usage)
    argument_parser_mock.assert_called_with(
        prog=None,
        usage=expected_usage,
        description=None,
    )


def test_create_arguments_parser_will_create_parser_with_given_description():
    expected_description = 'Program Description'

    argument_parser_mock = MagicMock(argparse.ArgumentParser)
    functions.ArgumentParser = argument_parser_mock

    functions.create_arguments_parser(description=expected_description)
    argument_parser_mock.assert_called_with(
        prog=None,
        usage=None,
        description=expected_description,
    )


def test_create_arguments_parser_will_create_parser_with_given_formatter_class():
    expected_formatter = MagicMock()

    argument_parser_mock = MagicMock(argparse.ArgumentParser)
    functions.ArgumentParser = argument_parser_mock

    functions.create_arguments_parser(formatter_class=expected_formatter)
    argument_parser_mock.assert_called_with(
        prog=None,
        usage=None,
        description=None,
        formatter_class=expected_formatter
    )
