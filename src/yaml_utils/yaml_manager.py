from yaml import safe_load, safe_dump

from src.files.file_opener import FileOpener


class YAMLManager:
    def __init__(self, file_opener: FileOpener):
        self.file_opener = file_opener

    def load_from_file(self, file_path: str):
        json_file = self.file_opener.open(file_path)
        return safe_load(json_file.get_content())

    def save_to_file(self, yaml_object: dict, file_path: str):
        yaml_string = safe_dump(yaml_object)

        file = self.file_opener.open(file_path)
        file.replace_content(yaml_string)
