import click

from . import discover_plugins_path, install_plugin
from .exceptions import AlreadyInstalledError


@click.command()
@click.option('--delete', '-d', 'operation', flag_value='delete', help='Delete a specific plugin.')
@click.option('--install', '-i', 'operation', flag_value='install', help='Install a specific plugin.')
@click.option('--update', '-u', 'operation', flag_value='update', help='Update a specific plugin.')
@click.option('--config', '-c', 'config_file', default='pelicanconf.py', help='The path to Pelican configuration file.')
@click.argument('plugin_name', required=False)
def main(plugin_name, operation, config_file):
    """Installs Pelican Plugins in an easy way"""

    click.echo('Discovering Pelican configuration file...')
    plugins_path = discover_plugins_path(config_file)

    if operation == 'install':
        try:
            click.echo('Installing plugin...')
            install_plugin(plugin_name, plugins_path)
        except AlreadyInstalledError as e:
            click.echo(e.msg)
        else:
            click.echo("Plugin installed!")
            click.echo("Don't forget to update the PLUGINS variable.")
