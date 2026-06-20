# Agentic

My personal collection of GitHub Copilot customizations — prompts, instructions, agents, and installable plugins — tailored to my specific workflows and preferences.

> Inspired by [github/awesome-copilot](https://github.com/github/awesome-copilot).

## Structure

```
agentic/
├── AGENTS.md                    # Repo-specific rules for future Codex/Copilot work
├── .claude-plugin/
│   └── marketplace.json          # Canonical marketplace catalog (Claude & Copilot)
├── .github/
│   ├── copilot-instructions.md   # Global Copilot instructions for this repo
│   └── plugin/
│       └── marketplace.json      # Compatibility copy of marketplace catalog
└── plugins/
    ├── README.md                 # How plugin packages are organized
    ├── devcontainer/
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── .plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── devcontainer/
    │           ├── SKILL.md
    │           └── references/
    ├── engineering-workflow/
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── .plugin/
    │   │   └── plugin.json
    │   ├── agents/
    │   │   ├── distiller.agent.md
    │   │   ├── implementer.agent.md
    │   │   └── technical-analyst.agent.md
    │   └── skills/
    │       ├── blind-spot-coverage/
    │       │   └── SKILL.md
    │       ├── orient/
    │       │   └── SKILL.md
    │       ├── realign/
    │       │   └── SKILL.md
    │       ├── scenario-design/
    │       │   └── SKILL.md
    │       ├── scenario-design-workspace/
    │       │   └── SKILL.md
    │       └── technical-debt-audit/
    │           └── SKILL.md
    ├── synouser/
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── .plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── synouser/
    │           └── SKILL.md
    ├── ugacltool/
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── .plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── ugacltool/
    │           └── SKILL.md
    └── aspire/
        ├── .claude-plugin/
        │   └── plugin.json
        ├── .plugin/
        │   └── plugin.json
        └── skills/
            └── aspire-deploy-pipeline/
                ├── SKILL.md
                └── references/
```

## Quick Reference

| Folder            | Purpose                                                     | File type              |
| ----------------- | ----------------------------------------------------------- | ---------------------- |
| `.claude-plugin/` | Canonical marketplace catalog (Claude & Copilot compatible) | `marketplace.json`     |
| `.github/plugin/` | Compatibility copy of marketplace catalog for Copilot users | `marketplace.json`     |
| `plugins/`        | Installable plugins with bundled skills and agents          | `**/*.md`, `**/*.json` |

## Usage

Plugins can be installed from `plugins/<name>/` directly or exposed through the canonical [`/.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) (compatible with both Claude Code and GitHub Copilot CLI). A compatibility copy is maintained at [`.github/plugin/marketplace.json`](.github/plugin/marketplace.json) for Copilot users.
