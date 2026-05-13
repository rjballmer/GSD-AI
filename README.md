# ProjectOS

**ProjectOS is an early-stage work-context operating layer for AI-assisted knowledge work.**

Modern work leaks context. Decisions hide in meetings. Risks show up once in chat and vanish. Tasks sit in one system while calendars fill from another. AI assistants help in the moment, but they usually start cold the next time.

ProjectOS is an attempt to close that loop:

> **Capture the signal. Build the project brain. Protect the time. Verify the work.**

This repository is intentionally early. The first public work here is product architecture, primitives, and prototype scaffolding. Code will follow the model below.

## The loop

```text
Work surfaces
  ↓
Capture important signals
  ↓
Maintain durable project memory
  ↓
Turn actions into protected calendar time
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

The hard part is not having these tools. The hard part is keeping the work state coherent across them.

ProjectOS focuses on the layer between tools: structured project memory, signal routing, approval queues, task-to-time planning, and verification.

## Modules

### ProjectOS Core

Durable project brains: project context, status, decisions, risks, dependencies, actions, open questions, references, and scope labels.

### ProjectOS Capture

Signal capture from meetings, chats, docs, tickets, and pasted notes. The system extracts structured signals such as decisions, risks, actions, dependencies, and context shifts.

### ProjectOS Time

Task-to-calendar planning. Approved actions become schedulable tasks, then protected work blocks.

### AgentOS controls

Verification around AI-generated signals, writes, scheduled jobs, public exports, and other agent actions.

## Design principles

- **AI interprets. Code enforces.** Use models for messy context; use code for schemas, routing, deduplication, calendar math, writes, and audit.
- **Human approval at write boundaries.** The agent proposes. The human decides.
- **Local-first memory.** Project state should be inspectable, portable, and editable.
- **Adapters over app lock-in.** ProjectOS should orchestrate existing Slack, Teams, calendar, task, doc, and repo integrations rather than rebuild them.
- **Trust is earned.** Start in review mode; promote automation only after evidence.

## Current status

This repo is in the architecture/prototype phase.

Planned first milestone:

1. local workspace generator
2. project context contract
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

ProjectOS is the connective tissue between those systems.

## License

License TBD while the project is still forming.
