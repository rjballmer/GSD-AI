"""Command-line interface for the GSD-AI Phase 1 skeleton."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .schema import ContextSource, SignalType
from .workspace import (
    DEFAULT_FRAMEWORK,
    FRAMEWORKS,
    approve_signal,
    create_project,
    framework_prompt,
    init_workspace,
    propose_signal,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gsd-ai", description="Local-first GSD-AI workspace tools.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a GSD-AI workspace.")
    init.add_argument("path", type=Path)
    init.add_argument("--framework", choices=sorted(FRAMEWORKS), help="Workspace framework to create. Default: para.")
    init.add_argument("--force", action="store_true", help="Overwrite generated root/index files.")

    project = sub.add_parser("project", help="Manage projects.")
    project_sub = project.add_subparsers(dest="project_command", required=True)
    create = project_sub.add_parser(
        "create",
        help="Create a project context contract. Prefer adding source links over typing a full charter.",
    )
    create.add_argument("workspace", type=Path)
    create.add_argument("name")
    create.add_argument("--purpose", default="", help="Optional one-line purpose. Source links can provide the richer context.")
    create.add_argument(
        "--source",
        action="append",
        default=[],
        help="Relevant source link or path for AI-assisted project setup. Repeatable.",
    )
    create.add_argument(
        "--doc",
        action="append",
        default=[],
        help="Alias for --source, intended for project/design/planning docs. Repeatable.",
    )

    signals = sub.add_parser("signals", help="Propose and approve project signals.")
    signals_sub = signals.add_subparsers(dest="signals_command", required=True)
    propose = signals_sub.add_parser(
        "propose",
        help="Queue a structured signal for human approval without mutating durable signal state.",
    )
    propose.add_argument("workspace", type=Path)
    propose.add_argument("project")
    propose.add_argument("--type", required=True, choices=sorted(item.value for item in SignalType))
    propose.add_argument("--summary", required=True)
    propose.add_argument("--source", required=True)
    propose.add_argument("--source-span", default="")
    propose.add_argument("--confidence", default="medium")

    approve = signals_sub.add_parser("approve", help="Approve a proposed signal into signals.jsonl.")
    approve.add_argument("workspace", type=Path)
    approve.add_argument("project")
    approve.add_argument("signal_id")

    return parser


def choose_framework(value: str | None) -> str:
    """Use an explicit framework, prompt interactively, or default safely in non-interactive contexts."""

    if value:
        return value
    if not sys.stdin.isatty():
        return DEFAULT_FRAMEWORK

    raw = input(framework_prompt()).strip().lower()
    if raw in {"", "1"}:
        return "para"
    if raw == "2":
        return "gsd"
    if raw in FRAMEWORKS:
        return raw

    choices = ", ".join(sorted(FRAMEWORKS))
    raise SystemExit(f"Unknown framework '{raw}'. Choose one of: {choices}")


def context_sources(source_values: list[str], doc_values: list[str]) -> list[ContextSource]:
    """Build typed context sources from CLI arguments."""

    sources = [ContextSource(value=value, source_type="source") for value in source_values]
    sources.extend(ContextSource(value=value, source_type="doc") for value in doc_values)
    return sources


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        framework = choose_framework(args.framework)
        created = init_workspace(args.path, framework=framework, force=args.force)
        print(f"Initialized GSD-AI workspace at {args.path} using framework: {framework}")
        for path in created:
            print(f"- {path}")
        return 0

    if args.command == "project" and args.project_command == "create":
        sources = context_sources(args.source, args.doc)
        path = create_project(args.workspace, args.name, purpose=args.purpose, sources=sources)
        print(f"Created project context: {path}")
        if sources:
            print("Added context sources for AI-assisted signal extraction:")
            for source in sources:
                print(f"- {source.source_type}: {source.value}")
            print("Next: ask your AI assistant to read these sources and propose goals, risks, decisions, dependencies, actions, and open questions before writing durable updates.")
        else:
            print("Tip: add --source or --doc links so AI can infer project signals instead of making you type a full charter.")
        return 0

    if args.command == "signals" and args.signals_command == "propose":
        signal = propose_signal(
            args.workspace,
            args.project,
            SignalType(args.type),
            args.summary,
            source=args.source,
            source_span=args.source_span,
            confidence=args.confidence,
        )
        print(f"Queued signal proposal: {signal.signal_id}")
        print(f"- fingerprint: {signal.fingerprint}")
        print("Next: review it, then approve with gsd-ai signals approve if it should become durable state.")
        return 0

    if args.command == "signals" and args.signals_command == "approve":
        signal = approve_signal(args.workspace, args.project, args.signal_id)
        print(f"Approved signal: {signal.signal_id}")
        print(f"- wrote durable signal fingerprint: {signal.fingerprint}")
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
