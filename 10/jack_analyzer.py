import sys
from pathlib import Path


def get_file_path() -> Path:
    return Path(sys.argv[1])


def get_vm_file(path: Path):
    if path.is_dir():
        return [file_name for file_name in path.glob("*.jack")]
    return [path]
