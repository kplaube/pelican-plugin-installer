import pytest
import sys
from click.testing import CliRunner
from pelican_plugin_installer import cli
from pelican_plugin_installer.cli import os


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def pelicanconf(mocker):
    prop = mocker.PropertyMock(return_value=['/tmp/plugins'])
    pelicanconf = mocker.Mock()
    type(pelicanconf).PLUGIN_PATHS = prop

    sys.modules['pelicanconf'] = pelicanconf

    return prop


@pytest.fixture
def mock_file_operations(mocker):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.return_value = False

    mocker.patch('os.makedirs')
    mocker.patch('os.system')


class TestInstallAPlugin:

    def test_discover_a_pelican_conf_file(self, pelicanconf, runner):
        runner.invoke(cli.main, ['-i', 'test', '-c', 'pelicanconf.py'])

        assert pelicanconf.call_count == 1

    def test_initialize_local_repository(self, mocker, pelicanconf, mock_file_operations, runner):
        runner.invoke(cli.main, ['-i', 'test', '-c', 'pelicanconf.py'])

        expected = (
            mocker.call(cli.GIT_CLONE_COMMAND, ),
            mocker.call(cli.GIT_SUBMODULE_COMMAND, ),
        )

        os.makedirs.assert_called_once_with(cli.PLUGINS_LOCAL_REPOSITORY)
        os.system.assert_has_calls(expected)
