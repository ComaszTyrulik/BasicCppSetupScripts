from unittest.mock import MagicMock

from src.files.file_opener import FileOpener
from src.yaml_utils import yaml_manager


class CommonTestData:
    def __init__(self):
        self.file_opener_mock = MagicMock(FileOpener)
        self.file_opener_mock.open = MagicMock()


def test_load_from_file_will_load_yaml_data_from_given_file_path():
    test_data = CommonTestData()

    expected_file_path = 'file/path/to.yaml'
    expected_yaml_string = 'this: is_yaml'
    expected_yaml_object = {'this': 'is_yaml'}

    file_mock = MagicMock(FileOpener.File)
    file_mock.get_content = MagicMock(return_value=expected_yaml_string)
    test_data.file_opener_mock.open.return_value = file_mock

    yaml_manager.safe_load = MagicMock(return_value=expected_yaml_object)

    sut = yaml_manager.YAMLManager(test_data.file_opener_mock)
    actual_yaml_object = sut.load_from_file(expected_file_path)

    yaml_manager.safe_load.assert_called_with(expected_yaml_string)
    assert expected_yaml_object == actual_yaml_object


def test_save_to_file_will_save_given_dictionary_as_yaml_string_to_given_file():
    test_data = CommonTestData()

    expected_yaml_string = 'this: is_yaml'
    expected_yaml_object = {'this': 'is_yaml'}
    expected_file_path = 'yaml_file/path.yaml'

    file_mock = MagicMock(FileOpener.File)
    file_mock.replace_content = MagicMock()
    test_data.file_opener_mock.open.return_value = file_mock

    yaml_manager.safe_dump = MagicMock(return_value=expected_yaml_string)

    sut = yaml_manager.YAMLManager(test_data.file_opener_mock)
    sut.save_to_file(expected_yaml_object, expected_file_path)

    yaml_manager.safe_dump.assert_called_with(expected_yaml_object)
    test_data.file_opener_mock.open.assert_called_with(expected_file_path)
    file_mock.replace_content.assert_called_with(expected_yaml_string)
