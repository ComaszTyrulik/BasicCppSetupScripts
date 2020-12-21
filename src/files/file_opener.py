from pathlib import Path


class FileOpener:
    class File:
        __file = None

        def __init__(self, file_path: str):
            try:
                file_mode_read_append_write = 'r+'
                self.__file = open(file_path, file_mode_read_append_write)
            except Exception:
                raise FileNotFoundError(f'Could not open "{file_path}" file')

        def __del__(self):
            if self.__file is not None:
                self.__file.close()

        def get_content(self):
            return self.__file.read()

        def replace_content(self, new_content):
            self.__file.truncate(0)
            self.__file.seek(0)
            self.__file.write(new_content)

    def open(self, file_path: str) -> File:
        return self.File(file_path)

    def create(self, file_path):
        Path(file_path).touch()
