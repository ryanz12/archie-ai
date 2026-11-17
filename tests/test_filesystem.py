from pathlib import Path
from tools.filesystem import *

def test_list_files():
    assert list_files(".") == sorted(['.pytest_cache', '.venv', 'agent', 'interface', 'llm', 'main.py', 'tests', 'tools'])

def test_find_directory():
    expected = str(Path.home() / "Documents/code/archie-ai")
    assert find_directory("archie-ai") == [expected]

def test_find_file():
    expected = str(Path.home() / "Documents/code/archie-ai/tests/test_filesystem.py")
    assert find_file("test_filesystem.py") == [expected]

def test_get_file_info():
    stats = get_file_info("main.py")

    assert stats["name"] == "main.py" and stats["stem"] == "main" \
        and stats["extension"] == ".py"

def test_read_unknown_file():
    assert read_file("awd") == "Error: Specified file does not exist or is not accessible"

def test_read_file():
    assert read_file("./tests/test.md") == "Beautiful is better than ugly.\nExplicit is better than implicit.\n"
