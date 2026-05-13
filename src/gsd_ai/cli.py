"""Command-line interface for the GSD-AI Phase 1 skeleton."""

from __future__ import annotations

import argparse
from pathlib import Path

from .workspace import create_project, init_workspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gsd-ai", description="Local-first GSD-AI workspace tools.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a GSD-AI workspace.")
    init.add_argument("path", type=Path)
    init.add_argument("--force", action="store_true", help="Overwrite generated root/index files.")

    project = sub.add_parser("project", help="Manage projects.")
    project_sub = project.add_subparsers(dest="project_command", required=True)
    create = project_sub.add_parser("create", help="Create a project context contract.")
    create.add_argument("workspace", type=Path)
    create.add_argument("name")
    create.add_argument("--purpose", default="")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        created = init_workspace(args.path, force=args.force)
        print(f"Initialized GSD-AI workspace at {args.path}")
        for path in created:
            print(f"- {path}")
        return 0

    if args.command == "project" and args.project_command == "create":
        path = create_project(args.workspace, args.name, purpose=args.purpose)
        print(f"Created project context: {path}")
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
