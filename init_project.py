import shutil
from inspect import getframeinfo, currentframe
from pathlib import Path

from src.files.file_opener import FileOpener
from src.yaml_utils.yaml_manager import YAMLManager
from argparse_prompt import PromptParser
from src.functions import get_scripts_dist_config_path, get_scripts_config_path


def init(cwd: str, project_path: str, config_path: str):
    dist_config_filename = get_scripts_dist_config_path(cwd)
    config_filename = get_scripts_config_path(cwd)

    shutil.copyfile(dist_config_filename, config_filename)
    yaml_manager = YAMLManager(FileOpener())

    config = yaml_manager.load_from_file(config_filename)
    config['project_path'] = project_path
    config['config_path'] = config_path

    yaml_manager.save_to_file(config, config_filename)


def get_project_path():
    current_filename = getframeinfo(currentframe()).filename
    default_project_path = Path(current_filename).resolve().parent.parent.__str__().replace('\\', '/')

    parser = PromptParser()
    parser.add_argument('--project_path', '-pp', help='Path to your C++ project\'s files', default=default_project_path)

    return parser.parse_args().project_path.replace('\\', '/')


def get_config_path(project_path: str):
    default_config_path = f'{project_path}/config/config.yaml'

    parser = PromptParser()
    parser.add_argument('--config_path', '-cp', help='Path to your C++ project\'s config', default=default_config_path)

    return parser.parse_args().config_path.replace('\\', '/')


def start():
    project_path = get_project_path()
    config_path = get_config_path(project_path)

    current_filename = getframeinfo(currentframe()).filename
    cwd = Path(current_filename).resolve().parent.__str__().replace('\\', '/')
    init(cwd + '/', project_path, config_path)


if __name__ == "__main__":
    start()
