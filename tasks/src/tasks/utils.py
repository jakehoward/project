import re
import subprocess


def normalise_name(name: str, max_len: int = 50) -> str:
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-zA-Z0-9_-]", "__", name)
    name = re.sub(r"___+", "__", name)
    if set(name) == {"_"}:
        raise ValueError("name cannot be normalised - use a-zA-Z0-9 in the task name")
    return name[:max_len]


def get_git_user() -> str:
    try:
        email = subprocess.check_output(["git", "config", "user.email"], text=True)  # noqa: S607
        name = subprocess.check_output(["git", "config", "user.name"], text=True)  # noqa: S607
        return f"{name} <{email}>"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Unknown"


def sanitise_for_single_line(s: str, max_len: int = 100) -> str:
    return s.replace("\n", "")[:max_len]
