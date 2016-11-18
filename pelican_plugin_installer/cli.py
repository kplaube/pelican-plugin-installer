import click

from . import (
    delete_plugin, discover_plugins_path, install_plugin, update_plugin)
from .exceptions import BaseException

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)

operations = {
    'install': (install_plugin, ('Plugin installed!')),
    'delete': (delete_plugin, ('Plugin removed!')),
    'update': (update_plugin, ('Plugin updated!')),
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--config', '-c', 'config_file', default='pelicanconf.py', help='The path to Pelican configuration file.')
@click.option('--delete', '-d', 'operation', flag_value='delete', help='Delete a specific plugin.')
@click.option('--install', '-i', 'operation', flag_value='install', help='Install a specific plugin.')
@click.option('--update', '-u', 'operation', flag_value='update', help='Update a specific plugin.')
@click.argument('plugin_name', required=False)
@click.pass_context
def main(ctx, plugin_name, operation, config_file):
    """Installs Pelican Plugins in an easy way"""

    if not operation:
        click.echo(ctx.get_help())
        return

    plugins_path = discover_plugins_path(config_file)
    fn = operations[operation][0]

    try:
        fn(plugin_name, plugins_path)
    except BaseException as e:
        click.echo(e.msg)
    else:
        success_msg = operations[operation][1]

        click.echo(success_msg)
        click.echo("Don't forget to update the PLUGINS variable.")
