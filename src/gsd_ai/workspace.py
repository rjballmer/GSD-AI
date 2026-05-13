"""Workspace creation for the local-first GSD-AI Phase 1 skeleton."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .schema import ContextContract


@dataclass(frozen=True)
class WorkspaceFramework:
    """A user-facing workspace organization model."""

    name: str
    description: str
    directories: tuple[tuple[str, str], ...]
    projects_dir: str = "01_projects"


FRAMEWORKS: dict[str, WorkspaceFramework] = {
    "gsd": WorkspaceFramework(
        name="gsd",
        description="Execution-first layout for goals, projects, actions, waiting items, someday items, and reviews.",
        directories=(
            ("00_inbox", "unprocessed captures"),
            ("01_projects", "active projects"),
            ("02_next_actions", "next executable actions"),
            ("03_waiting", "delegated or blocked items awaiting someone/something"),
            ("04_areas", "ongoing responsibilities"),
            ("05_someday", "deferred ideas and possible future projects"),
            ("06_resources", "reusable references"),
            ("07_archives", "completed or inactive work"),
            ("08_reports", "recaps, plans, and exported artifacts"),
            (".gsd-ai", "machine-readable index, registry, and audit state"),
        ),
    ),
    "para": WorkspaceFramework(
        name="para",
        description="Second Brain layout for projects, areas, resources, and archives.",
        directories=(
            ("00_inbox", "unprocessed captures"),
            ("01_projects", "active projects"),
            ("02_areas", "ongoing responsibilities"),
            ("03_resources", "reusable references"),
            ("04_archives", "completed or inactive work"),
            ("05_reports", "recaps, plans, and exported artifacts"),
            (".gsd-ai", "machine-readable index, registry, and audit state"),
        ),
    ),
}

DEFAULT_FRAMEWORK = "gsd"


def get_framework(name: str) -> WorkspaceFramework:
    """Return a known workspace framework by name."""

    key = name.lower().strip()
    if key not in FRAMEWORKS:
        choices = ", ".join(sorted(FRAMEWORKS))
        raise ValueError(f"Unknown framework '{name}'. Choose one of: {choices}")
    return FRAMEWORKS[key]


def framework_prompt() -> str:
    """Text shown when the CLI asks the user to choose a framework."""

    return "\n".join(
        [
            "Choose a workspace framework:",
            "  1. gsd  - execution-first: inbox, projects, next actions, waiting, areas, someday, resources, archives, reports",
            "  2. para - Second Brain: inbox, projects, areas, resources, archives, reports",
            "Framework [gsd]: ",
        ]
    )


def root_context(framework: WorkspaceFramework) -> str:
    """Generate root agent context for a framework."""

    layout_lines = "\n".join(f"- `{path}/` — {description}" for path, description in framework.directories)
    return f"""# GSD-AI Workspace

This workspace stores durable project context for AI-assisted execution.

## Framework

{framework.name}

{framework.description}

## Operating principle

AI interprets. Code enforces. Humans approve durable writes.

## Layout

{layout_lines}
"""


def init_workspace(path: Path, *, framework: str = DEFAULT_FRAMEWORK, force: bool = False) -> list[Path]:
    """Create a local-first GSD-AI workspace and return created paths."""

    selected = get_framework(framework)
    path = path.expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for dirname, _description in selected.directories:
        directory = path / dirname
        directory.mkdir(exist_ok=True)
        created.append(directory)

    root_context_path = path / "AGENTS.md"
    if force or not root_context_path.exists():
        root_context_path.write_text(root_context(selected), encoding="utf-8")
        created.append(root_context_path)

    index = path / ".gsd-ai" / "index.json"
    if force or not index.exists():
        index.write_text(
            json.dumps(
                {
                    "version": 1,
                    "framework": selected.name,
                    "projects_dir": selected.projects_dir,
                    "projects": [],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        created.append(index)

    audit = path / ".gsd-ai" / "audit.jsonl"
    if force or not audit.exists():
        audit.write_text("", encoding="utf-8")
        created.append(audit)

    return created


def workspace_projects_dir(path: Path) -> str:
    """Read the configured projects directory from the workspace index."""

    index_path = path / ".gsd-ai" / "index.json"
    if not index_path.exists():
        return FRAMEWORKS[DEFAULT_FRAMEWORK].projects_dir
    index = json.loads(index_path.read_text(encoding="utf-8"))
    return index.get("projects_dir", FRAMEWORKS[DEFAULT_FRAMEWORK].projects_dir)


def create_project(path: Path, name: str, *, purpose: str = "") -> Path:
    """Create a project context contract."""

    path = path.expanduser().resolve()
    slug = "-".join(name.lower().split())
    projects_dir = workspace_projects_dir(path)
    project_dir = path / projects_dir / slug
    project_dir.mkdir(parents=True, exist_ok=True)

    contract = ContextContract(name=name, purpose=purpose)
    contract_path = project_dir / "context.md"
    if contract_path.exists():
        raise FileExistsError(f"Project already exists: {contract_path}")
    contract_path.write_text(contract.to_markdown(), encoding="utf-8")

    index_path = path / ".gsd-ai" / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index.setdefault("projects", []).append(
        {"name": name, "slug": slug, "path": str(contract_path.relative_to(path)), "status": "active"}
    )
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    return contract_path
