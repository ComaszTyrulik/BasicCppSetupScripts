import re

from src.program.program_command_helper import ProgramCommandHelper
from src.files.file_opener import FileOpener
from src.config.config import Config


class TargetConfigManager:
    STRING_NOT_FOUND_VALUE = -1
    CONFIG_HEADERS = 'headers'
    CONFIG_SOURCES = 'sources'
    CONFIG_BASE_DIR = 'base_dir'

    FILE_EXISTS_INFO_TEMPLATE = 'Target already contains the "{}" file - skipping.'

    def __init__(self, file_opener: FileOpener):
        self.file_opener = file_opener

    def get_headers_base_directory(self, target_config, config: Config):
        return self.__get_files_base_directory(config, target_config[self.CONFIG_HEADERS][self.CONFIG_BASE_DIR])

    def get_sources_base_directory(self, target_config, config: Config):
        return self.__get_files_base_directory(config, target_config[self.CONFIG_SOURCES][self.CONFIG_BASE_DIR])

    def add_file_to_headers_list(self, config: Config, header_name: str, target_config):
        self.__modify_files_list(config, header_name, target_config[self.CONFIG_HEADERS], self.__add_file_action)

    def remove_file_from_headers_list(self, config: Config, header_name, target_config):
        self.__modify_files_list(config, header_name, target_config[self.CONFIG_HEADERS], self.__remove_file_action)

    def add_file_to_sources_list(self, config: Config, source_name, target_config):
        self.__modify_files_list(config, source_name, target_config[self.CONFIG_SOURCES], self.__add_file_action)

    def remove_file_from_sources_list(self, config: Config, source_name, target_config):
        self.__modify_files_list(config, source_name, target_config[self.CONFIG_SOURCES], self.__remove_file_action)

    def __get_files_base_directory(self, config: Config, target_files):
        return f'{config.project_path}/{target_files}'

    def __modify_files_list(self, config: Config, filename: str, target_config, action):
        variable_filename = f"{config.project_path}/{target_config['cmake_variable_file']}"
        variable_name = target_config['cmake_variable_name']

        file = self.file_opener.open(variable_filename)
        file_content = self.file_opener.open(variable_filename).get_content()

        var_start_pos = file_content.find(variable_name)
        if var_start_pos == self.STRING_NOT_FOUND_VALUE:
            raise RuntimeError(f'"{variable_filename}" file does not contain the "{variable_name}" variable!')

        var_end_pos = file_content.find(')', var_start_pos)
        if var_end_pos == self.STRING_NOT_FOUND_VALUE:
            raise RuntimeError(f'Cannot find closing parenthesis of the "{variable_name}" variable!')

        file_content = action(filename, file_content, var_start_pos + len(variable_name), var_end_pos)
        if file_content is not None:
            file.replace_content(file_content)

    def __add_file_action(self, filename, file_content: str, var_start_pos, var_end_pos):
        if file_content.find(filename) != self.STRING_NOT_FOUND_VALUE:
            self.__print_file_exists_message(filename)
            return

        # header or source file regex
        regex = re.compile(r'(\"[/A-Za-z0-9_-]+\.[a-z]{1,3}\")')

        content_before_var = file_content[:var_start_pos]

        files_list = file_content[var_start_pos:var_end_pos]
        files_list += f'\t"{filename}"\n'

        class_files = regex.findall(files_list)
        class_files = sorted(class_files)

        files_list = '\n'
        for class_file in class_files:
            files_list += f'\t{class_file}\n'

        content_after_var = file_content[var_end_pos:]
        return content_before_var + files_list + content_after_var

    def __remove_file_action(self, filename, file_content: str, var_start_pos, var_end_pos):
        file_pattern = f'\t"{filename}"\n'
        file_pos = file_content.find(file_pattern)
        if file_pos == self.STRING_NOT_FOUND_VALUE:
            raise RuntimeError(f'Target headers variable does not contain the "{filename}" file!')

        content_before_var = file_content[:var_start_pos]
        files_list_before_file = file_content[var_start_pos:file_pos]
        files_list_after_file = file_content[file_pos + len(file_pattern):]

        return content_before_var + files_list_before_file + files_list_after_file

    def __print_file_exists_message(self, filename):
        ProgramCommandHelper.print_message(self.FILE_EXISTS_INFO_TEMPLATE.format(filename))
