---
name: Serve HTML representation of tasks
status: todo
created_by: Jake Howard <jake@jakehoward.org>
created_at: 2026-06-29 21:54:17.225809
---

# Serve HTML representation of tasks

Allow users to see a basic kanban board of tasks in the browser. Clicking on a task shows the contents of the task.

Not in scope for this task:

- Moving tasks via HTTP request

## Acceptance criteria

- [x] `tasks serve -p {PORT}` starts an HTTP server listening on `http://127.0.0.1:PORT/`
- [ ] `/tasks` shows a kanban board of tasks
- [ ] `/tasks/some-way-to-id-task` shows the file contents
- [ ] `/tasks/some-way-to-id-task` has a back button to go back to the kanban board
- [ ] The HTML uses zero dependencies
- [ ] The Python code does not introduce any new dependencies

## Eng tasks

- [x] Figure out how to test the HTTP server (handler logic)
- [ ] Create a Kanban board in HTML
- [ ] Create a task view in HTML
- [ ] Figure out how to id a task in a path-friendly way
