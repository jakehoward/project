import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from textwrap import dedent

from tasks import actions
from tasks.task import Task


def li(task: Task) -> str:
    return (
        f"<li>{html.escape(task.name)}"
        f'(<a href="/coming-soon">{html.escape(task.filename)}</a>)</li>'
    )


def build_html(tasks: list[Task]):
    return dedent(f"""\
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <ul>
                    {"\n".join([li(task) for task in tasks])}
                </ul>
            </body>
        </html>
    """)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args, **kwargs):
        if os.environ.get("DEBUG", "").lower() == "tasks":
            super().log_message(format, *args)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            html_page = '<a href="/tasks">Tasks</a>'
        elif self.path.startswith("/coming-soon"):
            self.send_response(200)
            html_page = "<h1>Coming Soon</h1>"
        elif self.path.startswith("/tasks"):
            self.send_response(200)
            tasks = actions.list_tasks()
            html_page = build_html(tasks)
        else:
            self.send_response(404)
            html_page = "<h1>Not Found</h1>"

        body = bytes(html_page, "utf-8")
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        self.send_response(500)


def serve_http(port: int) -> None:
    print(f"Serving at: \nhttp://localhost:{port}/  --  (Press Ctrl+C to stop)")
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()
