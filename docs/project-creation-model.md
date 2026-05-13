# Project Lifecycle Model

GSD-AI should expose a small set of simple primitives:

```text
Initialize workspace → Create project → Update project → Review projects
```

The point is not to invent a complicated project-management vocabulary. The point is to make it easy for AI to help keep project context current, useful, and moving.

## The three core actions

### Create

**Create is an invoked skill.**

The user explicitly starts it when a project deserves a durable home.

Create should be primarily based on linked content, not a manually typed charter. In real work, the context already exists in docs, tickets, meeting notes, chat threads, dashboards, repo links, or prior AI sessions.

Create does three things:

1. creates the project structure
2. records source links/context
3. proposes the first project signals for review

Create should bias toward momentum: create the project first when enough signal exists, then refine.

### Update

**Update is how project memory changes.**

Updates can arrive through two paths:

1. **Captured signals** — Wakesurfer-style signal capture from meetings, chats, docs, tickets, email, and other work surfaces.
2. **Invoked updates** — the user explicitly adds context that automated capture missed, usually by dropping linked docs/content.

Update should merge new context into the project state after user review. It can add or change:

- decisions
- risks
- dependencies
- actions
- mitigations
- context shifts
- open questions
- source links
- session notes

Update is the one public verb. Do not expose a separate `enrich` action.

### Review

**Review is an invoked AI inspection of current project state.**

Review is not just a recap. It should inspect the project and help keep it moving forward.

A review should look for:

- stale actions
- unresolved risks
- waiting/dependency items
- open decisions
- quiet projects
- unprocessed source links
- contradictions or outdated context
- missing next steps
- opportunities to schedule work

Review can happen on demand or as a weekly ritual:

```bash
gsd-ai review weekly ~/Workspace
```

Review should produce recommendations, not silently rewrite project state.

## Design principles

### 1. Source-link-first, not charter-first

Users should not have to type a project charter into a CLI.

The project creation command should encourage users to drop links and let AI propose the initial project signals.

Example:

```bash
gsd-ai project create ~/Workspace "Billing Migration" \
  --purpose "Move billing jobs to the new platform" \
  --doc https://docs.example.com/billing-migration-prd \
  --source https://linear.example.com/issue/ENG-123 \
  --source https://github.com/acme/platform/pull/456
```

### 2. Create first, refine after

When a user invokes Create, they usually want a project container now. Do not make them fill out a long form first.

Default behavior:

1. infer a project name and one-line purpose from user input or source links
2. create the project structure immediately
3. record available source context
4. propose first signals for review

Only ask a clarifying question if there is truly no usable project signal.

### 3. Session context is a first-class source

Sometimes the current AI conversation *is* the project brief. The user should be able to say:

```bash
gsd-ai project create-from-session ~/Workspace "Billing Migration"
```

The agent should scan backward from the current moment, identify the relevant topic boundary, and extract only the context belonging to the current project.

Do not blindly summarize the whole session.

### 4. Update absorbs both automated and manual context

Wakesurfer-style capture is one input to Update. It should not be the only path.

Users also need an invoked update path for context that automation missed:

```bash
gsd-ai project update ~/Workspace "Billing Migration" \
  --doc https://docs.example.com/new-cutover-plan \
  --source https://slack.example.com/thread/123
```

Update should produce proposed signal changes and ask for approval before durable writes.

### 5. Review is the larger net

Automated capture will miss things. Manual updates will be incomplete. Review is the larger process that inspects project state and catches drift.

A weekly review should answer:

- What changed?
- What is stale?
- What is blocked?
- What decisions are still open?
- What actions lack owners or time?
- What source links were never processed?
- What should happen next?

## Extracted project signals

From links, session context, captured signals, or pasted notes, extract:

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

## Proposed command surfaces

### Create project

```bash
gsd-ai project create ~/Workspace "Project Name" \
  --purpose "One-line purpose" \
  --doc <url-or-path> \
  --source <url-or-path>
```

Creates project structure, records context sources, and prepares for AI-assisted signal extraction.

### Create project from session

```bash
gsd-ai project create-from-session ~/Workspace "optional name hint"
```

Uses recent session context as the project origin story.

### Update project

```bash
gsd-ai project update ~/Workspace "Project Name" \
  --source <url-or-path> \
  --from-session
```

Reads new context, proposes structured project signal changes, and asks for approval before updating durable context.

### Review projects

```bash
gsd-ai review weekly ~/Workspace
```

Sweeps project state to find missed context, stale actions, unresolved risks, waiting items, unprocessed sources, and quiet projects.


## Scheduling model

Every skill should be schedulable.

A skill should be callable in two modes:

```text
manual invocation → user asks now
scheduled invocation → system runs at a configured cadence
```

This applies to Create, Update, Review, and future skills, but Review is the most natural scheduled workflow.

Examples:

```bash
gsd-ai schedule add "weekly project review"   --skill review.weekly   --workspace ~/Workspace   --cron "0 9 * * MON"

gsd-ai schedule add "daily signal update"   --skill project.update   --workspace ~/Workspace   --source captured-signals   --cron "0 16 * * *"
```

Scheduled skills should still respect the same control model:

- declare inputs
- declare output artifact
- run with scoped permissions
- produce a reviewable summary
- avoid silent durable writes unless explicitly configured
- record audit state
- surface failures or empty runs

Default recommendation:

- **Create** — usually manual/invoked
- **Update** — manual or triggered by captured signals
- **Review** — manual or scheduled, commonly weekly

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

## AI proposal model

AI should propose, not silently mutate.

For Create, Update, or Review, present proposed changes in a reviewable form:

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
- inspecting project state during review

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

GSD-AI owns the project ontology, source registry, signal extraction flow, approval queue, review workflow, and durable project memory.

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
- `project update` command skeleton
- proposed signal output format
- approval queue file

### v0.3

- `project update --from-session`
- topic-boundary extraction prompt
- session note creation
- `sessions/YYYY-MM-DD-N.md`

### v0.4

- `review weekly`
- stale action detection
- unresolved risk/dependency report
- unprocessed source detection
- recommended next actions

### v0.5

- action extraction
- action/task export adapters
- optional calendar/time-block handoff

### v0.6

- AgentOS-style verification:
  - source grounding checks
  - duplicate signal detection
  - write audit
  - scope/privacy checks
