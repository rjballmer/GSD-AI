# Dependency Boundaries

ProjectOS should not rebuild every app integration.

It assumes host environments may already provide tools, APIs, MCP servers, or adapters for common systems.

## Assumed capability categories

- communication access: Slack, Teams, Discord, email, chat search/read/write
- calendar access: free/busy lookup, event creation, event verification
- task access: list/create/update/complete tasks
- document access: read/search/write docs and wikis
- repository/ticket access: GitHub, GitLab, Jira, Linear, issue trackers
- notification delivery: chat, email, push, CLI
- auth/session handling: OAuth, browser sessions, keychain, local config, environment tokens

## What ProjectOS adds

ProjectOS provides the orchestration layer:

- project memory
- signal schema
- routing
- deduplication
- approval queues
- task-to-time planning
- verification and audit

In other words:

```text
existing adapters provide access
ProjectOS provides work-context intelligence and control
```
