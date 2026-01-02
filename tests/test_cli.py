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
    assert "Allowed hex suffix lengths" in result.output
    assert "Actually delete" in result.output
    assert "anonymous volumes" in result.output


def test_remove_orphans_invalid_hex_lens() -> None:
    result = runner.invoke(app, ["remove-orphans", "--hex-lens", ""])
    assert result.exit_code == 2
    assert "Invalid" in result.output
