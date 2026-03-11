---
name: sample
description: Template skill showing how to structure a Copilot CLI plugin skill.
---

<!--
  Replace this comment and the sections below with the actual workflow for your skill.
  Keep the frontmatter accurate because Copilot uses it to decide when to load the skill.
-->

# Sample Skill

Use this template when creating a new plugin skill.

## First pass

1. State the task family this skill covers.
2. Lock any repository or environment context that affects file layout.
3. Load only the extra references needed for the current request.

## Shared rules

- Keep the root workflow concise.
- Put variant-specific details in `references/` instead of bloating this file.
- Prefer scripts for fragile or repetitive operations.
