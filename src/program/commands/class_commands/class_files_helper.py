import os
from pathlib import Path

from src.program.program_command_helper import ProgramCommandHelper
from src.files.file_opener import FileOpener


class ClassFilesHelper:
    HEADER_FILE_EXTENSION = 'h'
    SOURCE_FILE_EXTENSION = 'cpp'
    CLASS_NAME_DIRECTORY_SEPARATOR = '/'
    STRING_NOT_FOUND_VALUE = -1

    FILE_EXISTS_INFO_TEMPLATE = '"{}" file already exists. Skipping file creation'

    def __init__(self, file_opener: FileOpener):
        self.file_opener = file_opener

    def does_class_header_file_exist(self, class_name: str, headers_base_dir: str):
        header_file = self.get_header_filename(class_name)
        header_file_path = f'{headers_base_dir}/{header_file}'

        return self.__path_exists(header_file_path)

    def does_class_source_file_exist(self, class_name: str, source_base_dir: str):
        source_file = self.get_source_filename(class_name)
        source_file_path = f'{source_base_dir}/{source_file}'

        return self.__path_exists(source_file_path)

    def get_header_file_content(self, test_name: str, namespace: str, template_file_path: str):
        if test_name.find('/') != -1:
            test_name = test_name.split('/')[-1]

        template_file = self.file_opener.open(template_file_path)
        template_file_content = template_file.get_content()

        return template_file_content.format_map({'namespace': namespace, 'class_name': test_name})

    def create_class_header(self, class_name, headers_base_dir, namespace=None, file_content=None):
        header_filename = self.get_header_filename(class_name)
        header_file_path = f'{headers_base_dir}/{header_filename}'
        if self.__path_exists(header_file_path):
            self.__print_file_exists_message(header_file_path)
            return header_filename

        if class_name.find(self.CLASS_NAME_DIRECTORY_SEPARATOR) != self.STRING_NOT_FOUND_VALUE:
            class_sub_directories_path = self.__get_class_subdirectories_path(class_name)
            class_sub_directories_full_path = f'{headers_base_dir}/{class_sub_directories_path}'

            self.__create_file_sub_directories(class_sub_directories_full_path)

        self.__create_header_file(header_file_path, namespace, file_content)
        return header_filename

    def create_class_source(self, class_name, sources_base_dir, namespace=None):
        source_filename = self.get_source_filename(class_name)
        source_file_path = f'{sources_base_dir}/{source_filename}'
        if self.__path_exists(source_file_path):
            self.__print_file_exists_message(source_file_path)
            return source_filename

        if class_name.find(self.CLASS_NAME_DIRECTORY_SEPARATOR) != self.STRING_NOT_FOUND_VALUE:
            class_sub_directories_path = self.__get_class_subdirectories_path(class_name)
            class_sub_directories_full_path = f'{sources_base_dir}/{class_sub_directories_path}'

            self.__create_file_sub_directories(class_sub_directories_full_path)

        self.__create_source_file(source_file_path, namespace)
        return source_filename

    def rename_class_header(self, old_name: str, new_name: str, headers_base_dir: str):
        old_file_path = f'{headers_base_dir}/{self.get_header_filename(old_name)}'
        new_file_path = f'{headers_base_dir}/{self.get_header_filename(new_name)}'

        self.create_class_header(new_name, headers_base_dir)
        old_file_content = self.file_opener.open(old_file_path).get_content()
        self.file_opener.open(new_file_path).replace_content(old_file_content)

        self.remove_class_header_file(old_name, headers_base_dir)

    def rename_class_source(self, old_name: str, new_name: str, sources_base_dir: str):
        old_file_path = f'{sources_base_dir}/{self.get_source_filename(old_name)}'
        new_file_path = f'{sources_base_dir}/{self.get_source_filename(new_name)}'

        self.create_class_source(new_name, sources_base_dir)
        old_file_content = self.file_opener.open(old_file_path).get_content()
        self.file_opener.open(new_file_path).replace_content(old_file_content)

        self.remove_class_source_file(old_name, sources_base_dir)

    def remove_class_header_file(self, class_name: str, headers_base_dir: str):
        file_path = f'{headers_base_dir}/{self.get_header_filename(class_name)}'
        os.remove(file_path)

        if class_name.find(self.CLASS_NAME_DIRECTORY_SEPARATOR) == -1:
            return

        cwd = f'{headers_base_dir}'
        self.__remove_class_subdirectories(self.__get_class_subdirectories_path(class_name), cwd)

    def remove_class_source_file(self, class_name: str, sources_base_dir: str):
        file_path = f'{sources_base_dir}/{self.get_source_filename(class_name)}'
        os.remove(file_path)

        if class_name.find(self.CLASS_NAME_DIRECTORY_SEPARATOR) == self.STRING_NOT_FOUND_VALUE:
            return

        cwd = f'{sources_base_dir}'
        self.__remove_class_subdirectories(self.__get_class_subdirectories_path(class_name), cwd)

    @staticmethod
    def get_header_filename(class_name):
        return f'{class_name}.{ClassFilesHelper.HEADER_FILE_EXTENSION}'

    @staticmethod
    def get_source_filename(class_name):
        return f'{class_name}.{ClassFilesHelper.SOURCE_FILE_EXTENSION}'

    def __path_exists(self, file_path):
        return Path(file_path).exists()

    def __create_file_sub_directories(self, class_sub_directories_path: str):
        if self.__path_exists(class_sub_directories_path) is False:
            os.makedirs(class_sub_directories_path)

    def __remove_class_subdirectories(self, path: str, cwd: str):
        full_path = f'{cwd}/{path}'

        # Remove subdirectory if it exists and isn't empty
        if os.path.exists(full_path) and os.path.isdir(full_path) and not os.listdir(full_path):
            os.rmdir(full_path)

        # Check if path without the deepest directory still contains any subdirectories and remove them if any
        if path.find(self.CLASS_NAME_DIRECTORY_SEPARATOR) != self.STRING_NOT_FOUND_VALUE:
            last_occurrence = path.rfind(self.CLASS_NAME_DIRECTORY_SEPARATOR)
            self.__remove_class_subdirectories(path[:last_occurrence], cwd)

    def __create_header_file(self, header_file_path: str, namespace, file_content=None):
        if file_content is None:
            file_content = '#pragma once'
            if namespace is not None:
                file_content += f'\n\nnamespace {namespace}\n{{\n\n}} // namespace {namespace}\n'

        self.file_opener.create(header_file_path)
        header_file = self.file_opener.open(header_file_path)
        header_file.replace_content(file_content)

    def __create_source_file(self, source_file_path: str, namespace):
        file_content = ''

        if namespace is not None:
            file_content += f'\n\nnamespace {namespace}\n{{\n\n}} // namespace {namespace}\n'

        self.file_opener.create(source_file_path)
        source_file = self.file_opener.open(source_file_path)
        source_file.replace_content(file_content)

    def __get_class_subdirectories_path(self, class_name):
        directories = class_name.split(self.CLASS_NAME_DIRECTORY_SEPARATOR)
        directories.pop()

        class_sub_directories_path = ''
        for directory in directories:
            class_sub_directories_path += f'{directory}/'

        return class_sub_directories_path[:-1]

    def __print_file_exists_message(self, filename):
        ProgramCommandHelper.print_message(self.FILE_EXISTS_INFO_TEMPLATE.format(filename))
