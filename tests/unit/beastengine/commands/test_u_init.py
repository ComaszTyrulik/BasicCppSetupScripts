import pytest
from mock import MagicMock

from src.beastengine.commands import init

from src.commandrunners.cmake.cmake import CMake
from src.commandrunners.conan import Conan


def test_constructor_will_call_conan_and_cmake(tmpdir):
    project_directory = tmpdir

    conan_mock = MagicMock(Conan)
    conan_mock.install = MagicMock()

    cmake_mock = MagicMock(CMake)
    cmake_mock.generate_configs = MagicMock()
    cmake_mock.configure = MagicMock()

    init.mkdir = MagicMock()
    init.print = MagicMock()

    init.Init(project_directory, conan_mock, cmake_mock, [])
    conan_mock.install.assert_called_once()
    cmake_mock.generate_configs.assert_called_once()
    cmake_mock.configure.assert_called_once()


@pytest.mark.parametrize('arguments', [[], ['-G Ninja'], None])
def test_constructor_will_forward_arguments_to_cmake_configure_command(arguments):
    project_directory = 'project/dir'

    conan_mock = MagicMock(Conan)
    conan_mock.install = MagicMock()

    cmake_mock = MagicMock(CMake)
    cmake_mock.generate_configs = MagicMock()
    cmake_mock.configure = MagicMock()

    init.mkdir = MagicMock()
    init.print = MagicMock()

    init.Init(project_directory, conan_mock, cmake_mock, arguments)
    cmake_mock.configure.assert_called_once_with(arguments)
