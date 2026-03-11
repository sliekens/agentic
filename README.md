# Agentic

My personal collection of GitHub Copilot customizations — prompts, instructions, agents, and installable plugins — tailored to my specific workflows and preferences.

> Inspired by [github/awesome-copilot](https://github.com/github/awesome-copilot).

## Structure

```
skill-issues/
├── .github/
│   └── copilot-instructions.md   # Global Copilot instructions for this repo
├── prompts/
│   ├── README.md                 # How to use prompt files
│   └── sample.prompt.md          # Template for new prompts
├── instructions/
│   ├── README.md                 # How to use instruction files
│   └── sample.instructions.md    # Template for new instructions
├── agents/
│   ├── README.md                 # How to define custom agents
│   └── sample/
│       └── README.md             # Template for a new agent
└── plugins/
    ├── README.md                 # How plugin packages are organized
    ├── devcontainer/
    │   ├── plugin.json
    │   └── skills/
    │       └── devcontainer/
    │           ├── SKILL.md
    │           └── references/
    └── sample/
        ├── README.md             # Template for a new plugin
        ├── plugin.json
        └── skills/
            └── sample/
                └── SKILL.md
```

## Quick Reference

| Folder          | Purpose                                             | File type                            |
| --------------- | --------------------------------------------------- | ------------------------------------ |
| `.github/`      | Repo-level Copilot instructions                     | `copilot-instructions.md`            |
| `prompts/`      | Reusable, task-specific prompts                     | `*.prompt.md`                        |
| `instructions/` | Coding standards applied to matching files          | `*.instructions.md`                  |
| `agents/`       | Custom agent configurations (MCP / tools)           | `README.md` per agent                |
| `plugins/`      | Installable Copilot CLI plugins with bundled skills | `plugin.json` + `skills/**/SKILL.md` |

## Usage

Copy any prompt or instruction file into the `.github/prompts/` or `.github/instructions/` directory of a target repository to activate it in that project. Plugins can be installed from `plugins/<name>/` directly or exposed through [`.github/plugin/marketplace.json`](.github/plugin/marketplace.json).

See the `README.md` inside each folder for the expected format and workflow.
