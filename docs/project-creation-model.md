# Project Creation Model

GSD-AI project creation should be a workflow, not just a folder generator.

The reference architecture is strong because it treats project creation as the beginning of an AI-assisted context loop:

```text
Trigger → Infer → Create → Enrich → Confirm → Track → Resume
```

## Design principles

### 1. Create first, refine after

When a user says they want to start a project, they usually want momentum. Do not make them fill out a full charter before anything exists.

Default behavior:

1. infer a project name and one-line purpose from the user input or source links
2. create the project structure immediately
3. record whatever context is available
4. offer enrichment as the next step

Only ask a clarifying question if there is truly no usable project signal.

### 2. Source-link-first, not charter-first

Users should not have to type a project charter into a CLI.

In real work, context already exists in:

- planning docs
- design docs
- meeting notes
- tickets/issues
- PRDs
- dashboards
- chat threads
- repo links
- prior AI sessions

The project creation command should encourage users to drop links and let AI propose the initial project signals.

Example:

```bash
gsd-ai project create ~/Workspace "Billing Migration" \
  --purpose "Move billing jobs to the new platform" \
  --doc https://docs.example.com/billing-migration-prd \
  --source https://linear.example.com/issue/ENG-123 \
  --source https://github.com/acme/platform/pull/456
```

### 3. Session context is a first-class source

Sometimes the current AI conversation *is* the project brief. The user should be able to say:

```bash
gsd-ai project create-from-session ~/Workspace "Billing Migration"
```

The agent should scan backward from the current moment, identify the relevant topic boundary, and extract only the context belonging to the current project.

Do not blindly summarize the whole session.

### 4. Extract structured project signals

From links, session context, or pasted notes, extract:

- project name
- one-line description
- problem statement
- goals
- success metrics
- stakeholders/collaborators
- key documents
- code paths/repos
- decisions made
- key findings
- risks
- dependencies
- open questions
- follow-up actions

These should be proposed for review before becoming durable context.

### 5. Separate immediate creation from enrichment

Project creation should be fast. Enrichment can be deeper and optional.

Recommended flow:

```text
Phase 1: Create minimal project immediately
Phase 2: Gather/enrich context from sources
Phase 3: Present proposed extracted signals
Phase 4: Apply approved updates
Phase 5: Create initial actions/tasks if user confirms
```

This preserves momentum without sacrificing context quality.

## Proposed command surfaces

### Minimal create

```bash
gsd-ai project create ~/Workspace "Project Name" --purpose "One-line purpose"
```

Creates project structure and a context contract.

### Source-backed create

```bash
gsd-ai project create ~/Workspace "Project Name" \
  --doc <url-or-path> \
  --source <url-or-path>
```

Creates project structure and records context sources for AI extraction.

### Session-backed create

```bash
gsd-ai project create-from-session ~/Workspace "optional name hint"
```

Uses recent session context as the project origin story.

### Enrich existing project

```bash
gsd-ai project enrich ~/Workspace "Project Name"
```

Reads recorded sources, proposes structured project signals, and asks for approval before updating durable context.

### Update from session

```bash
gsd-ai project update-from-session ~/Workspace "Project Name"
```

Extracts what changed in the current session and appends session notes, findings, decisions, outputs, and follow-ups.

## Recommended project folder

Both PARA and GSD frameworks keep projects under `01_projects/`.

Each project should eventually look like:

```text
01_projects/<project-slug>/
├── context.md          # compact project context contract
├── sources.json        # user-provided docs/links/sources
├── signals.jsonl       # extracted/approved project signals
├── actions.md          # human-readable action list
├── sessions/           # session notes and updates
├── docs/               # local/reference docs
├── outputs/            # generated artifacts
└── archive/            # superseded local project files
```

The initial v0.1 implementation may only create `context.md` and `sources.json`, but the architecture should aim here.

## AI extraction model

AI should propose, not silently mutate.

For any source-backed or session-backed enrichment, present:

```text
Proposed Project Signals

Name: <project name>
Purpose: <one-line purpose>
Problem: <problem statement>
Goals:
- ...
Decisions:
- ...
Risks:
- ...
Dependencies:
- ...
Actions:
- ...
Open questions:
- ...
Sources:
- ...
```

Then ask the user what to accept, edit, or reject.

## Deterministic vs AI responsibilities

AI should handle:

- reading messy context
- identifying topic boundaries
- summarizing project purpose
- extracting candidate signals
- proposing next actions

Code should handle:

- folder creation
- slug generation
- source recording
- schema validation
- duplicate detection
- durable writes
- audit log entries
- approval state

Principle:

> AI interprets. Code enforces.

## Dependency boundary

GSD-AI should not rebuild every source integration.

It should rely on existing adapters, host tools, or MCP servers for:

- document read/search
- chat/thread read/search
- ticket/issue read/search
- repo access
- calendar/task integrations

GSD-AI owns the project ontology, source registry, signal extraction flow, approval queue, and durable project memory.

## Build sequence

### v0.1 — already started

- workspace init
- framework choice
- project create
- source capture via `--source` / `--doc`
- project context contract

### v0.2 — next high-value step

- `signals.jsonl`
- source registry schema
- `project enrich` command skeleton
- proposed signal output format
- approval queue file

### v0.3

- `create-from-session`
- topic-boundary extraction prompt
- session note creation
- `sessions/YYYY-MM-DD-N.md`

### v0.4

- action extraction
- action/task export adapters
- optional calendar/time-block handoff

### v0.5

- AgentOS-style verification:
  - source grounding checks
  - duplicate signal detection
  - write audit
  - scope/privacy checks
