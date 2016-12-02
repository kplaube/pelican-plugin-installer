import os
import shutil
import sys

from . import exceptions

PLUGINS_REMOTE_REPOSITORY = 'https://github.com/getpelican/pelican-plugins.git'
PLUGINS_LOCAL_REPOSITORY = os.path.join(os.path.expanduser('~'), '.pelican', 'plugins')

GIT_CLONE_COMMAND = "git clone {0} {1}".format(
    PLUGINS_REMOTE_REPOSITORY,
    PLUGINS_LOCAL_REPOSITORY
)
GIT_SUBMODULE_COMMAND = "cd {0}; git submodule init; git submodule update".format(
    PLUGINS_LOCAL_REPOSITORY,
)


def discover_plugins_path(config_file):
    site_path = os.path.dirname(config_file)

    if site_path == '':
        site_path = os.getcwd()

    file_name = os.path.basename(config_file)
    module_name = os.path.splitext(file_name)[0]

    sys.path.append(site_path)
    pelicanconf = __import__(module_name)
    plugins_path = pelicanconf.PLUGIN_PATHS

    return list(map(lambda path: os.path.join(site_path, path), plugins_path))


def install_plugin(plugin_name, plugins_path):
    if _find_plugin_in_plugins_path(plugin_name, plugins_path):
        raise exceptions.AlreadyInstalledError

    if not _is_local_repository_initialized():
        _initialize_local_repository()

    if not _plugin_exists(plugin_name):
        raise exceptions.PluginDoesNotExistError

    src = os.path.join(PLUGINS_LOCAL_REPOSITORY, plugin_name)
    dst = os.path.join(plugins_path[0], plugin_name)

    shutil.copytree(src, dst)


def delete_plugin(plugin_name, plugins_path):
    installed_plugin_path = _find_plugin_in_plugins_path(plugin_name, plugins_path)

    if not installed_plugin_path:
        raise exceptions.NotInstalledError

    shutil.rmtree(installed_plugin_path)


def update_plugin(plugin_name, plugins_path):
    installed_plugin_path = _find_plugin_in_plugins_path(plugin_name, plugins_path)

    if not installed_plugin_path:
        raise exceptions.NotInstalledError

    if not _is_local_repository_initialized():
        _initialize_local_repository()

    if not _plugin_exists(plugin_name):
        raise exceptions.PluginDoesNotExistError

    src = os.path.join(PLUGINS_LOCAL_REPOSITORY, plugin_name)
    dst = os.path.join(plugins_path[0], plugin_name)

    shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _find_plugin_in_plugins_path(plugin_name, plugins_path):
    for path in plugins_path:
        plugin_path = os.path.join(path, plugin_name)
        if os.path.exists(plugin_path):
            return plugin_path

    return None


def _is_local_repository_initialized():
    return os.path.exists(PLUGINS_LOCAL_REPOSITORY)


def _plugin_exists(plugin_name):
    plugin_path = os.path.join(PLUGINS_LOCAL_REPOSITORY, plugin_name)

    return os.path.exists(plugin_path)


def _initialize_local_repository():
    os.makedirs(PLUGINS_LOCAL_REPOSITORY)
    os.system(GIT_CLONE_COMMAND)
    os.system(GIT_SUBMODULE_COMMAND)
