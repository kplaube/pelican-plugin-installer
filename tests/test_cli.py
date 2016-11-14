import pytest
import sys
from click.testing import CliRunner
from pelican_plugin_installer import cli


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


class TestInstallAPlugin:

    def test_discover_a_pelican_conf_file(self, pelicanconf, runner):
        runner.invoke(cli.main, ['-i', 'test', '-c', 'pelicanconf.py'])

        assert pelicanconf.call_count == 1
