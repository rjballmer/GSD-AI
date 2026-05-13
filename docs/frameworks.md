# Workspace Frameworks

GSD-AI supports two workspace frameworks at bootstrap. The framework controls the folder layout. It does not change the core primitives: project, signal, action, time block, scope, and evidence.

## Recommendation

**Start with PARA unless you already have a strong preference.**

AI is a strong enabler for the Second Brain model because it can gather richer context across Projects, Areas, Resources, and Archives before proposing plans or actions. PARA gives the assistant more useful places to look without forcing every piece of context into an execution queue.

Use GSD when you want the workspace to emphasize execution flow first: next actions, waiting items, someday items, and reviews.

## Choosing a framework

Interactive:

```bash
gsd-ai init ~/Workspace
```

The prompt leads with PARA and links to background reading.

Non-interactive:

```bash
gsd-ai init ~/SecondBrain --framework para
gsd-ai init ~/GSD --framework gsd
```

## PARA framework — recommended default

Second Brain layout for people who prefer Tiago Forte's Projects, Areas, Resources, Archives taxonomy.

Foundation:

- PARA overview: https://fortelabs.com/blog/para/
- Building a Second Brain: https://www.buildingasecondbrain.com/book

```text
workspace/
├── AGENTS.md
├── 00_inbox/
├── 01_projects/
├── 02_areas/
├── 03_resources/
├── 04_archives/
├── 05_reports/
└── .gsd-ai/
    ├── PROJECT_SETUP.md
    ├── index.json
    └── audit.jsonl
```

Use this when durable knowledge organization matters most: projects, ongoing areas, reusable resources, and archived work.

## GSD framework

Execution-first layout for people who think in captures, active projects, next actions, waiting items, someday ideas, responsibilities, references, archives, and reviews.

Foundation:

- Getting Things Done: https://gettingthingsdone.com/
- GTD book: https://gettingthingsdone.com/what-is-gtd/

```text
workspace/
├── AGENTS.md
├── 00_inbox/
├── 01_projects/
├── 02_next_actions/
├── 03_waiting/
├── 04_areas/
├── 05_someday/
├── 06_resources/
├── 07_archives/
├── 08_reports/
└── .gsd-ai/
    ├── PROJECT_SETUP.md
    ├── index.json
    └── audit.jsonl
```

Use this when execution flow matters most: capture, decide, schedule, follow up, review.

## Project setup is source-link-first

GSD-AI should not make users type a full project charter into the CLI. Project context usually already exists somewhere: docs, planning threads, tickets, PRDs, meeting notes, dashboards, chat threads, or repo links.

Recommended flow:

```bash
gsd-ai project create ~/Workspace "Launch Billing Migration" \
  --purpose "Move billing jobs to the new platform" \
  --doc https://docs.example.com/billing-migration-prd \
  --source https://linear.example.com/issue/ENG-123 \
  --source https://github.com/acme/platform/pull/456
```

The CLI records those sources in the project context. The next AI-assisted layer will read them and propose project signals:

- goals
- decisions
- risks
- dependencies
- actions
- open questions

The user reviews before any durable writes land.

## Consistent ontology

Both frameworks use `project` everywhere:

- CLI: `gsd-ai project create`
- files: `01_projects/<project>/context.md`
- index: `.gsd-ai/index.json` stores `projects`
- signal schema: `Signal.project`

This avoids AI leakage where internal names surface in prompts, summaries, or generated docs.
