# tasks

Tasks lets you manage your project without a third party issue tracker.

Each task is a Markdown file which tracks its state and history in a footer. No magic, just text (and a .tasks file).

## Usage

Install
```
git clone https://github.com/jakehoward/project
cd project/tasks

```

## Running

Install dependencies and run the application:

```bash
uv sync --frozen
uv run tasks
uv pip install -e .
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
