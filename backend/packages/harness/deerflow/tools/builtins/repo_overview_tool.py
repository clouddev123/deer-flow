from __future__ import annotations

from pathlib import Path

from langchain.tools import tool

KEY_FILES = ["README.md", "package.json", "pyproject.toml", "Makefile", "Dockerfile"]


def _normalize_repo_path(repo_path: str) -> Path:
    path = Path(repo_path).expanduser().resolve()
    if not path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")
    if not path.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo_path}")
    return path


@tool("repo_overview", parse_docstring=True)
def repo_overview_tool(repo_path: str = ".") -> dict[str, object]:
    """Scan top-level repository structure and key metadata files.

    Args:
        repo_path: Target repository root path. Defaults to current directory.

    Returns:
        Structured overview including key file existence and top-level entries.
    """
    root = _normalize_repo_path(repo_path)
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

    top_level_directories = [p.name for p in entries if p.is_dir()][:100]
    top_level_files = [p.name for p in entries if p.is_file()][:100]

    key_files: dict[str, str] = {}
    for name in KEY_FILES:
        candidate = root / name
        if candidate.exists() and candidate.is_file():
            key_files[name] = str(candidate)

    return {
        "repo_path": str(root),
        "readme": key_files.get("README.md"),
        "key_files": key_files,
        "top_level_directories": top_level_directories,
        "top_level_files": top_level_files,
    }
