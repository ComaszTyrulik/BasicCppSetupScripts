from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.config import Config
from src.config.target_config_manager import TargetConfigManager


class ClassRemover:
    def __init__(self, config: Config, target_config_manager: TargetConfigManager, class_files_helper: ClassFilesHelper):
        self.config = config
        self.target_config_manager = target_config_manager
        self.class_files_helper = class_files_helper

    def remove_header(self, header_name: str, target_config):
        headers_base_dir = self.target_config_manager.get_headers_base_directory(target_config, self.config)
        if self.class_files_helper.does_class_header_file_exist(header_name, headers_base_dir) is True:
            self.class_files_helper.remove_class_header_file(header_name, headers_base_dir)

        header_name = self.class_files_helper.get_header_filename(header_name)
        self.target_config_manager.remove_file_from_headers_list(self.config, header_name, target_config)

    def remove_source(self, source_name: str, target_config):
        sources_base_dir = self.target_config_manager.get_sources_base_directory(target_config, self.config)
        if self.class_files_helper.does_class_source_file_exist(source_name, sources_base_dir) is True:
            self.class_files_helper.remove_class_source_file(source_name, sources_base_dir)

        class_name = self.class_files_helper.get_source_filename(source_name)
        self.target_config_manager.remove_file_from_sources_list(self.config, class_name, target_config)
