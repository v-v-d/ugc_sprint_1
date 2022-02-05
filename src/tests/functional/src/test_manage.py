from typer.testing import CliRunner

from manage import typer_app

runner = CliRunner()


def test_shell():
    result = runner.invoke(typer_app, ["shell"])
    assert result.exit_code == 0


def test_runserver():
    result = runner.invoke(typer_app, ["runserver"])
    assert result.exit_code == 0
