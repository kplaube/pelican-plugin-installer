import os
import shutil

from pelican_plugin_installer import cli
from pelican_plugin_installer.commands import (
    GIT_CLONE_COMMAND, GIT_SUBMODULE_COMMAND, PLUGINS_LOCAL_REPOSITORY,
)


def test_discover_a_pelican_conf_file(pelicanconf, runner):
    runner.invoke(cli.main, ['-i', 'plugin-name', '-c', 'pelicanconf.py'])

    assert pelicanconf.call_count == 1


def test_initialize_local_repository(mocker, runner):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.side_effect = [False, False, True]

    mocker.patch('os.makedirs')
    mocker.patch('os.system')

    mocker.patch('shutil.copytree')

    runner.invoke(cli.main, ['-i', 'plugin-name', '-c', 'pelicanconf.py'])

    expected = (
        mocker.call(GIT_CLONE_COMMAND, ),
        mocker.call(GIT_SUBMODULE_COMMAND, ),
    )

    os.makedirs.assert_called_once_with(PLUGINS_LOCAL_REPOSITORY)
    os.system.assert_has_calls(expected)


def test_install_plugin_from_official_pelican_repository(mock_install_operations, runner):
    result = runner.invoke(cli.main, ['-i', 'plugin-name', '-c', 'pelicanconf.py'])

    src_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, 'plugin-name')
    dst_path = '/tmp/plugins/plugin-name'

    shutil.copytree.assert_called_once_with(src_path, dst_path)

    assert 'Plugin installed' in result.output


def test_install_plugin_from_unofficial_pelican_repository(mock_install_operations, runner):
    result = runner.invoke(cli.main, ['-i', 'https://github.com/kplaube/extended_meta', '-c', 'pelicanconf.py'])

    src_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, '_unofficial/extended_meta')
    dst_path = '/tmp/plugins/extended_meta'

    shutil.copytree.assert_called_once_with(src_path, dst_path)
    os.system.assert_called_with(
        "git clone {0} {1}".format(
            'https://github.com/kplaube/extended_meta',
            src_path,
        )
    )

    assert 'Plugin installed' in result.output


def test_warn_when_the_plugin_is_already_installed(mocker, runner):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.return_value = True

    result = runner.invoke(cli.main, ['-i', 'plugin-name', '-c', 'pelicanconf.py'])

    assert 'The plugin is already installed' in result.output


def test_warn_when_plugin_doesnt_exist(mocker, runner):
    os_path_exists = mocker.patch('os.path.exists')
    os_path_exists.return_value = False

    mocker.patch('os.makedirs')
    mocker.patch('os.system')

    result = runner.invoke(cli.main, ['-i', 'inexistent-plugin', '-c', 'pelicanconf.py'])

    assert "The specified plugin doesn't exist" in result.output
