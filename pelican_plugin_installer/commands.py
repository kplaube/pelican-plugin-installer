import os
import shutil
import sys

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


def path_exists(path):
    return os.path.exists(path)


def is_pelican_repository_cloned():
    return path_exists(PLUGINS_LOCAL_REPOSITORY)


def clone_pelican_repository():
    os.makedirs(PLUGINS_LOCAL_REPOSITORY)
    os.system(GIT_CLONE_COMMAND)
    os.system(GIT_SUBMODULE_COMMAND)


def clone_unofficial_plugin(plugin):
    os.system(GIT_CLONE_COMMAND_TEMPLATE.format(
        plugin.id, plugin.local_repository_path
    ))


def copy_plugin_to_plugins_path(plugin, plugins_path):
    pelican_plugins_path = os.path.join(plugins_path[0], plugin.name)

    if path_exists(pelican_plugins_path):
        shutil.rmtree(pelican_plugins_path)

    shutil.copytree(plugin.local_repository_path, pelican_plugins_path)


def get_plugin_path(plugin_name, path=PLUGINS_LOCAL_REPOSITORY):
    return os.path.join(path, plugin_name)


def get_plugins_path(config_file_path):
    site_path = os.path.dirname(config_file_path)

    if site_path == '':
        site_path = os.getcwd()

    file_name = os.path.basename(config_file_path)
    module_name = os.path.splitext(file_name)[0]

    sys.path.append(site_path)
    pelicanconf = __import__(module_name)
    plugins_path = pelicanconf.PLUGIN_PATHS

    return list(map(lambda path: os.path.join(site_path, path), plugins_path))


def remove_path(path):
    shutil.rmtree(path)
