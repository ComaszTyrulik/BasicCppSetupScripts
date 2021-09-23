from argparse import ArgumentParser


def get_scripts_config_path(base_path: str):
    return f'{base_path}config'


def get_scripts_config_file_path(base_path: str):
    return f'{get_scripts_config_path(base_path)}/scripts_config.yaml'


def get_scripts_dist_config_path(base_path: str):
    return f'{get_scripts_config_path(base_path)}/scripts_config.yaml.dist'


def create_arguments_parser(program=None, usage=None, description=None, formatter_class=None):
    if formatter_class is None:
        parser = ArgumentParser(prog=program, usage=usage, description=description)
    else:
        parser = ArgumentParser(prog=program, usage=usage, description=description, formatter_class=formatter_class)

    return parser
