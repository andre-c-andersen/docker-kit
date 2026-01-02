"""Remove stopped Docker containers with hex suffixes (orphaned compose containers)."""

from __future__ import annotations

import re
import subprocess

HEX_PATTERN = re.compile(r"^[0-9a-f]+$")


def run_docker(cmd: list[str]) -> str:
    """Run a docker command and return stripped output."""
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()


def parse_hex_lengths(spec: str) -> set[int]:
    """Parse comma-separated hex suffix lengths."""
    lengths: set[int] = set()
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        n = int(token)
        if n <= 0:
            raise ValueError("length must be > 0")
        lengths.add(n)
    if not lengths:
        raise ValueError("no lengths provided")
    return lengths


def get_stopped_containers() -> list[str]:
    """Get names of all stopped containers."""
    out = run_docker(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            "status=exited",
            "--filter",
            "status=created",
            "--filter",
            "status=dead",
            "--format",
            "{{.Names}}",
        ]
    )
    if not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_orphan_container(name: str, allowed_lengths: set[int]) -> bool:
    """Check if container name has a hex suffix matching allowed lengths."""
    if "-" not in name:
        return False
    suffix = name.rsplit("-", 1)[1]
    if len(suffix) not in allowed_lengths:
        return False
    return HEX_PATTERN.fullmatch(suffix) is not None


def remove_container(name: str, volumes: bool) -> None:
    """Remove a container, optionally with its volumes."""
    cmd = ["docker", "rm"]
    if volumes:
        cmd.append("-v")
    cmd.append(name)
    subprocess.check_call(cmd)


def find_orphans(hex_lengths: set[int]) -> list[str]:
    """Find all orphaned containers matching the hex length criteria."""
    containers = get_stopped_containers()
    return [name for name in containers if is_orphan_container(name, hex_lengths)]


def remove_orphans(orphans: list[str], volumes: bool) -> int:
    """Remove orphaned containers. Returns count of failures."""
    failed = 0
    for name in orphans:
        try:
            remove_container(name, volumes=volumes)
        except subprocess.CalledProcessError as e:
            failed += 1
            print(f"FAILED: {name}: {e}")
    return failed
