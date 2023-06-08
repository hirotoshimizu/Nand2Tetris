import sys
from pathlib import Path

import pytest
from jack.jack_analyzer import get_file_path, get_vm_file


def test_get_file_path(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py", "../ExpressionLessSquare/Main.jack"])
    file_path = get_file_path()
    assert file_path == Path(sys.argv[1])


def test_get_vm_file(tmp_path):
    test_dir = tmp_path / "sub"
    test_dir.mkdir()
    jack_file = test_dir / "hello.jack"
    jack_file.write_text("hello")
    assert len(get_vm_file(jack_file)) == 1


def test_get_vm_file_dir(tmp_path):
    test_dir = tmp_path / "sub"
    test_dir.mkdir()
    jack_file1 = test_dir / "hello1.jack"
    jack_file1.write_text("hello")
    jack_file2 = test_dir / "hello2.jack"
    jack_file2.write_text("hello")
    assert len(get_vm_file(jack_file1.parent)) == 2
