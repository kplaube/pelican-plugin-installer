import click

from . import delete_plugin, discover_plugins_path, install_plugin
from .exceptions import BaseException


@click.command()
@click.option('--install', '-i', 'operation', flag_value='install', help='Install a specific plugin.')
@click.option('--delete', '-d', 'operation', flag_value='delete', help='Delete a specific plugin.')
@click.option('--config', '-c', 'config_file', default='pelicanconf.py', help='The path to Pelican configuration file.')
@click.argument('plugin_name', required=False)
def main(plugin_name, operation, config_file):
    """Installs Pelican Plugins in an easy way"""

    plugins_path = discover_plugins_path(config_file)

    if operation == 'install':
        try:
            install_plugin(plugin_name, plugins_path)
        except BaseException as e:
            click.echo(e.msg)
        else:
            click.echo('\n'.join([
                'Plugin installed!',
                "Don't forget to update the PLUGINS variable.",
            ]))
    if operation == 'delete':
        try:
            delete_plugin(plugin_name, plugins_path)
        except BaseException as e:
            click.echo(e.msg)
        else:
            click.echo('\n'.join([
                'Plugin removed!',
                "Don't forget to update the PLUGINS variable.",
            ]))
