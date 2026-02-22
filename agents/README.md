# Agents

This folder contains definitions for custom **GitHub Copilot agents**.

## What is an agent?

An agent extends Copilot with additional tools and context. Agents can connect to MCP (Model Context Protocol) servers, execute commands, or wrap a curated set of prompts and instructions into a named persona.

Reference: [VS Code – Copilot Chat agents](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)

## Structure

Each agent lives in its own sub-folder:

```
agents/
└── <agent-name>/
    └── README.md    # Description, setup steps, and usage examples
```

Additional files (config JSON, `.prompt.md` files, MCP server manifests) may also live in the agent folder.

## Creating a new agent

1. Copy the `sample/` folder and rename it.
2. Edit `README.md` to describe the agent's purpose, required tools, and how to invoke it.
3. Add any supporting files (prompts, config) alongside the `README.md`.

See [`sample/README.md`](sample/README.md) for a ready-to-copy template.
