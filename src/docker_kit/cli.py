"""Docker Kit CLI - A toolkit for common Docker tasks."""

from __future__ import annotations

from typing import Annotated

import typer

from docker_kit.tools.remove_orphans import find_orphans
from docker_kit.tools.remove_orphans import parse_hex_lengths
from docker_kit.tools.remove_orphans import remove_orphans

app = typer.Typer(
    name="docker-kit",
    help="A toolkit for common Docker tasks.",
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context) -> None:
    """A toolkit for common Docker tasks."""
    pass


def _remove_orphans_impl(hex_lens: str, apply: bool, volumes: bool) -> None:
    """Core implementation for removing orphaned containers."""
    try:
        allowed_lengths = parse_hex_lengths(hex_lens)
    except ValueError as e:
        typer.echo(f"Invalid --hex-lens: {e}", err=True)
        raise typer.Exit(2) from None

    orphans = find_orphans(allowed_lengths)

    if not orphans:
        typer.echo("No matching stopped containers.")
        return

    typer.echo(f"Matched {len(orphans)} stopped container(s) (hex suffix lens={sorted(allowed_lengths)}):")
    for name in orphans:
        typer.echo(f"  - {name}")

    if not apply:
        typer.echo("\nDRY RUN. Re-run with --apply to delete.")
        return

    failed = remove_orphans(orphans, volumes=volumes)
    if failed > 0:
        raise typer.Exit(3)


@app.command("remove-orphans")
def remove_orphans_cmd(
    hex_lens: Annotated[str, typer.Option("--hex-lens", help="Allowed hex suffix lengths (comma-separated)")] = "12",
    apply: Annotated[bool, typer.Option("--apply", "-a", help="Actually delete. Default is dry-run.")] = False,
    volumes: Annotated[bool, typer.Option("--volumes", "-v", help="Also remove anonymous volumes")] = False,
) -> None:
    """Remove stopped containers with hex suffixes (orphaned compose containers)."""
    _remove_orphans_impl(hex_lens, apply, volumes)


@app.command("nuke-kids")
def nuke_kids_cmd(
    hex_lens: Annotated[str, typer.Option("--hex-lens", help="Allowed hex suffix lengths (comma-separated)")] = "12",
) -> None:
    """Alias for 'remove-orphans --apply --volumes'."""
    _remove_orphans_impl(hex_lens, apply=True, volumes=True)


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
