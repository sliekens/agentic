# Prompts

This folder contains reusable **prompt files** for GitHub Copilot Chat.

## What is a prompt file?

A prompt file (`.prompt.md`) is a Markdown file that defines a reusable chat prompt. When you open one in VS Code and click **Run Prompt**, or reference it with `#file:`, Copilot uses the file content as the initial message.

Reference: [VS Code – Reusable prompt files](https://code.visualstudio.com/docs/copilot/copilot-customization#_reusable-prompt-files-experimental)

## File naming

```
<short-descriptive-name>.prompt.md
```

Examples: `refactor-function.prompt.md`, `write-unit-tests.prompt.md`

## Where to store prompts for a project

Copy any `.prompt.md` file from this folder into the target project's `.github/prompts/` directory. VS Code picks them up automatically.

## Format

See [`sample.prompt.md`](sample.prompt.md) for a ready-to-copy template.

```markdown
---
mode: 'ask'          # ask | edit | agent
description: 'One-line summary shown in the prompt picker'
---

Your prompt text here.
Use #{variable} for placeholders that Copilot will fill in.
```

### Supported front-matter fields

| Field | Values | Description |
|---|---|---|
| `mode` | `ask`, `edit`, `agent` | How Copilot invokes the prompt |
| `description` | string | Short label shown in the prompt picker |
| `tools` | list | (agent mode) MCP tools the prompt may use |
