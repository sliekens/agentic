# Instructions

This folder contains **instruction files** for GitHub Copilot.

## What is an instruction file?

An instruction file (`.instructions.md`) defines coding standards or best practices that Copilot applies automatically when working on files that match a glob pattern. Unlike prompt files, they run silently in the background — you don't invoke them manually.

Reference: [VS Code – Custom instructions](https://code.visualstudio.com/docs/copilot/copilot-customization#_custom-instructions)

## File naming

```
<short-descriptive-name>.instructions.md
```

Examples: `typescript.instructions.md`, `react-components.instructions.md`

## Where to store instructions for a project

Copy any `.instructions.md` file from this folder into the target project's `.github/instructions/` directory.

## Format

See [`sample.instructions.md`](sample.instructions.md) for a ready-to-copy template.

```markdown
---
applyTo: '**/*.ts'   # glob pattern — which files these instructions apply to
---

Your instructions here.
```

### `applyTo` examples

| Pattern | Applies to |
|---|---|
| `**` | Every file in the project |
| `**/*.ts` | All TypeScript files |
| `src/**` | Everything under `src/` |
| `**/*.test.*` | All test files |
