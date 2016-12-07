import click

from .manager import Manager
from .exceptions import BaseException

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)

SUCCESS_MESSAGES = {
    'install': 'Plugin installed!',
    'delete': 'Plugin removed!',
    'update': 'Plugin updated!',
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

    manager = Manager(config_file)
    manager.initialize_local_repository()

    plugin = manager.instance_plugin(plugin_name)

    try:
        manager.run(operation, plugin)
    except BaseException as e:
        click.echo(e.msg)
    else:
        success_msg = SUCCESS_MESSAGES[operation]

        click.echo(success_msg)
        click.echo("Don't forget to update the PLUGINS variable.")
