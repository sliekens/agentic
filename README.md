# Agentic

My personal collection of GitHub Copilot customizations — prompts, instructions, agents, and installable plugins — tailored to my specific workflows and preferences.

> Inspired by [github/awesome-copilot](https://github.com/github/awesome-copilot).

## Structure

```
agentic/
├── AGENTS.md                    # Repo-specific rules for future Codex/Copilot work
├── .github/
│   ├── copilot-instructions.md   # Global Copilot instructions for this repo
│   └── plugin/
│       └── marketplace.json      # Marketplace catalog for this repo's plugins
└── plugins/
    ├── README.md                 # How plugin packages are organized
    ├── devcontainer/
    │   ├── plugin.json
    │   └── skills/
    │       └── devcontainer/
    │           ├── SKILL.md
    │           └── references/
    ├── engineering-workflow/
    │   ├── plugin.json
    │   └── agents/
    │       ├── distiller.agent.md
    │       ├── implementation.agent.md
    │       └── technical-analyst.agent.md
    ├── synouser/
    │   ├── plugin.json
    │   └── skills/
    │       └── synouser/
    │           └── SKILL.md
    └── ugacltool/
        ├── plugin.json
        └── skills/
            └── ugacltool/
                └── SKILL.md
```

## Quick Reference

| Folder            | Purpose                                                        | File type                                                      |
| ----------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `AGENTS.md`       | Repo-specific rules for future agent work                      | `AGENTS.md`                                                    |
| `.github/`        | Repo-level Copilot instructions and plugin catalog             | `copilot-instructions.md`, `*.json`                            |
| `.github/agents/` | Workspace custom agent configurations                          | `*.agent.md`                                                   |
| `plugins/`        | Installable Copilot CLI plugins with bundled skills and agents | `plugin.json` + `skills/**/SKILL.md` or `agents/**/*.agent.md` |

## Usage

Plugins can be installed from `plugins/<name>/` directly or exposed through [`.github/plugin/marketplace.json`](.github/plugin/marketplace.json).

See the `README.md` inside each folder for the expected format and workflow.
