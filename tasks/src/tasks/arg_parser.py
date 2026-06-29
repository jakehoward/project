import argparse
from importlib.metadata import version
from pathlib import Path

from tasks.task import TaskStatus


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A filesystem-based task tracker for small projects.",
        epilog="Run 'tasks <command> --help' for more info on a specific command.",
    )
    parser.add_argument("--version", action="version", version=version("tasks"))

    subparsers = parser.add_subparsers(dest="command", title="commands")

    _list_parser = subparsers.add_parser("list", help="list tasks")

    serve_parser = subparsers.add_parser("serve", help="serve tasks on an http server")
    serve_parser.add_argument("--port", default=8000, type=int)

    move_parser = subparsers.add_parser("move", help="change a tasks status")
    move_parser.add_argument("--task-file", type=Path, required=True, help="path to task file")
    move_parser.add_argument(
        "--status",
        required=True,
        type=TaskStatus,
        choices=[m.value for m in TaskStatus],
        help="new status",
    )

    init_parser = subparsers.add_parser("init", help="initialise a new tasks project")
    init_parser.add_argument(
        "--tasks-dir",
        required=False,
        default="tasks",
        help=(
            "Path to where tasks will be stored. "
            "Must be inside current working directory. "
            'Defaults to "tasks"'
        ),
    )

    add_parser = subparsers.add_parser("add", help="add a new task")
    add_parser.add_argument("--name", required=True)

    return parser
