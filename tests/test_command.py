from pelican_plugin_installer import cli


def test_without_option_prints_the_help_menu(runner):
    result = runner.invoke(cli.main)

    assert 'Usage:' in result.output
