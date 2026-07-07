from http.server import ThreadingHTTPServer

from tasks.kanban import KanbanHandler


def serve_http(port: int) -> None:
    print(f"Serving at: \nhttp://localhost:{port}/  --  (Press Ctrl+C to stop)")
    server = ThreadingHTTPServer(("127.0.0.1", port), KanbanHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()
