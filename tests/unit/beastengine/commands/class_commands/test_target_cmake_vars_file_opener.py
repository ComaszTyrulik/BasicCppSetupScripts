import pytest
from mock import MagicMock

from src.config.config import Config
from src.files.file_opener import FileOpener
import src.beastengine.commands.class_commands.target_cmake_vars_file_opener as file_opener
from tests.tests_utilities.micro_mock import MicroMock


class CommonTestData:
    def __init__(self):
        self.file_mock = MagicMock(FileOpener.File)
        self.file_opener_mock = MagicMock(FileOpener)
        self.file_opener_mock.open = MagicMock(return_value=self.file_mock)


def test_open_will_open_proper_file():
    expected_project_path = 'project_path'
    expected_cmake_dir_name = 'cmake_dir_name'
    expected_file_path = 'target/cmake/vars/file/path.txt'
    expected_full_file_path = f'{expected_project_path}/{expected_cmake_dir_name}/{expected_file_path}'

    cmake_config = {'directory_name': expected_cmake_dir_name}

    config = MagicMock(Config)
    config.cmake = cmake_config
    config.project_path = expected_project_path

    target_config = {'variables': {'target_cmake_variables_file_path': expected_file_path}}

    test_data = CommonTestData()

    sut = file_opener.TargetCMakeVarsFileOpener(test_data.file_opener_mock)
    sut.open(config, target_config)

    test_data.file_opener_mock.open.assert_called_with(expected_full_file_path)


def test_open_will_return_file_content_arranged_in_map_of_variables_and_values():
    config = MagicMock(Config)
    config.project_path = ''
    config.cmake = {'directory_name': ''}
    target_config = {'variables': {'target_cmake_variables_file_path': 'file_path'}}

    variable1_name = 'var_1'
    variable1_value = 'var_1_value'

    variable2_name = 'var_2'
    variable2_value = 'var_2_value'

    file_content_before_split = f'''{variable1_name}={variable1_value}\n{variable2_name}={variable2_value}'''
    expected_content_map = {variable1_name: variable1_value, variable2_name: variable2_value}

    test_data = CommonTestData()
    test_data.file_mock.get_content = MagicMock(return_value=file_content_before_split)

    sut = file_opener.TargetCMakeVarsFileOpener(test_data.file_opener_mock)
    actual_content_map = sut.open(config, target_config)

    assert actual_content_map == expected_content_map


def test_open_will_throw_exception_if_any_line_in_file_does_not_contain_variable():
    with pytest.raises(ValueError):
        config = MagicMock(Config)
        config.project_path = ''
        config.cmake = {'directory_name': ''}
        target_config = {'variables': {'target_cmake_variables_file_path': 'file_path'}}

        variable1_name = 'var_1'
        variable1_value = 'var_1_value'

        variable2_name = 'var_2'
        variable2_value = 'var_2_value'

        # Missing '=' sign
        file_content_before_split = f'''{variable1_name}{variable1_value}\n{variable2_name}={variable2_value}'''

        test_data = CommonTestData()
        test_data.file_mock.get_content = MagicMock(return_value=file_content_before_split)

        sut = file_opener.TargetCMakeVarsFileOpener(test_data.file_opener_mock)
        sut.open(config, target_config)
