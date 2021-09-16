import colorama


class ProgramCommandHelper:
    DIRECTORY_BUILD = 'build'

    COMMAND_NAME_CONAN = 'conan'
    COMMAND_NAME_CMAKE = 'cmake'
    COMMAND_NAME_BUILD = 'build'
    COMMAND_NAME_HEADER = 'header'
    COMMAND_NAME_SOURCE = 'source'
    COMMAND_NAME_CLASS = 'class'
    COMMAND_NAME_CLASS_ADD = 'add'
    COMMAND_NAME_CLASS_RENAME = 'ren'
    COMMAND_NAME_CLASS_REMOVE = 'del'
    COMMAND_NAME_CLASS_PATH_SHOW = 'path'
    COMMAND_NAME_CONFIG = 'config'

    NAMESPACE_PARAM_HELP = 'namespace in which the class should reside. By default it uses the namespace defined in target\'s config'

    @staticmethod
    def format_text(text: str, substitution_map=None):
        mappings = {
            'red': colorama.Fore.LIGHTRED_EX,
            'green': colorama.Fore.LIGHTGREEN_EX,
            'white': colorama.Fore.LIGHTWHITE_EX,
            'purple': colorama.Fore.LIGHTMAGENTA_EX,
            'yellow': colorama.Fore.YELLOW,
            'light_yellow': colorama.Fore.LIGHTYELLOW_EX,
            'reset': colorama.Fore.RESET,
            'build': ProgramCommandHelper.COMMAND_NAME_BUILD,
            'header': ProgramCommandHelper.COMMAND_NAME_HEADER,
            'source': ProgramCommandHelper.COMMAND_NAME_SOURCE,
            'class': ProgramCommandHelper.COMMAND_NAME_CLASS,
            'class_add': ProgramCommandHelper.COMMAND_NAME_CLASS_ADD,
            'class_rename': ProgramCommandHelper.COMMAND_NAME_CLASS_RENAME,
            'class_remove': ProgramCommandHelper.COMMAND_NAME_CLASS_REMOVE,
            'class_path_show': ProgramCommandHelper.COMMAND_NAME_CLASS_PATH_SHOW,
            'config': ProgramCommandHelper.COMMAND_NAME_CONFIG,
            'conan': ProgramCommandHelper.COMMAND_NAME_CONAN,
            'cmake': ProgramCommandHelper.COMMAND_NAME_CMAKE,
        }

        if substitution_map is not None:
            mappings.update(substitution_map)

        return text.format_map(mappings)

    @staticmethod
    def print_message(message_content):
        message = '\n{yellow}Message:\n{white}{message_content}{reset}\n'
        print(ProgramCommandHelper.format_text(message, {'message_content': message_content}))
