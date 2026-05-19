from __future__ import annotations

import json
import re
from pathlib import Path

from langchain.tools import tool


CATEGORIES = {
    "install": ["install", "bootstrap", "setup", "deps"],
    "dev": ["dev", "start", "serve", "watch"],
    "test": ["test", "pytest", "jest", "vitest", "unittest"],
    "build": ["build", "compile", "bundle", "dist"],
}


def _normalize_repo_path(repo_path: str) -> Path:
    path = Path(repo_path).expanduser().resolve()
    if not path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")
    if not path.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo_path}")
    return path


def _categorize(name: str) -> list[str]:
    lowered = name.lower()
    return [cat for cat, keywords in CATEGORIES.items() if any(k in lowered for k in keywords)]


@tool("dependency_summary", parse_docstring=True)
def dependency_summary_tool(repo_path: str = ".") -> dict[str, object]:
    """Summarize dependency files and extract common dev commands.

    Args:
        repo_path: Target repository root path. Defaults to current directory.

    Returns:
        Dependency file inventory and categorized commands.
    """
    root = _normalize_repo_path(repo_path)

    files = {
        "package_json": root / "package.json",
        "pyproject_toml": root / "pyproject.toml",
        "requirements_txt": root / "requirements.txt",
        "go_mod": root / "go.mod",
        "cargo_toml": root / "Cargo.toml",
        "makefile": root / "Makefile",
    }

    existing_files = {key: str(path) for key, path in files.items() if path.exists() and path.is_file()}

    commands: list[dict[str, object]] = []

    package_json = files["package_json"]
    if package_json.exists() and package_json.is_file():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = data.get("scripts") if isinstance(data, dict) else None
            if isinstance(scripts, dict):
                for name, cmd in scripts.items():
                    if isinstance(cmd, str):
                        commands.append(
                            {
                                "source": str(package_json),
                                "name": f"npm run {name}",
                                "command": cmd,
                                "categories": _categorize(name),
                            }
                        )
        except Exception:
            pass

    makefile = files["makefile"]
    if makefile.exists() and makefile.is_file():
        for line in makefile.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line or line.startswith("#"):
                continue
            if re.match(r"^[A-Za-z0-9_.-]+\s*:", line):
                target = line.split(":", 1)[0].strip()
                commands.append(
                    {
                        "source": str(makefile),
                        "name": f"make {target}",
                        "command": f"make {target}",
                        "categories": _categorize(target),
                    }
                )

    categorized: dict[str, list[dict[str, object]]] = {k: [] for k in CATEGORIES}
    uncategorized: list[dict[str, object]] = []

    for item in commands:
        cats = item.get("categories") or []
        if not cats:
            uncategorized.append(item)
            continue
        for cat in cats:
            categorized[cat].append(item)

    return {
        "repo_path": str(root),
        "dependency_files": existing_files,
        "commands": {
            **categorized,
            "uncategorized": uncategorized,
        },
    }
