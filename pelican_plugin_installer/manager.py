import re

from . import exceptions
from . import commands as cmd

OFFICIAL_REPOSITORY_URL_PATTERN = r'https?://github\.com/'


class Manager:

    def __init__(self, config_file_path):
        self._config_file_path = config_file_path
        self._plugins_path = cmd.get_plugins_path(config_file_path)

    def instance_plugin(self, plugin_name):
        return Plugin(plugin_name)

    def initialize_local_repository(self):
        if cmd.is_pelican_repository_cloned():
            return

        cmd.clone_pelican_repository()

    def run(self, operation, plugin):
        fn = getattr(self, operation)

        return fn(plugin)

    def install(self, plugin):
        if plugin.is_installed(self._plugins_path):
            raise exceptions.AlreadyInstalledError

        if not plugin.exists():
            raise exceptions.PluginDoesNotExistError

        if not plugin.is_official():
            plugin.initialize_local_repository()

        plugin.copy(self._plugins_path)

    def delete(self, plugin):
        if not plugin.is_installed(self._plugins_path):
            raise exceptions.NotInstalledError

        plugin.remove(self._plugins_path)

    def update(self, plugin):
        self.install(plugin)


class Plugin:

    def __init__(self, name):
        self.id = name

        if self.is_official():
            self.name = name
            self.local_repository_path = cmd.get_plugin_path(name)
        else:
            self.name = name.split('/')[-1]
            self.local_repository_path = cmd.get_plugin_path(
                "_unofficial/{0}".format(self.name)
            )

    def initialize_local_repository(self):
        cmd.clone_unofficial_plugin(self)

    def copy(self, plugins_path):
        cmd.copy_plugin_to_plugins_path(self, plugins_path)

    def remove(self, plugins_path):
        plugin_path = self.find_in(plugins_path)

        if not plugin_path:
            return False

        cmd.remove_path(plugin_path)

    def exists(self):
        return cmd.path_exists(self.local_repository_path)

    def find_in(self, plugins_path):
        for path in plugins_path:
            plugin_path = cmd.get_plugin_path(self.name, path=path)

            if cmd.path_exists(plugin_path):
                return plugin_path

        return None

    def is_installed(self, plugins_path):
        return bool(self.find_in(plugins_path))

    def is_official(self):
        return not re.search(
            OFFICIAL_REPOSITORY_URL_PATTERN,
            self.id
        )
