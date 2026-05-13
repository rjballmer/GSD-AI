# Vision

Modern knowledge work has a structural problem: context evaporates faster than it can be acted on.

A decision appears in a meeting. A mitigation appears days later in chat. An action item goes into a task manager but never gets calendar time. A status update gets written from memory because nobody wants to dig through five systems again.

AI makes this both better and worse. It can summarize, extract, and propose. But without durable context and verification, each assistant session becomes another temporary surface.

GSD-AI is an AI-native execution system for that gap.

## Product thesis

GSD-AI helps people:

1. capture important work signals before they disappear
2. translate those signals into goals, plans, and durable work context
3. convert actions into protected time
4. verify that AI-generated updates and writes are grounded and correct

Short version:

> Capture the signal. Clarify the goal. Build the plan. Protect the time. Verify the work.

## The user experience we are aiming for

You should be able to come back to a goal or workstream after two weeks and ask:

> Where did I leave off, and what should I do next?

And get:

- current state
- active decisions
- unresolved risks
- dependencies
- actions
- upcoming commitments
- recommended next steps
- source links for anything important

Then you should be able to ask:

> What should I protect time for this week?

And get a realistic plan based on the work state, task list, and calendar.

## The architecture bet

The core bet is not that an LLM should do everything.

The bet is:

> AI should interpret messy work context. Code should enforce durable invariants.

Models are useful for reading meeting notes, classifying signals, explaining urgency, and drafting summaries. Code should handle schemas, deduplication, routing, calendar math, permission checks, writes, and verification.
