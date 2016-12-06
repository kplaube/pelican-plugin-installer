from pelican_plugin_installer import cli
from pelican_plugin_installer.manager import shutil


def test_remove_a_plugin_from_pelican_project(mocker, pelicanconf, runner):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.return_value = True

    mocker.patch('shutil.rmtree')

    result = runner.invoke(cli.main,
                           ['-d', 'plugin-name', '-c', 'pelicanconf.py'])

    shutil.rmtree.assert_called_once_with('/tmp/plugins/plugin-name')
    assert 'Plugin removed!' in result.output


def test_warn_when_plugin_is_not_installed(mocker, pelicanconf, runner):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.side_effect = [True, False]

    mocker.patch('shutil.rmtree')

    result = runner.invoke(cli.main,
                           ['-d', 'plugin-name', '-c', 'pelicanconf.py'])

    assert shutil.rmtree.call_count == 0
    assert "The specified plugin isn't installed" in result.output
