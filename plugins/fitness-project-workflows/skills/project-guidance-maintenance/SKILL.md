---
name: project-guidance-maintenance
description: Update this repository's AGENTS guidance, handoff state, skills, Codex configuration, or command rules while keeping their responsibilities distinct and concise.
---

# Project guidance maintenance

Read the root and applicable nested `AGENTS.md` files plus `docs/handoffs/project-state.md` before making a guidance change. Preserve active rules, current decisions, and the user's scope; do not turn one temporary request into permanent policy.

## Classify the instruction first

- Put a durable, mandatory repository convention in root `AGENTS.md`.
- Put an application- or directory-specific convention in a nested `AGENTS.md`.
- Put a reusable, task-specific workflow in a skill.
- Put changing facts in `docs/handoffs/project-state.md`.
- Put sandbox, model, MCP, hook, or approval defaults in `.codex/config.toml` only when needed. Do not put prose guidance or secrets there.
- Put external shell-command permissions in `.codex/rules/` only. Rules do not define code style or task workflow.

## Editing rules

- Keep root guidance short, non-duplicative, and limited to cross-project requirements.
- When updating the handoff, replace it with compact current state. Keep exactly one handoff file and omit session history and superseded alternatives.
- Give skills discriminating descriptions and include only non-obvious, reusable workflow detail. Do not move mandatory safety, privacy, or authorization constraints out of `AGENTS.md`.
- For a plugin change, validate the plugin manifest and each changed skill before handoff.
