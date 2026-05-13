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

- workspace generator with `gsd` and `para` framework choices
- project index
- project context contract
- scope labels
- manual add-context workflow
- resume-from-here status
- local audit log

## Phase 2 — Management workflows

Make the context operational.

User stories:

- As a user preparing for a meeting, I want relevant risks, decisions, and actions surfaced automatically.
- As a user ending a session, I want work state updated with what changed.
- As a user reviewing the week, I want a recap generated from durable context.

Deliverables:

- meeting prep
- end-session update
- weekly recap
- health check
- archive/stale project workflow
- public-safe export workflow

## Phase 3 — Signal capture

Add structured signal ingestion.

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
