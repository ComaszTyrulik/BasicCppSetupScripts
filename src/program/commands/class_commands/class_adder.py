from src.program.commands.class_commands.class_files_helper import ClassFilesHelper
from src.config.config import Config
from src.config.target_config_manager import TargetConfigManager


class ClassAdder:
    def __init__(self, target_config_manager: TargetConfigManager, class_files_helper: ClassFilesHelper):
        self.target_config_manager = target_config_manager
        self.class_files_helper = class_files_helper

    def add_header(self, class_name, target_config, config: Config, namespace, file_content=None):
        header_name = self.class_files_helper.create_class_header(
            class_name,
            self.target_config_manager.get_headers_base_directory(target_config, config),
            namespace,
            file_content
        )
        self.target_config_manager.add_file_to_headers_list(config, header_name, target_config)

    def add_source(self, class_name, target_config, config: Config, namespace):
        source_name = self.class_files_helper.create_class_source(
            class_name,
            self.target_config_manager.get_sources_base_directory(target_config, config),
            namespace
        )
        self.target_config_manager.add_file_to_sources_list(config, source_name, target_config)
