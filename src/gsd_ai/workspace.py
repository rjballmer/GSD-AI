"""Workspace creation for the local-first GSD-AI Phase 1 skeleton."""

from __future__ import annotations

import json
from pathlib import Path

from .schema import ContextContract

DEFAULT_DIRS = [
    "00_inbox",
    "01_workstreams",
    "02_areas",
    "03_resources",
    "04_archives",
    "05_reports",
    ".gsd-ai",
]


ROOT_CONTEXT = """# GSD-AI Workspace

This workspace stores durable goal/work context for AI-assisted execution.

## Operating principle

AI interprets. Code enforces. Humans approve durable writes.

## Layout

- `00_inbox/` — unprocessed captures
- `01_workstreams/` — active goals, projects, and workstreams
- `02_areas/` — ongoing responsibilities
- `03_resources/` — reusable references
- `04_archives/` — completed or inactive work
- `05_reports/` — recaps, plans, and exported artifacts
- `.gsd-ai/` — machine-readable index, registry, and audit state
"""


def init_workspace(path: Path, *, force: bool = False) -> list[Path]:
    """Create a local-first GSD-AI workspace and return created paths."""

    path = path.expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for dirname in DEFAULT_DIRS:
        directory = path / dirname
        directory.mkdir(exist_ok=True)
        created.append(directory)

    root_context = path / "AGENTS.md"
    if force or not root_context.exists():
        root_context.write_text(ROOT_CONTEXT, encoding="utf-8")
        created.append(root_context)

    index = path / ".gsd-ai" / "index.json"
    if force or not index.exists():
        index.write_text(json.dumps({"version": 1, "workstreams": []}, indent=2) + "\n", encoding="utf-8")
        created.append(index)

    audit = path / ".gsd-ai" / "audit.jsonl"
    if force or not audit.exists():
        audit.write_text("", encoding="utf-8")
        created.append(audit)

    return created


def create_workstream(path: Path, name: str, *, purpose: str = "") -> Path:
    """Create a workstream context contract."""

    path = path.expanduser().resolve()
    slug = "-".join(name.lower().split())
    workstream_dir = path / "01_workstreams" / slug
    workstream_dir.mkdir(parents=True, exist_ok=True)

    contract = ContextContract(name=name, purpose=purpose)
    contract_path = workstream_dir / "context.md"
    if contract_path.exists():
        raise FileExistsError(f"Workstream already exists: {contract_path}")
    contract_path.write_text(contract.to_markdown(), encoding="utf-8")

    index_path = path / ".gsd-ai" / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index.setdefault("workstreams", []).append({"name": name, "slug": slug, "path": str(contract_path.relative_to(path)), "status": "active"})
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    return contract_path
