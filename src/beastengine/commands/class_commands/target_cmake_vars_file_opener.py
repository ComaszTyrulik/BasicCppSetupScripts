from src.config.config import Config
from src.files.file_opener import FileOpener


class TargetCMakeVarsFileOpener:
    FILE_NEW_LINE_SEPARATOR = '\n'
    FILE_VARIABLE_NAME_AND_VALUE_SEPARATOR = '='
    VARIABLE_LIST_EXPECTED_LENGTH = 2

    EXCEPTION_MESSAGE_TEMPLATE = "'{}' line does not contain any variable! No '{}' character found."

    def __init__(self, file_opener: FileOpener):
        self.file_opener = file_opener

    def open(self, config: Config, target_config):
        file_path = self.__get_target_cmake_variables_full_file_path(config.project_path, config.cmake['directory_name'], target_config['variables'])
        file = self.file_opener.open(file_path)

        content_lines = file.get_content().split(self.FILE_NEW_LINE_SEPARATOR)
        variables_map = {}
        for line in content_lines:
            variable = line.split(self.FILE_VARIABLE_NAME_AND_VALUE_SEPARATOR)
            if variable.__len__() != self.VARIABLE_LIST_EXPECTED_LENGTH:
                raise ValueError(self.EXCEPTION_MESSAGE_TEMPLATE.format(line, self.FILE_VARIABLE_NAME_AND_VALUE_SEPARATOR))

            variables_map[variable[0]] = variable[1]

        return variables_map

    @staticmethod
    def __get_target_cmake_variables_full_file_path(project_path: str, cmake_dir_name: str, variables_config: dict):
        return f'{project_path}/{cmake_dir_name}/{variables_config["target_cmake_variables_file_path"]}'
