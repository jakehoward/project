import dataclasses
from pathlib import Path

from tasks import actions
from tasks.config import read_config
from tasks.task import Task, TaskStatus


def move_task(path_to_task: Path, new_status: TaskStatus) -> Task:
    config = read_config()
    if config is None:
        ## improvement: deduplicate this message
        raise RuntimeError("No config file found. Maybe you need to run `tasks init`?")

    task = actions.read_task(path_to_task)
    if task.metadata.status == new_status:
        raise ValueError(f"Error: task {task.name} already has status {task.metadata.status}")

    updated_task = dataclasses.replace(
        task, metadata=dataclasses.replace(task.metadata, status=new_status)
    )

    actions.persist_task(updated_task)

    return updated_task
