from src.yaml_utils.yaml_manager import YAMLManager


class Config:
    TARGET_NAME_LIB = 'lib'
    TARGET_NAME_TESTS = 'tests'

    config: dict
    cmake: dict

    project_path: str
    build_directory_path: str
    test_template_file_path: str
    interface_template_file_path: str
    class_template_file_path: str

    def __init__(
        self,
        scripts_config_path: str,
        config_files_manager: YAMLManager,
        test_template_file_path: str,
        interface_template_file_path: str,
        class_template_file_path: str
    ):
        self.config_files_manager = config_files_manager

        scripts_config = config_files_manager.load_from_file(scripts_config_path)
        self.project_path = scripts_config['project_path']
        self.config_path = scripts_config['config_path']
        self.build_directory_path = scripts_config['build_dir_path']

        self.config = config_files_manager.load_from_file(self.config_path)
        self.test_template_file_path = test_template_file_path
        self.interface_template_file_path = interface_template_file_path
        self.class_template_file_path = class_template_file_path

    def __getitem__(self, item):
        return self.config[item]

    def update(self):
        self.config_files_manager.save_to_file(self.config, self.config_path)

    def get_target_config_by_name(self, target_name):
        try:
            return self['targets'][target_name]
        except KeyError:
            raise ValueError(f'"{target_name}" is not a valid target!')

    def list_targets_names(self):
        targets_names = []
        for target in self['targets']:
            targets_names.append(target)

        return targets_names
