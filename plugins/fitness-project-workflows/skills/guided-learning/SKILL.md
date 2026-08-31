---
name: guided-learning
description: Guide a user through a repository change one verified step at a time, with complete copyable edits and focused explanations. Use when the user asks for a guided implementation or teaching-oriented walkthrough.
---

# Guided learning workflow

## Delivery mode

Work on one explicit implementation step at a time unless the user explicitly asks for a complete roadmap or all remaining steps at once.

When the user asks for a complete roadmap, provide every remaining implementation step in one response, in execution order. This changes only the number of steps delivered per response; it never waives any explanation, code-detail, or verification requirement below.

Before each manual action, explain its goal, prerequisites, why it is needed, what it changes, and the result to expect.

## Each implementation step

1. Identify every file to add, replace, or edit.
2. Provide the complete contents of a small file or an unambiguous copyable replacement or insertion block for an existing file. Do not use pseudocode or ellipses.
3. Immediately after every code block, explain each changed construct relative to the current code: additions, removals, renames, altered parameters, control flow, imports, configuration keys, decorators, classes, functions, and unfamiliar expressions. State both what changed and why it belongs in the current architecture.
4. When an existing component needs no change, explicitly explain why it remains unchanged.
5. Give an exact verification command or action, explain what it does and its expected non-secret output, and state the success condition.
6. Stop after that step has been verified unless the user explicitly requests more. In complete-roadmap mode, stop only after all requested steps have been explained.

Keep explanations focused on the user's requested change. Do not introduce related features or additional business logic ahead of the approved scope.
