# GSD-AI

**GSD-AI is an early-stage AI-native execution system for converting work signals into goals, plans, protected time, and impact.**

Modern work leaks context. Decisions hide in meetings. Risks show up once in chat and vanish. Tasks sit in one system while calendars fill from another. AI assistants help in the moment, but they usually start cold the next time.

GSD-AI is an attempt to close that loop:

> **Capture the signal. Clarify the goal. Build the plan. Protect the time. Verify the work.**

This repository is intentionally early. The first public work here is product architecture, primitives, and prototype scaffolding. Code will follow the model below.

## The loop

```text
Work surfaces
  ↓
Capture important signals
  ↓
Translate signals into goals and plans
  ↓
Protect time for execution
  ↓
Verify AI-generated updates and writes
```

## Why this exists

Most productivity tools manage one slice of work:

- notes store context
- task managers store intent
- calendars store commitments
- chat contains decisions
- AI assistants generate helpful fragments

The hard part is not having these tools. The hard part is keeping the execution state coherent across them.

GSD-AI focuses on the layer between tools: structured goal context, signal routing, approval queues, task-to-time planning, and verification.

## Modules

### GSD-AI Core

Durable goal and work context: current state, decisions, risks, dependencies, actions, open questions, references, and scope labels.

### GSD-AI Capture

Signal capture from meetings, chats, docs, tickets, and pasted notes. The system extracts structured signals such as decisions, risks, actions, dependencies, and context shifts.

### GSD-AI Time

Task-to-calendar planning. Approved actions become schedulable tasks, then protected work blocks.

### AgentOS controls

Verification around AI-generated signals, writes, scheduled jobs, public exports, and other agent actions.

## Design principles

- **AI interprets. Code enforces.** Use models for messy context; use code for schemas, routing, deduplication, calendar math, writes, and audit.
- **Human approval at write boundaries.** The agent proposes. The human decides.
- **Local-first memory.** Work state should be inspectable, portable, and editable.
- **Adapters over app lock-in.** GSD-AI should orchestrate existing Slack, Teams, calendar, task, doc, and repo integrations rather than rebuild them.
- **Trust is earned.** Start in review mode; promote automation only after evidence.

## Current status

This repo is in the architecture/prototype phase.

Planned first milestone:

1. local workspace generator
2. goal/work context contract
3. signal schema and registry
4. manual capture from pasted notes/files
5. approval queue
6. resume-from-here status command

See [`docs/roadmap.md`](docs/roadmap.md) for the phased build plan.

## What this is not

- not another note app
- not a task manager replacement
- not a calendar replacement
- not an autonomous agent that writes everywhere by default
- not tied to one chat, docs, or calendar vendor

GSD-AI is execution infrastructure between those systems.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
