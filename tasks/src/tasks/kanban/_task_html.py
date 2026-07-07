import html
from textwrap import dedent

from tasks import actions
from tasks.task import Task


def li(task: Task) -> str:
    return (
        f"<li>{html.escape(task.name)}"
        f'(<a href="/coming-soon">{html.escape(task.filename)}</a>)</li>'
    )


def tasks_html_body() -> str:
    tasks = actions.list_tasks()
    return dedent(f"""
        <h1>Tasks</h1>
        <ul>
            {"\n".join([li(task) for task in tasks])}
        </ul>
    """)
