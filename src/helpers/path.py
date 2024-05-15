from pathlib import Path

type PathLike = Path | str


def parse_path(path: PathLike, ensure_parent: bool = False) -> Path:
    """
    Converte um objeto que tem formato de caminho de arquivo para um
    objeto de caminho de arquivo.
    """
    if isinstance(path, str):
        path = Path(path)

    path = path.resolve()
    if ensure_parent and not path.parent.exists():
        path.parent.mkdir()

    return path
