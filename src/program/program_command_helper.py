import colorama


class ProgramCommandHelper:
    DIRECTORY_BUILD = 'build'
    PROGRAM_NAME = 'run'

    COMMAND_NAME_CONAN = 'conan'
    COMMAND_NAME_CMAKE = 'cmake'
    COMMAND_NAME_BUILD = 'build'
    COMMAND_NAME_HEADER = 'header'
    COMMAND_NAME_SOURCE = 'source'
    COMMAND_NAME_CLASS = 'class'
    COMMAND_NAME_CLASS_ADD = 'add'
    COMMAND_NAME_CLASS_RENAME = 'mv'
    COMMAND_NAME_CLASS_REMOVE = 'rm'
    COMMAND_NAME_CLASS_PATH_SHOW = 'path'
    COMMAND_NAME_CONFIG = 'config'
    COMMAND_NAME_TARGET = 'target'
    PARAM_TARGETS_LIST = '--targets-list'

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
            'targets_list': ProgramCommandHelper.PARAM_TARGETS_LIST,
            'target': ProgramCommandHelper.COMMAND_NAME_TARGET,
            'program_name': ProgramCommandHelper.PROGRAM_NAME,
        }

        if substitution_map is not None:
            mappings.update(substitution_map)

        return text.format_map(mappings)

    @staticmethod
    def print_message(message_content):
        message = '\n{yellow}Message:\n{white}{message_content}{reset}\n'
        print(ProgramCommandHelper.format_text(message, {'message_content': message_content}))
