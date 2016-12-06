from pelican_plugin_installer import cli
from pelican_plugin_installer.manager import (PLUGINS_LOCAL_REPOSITORY, os, shutil)


def test_update_plugin_by_copying_its_files_to_plugins_path(mock_update_operations, runner):
    runner.invoke(cli.main, ['-u', 'plugin-name', '-c', 'pelicanconf.py'])

    src_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, 'plugin-name')
    dst_path = '/tmp/plugins/plugin-name'

    shutil.rmtree.assert_called_once_with(dst_path)
    shutil.copytree.assert_called_once_with(src_path, dst_path)
