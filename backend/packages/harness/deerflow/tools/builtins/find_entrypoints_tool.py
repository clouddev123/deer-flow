from __future__ import annotations

import json
from pathlib import Path

from langchain.tools import tool


PATTERNS = {
    "python": ["main.py", "app.py", "__main__.py"],
    "node": ["src/index.ts", "src/index.js", "server.ts", "server.js"],
    "nextjs": ["next.config.js", "next.config.mjs", "next.config.ts"],
    "go": ["main.go"],
}


def _normalize_repo_path(repo_path: str) -> Path:
    path = Path(repo_path).expanduser().resolve()
    if not path.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")
    if not path.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo_path}")
    return path


def _add_hit(results: list[dict[str, str]], language: str, path: Path, reason: str) -> None:
    results.append({"language": language, "path": str(path), "reason": reason})


@tool("find_entrypoints", parse_docstring=True)
def find_entrypoints_tool(repo_path: str = ".") -> dict[str, object]:
    """Detect likely application startup entrypoints across common stacks.

    Args:
        repo_path: Target repository root path. Defaults to current directory.

    Returns:
        List of detected entrypoint candidates with language and reason.
    """
    root = _normalize_repo_path(repo_path)
    results: list[dict[str, str]] = []

    for language, rel_paths in PATTERNS.items():
        for rel in rel_paths:
            candidate = root / rel
            if candidate.exists() and candidate.is_file():
                _add_hit(results, language, candidate, f"matched common path {rel}")

    package_json = root / "package.json"
    if package_json.exists() and package_json.is_file():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = data.get("scripts") if isinstance(data, dict) else None
            if isinstance(scripts, dict) and scripts:
                _add_hit(results, "node", package_json, f"package.json scripts: {', '.join(sorted(scripts.keys()))}")
        except Exception:
            pass

    for next_dir in ["app", "pages"]:
        candidate = root / next_dir
        if candidate.exists() and candidate.is_dir():
            _add_hit(results, "nextjs", candidate, f"Next.js directory '{next_dir}/' found")

    go_cmd = root / "cmd"
    if go_cmd.exists() and go_cmd.is_dir():
        _add_hit(results, "go", go_cmd, "Go cmd/ directory found")

    java_application_files = list(root.rglob("*Application.java"))[:20]
    for java_file in java_application_files:
        _add_hit(results, "java", java_file, "Spring Boot style Application.java")

    java_main_candidates = list(root.rglob("*.java"))[:500]
    for java_file in java_main_candidates:
        try:
            content = java_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "public static void main(" in content:
            _add_hit(results, "java", java_file, "contains public static void main(...)")

    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for item in results:
        key = (item["language"], item["path"], item["reason"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)

    return {"repo_path": str(root), "entrypoints": deduped}
