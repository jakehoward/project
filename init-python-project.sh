#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:?usage: ./setup-python-project.sh <project-name>}"

# Distribution name normalised to a valid Python package (module) name:
# lowercase, and -/./space collapsed to underscore.
MODULE_NAME="$(printf '%s' "$PROJECT_NAME" \
  | tr '[:upper:]' '[:lower:]' \
  | tr -s '. -' '_')"

# Module name must be a valid Python identifier.
if ! printf '%s' "$MODULE_NAME" | grep -Eq '^[a-z_][a-z0-9_]*$'; then
  echo "Derived package name '$MODULE_NAME' is not a valid Python identifier." >&2
  echo "Pick a name made of letters, digits, hyphens or underscores, not starting with a digit." >&2
  exit 1
fi

command -v uv >/dev/null 2>&1 || { echo "uv not found on PATH. Install: https://docs.astral.sh/uv/getting-started/installation/" >&2; exit 1; }

mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

mkdir -p "src/$MODULE_NAME" tests

cat > pyproject.toml << EOF
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "mypy>=2.1.0",
    "pytest>=9.1.1",
    "pytest-cov>=7.1.0",
    "ruff>=0.15.20",
]

[build-system]
requires = ["uv_build>=0.9.15,<0.10.0"]
build-backend = "uv_build"

[project.scripts]
$PROJECT_NAME = "$MODULE_NAME.__main__:main"

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "S"]
ignore = []

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]

[tool.mypy]
python_version = "3.12"
files = ["src", "tests"]

check_untyped_defs = true
warn_unreachable = true
strict_equality = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_unused_configs = true
no_implicit_reexport = true
extra_checks = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q --import-mode=importlib"

[tool.coverage.run]
source = ["$MODULE_NAME"]
omit = [
    "*/__init__.py",
    "*/__main__.py",
]
EOF

cat > README.md << EOF
# $PROJECT_NAME

## Running

Install dependencies and run the application:

\`\`\`bash
uv sync --frozen
uv run $PROJECT_NAME
\`\`\`

Equivalently, as a module:

\`\`\`bash
uv run python -m $MODULE_NAME
\`\`\`

## Development

Install with dev dependencies:

\`\`\`bash
uv sync
\`\`\`

### Checks

\`\`\`bash
./test.sh
\`\`\`

Or run each step individually:

\`\`\`bash
uv run ruff check              # lint
uv run ruff format --check     # format check (drop --check to apply)
uv run mypy                    # type check
uv run pytest --cov            # tests with coverage
\`\`\`

Tooling configuration (ruff, mypy, pytest, coverage) lives in \`pyproject.toml\`.
EOF

cat > test.sh << 'EOF'
#!/usr/bin/env bash

set -euo pipefail

## Ensure we're running from the script location
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 1

## lint and format
uv run ruff check
uv run ruff format --check --diff

## typecheck
uv run mypy

## test
uv run pytest --cov
EOF
chmod +x test.sh

# --- inferred source bodies; replace with your real code ---

: > "src/$MODULE_NAME/__init__.py"

cat > "src/$MODULE_NAME/hello.py" << EOF
def hello() -> str:
    return "Hello from $PROJECT_NAME!"
EOF

cat > "src/$MODULE_NAME/__main__.py" << EOF
from $MODULE_NAME.hello import hello


def main() -> None:
    print(hello())


if __name__ == "__main__":
    main()
EOF

cat > "tests/test_hello.py" << EOF
from $MODULE_NAME.hello import hello


def test_hello() -> None:
    assert hello() == "Hello from $PROJECT_NAME!"
EOF

# --- end inferred bodies ---

uv sync

echo "Done. Next:"
echo "  cd $PROJECT_NAME"
echo "  ./test.sh"
echo "  uv run $PROJECT_NAME"
