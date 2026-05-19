# GSD-AI E2E Review Feedback

Generated: 2026-05-19T03:40:45.067417+00:00
Plan reviewed: testplan/GSD_AI_E2E_TEST_PLAN.md
Deterministic preflight: 8/8 checks passed (100.0%)

## Preflight Checks

- [x] required_sections - all required sections present
- [x] two_week_daily_batches - found 10 day batch headings; expected at least 10
- [x] signal_type_coverage - all 8 signal types mentioned
- [x] module_coverage - all module names present
- [x] lifecycle_coverage - core lifecycle terms present
- [x] expected_json_examples - expected JSON artifact references present
- [x] agent_ops_3c_gates - Claim/Confirm/Commit gates present
- [x] pass_fail_gates - MVP pass/fail gates present

Failed checks: None

## Independent Model Review

### Executive Assessment

Verdict: usable with revisions.

The plan is directionally strong and has the right architecture, but it is not yet implementation-ready as an automated AI-executable E2E test. It is currently strongest as a narrative simulation and weakest as a deterministic scoring corpus.

Main false-confidence risk: the system could appear to pass by producing plausible prose or Day 01-style outputs while never proving durable state mutation, task lifecycle handling, Time Guardian scheduling, or Agent-Ops enforcement across the full two weeks.

Best next change: convert the illustrative plan into a complete fixture tree with machine-readable expected outputs for every batch.

### Major Findings

1. [P1] Module coverage is uneven.
   - Evidence: Wakesurfer/Capture has the richest coverage; ProjectOS Core has final-state coverage but no per-day expected state; GSD/task mutations are concrete only for Day 01; Time Guardian has behavior examples but no machine-readable per-day proposals; Agent-Ops has principles but no audit/sentinel/read-back artifacts.
   - Why it matters: the current test could validate extraction while missing state, task, calendar, and verification regressions.
   - Recommendation: add per-day expected state files for signal registry, task store, time proposal, and Agent-Ops report.

2. [P1] Example artifacts are realistic but too clean.
   - Evidence: most facts are directly stated with clean owner/deadline language.
   - Why it matters: real work traffic includes ambiguity, contradiction, stale claims, aliasing, noisy chatter, missing dates, and partial completion.
   - Recommendation: add negative and edge-case fixtures before treating the corpus as a reliability test.

3. [P1] Expected outputs are not concrete enough after Day 01.
   - Evidence: Day 01 has structured expected signal/task JSON; Days 02-10 mostly use prose bullets.
   - Why it matters: automated scoring needs canonical IDs, fingerprints, source spans, lifecycle statuses, related-signal links, task mutations, and audit events.
   - Recommendation: create complete expected_signals.json, expected_task_mutations.json, expected_project_state.json, and expected_time_proposal.json for every daily batch.

4. [P1] Agent-Ops compliance is asserted but not yet testable.
   - Evidence: Claim/Confirm/Commit, Iron Laws, idempotency, read-back witnesses, and sentinels are named but not represented as expected artifacts.
   - Why it matters: a system can claim controls ran without proving any independent witness observed the side effect.
   - Recommendation: add audit log schema plus expected audit events for extraction, approval, signal writes, task mutations, task closures, and calendar proposals.

5. [P2] Module taxonomy needs clarification.
   - Evidence: the request says four core modules; the plan describes ProjectOS Core, Wakesurfer/Capture, GSD/task layer, Time Guardian, and Agent-Ops.
   - Why it matters: implementation ownership and scoring can drift if the task layer is ambiguous.
   - Recommendation: either call it five modules or explicitly define GSD/task layer as a subcomponent of ProjectOS Core.

### Scoring Rubric Feedback

Hard-fail gates:

- accepted signal without source file and source span
- task mutation without approved signal or initial-task source
- task closure without explicit completion evidence
- risk resolved without linked mitigation or decision evidence
- unapproved signal mutating project brain or task store
- calendar proposal includes closed task
- final status claim lacks registry/task/source evidence

Weighted scoring proposal:

- Signal extraction: 25%
- Dedupe and lifecycle transitions: 20%
- Task mutation accuracy: 20%
- Time Guardian scheduling accuracy: 15%
- Agent-Ops verification completeness: 15%
- Negative/noise handling: 5%

Scoring definitions to add:

- source grounding: exact source span or acceptable span-overlap threshold
- priority-order agreement: ranking metric for expected vs actual task order
- lifecycle accuracy: structured before/after state comparison
- final snapshot correctness: generated from structured state, not scored as freeform markdown

### Missing Artifacts

- complete expected JSON for Days 02-10
- per-day expected project state snapshots
- machine-readable calendar fixtures
- machine-readable Time Guardian proposals for every checkpoint
- approval queue states and approval simulation modes
- audit event schema and expected audit logs
- idempotency key examples and read-back witness examples
- negative/noise fixtures
- malformed artifact / malformed JSON cases
- duplicate source replay case
- stale-state contradiction case
- multi-project or cross-project contamination case

## Feedback To Action

| Status | Priority | Feedback | Action | Owner/Notes |
|---|---|---|---|---|
| open | P1 | Add full expected JSON files for every daily batch, not only Day 01 examples. | Expand corpus from illustrative plan to executable fixture tree. | |
| open | P1 | Separate AI-judged extraction quality from deterministic state-transition scoring. | Add scorer sections for extraction, dedupe, lifecycle, task mutation, time proposal, and controls. | |
| open | P1 | Add per-day expected ProjectOS Core state snapshots. | Create expected signal registry, risk register, decision log, dependency register, action register, and status snapshot after each batch. | |
| open | P1 | Add machine-readable Time Guardian fixtures. | Define calendar JSON, working hours, collision rules, task estimates, and expected per-day ranked proposals. | |
| open | P1 | Add Agent-Ops verification artifacts. | Define audit event schema, batch sentinels, idempotency keys, read-back witnesses, and expected verification reports. | |
| open | P2 | Add negative/noise artifacts. | Include casual chat, ambiguous discussion, duplicate source replay, and ungrounded claims. | |
| open | P2 | Add explicit approval simulation modes. | Define approve_all, partial approve, reject noise, corrected owner/date scenarios. | |
| open | P2 | Add final machine-readable expected state. | Create final signal registry, task store, project snapshot, and audit log fixtures. | |
| open | P2 | Clarify module taxonomy. | Decide whether GSD/task layer is a fifth module or part of ProjectOS Core. | |
| open | P2 | Add schemas before scorer implementation. | Define signal, signal history, task mutation, task state, calendar proposal, audit event, batch result, and scorer output schemas. | |
| open | P3 | Keep markdown snapshots as generated artifacts, not primary scoring targets. | Score structured state first, then generate human-readable markdown from state. | |

## Decision Log

- 2026-05-18: Independent review accepted the plan as a strong skeleton but not yet executable. Main action is to convert the illustrative two-week narrative into complete machine-readable fixtures and scorer contracts.
