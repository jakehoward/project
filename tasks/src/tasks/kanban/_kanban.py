import os
from http.server import BaseHTTPRequestHandler

from tasks.kanban._html_helpers import build_html
from tasks.kanban._http_helpers import Method, content_type_html
from tasks.kanban._task_html import tasks_html_body


def handle(method: Method, path: str, body: bytes = b"") -> tuple[int, dict[str, str], bytes]:
    """
    No IO function that handles important part of HTTP Request -> Response

    :param method: HTTP method, e.g. GET
    :param path: the http path, e.g. /tasks
    :param body: bytes representing the body of the request
    :return: tuple(status, headers, body)
    """
    if method == Method.GET:
        if path == "/":
            return 200, {**content_type_html}, build_html('<a href="/tasks">Tasks</a>')
        if path == "/tasks":
            return 200, {**content_type_html}, build_html(tasks_html_body())

    return 404, content_type_html, build_html("<h1>Not found</h1>")


class KanbanHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args, **kwargs):
        if os.environ.get("DEBUG", "").lower() == "tasks":
            super().log_message(format, *args)

    def do_GET(self):
        status, headers, body = handle(Method.GET, self.path)
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        self.send_response(500)
