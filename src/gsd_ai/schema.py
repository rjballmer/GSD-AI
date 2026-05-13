"""Small, local-first schemas for the Phase 1 GSD-AI skeleton."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Scope(str, Enum):
    PRIVATE = "private"
    TEAM = "team"
    CLIENT = "client"
    PUBLIC_SAFE = "public-safe"
    SENSITIVE_NEVER_SHARE = "sensitive-never-share"


class SignalType(str, Enum):
    CONTEXT_SHIFT = "context_shift"
    RISK = "risk"
    DEPENDENCY = "dependency"
    DECISION = "decision"
    OPEN_DECISION = "open_decision"
    MITIGATION = "mitigation"
    ACTION = "action"
    ESCALATION = "escalation"


@dataclass(frozen=True)
class ContextSource:
    """User-provided source material for AI-assisted project setup."""

    value: str
    source_type: str = "link"
    note: str = ""

    def to_markdown(self) -> str:
        suffix = f" — {self.note}" if self.note else ""
        return f"- [{self.source_type}] {self.value}{suffix}"


@dataclass(frozen=True)
class ContextContract:
    """Durable, inspectable state for a project."""

    name: str
    purpose: str = ""
    status: str = "active"
    scope: Scope = Scope.PRIVATE
    active_goals: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    context_sources: list[ContextSource] = field(default_factory=list)

    def to_markdown(self) -> str:
        sections: list[tuple[str, list[str] | str]] = [
            ("Purpose", self.purpose),
            ("Current status", self.status),
            ("Scope", self.scope.value),
            ("Active goals", self.active_goals),
            ("Decisions", self.decisions),
            ("Risks", self.risks),
            ("Dependencies", self.dependencies),
            ("Actions", self.actions),
            ("Open questions", self.open_questions),
            ("Key references", self.references),
            ("Context sources", [source.to_markdown().removeprefix("- ") for source in self.context_sources]),
        ]
        lines = [f"# {self.name}", ""]
        for heading, value in sections:
            lines.extend([f"## {heading}", ""])
            if isinstance(value, str):
                lines.extend([value or "_Not set._", ""])
            else:
                lines.extend([*(f"- {item}" for item in value), ""] if value else ["_None yet._", ""])
        return "\n".join(lines).rstrip() + "\n"


@dataclass(frozen=True)
class Signal:
    """Structured work state extracted from messy context."""

    signal_type: SignalType
    summary: str
    project: str
    source: str
    confidence: str = "medium"
    scope: Scope = Scope.PRIVATE
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def fingerprint(self) -> str:
        slug = "-".join(self.summary.lower().split())[:80].strip("-")
        project = "-".join(self.project.lower().split())
        return f"{self.signal_type.value}:{project}:{slug}"
