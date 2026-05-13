# Roadmap

This roadmap is intentionally staged. The build order is different from the product loop.

The product loop is:

```text
Capture → Context → Plan → Time → Verify
```

The build order is:

```text
1. Project context substrate
2. Management workflows
3. Signal capture automation
4. Calendar / execution management
5. Trust, verification, and controls
```

## Phase 1 — Core context

Build the durable execution substrate.

User stories:

- As a worker managing multiple projects, I want durable context so I can resume without reconstructing everything from memory.
- As an AI assistant user, I want context stored in inspectable files so I can trust and edit it.
- As an owner, I want current status, decisions, risks, dependencies, actions, and open questions in one place.

Deliverables:

- workspace generator with recommended `para` and optional `gsd` framework choices
- project index
- project context contract with source-link capture
- scope labels
- manual add-context workflow
- resume-from-here status
- local audit log

## Phase 2 — Create / Update / Review workflows

Make the context operational through three simple actions.

User stories:

- As a user starting a project, I want to invoke Create with links/docs instead of typing a project charter.
- As a user with new context, I want Update to merge Wakesurfer-captured signals and manually supplied links into project memory after review.
- As a user reviewing a project, I want Review to inspect current state, find stale or missing pieces, and recommend how to keep the project moving.

Deliverables:

- source-link-first Create workflow
- Update workflow for captured signals and invoked context additions
- Review workflow for current-state inspection
- schedule metadata model for manually invoked vs scheduled skills
- proposed signal output format
- approval queue
- local audit log for approved writes

## Phase 3 — Automated signal capture

Add Wakesurfer-style structured signal ingestion.

User stories:

- As a worker in meeting/chat overload, I want decisions, risks, actions, and dependencies captured before they disappear.
- As a user, I want duplicate or stale signals suppressed.
- As a user, I want proposed updates to show their source before I approve them.

Deliverables:

- signal schema
- signal registry
- manual extraction from pasted notes/files
- approval queue
- fingerprint/dedup logic
- noise learning
- later: adapters for chat, email, docs, calendar notes, tickets
- scheduled update runs from captured signal queues

## Phase 4 — Time and execution

Turn actions into protected execution time.

User stories:

- As a user, I want actions to become schedulable tasks.
- As a user with a packed calendar, I want realistic work blocks proposed.
- As a user, I want repeated deferrals surfaced as workload or priority signals.

Deliverables:

- task import adapter
- active action → task proposal
- calendar availability model
- numbered time-block proposal
- calendar writeback
- scheduling preference learning

## Phase 5 — AgentOS controls

Add trust and verification around AI-generated work.

User stories:

- As a user, I want to know whether an extracted signal is grounded in source material.
- As a user, I want duplicate writes blocked before they create noise.
- As a user, I want proof that approved updates and calendar blocks actually landed.
- As a user, I want private details blocked from public-safe exports.

Deliverables:

- evidence chain: Intent → Claim → Witness → Verdict → Commit → Audit
- fact QA
- write QA
- job/sweep health checks
- scope gates
- public-export leakage checks
