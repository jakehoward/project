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
