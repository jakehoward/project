import argparse
from importlib.metadata import version


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
