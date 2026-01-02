# docker-kit

A toolkit for common Docker tasks.

## Installation

```bash
uvx docker-kit --help
```

Or install globally:

```bash
uv tool install docker-kit
```

## Commands

### remove-orphans

Remove stopped containers with hex suffixes (orphaned compose containers).

```bash
# Dry run (default) - shows what would be deleted
uvx docker-kit remove-orphans

# Actually delete the containers
uvx docker-kit remove-orphans --apply

# Also remove anonymous volumes
uvx docker-kit remove-orphans --apply --volumes

# Custom hex suffix lengths (default: 12)
uvx docker-kit remove-orphans --hex-lens 12,64
```

## Development

```bash
# Install dependencies
uv sync

# Run linting
uv run ruff format .
uv run ruff check .

# Run type checking
uv run pyright

# Run tests
uv run pytest -v
```

## License

MIT
