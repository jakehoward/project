from pathlib import Path

import pytest

from tasks.commands import list_tasks


class TestListTasks:
    def test_list_throws_if_not_init(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        with pytest.raises(RuntimeError, match="No config file found."):
            list_tasks()
