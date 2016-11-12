import click
import os
import shutil

PLUGINS_REMOTE_REPOSITORY = 'https://github.com/getpelican/pelican-plugins.git'
PLUGINS_LOCAL_REPOSITORY = os.path.join(os.path.expanduser('~'), '.pelican', 'plugins')
SITE_PLUGINS_PATH = os.path.join('tmp', 'plugins')  # FIXME


def is_local_repository_initilized():
    return os.path.exists(PLUGINS_LOCAL_REPOSITORY)


def is_plugin_already_installed(plugin_name):
    return os.path.exists(os.path.join(SITE_PLUGINS_PATH, plugin_name))


def initialize_local_repository():
    os.makedirs(PLUGINS_LOCAL_REPOSITORY)
    os.system("git clone {0} {1}".format(
        PLUGINS_REMOTE_REPOSITORY,
        PLUGINS_LOCAL_REPOSITORY,
    ))
    os.system("cd {0}; git submodule init; git submodule update".format(
        PLUGINS_LOCAL_REPOSITORY,
    ))


def install_plugin(plugin_name):
    src = os.path.join(PLUGINS_LOCAL_REPOSITORY, plugin_name)
    dst = os.path.join(SITE_PLUGINS_PATH, plugin_name)

    shutil.copytree(src, dst)


@click.command()
@click.option('--delete', '-d', 'operation', flag_value='delete', help='Delete a specific plugin.')
@click.option('--install', '-i', 'operation', flag_value='install', help='Install a specific plugin.')
@click.option('--update', '-u', 'operation', flag_value='update', help='Update a specific plugin.')
@click.argument('plugin_name', required=False)
def main(plugin_name, operation):
    """Installs Pelican Plugins in an easy way"""

    if operation == 'install':
        if is_plugin_already_installed(plugin_name):
            click.echo('The plugin is already installed, use the option -u to update.')
            return

        if not is_local_repository_initilized():
            click.echo('Initializing local repository...')
            initialize_local_repository()

        click.echo('Installing plugin...')
        install_plugin(plugin_name)
        click.echo("Plugin installed in {0}!".format(os.path.join(SITE_PLUGINS_PATH, plugin_name)))
        click.echo("Don't forget to update the PLUGINS variable.")
    else:
        click.echo("Operation: {0}; Plugin: {1}".format(operation, plugin_name))
