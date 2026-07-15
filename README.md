# Agentic

My personal collection of GitHub Copilot customizations — prompts, instructions, agents, and installable plugins — tailored to my specific workflows and preferences.

> Inspired by [github/awesome-copilot](https://github.com/github/awesome-copilot).

## Structure

<!-- STRUCTURE_START -->
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
    ├── devcontainer/
    │   ├── .plugin/
    │   │   └── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── devcontainer/
    │           ├── SKILL.md
    │           └── references/
    │               ├── checklists.md
    │               ├── cli.md
    │               ├── configuration.md
    │               ├── decision-trees.md
    │               ├── features.md
    │               ├── persistence.md
    │               └── troubleshooting.md
    ├── engineering-workflow/
    │   ├── README.md                 # How plugin packages are organized
    │   ├── .plugin/
    │   │   └── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       ├── blind-spot-coverage/
    │       │   └── SKILL.md
    │       ├── cause-effect-graphing/
    │       │   └── SKILL.md
    │       ├── combinatorial-testing/
    │       │   └── SKILL.md
    │       ├── decision-tables/
    │       │   └── SKILL.md
    │       ├── design-space-exploration/
    │       │   └── SKILL.md
    │       ├── equivalence-partitioning-bva/
    │       │   └── SKILL.md
    │       ├── fmea/
    │       │   └── SKILL.md
    │       ├── operator-setup/
    │       │   └── SKILL.md
    │       ├── realign/
    │       │   └── SKILL.md
    │       ├── scenario-analysis/
    │       │   └── SKILL.md
    │       ├── scenario-design/
    │       │   └── SKILL.md
    │       ├── state-transition-testing/
    │       │   └── SKILL.md
    │       └── technical-debt-audit/
    │           └── SKILL.md
    ├── synouser/
    │   ├── .plugin/
    │   │   └── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── synouser/
    │           └── SKILL.md
    ├── ugacltool/
    │   ├── .plugin/
    │   │   └── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── ugacltool/
    │           └── SKILL.md
    └── aspire/
        ├── .plugin/
        │   └── plugin.json
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── aspire-deploy-pipeline/
                ├── SKILL.md
                └── references/
                    ├── adding-steps.md
                    ├── gotchas.md
                    ├── multi-step-factory.md
                    ├── ordering-steps.md
                    ├── parameters-and-config.md
                    ├── pipeline-services.md
                    ├── tagging-steps.md
                    └── well-known-steps.md
```
<!-- STRUCTURE_END -->

## Quick Reference

| Folder            | Purpose                                                     | File type              |
| ----------------- | ----------------------------------------------------------- | ---------------------- |
| `.claude-plugin/` | Canonical marketplace catalog (Claude & Copilot compatible) | `marketplace.json`     |
| `.github/plugin/` | Compatibility copy of marketplace catalog for Copilot users | `marketplace.json`     |
| `plugins/`        | Installable plugins with bundled skills and agents          | `**/*.md`, `**/*.json` |

## Usage

Plugins can be installed from `plugins/<name>/` directly or exposed through the canonical [`/.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) (compatible with both Claude Code and GitHub Copilot CLI). A compatibility copy is maintained at [`.github/plugin/marketplace.json`](.github/plugin/marketplace.json) for Copilot users.
