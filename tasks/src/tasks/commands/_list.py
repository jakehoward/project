from collections.abc import Sequence

from tasks import actions


def _format_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    columns = list(zip(headers, *rows, strict=True)) if rows else [(header,) for header in headers]
    widths = [max(len(str(cell)) for cell in column) for column in columns]

    def format_row(row: Sequence[str]) -> str:
        return "  ".join(str(cell).ljust(width) for cell, width in zip(row, widths, strict=True))

    return "\n".join([format_row(headers), *(format_row(row) for row in rows)])


def _ellipses(s: str) -> str:
    if len(s) > 53:
        return s[0:50] + "..."
    return s


def list_tasks() -> None:
    tasks = actions.list_tasks()
    if not tasks:
        print("No tasks found.")
        return

    headers = ("CREATED", "STATUS", "NAME", "AUTHOR")
    rows = [
        (
            task.metadata.created_at.strftime("%Y-%m-%d %H:%M"),
            task.metadata.status,
            _ellipses(task.name),
            _ellipses(task.metadata.created_by),
        )
        for task in tasks
    ]
    print(_format_table(headers, rows))
