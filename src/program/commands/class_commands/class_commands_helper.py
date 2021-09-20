from src.program.program_command_helper import ProgramCommandHelper


class ClassCommandsHelper:
    PROGRAM_USAGE = '''{green}{program_name} {target} <target> {command_name} <command> [<args>][-h|--help]

{white}This command operates on {command_name} files relatively to the target's {files_directories} defined in the project config.

{purple}Available commands{white}
 {green}{class_add}{white}    Adds new {command_name} {file_word_form} to the given target
 {green}{class_rename}{white}     Moves existing {command_name} {file_word_form} from one location to another
 {green}{class_remove}{white}     Removes existing {command_name} {file_word_form} both from the given target and from the drive
'''
    COMMAND_ADD_USAGE = '''{green}{program_name} {target} <target> {command_name} {class_add} <{command_name}_name>[-h|--help]

{white}This command creates {created_files} {file_word_form} under the {files_directories} of the given CMake target.
If name contains slashes, it will create subdirectories inside the base directory as a root directory.
Eg. {yellow}{program_name} {target} lib {command_name} {class_add} subDir/myClass{white} will result in creation of the {example_new_file}
{file_word_form} under the 'baseDirectory/subDir' path of the 'lib' target.{white}
'''
    COMMAND_RENAME_USAGE = '''{green}{program_name} {target} <target> {command_name} {class_rename} <old_{command_name}_name> <new_{command_name}_name>[-h|--help]

{white}This command moves the <old_{command_name}_name> {moved_files} {file_word_form} into new location provided by the <new_{command_name}_name> argument.
'''
    COMMAND_REMOVE_USAGE = '''{green}{program_name} {target} <target> {command_name} {class_remove} <{command_name}_name>[-h|--help]

{white}This command removes {removed_files} {file_word_form} from the target's {files_directories}.
If <{command_name}_name> contains slashes, it will also delete all empty subdirectories being part of the given <{command_name}_name>.
'''

    @staticmethod
    def get_class_file_program_usage():
        command = ProgramCommandHelper.COMMAND_NAME_CLASS
        directories = 'sources and headers directories'

        return ClassCommandsHelper._get_program_usage(command, directories, 'files')

    @staticmethod
    def get_single_file_program_usage(command_name: str):
        return ClassCommandsHelper._get_program_usage(command_name, f'{command_name}s directory', 'file')

    @staticmethod
    def get_class_add_command_usage():
        command = ProgramCommandHelper.COMMAND_NAME_CLASS
        created_files = 'single header and single source'
        files_directories = 'headers and sources base directories'
        new_files = "'myClass.h' and 'myClass.cpp'"

        return ClassCommandsHelper._get_add_command_usage(command, created_files, 'files', files_directories, new_files)

    @staticmethod
    def get_class_rename_command_usage():
        command = ProgramCommandHelper.COMMAND_NAME_CLASS
        moved_files = f'{command} header and source'

        return ClassCommandsHelper._get_rename_command_usage(command, moved_files, 'files')

    @staticmethod
    def get_class_remove_command_usage():
        command = ProgramCommandHelper.COMMAND_NAME_CLASS
        removed_files = 'header and source'
        files_directories = 'headers and sources base directories'

        return ClassCommandsHelper._get_remove_command_usage(command, removed_files, 'files', files_directories)

    @staticmethod
    def get_add_command_usage(command_name: str, file_extension: str):
        created_files = f'a single {command_name}'
        files_directories = f'{command_name}s base directory'
        new_file = f"'myClass{file_extension}'"

        return ClassCommandsHelper._get_add_command_usage(command_name, created_files, 'file', files_directories, new_file)

    @staticmethod
    def get_rename_command_usage(command_name: str):
        return ClassCommandsHelper._get_rename_command_usage(command_name, f'{command_name}', 'file')

    @staticmethod
    def get_remove_command_usage(command_name: str):
        return ClassCommandsHelper._get_remove_command_usage(command_name, command_name, 'file', f'{command_name}s directory')

    @staticmethod
    def _get_program_usage(command_name: str, files_directories: str, file: str):
        substitution_map = {
            'command_name': command_name,
            'files_directories': files_directories,
            'file_word_form': file
        }

        return ProgramCommandHelper.format_text(ClassCommandsHelper.PROGRAM_USAGE, substitution_map)

    @staticmethod
    def _get_add_command_usage(
            command_name: str,
            created_files: str,
            file_word_form: str,
            files_directories: str,
            example_new_file: str
    ):
        substitution_map = {
            'command_name': command_name,
            'created_files': created_files,
            'file_word_form': file_word_form,
            'files_directories': files_directories,
            'example_new_file': example_new_file
        }

        return ProgramCommandHelper.format_text(ClassCommandsHelper.COMMAND_ADD_USAGE, substitution_map)

    @staticmethod
    def _get_rename_command_usage(
            command_name: str,
            moved_files: str,
            file_word_form: str,
    ):
        substitution_map = {
            'command_name': command_name,
            'moved_files': moved_files,
            'file_word_form': file_word_form,
        }

        return ProgramCommandHelper.format_text(ClassCommandsHelper.COMMAND_RENAME_USAGE, substitution_map)

    @staticmethod
    def _get_remove_command_usage(command_name: str, removed_files: str, file_word_form: str, files_directories: str):
        substitution_map = {
            'command_name': command_name,
            'removed_files': removed_files,
            'file_word_form': file_word_form,
            'files_directories': files_directories
        }

        return ProgramCommandHelper.format_text(ClassCommandsHelper.COMMAND_REMOVE_USAGE, substitution_map)
