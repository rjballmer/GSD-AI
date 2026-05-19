#!/usr/bin/env python3
"""Generate an AI review packet and deterministic preflight report for the GSD-AI E2E plan."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "GSD_AI_E2E_TEST_PLAN.md"
DEFAULT_PACKET = ROOT / "GSD_AI_E2E_REVIEW_PACKET.md"
DEFAULT_FEEDBACK = ROOT / "GSD_AI_E2E_REVIEW_FEEDBACK.md"

REQUIRED_SECTIONS = [
    "Test Thesis",
    "Modules Under Test",
    "Test Harness Recommendation",
    "Fictional Program",
    "Two-Week Simulation Calendar",
    "Example Artifact Batches",
    "Expected Final State",
    "Time Guardian Simulation",
    "Agent-Ops Controls",
    "Evaluation Metrics",
    "Pass/Fail Gates",
    "Suggested Corpus File Tree",
    "Build Order",
]

SIGNAL_TYPES = [
    "context_shift",
    "risk",
    "dependency",
    "decision",
    "open_decision",
    "mitigation",
    "action",
    "escalation",
]

MODULE_TERMS = [
    "ProjectOS Core",
    "Wakesurfer",
    "GSD / Task Layer",
    "Time Guardian",
    "Agent-Ops",
]

LIFECYCLE_TERMS = [
    "risk",
    "mitigation",
    "open decision",
    "decision",
    "dependency",
    "escalation",
    "action closure",
]


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def heading_exists(text: str, heading: str) -> bool:
    return re.search(rf"^#+\s+{re.escape(heading)}\s*$", text, flags=re.MULTILINE) is not None


def missing_terms(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term.lower() not in lowered]


def run_checks(plan_text: str) -> list[Check]:
    checks: list[Check] = []

    missing_sections = [s for s in REQUIRED_SECTIONS if not heading_exists(plan_text, s)]
    checks.append(Check(
        "required_sections",
        not missing_sections,
        "missing: " + ", ".join(missing_sections) if missing_sections else "all required sections present",
    ))

    day_count = len(re.findall(r"^### Day \d{2}:", plan_text, flags=re.MULTILINE))
    checks.append(Check(
        "two_week_daily_batches",
        day_count >= 10,
        f"found {day_count} day batch headings; expected at least 10",
    ))

    missing_signal_types = missing_terms(plan_text, SIGNAL_TYPES)
    checks.append(Check(
        "signal_type_coverage",
        not missing_signal_types,
        "missing: " + ", ".join(missing_signal_types) if missing_signal_types else "all 8 signal types mentioned",
    ))

    missing_modules = missing_terms(plan_text, MODULE_TERMS)
    checks.append(Check(
        "module_coverage",
        not missing_modules,
        "missing: " + ", ".join(missing_modules) if missing_modules else "all module names present",
    ))

    missing_lifecycle = missing_terms(plan_text, LIFECYCLE_TERMS)
    checks.append(Check(
        "lifecycle_coverage",
        not missing_lifecycle,
        "missing: " + ", ".join(missing_lifecycle) if missing_lifecycle else "core lifecycle terms present",
    ))

    has_json_examples = "expected_signals.json" in plan_text and "expected_task_mutations.json" in plan_text
    checks.append(Check(
        "expected_json_examples",
        has_json_examples,
        "expected JSON artifact references present" if has_json_examples else "missing expected JSON artifact references",
    ))

    has_agent_ops_gates = all(term in plan_text for term in ["Claim", "Confirm", "Commit"])
    checks.append(Check(
        "agent_ops_3c_gates",
        has_agent_ops_gates,
        "Claim/Confirm/Commit gates present" if has_agent_ops_gates else "missing 3C gate language",
    ))

    has_pass_fail = "MVP Pass" in plan_text and "MVP Fail" in plan_text
    checks.append(Check(
        "pass_fail_gates",
        has_pass_fail,
        "MVP pass/fail gates present" if has_pass_fail else "missing explicit MVP pass/fail gates",
    ))

    return checks


def score_checks(checks: list[Check]) -> dict[str, object]:
    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    failed = [check.name for check in checks if not check.passed]
    return {
        "passed": passed,
        "total": total,
        "score_pct": round((passed / total) * 100, 1) if total else 0.0,
        "failed": failed,
    }


def build_packet(plan_path: Path, plan_text: str, checks: list[Check]) -> str:
    check_lines = "\n".join(
        f"- [{'PASS' if c.passed else 'FAIL'}] {c.name}: {c.detail}" for c in checks
    )
    return f"""# AI Review Packet: GSD-AI E2E Test Plan

Generated: {datetime.now(timezone.utc).isoformat()}
Plan path: {plan_path}

## Deterministic Preflight

{check_lines}

## Reviewer Task

Independently review the GSD-AI end-to-end test plan and example artifacts below.

Evaluate whether the plan can actually test:

1. ProjectOS Core / project brain state
2. Wakesurfer / Capture signal extraction
3. GSD task creation, updates, dedupe, and closure
4. Time Guardian task-to-calendar review
5. Agent-Ops grounding, Claim/Confirm/Commit, write safety, dedupe, and auditability

Focus on false-confidence risks. Identify what would fail when this becomes an executable test corpus.

## Required Output Format

# Independent Review: GSD-AI E2E Test Plan

## Executive Assessment
- Verdict: strong / usable with revisions / weak
- Main risk:
- Best next change:

## Major Findings
1. [Severity: P0/P1/P2/P3] Finding
   - Evidence:
   - Why it matters:
   - Recommendation:

## Minor Findings
- ...

## Scoring Rubric Feedback
- What should be scored deterministically:
- What should be judged by an AI reviewer:
- Missing pass/fail thresholds:

## Missing Artifacts
- ...

## Recommended Action List
1. ...

## Scoring Guidance

- P0: the harness would validate the wrong behavior or permit unsafe/autonomous writes
- P1: the test would give false confidence in a core module
- P2: meaningful coverage/scoring gap
- P3: clarity or maintainability improvement

## Plan Under Review

{plan_text}
"""


def build_feedback(plan_path: Path, checks: list[Check], score: dict[str, object]) -> str:
    check_lines = "\n".join(
        f"- [{'x' if c.passed else ' '}] {c.name} - {c.detail}" for c in checks
    )
    failed = score["failed"]
    failed_text = ", ".join(failed) if failed else "None"
    return f"""# GSD-AI E2E Review Feedback

Generated: {datetime.now(timezone.utc).isoformat()}
Plan reviewed: {plan_path}
Deterministic preflight: {score['passed']}/{score['total']} checks passed ({score['score_pct']}%)

## Preflight Checks

{check_lines}

Failed checks: {failed_text}

## Independent Model Review

Pending. Paste or append the independent model review here using GSD_AI_E2E_REVIEW_PACKET.md.

## Feedback To Action

| Status | Priority | Feedback | Action | Owner/Notes |
|---|---|---|---|---|
| open | P1 | Add full expected JSON files for every daily batch, not only Day 01 examples. | Expand corpus from illustrative plan to executable fixture tree. | |
| open | P1 | Separate AI-judged extraction quality from deterministic state-transition scoring. | Add scorer sections for extraction, dedupe, lifecycle, task mutation, time proposal, and controls. | |
| open | P2 | Add negative/noise artifacts. | Include casual chat, ambiguous discussion, duplicate source replay, and ungrounded claims. | |
| open | P2 | Add explicit approval simulation modes. | Define approve_all, partial approve, reject noise, corrected owner/date scenarios. | |
| open | P2 | Add final machine-readable expected state. | Create final signal registry, task store, project snapshot, and audit log fixtures. | |

## Decision Log

- Pending review.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--out", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--feedback-out", type=Path, default=DEFAULT_FEEDBACK)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    plan_text = args.plan.read_text(encoding="utf-8")
    checks = run_checks(plan_text)
    score = score_checks(checks)

    args.out.write_text(build_packet(args.plan, plan_text, checks), encoding="utf-8")
    args.feedback_out.write_text(build_feedback(args.plan, checks, score), encoding="utf-8")

    if args.json:
        args.json.write_text(json.dumps({
            "plan": str(args.plan),
            "score": score,
            "checks": [check.__dict__ for check in checks],
        }, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote AI review packet: {args.out}")
    print(f"Wrote feedback/action file: {args.feedback_out}")
    print(f"Preflight: {score['passed']}/{score['total']} checks passed ({score['score_pct']}%)")
    if score["failed"]:
        print("Failed checks: " + ", ".join(score["failed"]))
    return 0 if not score["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
