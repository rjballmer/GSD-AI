# GSD-AI Test Plan Artifacts

This directory contains the current end-to-end simulation test plan for GSD-AI.

## Files

- GSD_AI_E2E_TEST_PLAN.md - two-week simulation plan and evaluation contract.
- GSD_AI_E2E_REVIEW_PACKET.md - AI review packet generated from the plan.
- GSD_AI_E2E_REVIEW_FEEDBACK.md - independent review feedback and action log.
- GSD_AI_E2E_PREFLIGHT.json - latest deterministic preflight result.
- scripts/gsd_ai_e2e_review.py - local script that regenerates a review packet and preflight report.

## Evaluation Model

The expected JSON described in the plan is the hidden oracle. Agents under test should read only the messy input corpus and current simulated state. The scorer compares agent-produced actual JSON against expected JSON after the run.

Use structured equivalence for signal extraction and exact checks for deterministic layers such as task mutations, lifecycle transitions, audit events, and read-back witnesses.

## Regenerating Review Artifacts

From the repository root:

~~~bash
python3 testplan/scripts/gsd_ai_e2e_review.py \
  --plan testplan/GSD_AI_E2E_TEST_PLAN.md \
  --out testplan/GSD_AI_E2E_REVIEW_PACKET.md \
  --feedback-out testplan/GSD_AI_E2E_REVIEW_FEEDBACK.generated.md \
  --json testplan/GSD_AI_E2E_PREFLIGHT.json
~~~

The command above writes generated feedback to a separate file so the curated review/action log is not overwritten.
