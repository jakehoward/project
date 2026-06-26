import re

import pytest

from tasks.arg_parser import make_parser


def test_init_command():
    parser = make_parser()
    args = parser.parse_args(["init"])
    assert args.command == "init"


def test_init_command_tasks_dir_flag():
    parser = make_parser()
    args = parser.parse_args(["init", "--tasks-dir", "the/tasks/dir"])
    assert args.command == "init"
    assert args.tasks_dir == "the/tasks/dir"


def test_version_flag(capsys):
    parser = make_parser()
    with pytest.raises(SystemExit) as exec_info:
        parser.parse_args(["--version"])
    assert exec_info.value.code == 0
    assert re.search(r"\d+\.\d+\.\d+", capsys.readouterr().out)
