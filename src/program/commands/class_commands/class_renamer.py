from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.config import Config
from src.config.target_config_manager import TargetConfigManager


class ClassRenamer:
    def __init__(self, config: Config, target_config_manager: TargetConfigManager, class_files_helper: ClassFilesHelper):
        self.config = config
        self.target_config_manager = target_config_manager
        self.class_files_helper = class_files_helper

    def rename_header(self, old_header_name: str, new_header_name: str, target_config):
        headers_base_dir = self.target_config_manager.get_headers_base_directory(target_config, self.config)
        self.class_files_helper.rename_class_header(old_header_name, new_header_name, headers_base_dir)

        old_header_name = self.class_files_helper.get_header_filename(old_header_name)
        self.target_config_manager.remove_file_from_headers_list(self.config, old_header_name, target_config)

        new_header_name = self.class_files_helper.get_header_filename(new_header_name)
        self.target_config_manager.add_file_to_headers_list(self.config, new_header_name, target_config)
    
    def rename_source(self, old_source_name: str, new_source_name: str, target_config):
        sources_base_dir = self.target_config_manager.get_sources_base_directory(target_config, self.config)
        self.class_files_helper.rename_class_source(old_source_name, new_source_name, sources_base_dir)

        old_source_name = self.class_files_helper.get_source_filename(old_source_name)
        self.target_config_manager.remove_file_from_sources_list(self.config, old_source_name, target_config)

        new_source_name = self.class_files_helper.get_source_filename(new_source_name)
        self.target_config_manager.add_file_to_sources_list(self.config, new_source_name, target_config)
