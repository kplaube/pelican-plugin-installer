import click
import os
import shutil
import sys

PLUGINS_REMOTE_REPOSITORY = 'https://github.com/getpelican/pelican-plugins.git'
PLUGINS_LOCAL_REPOSITORY = os.path.join(os.path.expanduser('~'), '.pelican', 'plugins')

GIT_CLONE_COMMAND = "git clone {0} {1}".format(
    PLUGINS_REMOTE_REPOSITORY,
    PLUGINS_LOCAL_REPOSITORY
)
GIT_SUBMODULE_COMMAND = "cd {0}; git submodule init; git submodule update".format(
    PLUGINS_LOCAL_REPOSITORY,
)


def is_local_repository_initilized():
    return os.path.exists(PLUGINS_LOCAL_REPOSITORY)


def is_plugin_already_installed(plugin_name, plugin_paths):
    for path in plugin_paths:
        if os.path.exists(os.path.join(path, plugin_name)):
            return True

    return False


def initialize_local_repository():
    os.makedirs(PLUGINS_LOCAL_REPOSITORY)
    os.system(GIT_CLONE_COMMAND)
    os.system(GIT_SUBMODULE_COMMAND)


def install_plugin(plugin_name, plugin_path):
    src = os.path.join(PLUGINS_LOCAL_REPOSITORY, plugin_name)
    dst = os.path.join(plugin_path, plugin_name)

    shutil.copytree(src, dst)


def discover_plugin_paths(config_file):
    site_path = os.path.dirname(config_file)

    if site_path == '':
        site_path = os.getcwd()

    file_name = os.path.basename(config_file)
    module_name = os.path.splitext(file_name)[0]

    sys.path.append(site_path)
    pelicanconf = __import__(module_name)
    plugins_path = pelicanconf.PLUGIN_PATHS

    return list(map(lambda path: os.path.join(site_path, path), plugins_path))


@click.command()
@click.option('--delete', '-d', 'operation', flag_value='delete', help='Delete a specific plugin.')
@click.option('--install', '-i', 'operation', flag_value='install', help='Install a specific plugin.')
@click.option('--update', '-u', 'operation', flag_value='update', help='Update a specific plugin.')
@click.option('--config', '-c', 'config_file', default='pelicanconf.py', help='The path to Pelican configuration file.')
@click.argument('plugin_name', required=False)
def main(plugin_name, operation, config_file):
    """Installs Pelican Plugins in an easy way"""

    click.echo('Discovering Pelican configuration file...')
    plugin_paths = discover_plugin_paths(config_file)

    if operation == 'install':
        if is_plugin_already_installed(plugin_name, plugin_paths):
            click.echo('The plugin is already installed, use the option -u to update.')
            return

        if not is_local_repository_initilized():
            click.echo('Initializing local repository...')
            initialize_local_repository()

        click.echo('Installing plugin...')
        install_plugin(plugin_name, plugin_paths[0])
        click.echo("Plugin installed in {0}!".format(os.path.join(plugin_paths[0], plugin_name)))
        click.echo("Don't forget to update the PLUGINS variable.")
    else:
        click.echo("Operation: {0}; Plugin: {1}".format(operation, plugin_name))
