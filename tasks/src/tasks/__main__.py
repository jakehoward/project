from pathlib import Path

from tasks.arg_parser import make_parser
from tasks.commands.add import add
from tasks.commands.init import init


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        raise SystemExit(0)

    try:
        if args.command == "init":
            init(tasks_dir=Path(args.tasks_dir))
        if args.command == "add":
            add(name=args.name)
    except (FileExistsError, ValueError, RuntimeError, FileNotFoundError) as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
