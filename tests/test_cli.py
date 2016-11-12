import pytest
from click.testing import CliRunner
from pelican_plugin_installer import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Operation: None; Plugin: None'


def test_installing_a_plugin(runner):
    result = runner.invoke(cli.main, ['-i', 'test'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Operation: install; Plugin: test'


def test_updating_a_plugin(runner):
    result = runner.invoke(cli.main, ['-u', 'test'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Operation: update; Plugin: test'


def test_removing_a_plugin(runner):
    result = runner.invoke(cli.main, ['-d', 'test'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Operation: delete; Plugin: test'
