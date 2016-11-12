import click


@click.command()
@click.option('--delete', '-d', 'operation', flag_value='delete', help='Delete a specific plugin.')
@click.option('--install', '-i', 'operation', flag_value='install', help='Install a specific plugin.')
@click.option('--update', '-u', 'operation', flag_value='update', help='Update a specific plugin.')
@click.argument('plugin_name', required=False)
def main(plugin_name, operation):
    """Installs Pelican Plugins in an easy way"""
    click.echo("Operation: {0}; Plugin: {1}".format(operation, plugin_name))
