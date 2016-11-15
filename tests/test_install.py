from pelican_plugin_installer import cli
from pelican_plugin_installer import (
    GIT_CLONE_COMMAND, GIT_SUBMODULE_COMMAND, PLUGINS_LOCAL_REPOSITORY, os, shutil)


class TestInstallAPlugin:

    def test_discover_a_pelican_conf_file(self, pelicanconf, runner):
        runner.invoke(cli.main, ['-i', 'plugin-name', '-c', 'pelicanconf.py'])

        assert pelicanconf.call_count == 1

    def test_initialize_local_repository(self, mocker, pelicanconf, mock_file_operations, runner):
        runner.invoke(cli.main, ['-i', 'plugin-name', '-c', 'pelicanconf.py'])

        expected = (
            mocker.call(GIT_CLONE_COMMAND, ),
            mocker.call(GIT_SUBMODULE_COMMAND, ),
        )

        os.makedirs.assert_called_once_with(PLUGINS_LOCAL_REPOSITORY)
        os.system.assert_has_calls(expected)

    def test_install_plugin_by_copying_its_files_to_plugins_path(self, pelicanconf, mock_file_operations, runner):
        runner.invoke(cli.main, ['-i', 'plugin-name', '-c', 'pelicanconf.py'])

        src_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, 'plugin-name')
        dst_path = '/tmp/plugins/plugin-name'

        shutil.copytree.assert_called_once_with(src_path, dst_path)
