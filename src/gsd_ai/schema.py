"""Small, local-first schemas for the Phase 1 GSD-AI skeleton."""

from __future__ import annotations

import hashlib
import re
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


class ApprovalStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_slug(value: str, *, max_length: int = 80) -> str:
    """Return a lowercase path/id-safe slug."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (slug or "untitled")[:max_length].strip("-") or "untitled"


def stable_hash(parts: list[str], *, length: int = 16) -> str:
    payload = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:length]


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
    source_span: str = ""
    confidence: str = "medium"
    scope: Scope = Scope.PRIVATE
    status: ApprovalStatus = ApprovalStatus.PROPOSED
    signal_id: str = ""
    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.signal_id:
            object.__setattr__(self, "signal_id", f"sig_{stable_hash([self.fingerprint, self.source, self.source_span])}")

    @property
    def fingerprint(self) -> str:
        slug = stable_slug(self.summary)
        project = stable_slug(self.project)
        return f"{self.signal_type.value}:{project}:{slug}"

    def to_record(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "signal_type": self.signal_type.value,
            "summary": self.summary,
            "project": self.project,
            "source": self.source,
            "source_span": self.source_span,
            "confidence": self.confidence,
            "scope": self.scope.value,
            "status": self.status.value,
            "fingerprint": self.fingerprint,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "Signal":
        return cls(
            signal_type=SignalType(record["signal_type"]),
            summary=record["summary"],
            project=record["project"],
            source=record["source"],
            source_span=record.get("source_span", ""),
            confidence=record.get("confidence", "medium"),
            scope=Scope(record.get("scope", Scope.PRIVATE.value)),
            status=ApprovalStatus(record.get("status", ApprovalStatus.PROPOSED.value)),
            signal_id=record.get("signal_id", ""),
            created_at=record.get("created_at", utc_now()),
            metadata=record.get("metadata", {}),
        )


@dataclass(frozen=True)
class AuditEvent:
    """Append-only witness for durable local writes."""

    event_type: str
    project: str
    target: str
    actor: str = "cli"
    verdict: str = "committed"
    event_id: str = ""
    created_at: str = field(default_factory=utc_now)
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.event_id:
            object.__setattr__(
                self,
                "event_id",
                f"evt_{stable_hash([self.event_type, self.project, self.target, self.created_at])}",
            )

    def to_record(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "project": self.project,
            "target": self.target,
            "actor": self.actor,
            "verdict": self.verdict,
            "created_at": self.created_at,
            "details": self.details,
        }
