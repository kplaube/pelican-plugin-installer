import pytest
import sys
from click.testing import CliRunner


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
def mock_install_operations(mocker):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.side_effect = [True, False, True, False]

    mocker.patch('os.makedirs')
    mocker.patch('os.system')

    mocker.patch('shutil.copytree')


@pytest.fixture
def mock_update_operations(mocker):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.side_effect = [True, False, True, True]

    mocker.patch('os.makedirs')
    mocker.patch('os.system')

    mocker.patch('shutil.rmtree')
    mocker.patch('shutil.copytree')
