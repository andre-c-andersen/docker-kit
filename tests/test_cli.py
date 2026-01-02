"""Tests for CLI."""

from typer.testing import CliRunner

from docker_kit.cli import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "A toolkit for common Docker tasks" in result.output


def test_remove_orphans_help() -> None:
    result = runner.invoke(app, ["remove-orphans", "--help"])
    assert result.exit_code == 0
    assert "--hex-lens" in result.output
    assert "--apply" in result.output
    assert "--volumes" in result.output


def test_remove_orphans_invalid_hex_lens() -> None:
    result = runner.invoke(app, ["remove-orphans", "--hex-lens", ""])
    assert result.exit_code == 2
    assert "Invalid --hex-lens" in result.output
