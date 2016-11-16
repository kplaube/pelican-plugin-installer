from pelican_plugin_installer import (
    GIT_CLONE_COMMAND, GIT_SUBMODULE_COMMAND, PLUGINS_LOCAL_REPOSITORY, cli,
    os, shutil)


def test_initialize_local_repository(mocker, mock_update_operations, runner):
    runner.invoke(cli.main, ['-u', 'plugin-name', '-c', 'pelicanconf.py'])

    expected = (
        mocker.call(GIT_CLONE_COMMAND, ),
        mocker.call(GIT_SUBMODULE_COMMAND, ),
    )

    os.makedirs.assert_called_once_with(PLUGINS_LOCAL_REPOSITORY)
    os.system.assert_has_calls(expected)


def test_update_plugin_by_copying_its_files_to_plugins_path(mock_update_operations, runner):
    runner.invoke(cli.main, ['-u', 'plugin-name', '-c', 'pelicanconf.py'])

    src_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, 'plugin-name')
    dst_path = '/tmp/plugins/plugin-name'

    shutil.copytree.assert_called_once_with(src_path, dst_path)
    shutil.rmtree.assert_called_once_with(dst_path)
