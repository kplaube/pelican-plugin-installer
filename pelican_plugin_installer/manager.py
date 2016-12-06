import os
import re
import shutil
import sys

from . import exceptions

OFFICIAL_REPOSITORY_URL_PATTERN = r'https?://github\.com/'

PLUGINS_REMOTE_REPOSITORY = 'https://github.com/getpelican/pelican-plugins.git'
PLUGINS_LOCAL_REPOSITORY = os.path.join(os.path.expanduser('~'), '.pelican', 'plugins')

GIT_CLONE_COMMAND_TEMPLATE = "git clone {0} {1}"
GIT_CLONE_COMMAND = GIT_CLONE_COMMAND_TEMPLATE.format(
    PLUGINS_REMOTE_REPOSITORY,
    PLUGINS_LOCAL_REPOSITORY
)
GIT_SUBMODULE_COMMAND = "cd {0}; git submodule init; git submodule update".format(
    PLUGINS_LOCAL_REPOSITORY,
)


class PluginManager:

    def __init__(self, config_file_path):
        self._config_file_path = config_file_path
        self._plugins_path = self._get_plugins_path(config_file_path)

    def initialize_local_repository(self):
        if os.path.exists(PLUGINS_LOCAL_REPOSITORY):
            return

        os.makedirs(PLUGINS_LOCAL_REPOSITORY)
        os.system(GIT_CLONE_COMMAND)
        os.system(GIT_SUBMODULE_COMMAND)

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

    def _get_plugins_path(self, config_file_path):
        site_path = os.path.dirname(config_file_path)

        if site_path == '':
            site_path = os.getcwd()

        file_name = os.path.basename(config_file_path)
        module_name = os.path.splitext(file_name)[0]

        sys.path.append(site_path)
        pelicanconf = __import__(module_name)
        plugins_path = pelicanconf.PLUGIN_PATHS

        return list(map(lambda path: os.path.join(site_path, path), plugins_path))


class Plugin:

    def __init__(self, name):
        self.id = name

        if self.is_official():
            self.name = name
            self.local_repository_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, name)
        else:
            self.name = name.split('/')[-1]
            self.local_repository_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, '_unofficial', self.name)

    def initialize_local_repository(self):
        os.system(GIT_CLONE_COMMAND_TEMPLATE.format(
            self.id, self.local_repository_path
        ))

    def copy(self, plugins_path):
        pelican_plugins_path = os.path.join(plugins_path[0], self.name)

        if os.path.exists(pelican_plugins_path):
            shutil.rmtree(pelican_plugins_path)

        shutil.copytree(self.local_repository_path, pelican_plugins_path)

    def remove(self, plugins_path):
        plugin_path = self.find_in(plugins_path)

        if not plugin_path:
            return False

        shutil.rmtree(plugin_path)

    def exists(self):
        return os.path.exists(self.local_repository_path)

    def find_in(self, plugins_path):
        for path in plugins_path:
            plugin_path = os.path.join(path, self.name)

            if os.path.exists(plugin_path):
                return plugin_path

        return None

    def is_installed(self, plugins_path):
        return bool(self.find_in(plugins_path))

    def is_official(self):
        return not re.search(
            OFFICIAL_REPOSITORY_URL_PATTERN,
            self.id
        )
