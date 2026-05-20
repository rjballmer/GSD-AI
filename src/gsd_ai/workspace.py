"""Workspace creation for the local-first GSD-AI Phase 1 skeleton."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .schema import ApprovalStatus, AuditEvent, ContextContract, ContextSource, Signal, SignalType, stable_slug


@dataclass(frozen=True)
class WorkspaceFramework:
    """A user-facing workspace organization model."""

    name: str
    description: str
    directories: tuple[tuple[str, str], ...]
    projects_dir: str = "01_projects"


FRAMEWORKS: dict[str, WorkspaceFramework] = {
    "para": WorkspaceFramework(
        name="para",
        description="Recommended. Second Brain layout for projects, areas, resources, and archives. PARA is especially useful with AI because it creates rich, durable context for project reasoning.",
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
    "gsd": WorkspaceFramework(
        name="gsd",
        description="Execution-first layout for projects, next actions, waiting items, someday items, responsibilities, references, and reviews.",
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
}

DEFAULT_FRAMEWORK = "para"

FRAMEWORK_LINKS = {
    "para": "https://fortelabs.com/blog/para/",
    "gsd": "https://gettingthingsdone.com/",
}


PROJECT_CONTEXT_GUIDANCE = """# Project Setup Guidance

You do not need to type a full project charter into the CLI.

Recommended flow:

1. Create the project with a short name and optional one-line purpose.
2. Add relevant source links with `--source` or `--doc`.
3. Let an AI assistant read those sources and propose project signals: goals, decisions, risks, dependencies, actions, and open questions.
4. Review and approve any durable writes before the project context is updated.

Useful sources:

- project docs
- planning docs
- design docs
- meeting notes
- tickets/issues
- PRDs
- dashboards
- chat threads
- repo links
"""


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
            "  1. para - RECOMMENDED: Second Brain layout for richer AI context gathering",
            "            Learn more: https://fortelabs.com/blog/para/",
            "  2. gsd  - execution-first layout inspired by Getting Things Done",
            "            Learn more: https://gettingthingsdone.com/",
            "Framework [para]: ",
        ]
    )


def root_context(framework: WorkspaceFramework) -> str:
    """Generate root agent context for a framework."""

    layout_lines = "\n".join(f"- `{path}/` — {description}" for path, description in framework.directories)
    para_note = "\nPARA is recommended because AI can use the Projects / Areas / Resources / Archives structure to gather richer context before proposing plans or actions.\n" if framework.name == "para" else ""
    return f"""# GSD-AI Workspace

This workspace stores durable project context for AI-assisted execution.

## Framework

{framework.name}

{framework.description}{para_note}

Reference links:

- PARA / Second Brain: {FRAMEWORK_LINKS['para']}
- Getting Things Done: {FRAMEWORK_LINKS['gsd']}

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

    guidance_path = path / ".gsd-ai" / "PROJECT_SETUP.md"
    if force or not guidance_path.exists():
        guidance_path.write_text(PROJECT_CONTEXT_GUIDANCE, encoding="utf-8")
        created.append(guidance_path)

    index = path / ".gsd-ai" / "index.json"
    if force or not index.exists():
        index.write_text(
            json.dumps(
                {
                    "version": 1,
                    "framework": selected.name,
                    "projects_dir": selected.projects_dir,
                    "framework_links": FRAMEWORK_LINKS,
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


def read_index(path: Path) -> dict:
    """Read the workspace index with a clearer error for corrupt state."""

    index_path = path / ".gsd-ai" / "index.json"
    try:
        return json.loads(index_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Missing workspace index: {index_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid workspace index JSON: {index_path}") from exc


def write_index(path: Path, index: dict) -> None:
    (path / ".gsd-ai" / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")


def project_dir_for(path: Path, project: str) -> Path:
    """Return the existing project directory for a project name or slug."""

    path = path.expanduser().resolve()
    wanted = stable_slug(project)
    index = read_index(path)
    for record in index.get("projects", []):
        if record.get("slug") == wanted or stable_slug(record.get("name", "")) == wanted:
            return path / workspace_projects_dir(path) / record["slug"]
    raise FileNotFoundError(f"Project not found in workspace index: {project}")


def create_project(
    path: Path,
    name: str,
    *,
    purpose: str = "",
    sources: list[ContextSource] | None = None,
) -> Path:
    """Create a project context contract."""

    path = path.expanduser().resolve()
    slug = stable_slug(name)
    projects_dir = workspace_projects_dir(path)
    project_dir = path / projects_dir / slug
    project_dir.mkdir(parents=True, exist_ok=True)

    contract = ContextContract(name=name, purpose=purpose, context_sources=sources or [])
    contract_path = project_dir / "context.md"
    if contract_path.exists():
        raise FileExistsError(f"Project already exists: {contract_path}")
    contract_path.write_text(contract.to_markdown(), encoding="utf-8")

    source_records = [source.__dict__ for source in sources or []]
    sources_path = project_dir / "sources.json"
    if source_records:
        sources_path.write_text(json.dumps({"sources": source_records}, indent=2) + "\n", encoding="utf-8")

    index = read_index(path)
    if any(record.get("slug") == slug for record in index.get("projects", [])):
        raise FileExistsError(f"Project already exists in index: {slug}")
    index.setdefault("projects", []).append(
        {
            "name": name,
            "slug": slug,
            "path": str(contract_path.relative_to(path)),
            "status": "active",
            "source_count": len(source_records),
        }
    )
    write_index(path, index)

    return contract_path


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records: list[dict] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            records.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_number}") from exc
    return records


def audit(path: Path, event: AuditEvent) -> AuditEvent:
    path = path.expanduser().resolve()
    append_jsonl(path / ".gsd-ai" / "audit.jsonl", event.to_record())
    return event


def propose_signal(
    path: Path,
    project: str,
    signal_type: SignalType,
    summary: str,
    *,
    source: str,
    source_span: str = "",
    confidence: str = "medium",
) -> Signal:
    """Queue a proposed signal for human review without mutating durable signal state."""

    path = path.expanduser().resolve()
    project_dir = project_dir_for(path, project)
    signal = Signal(
        signal_type=signal_type,
        summary=summary,
        project=project,
        source=source,
        source_span=source_span,
        confidence=confidence,
    )
    proposals_path = project_dir / "signal_proposals.jsonl"
    existing = read_jsonl(proposals_path)
    if any(record.get("fingerprint") == signal.fingerprint and record.get("source") == source for record in existing):
        raise ValueError(f"Duplicate signal proposal: {signal.fingerprint}")
    append_jsonl(proposals_path, signal.to_record())
    audit(
        path,
        AuditEvent(
            event_type="signal.proposed",
            project=project,
            target=str(proposals_path.relative_to(path)),
            details={"signal_id": signal.signal_id, "fingerprint": signal.fingerprint},
        ),
    )
    return signal


def approve_signal(path: Path, project: str, signal_id: str) -> Signal:
    """Approve a queued signal and append it to the durable signal registry."""

    path = path.expanduser().resolve()
    project_dir = project_dir_for(path, project)
    proposals_path = project_dir / "signal_proposals.jsonl"
    signals_path = project_dir / "signals.jsonl"
    proposals = read_jsonl(proposals_path)
    match = next((record for record in proposals if record.get("signal_id") == signal_id), None)
    if not match:
        raise FileNotFoundError(f"Signal proposal not found: {signal_id}")

    approved = Signal.from_record({**match, "status": ApprovalStatus.APPROVED.value})
    existing_signals = read_jsonl(signals_path)
    if any(record.get("fingerprint") == approved.fingerprint for record in existing_signals):
        raise ValueError(f"Signal already approved: {approved.fingerprint}")
    append_jsonl(signals_path, approved.to_record())
    audit(
        path,
        AuditEvent(
            event_type="signal.approved",
            project=project,
            target=str(signals_path.relative_to(path)),
            details={"signal_id": approved.signal_id, "fingerprint": approved.fingerprint},
        ),
    )
    return approved
