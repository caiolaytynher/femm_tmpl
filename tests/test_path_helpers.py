from pathlib import Path

from src.helpers.path import parse_path


def test_parse_path():
    assert isinstance(parse_path('foo'), Path)
    assert isinstance(parse_path(Path('foo')), Path)

    path = parse_path('foo/bar', ensure_parent=True)
    assert path.parent.exists()

    path.parent.rmdir()
