import os
from pathlib import Path
from init_project import init
from src.files.file_opener import FileOpener
from src.yaml_utils.yaml_manager import YAMLManager


def test_init_will_copy_dist_file_into_config_file(tmpdir):
    yaml_manager = YAMLManager(FileOpener())
    project_directory = f'{tmpdir.__str__()}/'

    config_filename = 'scripts_config.yaml'
    expected_project_path = project_directory
    expected_config_directory = f'{expected_project_path}config/'
    expected_config_path = f'{expected_config_directory}{config_filename}'

    config_dist_content = '''
project_path: empty
config_path: empty
'''
    config_dist_filename = 'scripts_config.yaml.dist'
    config_dist_directory = f'{project_directory}config/'
    config_dist_path = f'{config_dist_directory}{config_dist_filename}'

    os.mkdir(expected_config_directory)
    Path(config_dist_path).touch()
    config_dist_file = open(config_dist_path, 'w')
    config_dist_file.write(config_dist_content)
    config_dist_file.close()

    # sut
    init(project_directory, expected_project_path, expected_config_path)

    actual_config = yaml_manager.load_from_file(expected_config_path)
    assert actual_config['project_path'] == expected_project_path
    assert actual_config['config_path'] == expected_config_path
