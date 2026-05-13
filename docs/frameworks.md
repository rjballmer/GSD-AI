# Workspace Frameworks

GSD-AI supports two workspace frameworks at bootstrap. The framework controls the folder layout. It does not change the core primitives: project, signal, action, time block, scope, and evidence.

## Choosing a framework

Interactive:

```bash
gsd-ai init ~/GSD
```

Non-interactive:

```bash
gsd-ai init ~/GSD --framework gsd
gsd-ai init ~/SecondBrain --framework para
```

## GSD framework

Execution-first layout for people who think in captures, active projects, next actions, waiting items, someday ideas, responsibilities, references, archives, and reviews.

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
    ├── index.json
    └── audit.jsonl
```

Use this when execution flow matters most: capture, decide, schedule, follow up, review.

## PARA framework

Second Brain layout for people who prefer Tiago Forte's Projects, Areas, Resources, Archives taxonomy.

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
    ├── index.json
    └── audit.jsonl
```

Use this when durable knowledge organization matters most: projects, ongoing areas, reusable resources, and archived work.

## Consistent ontology

Both frameworks use `project` everywhere:

- CLI: `gsd-ai project create`
- files: `01_projects/<project>/context.md`
- index: `.gsd-ai/index.json` stores `projects`
- signal schema: `Signal.project`

This avoids AI leakage where internal names surface in prompts, summaries, or generated docs.
