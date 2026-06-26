# tasks

## Running

Install dependencies and run the application:

```bash
uv sync --frozen
uv run tasks
```

Equivalently, as a module:

```bash
uv run python -m tasks
```

## Development

Install with dev dependencies:

```bash
uv sync
```

### Checks

```bash
./test.sh
```

Or run each step individually:

```bash
uv run ruff check              # lint
uv run ruff format --check     # format check (drop --check to apply)
uv run mypy                    # type check
uv run pytest --cov            # tests with coverage
```

Tooling configuration (ruff, mypy, pytest, coverage) lives in `pyproject.toml`.
