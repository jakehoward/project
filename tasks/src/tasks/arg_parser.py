import argparse
from importlib.metadata import version


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=version("tasks"))

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--tasks-dir", required=False, default="./tasks")

    return parser
