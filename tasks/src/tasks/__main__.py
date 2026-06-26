from pathlib import Path

from tasks.arg_parser import make_parser
from tasks.commands.init import init


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        raise SystemExit(0)

    if args.command == "init":
        try:
            init(tasks_dir=Path(args.tasks_dir))
        except FileExistsError as e:
            print("Error:", e)
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
