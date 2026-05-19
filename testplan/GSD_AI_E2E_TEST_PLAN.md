# GSD-AI End-to-End Simulation Test Plan

**Date:** 2026-05-18
**Status:** Draft test-design artifact
**Purpose:** Define a two-week simulated program corpus that can test GSD-AI across the four core modules: ProjectOS Core, Wakesurfer/Capture, Time Guardian, and Agent-Ops controls.

Related review artifacts:

- scripts/gsd_ai_e2e_review.py generates the AI review packet and deterministic preflight report.
- GSD_AI_E2E_REVIEW_PACKET.md is the model-review prompt packet.
- GSD_AI_E2E_REVIEW_FEEDBACK.md captures independent review feedback and action items.
- GSD_AI_E2E_PREFLIGHT.json stores the latest deterministic preflight result.

## Test Thesis

GSD-AI should prove one loop before adding live integrations:

~~~text
Program overview
  -> simulated meetings/chats/docs
  -> Wakesurfer extracts typed signals
  -> ProjectOS Core updates project brain
  -> ACTION signals become task mutations
  -> Time Guardian proposes calendar blocks
  -> Agent-Ops verifies grounding, dedupe, writes, and job completion
~~~

The two-week simulation should test signal lifecycle, not just extraction accuracy. A good run should show risks emerging, mitigations reducing them, open decisions closing, dependencies resolving or escalating, actions being created and completed, and the project brain staying coherent.

## Modules Under Test

### ProjectOS Core

Owns durable project state:

- project registry
- program overview / context contract
- signal registry
- action, risk, decision, dependency state
- status snapshots
- audit log

### Wakesurfer / Capture

Owns messy-input to structured-signal conversion:

- ingest meeting notes, chat excerpts, planning docs, and status snippets
- extract the eight signal types
- generate deterministic fingerprints
- dedupe against prior signals
- propose updates for approval

### GSD / Task Layer

Owns task mutations derived from approved signals:

- create tasks from ACTION signals
- update tasks from MITIGATION, DECISION, and DEPENDENCY changes
- close tasks based on completion evidence
- preserve source traceability

### Time Guardian

Owns task-to-time planning:

- read current tasks and calendar availability
- propose time blocks
- learn from user feedback
- detect overdue/stale tasks
- recommend reschedule, defer, or escalate

### Agent-Ops Controls

Owns trust:

- Claim/Confirm/Commit checks for writes
- dedupe before task/calendar creation
- source grounding for facts and status
- job sentinels for each batch run
- audit log for every accepted mutation

## Test Harness Recommendation

Build the harness local-first. No Slack, Google Calendar, GSD, Jira, or live APIs are required for the first version.

~~~text
fixtures/
  program/
    program_overview.md
    initial_tasks.json
    calendar_week_1.json
    calendar_week_2.json
  batches/
    day_01/
      inputs/
        meeting_001_kickoff.md
        chat_001_launch_room.md
      expected/
        signals.json
        task_mutations.json
      actual/
        signals.json
        task_mutations.json
    day_02/
      ...
  expected_final/
    final_project_state.json
    final_tasks.json
    final_signal_registry.json
    final_audit_log.json
  actual_final/
    final_project_state.json
    final_tasks.json
    final_signal_registry.json
    final_audit_log.json

runner/
  ingest_batch.py
  extract_signals.py
  dedupe_signals.py
  apply_approved_signals.py
  mutate_tasks.py
  propose_time_blocks.py
  verify_agent_ops.py
~~~

## Evaluation Contract

The expected JSON files are the hidden oracle. They are not agent input.

Each test run has four layers:

1. **Input corpus:** messy human artifacts that agents are allowed to read.
   - program overview
   - meeting notes
   - chat logs
   - task updates
   - calendar fixtures
2. **Expected JSON:** hidden answer key used only by the scorer.
   - expected signals
   - expected lifecycle transitions
   - expected task mutations
   - expected Time Guardian proposals
   - expected Agent-Ops audit events
   - expected final project state
3. **Actual JSON:** outputs produced by the agents/system under test.
   - actual extracted signals
   - actual state mutations
   - actual task store
   - actual time proposals
   - actual audit events
4. **Scorer:** compares expected JSON to actual JSON and produces a report.

Agents should run as if they are operating the product. They should see the input corpus and current simulated state, but never the expected JSON.

### Scoring Strictness

Use different strictness by layer.

Signal extraction should use structured equivalence, not exact prose matching:

- same signal type
- same project
- source-grounded span in the right artifact
- semantically equivalent summary
- correct owner/deadline when present
- correct lifecycle relationship, such as mitigation linked to risk

Deterministic layers should use exact or near-exact comparison:

- exact mutation operation: create, update, close, schedule, reject
- exact target entity or deterministic equivalent
- exact lifecycle transition
- exact audit event type
- no duplicate task IDs
- no task closure without completion evidence
- no write without audit/read-back event

### Oracle Visibility Rules

- The extraction agent can read only program files, daily input artifacts, and current simulated state.
- The task mutation agent can read approved actual signals and current task state, not expected mutations.
- The Time Guardian agent can read current task state, calendar fixtures, and scheduling preferences, not expected proposals.
- The scorer can read both actual outputs and expected JSON.
- The review agent can read the full corpus after a run to critique failures, but that is separate from the product simulation.

This split matters because the goal is to test whether agents can capture and process real signals, not whether they can echo the answer key.

For v0, the LLM should only do extraction from messy text. Everything after extraction should be deterministic:

- fingerprint generation
- source dedupe
- signal dedupe
- project routing
- task mutation
- calendar gap detection
- final scoring

## Fictional Program

### Program Name

Atlas Launch Readiness

### Program Overview

Atlas is a B2B analytics product launching a private beta for five design partners. The initiative is cross-functional and time-bound: beta starts on Friday of Week 2.

### Objective

Ship a private beta that lets design partners:

- upload a CSV dataset
- map columns to core metrics
- generate a dashboard
- invite one teammate
- export a PDF summary

### Success Criteria

- five design partners onboarded by beta start
- dashboard generation p95 under 8 seconds for files under 20 MB
- onboarding flow completed by three internal dogfood users before Week 2 Wednesday
- support runbook approved before beta start
- no P0/P1 privacy issues open at launch

### Workstreams

| Workstream | Owner | Goal |
|---|---|---|
| Product | Maya | beta scope, partner readiness, launch criteria |
| Engineering | Omar | upload, dashboard generation, export |
| Data Platform | Priya | query performance and dataset validation |
| Design | Lena | onboarding and empty states |
| Privacy | Chen | data handling review |
| Support | Eli | runbook and escalation path |

### Initial Known State

- Upload and dashboard generation are implemented in staging.
- PDF export is functional but slow on large datasets.
- Privacy review has not started.
- Design partner list is still pending final approval.
- Support runbook has a skeleton but no escalation path.

### Initial Tasks

~~~json
[
  {
    "id": "task-atlas-001",
    "title": "Complete Atlas privacy review intake",
    "owner": "Maya",
    "status": "open",
    "due": "2026-06-02",
    "source": "program_overview.md"
  },
  {
    "id": "task-atlas-002",
    "title": "Profile PDF export for 20 MB datasets",
    "owner": "Omar",
    "status": "open",
    "due": "2026-06-03",
    "source": "program_overview.md"
  },
  {
    "id": "task-atlas-003",
    "title": "Draft support escalation path",
    "owner": "Eli",
    "status": "open",
    "due": "2026-06-05",
    "source": "program_overview.md"
  }
]
~~~

## Two-Week Simulation Calendar

Assume Week 1 starts Monday 2026-06-01 and Week 2 ends Friday 2026-06-12.

### Week 1

| Day | Batch Theme | Artifacts | Expected Main Signals |
|---|---|---|---|
| Mon W1 | kickoff and scope | kickoff notes, launch-room chat | context shift, open decision, action |
| Tue W1 | privacy risk appears | privacy sync notes, eng chat | risk, dependency, action |
| Wed W1 | performance blocker | perf triage notes, data-platform chat | risk, dependency, mitigation |
| Thu W1 | scope decision | product/design sync, partner chat | decision, action, context shift |
| Fri W1 | weekly review | weekly status notes, support chat | escalation candidate, mitigation, action closure |

### Week 2

| Day | Batch Theme | Artifacts | Expected Main Signals |
|---|---|---|---|
| Mon W2 | mitigation lands | perf follow-up notes, task updates | mitigation, risk status update, action closure |
| Tue W2 | privacy decision | privacy review notes, launch-room chat | decision, dependency resolved, action |
| Wed W2 | dogfood failure | dogfood notes, bug chat | risk, action, open decision |
| Thu W2 | launch readiness | go/no-go notes, support runbook update | decision, mitigation, action closure |
| Fri W2 | beta launch | launch notes, partner feedback chat | context shift, action, weekly snapshot |

## Example Artifact Batches

### Day 01: Kickoff

#### meeting_001_kickoff.md

~~~markdown
# Atlas Beta Kickoff - 2026-06-01

Attendees: Maya, Omar, Priya, Lena, Chen, Eli

Maya: The beta date is Friday 6/12. We are narrowing the beta to CSV upload, dashboard generation, teammate invite, and PDF export. Custom branding is no longer in scope for beta.

Omar: PDF export works, but large datasets are slow. I need to profile the 20 MB case before we commit it.

Chen: Privacy review needs the data retention details before I can approve the intake.

Open question: Do we include the teammate invite in beta if privacy review slips? Maya will decide by Thursday.

Actions:
- Omar will profile PDF export by Wednesday 6/3.
- Maya will send Chen the data retention details by Tuesday 6/2.
- Eli will draft the support escalation path by Friday 6/5.
~~~

#### chat_001_launch_room.md

~~~markdown
2026-06-01 14:10 Maya: Confirming beta scope: no custom branding for private beta. We need to keep scope tight.
2026-06-01 14:22 Lena: Good. I will update onboarding copy to remove branding references.
2026-06-01 15:05 Omar: I am worried PDF export is the long pole. The 20 MB test file took 19s locally.
~~~

#### expected_signals.json

~~~json
[
  {
    "id": "sig-atlas-context-scope-branding-out",
    "type": "context_shift",
    "project": "atlas",
    "summary": "Private beta scope excludes custom branding.",
    "source": "meeting_001_kickoff.md",
    "fingerprint": "context_shift:atlas:custom-branding-out-of-beta",
    "confidence": "high"
  },
  {
    "id": "sig-atlas-open-decision-invite-privacy-slip",
    "type": "open_decision",
    "project": "atlas",
    "summary": "Need to decide whether teammate invite remains in beta if privacy review slips.",
    "owner": "Maya",
    "deadline": "2026-06-04",
    "source": "meeting_001_kickoff.md",
    "fingerprint": "open_decision:atlas:teammate-invite-if-privacy-slips",
    "confidence": "high"
  },
  {
    "id": "sig-atlas-risk-pdf-export-slow",
    "type": "risk",
    "project": "atlas",
    "summary": "PDF export may miss the p95 performance target for 20 MB datasets.",
    "owner": "Omar",
    "source": "chat_001_launch_room.md",
    "fingerprint": "risk:atlas:pdf-export-slow-20mb",
    "confidence": "medium"
  },
  {
    "id": "sig-atlas-action-send-retention-details",
    "type": "action",
    "project": "atlas",
    "summary": "Maya will send Chen data retention details.",
    "owner": "Maya",
    "deadline": "2026-06-02",
    "source": "meeting_001_kickoff.md",
    "fingerprint": "action:atlas:maya-send-retention-details",
    "confidence": "high"
  }
]
~~~

#### expected_task_mutations.json

~~~json
[
  {
    "op": "create",
    "task_id": "task-atlas-004",
    "from_signal": "sig-atlas-action-send-retention-details",
    "title": "Send Atlas data retention details to Privacy",
    "owner": "Maya",
    "due": "2026-06-02",
    "tags": ["atlas", "auto_from_signal", "privacy"]
  },
  {
    "op": "update",
    "task_id": "task-atlas-002",
    "from_signal": "sig-atlas-risk-pdf-export-slow",
    "append_note": "Risk surfaced: 20 MB PDF export took 19s locally; target is p95 under 8s."
  }
]
~~~

### Day 02: Privacy Risk

~~~markdown
# Privacy Intake Sync - 2026-06-02

Chen: I still do not have final retention language. Without that, privacy cannot approve teammate invite.

Maya: I sent the retention draft this morning, but it needs Eng confirmation.

Omar: We store uploaded CSVs for 14 days in staging. For beta we can reduce retention to 72 hours if needed.

Chen: That would materially reduce risk. I need confirmation by Thursday noon.

Action: Omar to confirm whether 72-hour retention is feasible by Wednesday EOD.
~~~

Expected signals:

- dependency: privacy approval depends on data retention confirmation
- risk: teammate invite may be blocked by privacy review
- mitigation: reducing uploaded CSV retention to 72 hours would reduce privacy risk
- action: Omar to confirm retention feasibility

### Day 03: Performance Blocker

~~~markdown
# Performance Triage - 2026-06-03

Priya: The slow PDF export is not rendering. It is query fanout. Dashboard generation runs 11 parallel metric queries after upload.

Omar: We can cache the normalized dataset after column mapping.

Priya: That should cut dashboard generation and export time, but Data Platform needs one day to add a cache TTL config.

Maya: If cache TTL config is not ready by Monday, we need to decide whether to cap beta files at 10 MB.

Action: Priya owns cache TTL config by Monday 6/8.
~~~

Expected signals:

- dependency: PDF/export performance depends on Data Platform cache TTL config
- mitigation: normalized dataset cache can reduce query fanout
- open decision: cap beta files at 10 MB if cache TTL slips
- action: Priya adds cache TTL config by 6/8

### Day 04: Scope Decision

~~~markdown
# Product/Design Sync - 2026-06-04

Maya: Decision: teammate invite stays in beta only for internal dogfood. Design partners will not get teammate invite until privacy signs off.

Lena: I will update onboarding screens to hide invite for external beta accounts.

Chen: That unblocks privacy review for CSV upload and dashboard generation.
~~~

Expected signals:

- decision: teammate invite limited to internal dogfood
- context shift: external beta scope is now upload/dashboard/PDF only
- action: Lena hides invite for external beta accounts
- dependency update: privacy no longer blocks upload/dashboard review path

### Day 05: Escalation Candidate

~~~markdown
# Week 1 Launch Review - 2026-06-05

Maya: Cache TTL is still not started because Data Platform is handling an incident.

Priya: I asked twice in the DP channel. No owner yet.

Omar: Without TTL config, 20 MB export will stay over target.

Maya: If we do not have an owner by Monday noon, I will escalate to Priya's manager.
~~~

Expected signals:

- escalation: repeated Data Platform blocker with no owner
- risk status update: PDF export performance remains at risk
- action: Maya to escalate if no owner by Monday noon

### Day 06: Mitigation Lands

~~~markdown
# Performance Follow-up - 2026-06-08

Priya: Cache TTL config is merged in staging.

Omar: Retested 20 MB PDF export. p95 is now 7.4 seconds across 20 runs.

Maya: Great. We no longer need the 10 MB cap decision.
~~~

Expected signals:

- mitigation: cache TTL config landed and reduced PDF p95 to 7.4s
- risk update: PDF export risk reduced/resolved
- decision update: 10 MB cap open decision closed as no longer needed
- action closure: Priya cache TTL task complete

### Day 07: Privacy Decision

~~~markdown
# Privacy Review - 2026-06-09

Chen: With 72-hour retention and external beta invite disabled, privacy approves CSV upload and dashboard generation for design partners.

Chen: Teammate invite remains internal-only until deletion audit logs are available.

Action: Omar to add deletion audit log task to post-beta backlog.
~~~

Expected signals:

- decision: privacy approves CSV upload and dashboard generation for design partners
- dependency resolved: privacy no longer blocks beta launch
- action: add deletion audit logs to post-beta backlog

### Day 08: Dogfood Failure

~~~markdown
# Dogfood Notes - 2026-06-10

Internal dogfood user 2 failed onboarding because the CSV parser rejected a valid quoted comma in a column value.

Omar: This is a parser bug, not user error.

Maya: Is this launch blocking?

Omar: If design partners have quoted commas, yes. I can patch today.

Open decision: If parser patch is not verified by Thursday 2pm, delay beta or manually clean partner CSVs?
~~~

Expected signals:

- risk: CSV parser bug may block beta
- action: Omar patches quoted-comma parsing
- open decision: delay beta vs manually clean CSVs if patch not verified

### Day 09: Launch Readiness

~~~markdown
# Go/No-Go - 2026-06-11

Omar: Parser patch verified in staging with all five partner sample CSVs.

Eli: Support runbook now includes escalation path and sample partner response templates.

Maya: Decision: we are go for Friday beta. Known limitation: teammate invite remains internal-only.

Action: Maya sends partner launch note Friday morning.
~~~

Expected signals:

- mitigation: parser patch verified with partner samples
- action closure: support runbook escalation path complete
- decision: go for Friday beta
- action: send partner launch note

### Day 10: Beta Launch

~~~markdown
# Beta Launch Notes - 2026-06-12

Maya: Launch note sent to all five partners.

Eli: First partner uploaded a dataset successfully. They asked for Salesforce export, which is not in beta scope.

Lena: We should capture Salesforce export as post-beta discovery, not beta scope.

Maya: Agreed. Context shift for post-beta: exports may become the next partner priority.
~~~

Expected signals:

- action closure: partner launch note sent
- context shift: Salesforce export is emerging as post-beta partner priority
- decision: keep Salesforce export out of beta scope
- action: capture Salesforce export in post-beta discovery backlog

## Expected Final State

### Signal Registry

The final registry should contain at least one accepted signal for each type:

| Type | Expected Example |
|---|---|
| context_shift | custom branding removed; Salesforce export becomes post-beta discovery |
| risk | PDF export slow; privacy may block invite; parser bug may block beta |
| dependency | privacy approval depends on retention; performance depends on cache TTL |
| decision | invite internal-only; privacy approves launch; beta go |
| open_decision | 10 MB cap if cache slips; delay beta/manual CSV cleanup if parser patch fails |
| mitigation | 72-hour retention; cache TTL; parser patch |
| action | send retention details; add cache TTL; update onboarding; send partner note |
| escalation | Data Platform cache TTL blocker unresolved by Week 1 Friday |

### Task State

Expected task mutations:

- create tasks from ACTION signals with owners/deadlines
- append signal-source notes to related existing tasks
- close completed actions when explicit completion evidence appears
- mark stale/unowned dependencies for escalation
- convert post-beta items into backlog tasks, not launch-blocking tasks

Expected final task examples:

~~~json
[
  {
    "title": "Profile PDF export for 20 MB datasets",
    "status": "done",
    "closed_by_signal": "sig-atlas-mitigation-cache-ttl-p95-74s"
  },
  {
    "title": "Draft support escalation path",
    "status": "done",
    "closed_by_signal": "sig-atlas-action-support-runbook-complete"
  },
  {
    "title": "Add deletion audit logs for teammate invite",
    "status": "backlog",
    "source_signal": "sig-atlas-action-deletion-audit-logs"
  },
  {
    "title": "Capture Salesforce export as post-beta discovery",
    "status": "open",
    "source_signal": "sig-atlas-action-salesforce-export-discovery"
  }
]
~~~

### Project Status Snapshot

Expected Week 2 Friday snapshot:

~~~markdown
# Atlas Launch Readiness Snapshot - 2026-06-12

Status: Green

Private beta launched to five design partners.

Resolved:
- PDF export p95 reduced to 7.4s after cache TTL mitigation.
- Privacy approved CSV upload and dashboard generation with 72-hour retention.
- CSV parser quoted-comma bug patched and verified against partner samples.
- Support escalation path completed.

Known limitations:
- Teammate invite remains internal-only until deletion audit logs are available.
- Salesforce export is post-beta discovery, not beta scope.

Open follow-ups:
- Add deletion audit logs.
- Capture Salesforce export discovery.
- Monitor first-week partner onboarding.
~~~

## Time Guardian Simulation

### Calendar Fixture

Create a mock calendar with realistic constraints:

- daily standup 09:30-10:00
- product sync Tuesday/Thursday 13:00-14:00
- focus blocks available most days 10:00-12:00 and 15:00-17:00
- Week 2 Wednesday has heavy meetings, forcing prioritization

### Review Checkpoints

Run Time Guardian after each daily batch.

Expected behavior:

| Day | Expected Proposal |
|---|---|
| Mon W1 | Schedule retention details and PDF profiling before their due dates |
| Tue W1 | Prioritize retention feasibility confirmation over lower-priority support docs |
| Wed W1 | Schedule cache TTL follow-up and parser/perf retest |
| Fri W1 | Flag Data Platform dependency as stale; propose escalation prep block |
| Mon W2 | Close perf-risk tasks after mitigation evidence; schedule privacy follow-up |
| Wed W2 | Prioritize parser patch above non-launch work |
| Thu W2 | Schedule partner launch note and final runbook review |

### Example Time Proposal

~~~markdown
ProjectOS Time proposal - 2026-06-10

1. 10:00-11:30 - Patch quoted-comma CSV parser
   Why: launch-blocking risk from dogfood; decision deadline Thursday 2pm.

2. 15:00-15:45 - Verify parser against five partner sample CSVs
   Why: completion evidence required before beta go/no-go.

3. 16:00-16:30 - Update Atlas project snapshot with parser risk status
   Why: go/no-go notes need current state.
~~~

## Agent-Ops Controls

### Claim/Confirm/Commit Surfaces

| Surface | Claim | Confirm | Commit |
|---|---|---|---|
| signal extraction | extractor emits signal JSON | source span exists and matches summary | signal enters approval queue only if grounded |
| signal write | approved signal appended to registry | registry read-back contains same signal ID | downstream task mutation only after read-back |
| task create | task mutation emitted | task store read-back contains task with source signal | calendar proposal can include task |
| task close | completion mutation emitted | source evidence exists and task read-back is closed | final status can report task done |
| calendar block | time block emitted | calendar fixture/read-back has event | task marked scheduled |

### Iron Laws For The Test

Use these as hard pass/fail checks:

- No signal without a source artifact and source span.
- No task mutation without an approved signal or explicit initial program task.
- No task closure without completion evidence.
- No risk marked resolved without a linked mitigation or decision.
- No escalation synthesized from a single source unless explicit escalation language exists.
- No final status claim without registry/task evidence.

### Dedupe Tests

Include repeated mentions across artifacts:

- PDF export risk appears in Day 01 chat and Day 03 triage.
- Privacy dependency appears in Day 01 kickoff and Day 02 privacy sync.
- Cache TTL mitigation appears in Day 03 and Day 06.

Expected:

- repeated mentions update existing signals, not create duplicates
- signal history records new sources
- task notes append new evidence without duplicate task creation

### Source Grounding Tests

Each expected signal should include:

- source file
- quoted or character-offset source span
- confidence
- owner/deadline when available
- lifecycle status

Signals without source grounding should be rejected or flagged as needs-review.

## Evaluation Metrics

### Scoring Model

The scorer should produce both hard gates and weighted scores.

#### Hard Fail Gates

Any of these fails the run regardless of weighted score:

- accepted signal lacks source file and source span
- task mutation lacks approved signal or explicit initial-task source
- task closure lacks explicit completion evidence
- risk is resolved without linked mitigation or decision evidence
- open decision is closed without a later decision or explicit cancellation
- unapproved signal mutates project brain or task store
- calendar proposal includes an already-closed task
- final status claim lacks registry/task/source evidence
- Agent-Ops write claim has no independent read-back witness

#### Weighted Score

| Area | Weight | Scored By |
|---|---:|---|
| Signal extraction | 25% | structured equivalence against expected signals |
| Dedupe and lifecycle transitions | 20% | deterministic registry/state comparison |
| Task mutation accuracy | 20% | exact operation and state comparison |
| Time Guardian scheduling accuracy | 15% | ranked proposal comparison and constraint checks |
| Agent-Ops verification completeness | 15% | audit/sentinel/read-back event comparison |
| Negative/noise handling | 5% | rejection/needs-review comparison |

Suggested passing threshold:

- no hard-fail gates triggered
- weighted score >= 90%
- no module below 80%

#### Expected vs Actual Matching

The scorer should separate three classes of comparison:

1. **Exact match:** IDs, dates, statuses, mutation ops, audit event types, task closure evidence.
2. **Structured match:** signal type, project, owner, deadline, linked entity, lifecycle relation.
3. **Semantic match:** signal summary equivalence and Time Guardian rationale quality.

Semantic matches should be judged by an evaluator model or a constrained rubric. They should not decide hard-fail gates.

### Signal Extraction

- precision by signal type
- recall by signal type
- owner/deadline extraction accuracy
- source grounding accuracy
- false positive rate for low-value chatter

Target for v0:

- 90% recall on ACTION, RISK, DECISION
- 80% recall on DEPENDENCY, OPEN_DECISION, MITIGATION
- 70% recall on CONTEXT_SHIFT
- escalation evaluated separately because it is synthesized across sources

### Lifecycle Accuracy

- risk created then resolved by mitigation
- open decision created then closed by decision
- dependency created then resolved or escalated
- action created then closed by completion evidence

Target:

- 100% of lifecycle transitions correct in deterministic expected corpus

### Task Mutation Accuracy

- no duplicate tasks for repeated action mentions
- source signal attached to every generated task
- due dates preserved
- completed tasks only close with explicit evidence

Target:

- zero duplicate tasks
- zero unsourced task mutations
- zero false task closures

### Time Guardian Accuracy

- launch-blocking tasks scheduled before lower-priority work
- overdue/stale tasks surfaced
- blocked tasks not scheduled as executable work unless next action is unblock/escalate
- completion evidence removes tasks from schedule proposals

Target:

- 90% priority-order agreement with expected proposals
- zero proposals for already-closed tasks

### Agent-Ops Accuracy

- every batch run has start/end/result sentinel
- every write has idempotency key
- every committed write has read-back witness
- every final status claim maps to source evidence

Target:

- 100% for deterministic harness checks

## Pass/Fail Gates

### MVP Pass

The harness passes if:

- all eight signal types are extracted at least once
- expected lifecycle transitions are correct
- no duplicate task is created from repeated signals
- final project snapshot matches source-grounded state
- Time Guardian proposes launch-critical work on the correct days
- Agent-Ops verification finds no unsourced writes or false completions

### MVP Fail

The harness fails if:

- any final status claim lacks source evidence
- a risk is resolved without mitigation/decision evidence
- a task is created twice from repeated mentions
- a completed task remains in the schedule proposal
- an unapproved signal mutates the project brain or task store

## Suggested Corpus File Tree

~~~text
gsd_ai_e2e/
  README.md
  program/
    program_overview.md
    project_registry.json
    initial_tasks.json
    initial_calendar_week_1.json
    initial_calendar_week_2.json
    scheduling_preferences.json
  batches/
    2026-06-01/
      inputs/
        meeting_001_kickoff.md
        chat_001_launch_room.md
      expected/
        signals.json
        task_mutations.json
        project_state_after.json
        time_proposal.json
        agent_ops_events.json
      actual/
        signals.json
        task_mutations.json
        project_state_after.json
        time_proposal.json
        agent_ops_events.json
    2026-06-02/
      inputs/
        meeting_002_privacy_sync.md
        chat_002_eng_privacy.md
      expected/
        signals.json
        task_mutations.json
        project_state_after.json
        time_proposal.json
        agent_ops_events.json
      actual/
        signals.json
        task_mutations.json
        project_state_after.json
        time_proposal.json
        agent_ops_events.json
    ...
  expected_final/
    signal_registry.json
    tasks.json
    project_snapshot.md
    audit_log.json
    agent_ops_report.json
  actual_final/
    signal_registry.json
    tasks.json
    project_snapshot.md
    audit_log.json
    agent_ops_report.json
  reports/
    score_summary.json
    score_report.md
    independent_review.md
  runner/
    README.md
    schemas/
      signal.schema.json
      signal_history.schema.json
      task_mutation.schema.json
      task_state.schema.json
      calendar_proposal.schema.json
      audit_event.schema.json
      batch_result.schema.json
      score_report.schema.json
    scripts/
      run_batch.sh
      score_run.sh
~~~

## Build Order

1. Create static corpus manually: program overview, 10 daily batches, expected outputs.
2. Define JSON schemas for signals, task mutations, task state, and audit events.
3. Build deterministic scorer that compares actual outputs to expected outputs.
4. Add a mocked Wakesurfer extractor interface.
5. Add the actual LLM extraction step behind a flag.
6. Add task mutation simulation.
7. Add Time Guardian proposal simulation.
8. Add Agent-Ops verification report.
9. Run the full two-week replay.
10. Save failures as regression fixtures.

## Next Strengthening Pass

Before implementing live extraction, strengthen this plan into an executable corpus:

1. Add complete expected JSON for Days 02-10.
2. Add per-day expected project state snapshots.
3. Add machine-readable Time Guardian proposals for every daily checkpoint.
4. Add Agent-Ops audit events, idempotency keys, sentinels, and read-back witnesses.
5. Add negative/noise batches:
   - casual chatter with no signal
   - ambiguous action with no owner
   - missing due date
   - duplicate source replay
   - stale claim contradicted by later source
   - unapproved signal that must not mutate state
   - malformed actual JSON
   - cross-project contamination case
6. Define approval simulation modes:
   - approve_all_valid
   - partial_approval
   - reject_noise
   - correct_owner
   - correct_due_date
7. Make markdown snapshots generated artifacts from structured state, not primary scoring targets.

## Key Design Choice

Do not start by testing live integrations. The first useful GSD-AI test is a replayable simulation where the correct answer is known. Once this corpus is stable, live integrations can be adapter tests layered on top.

The durable product question is not whether the system can read one meeting note. It is whether it can preserve operational truth across two weeks of noisy work without duplicating, losing, or inventing state.
