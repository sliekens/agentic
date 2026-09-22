# Agentic

My personal collection of portable Agent Plugins, skills, and client-specific agent customizations.

> Inspired by [github/awesome-copilot](https://github.com/github/awesome-copilot).

## Structure

<!-- STRUCTURE_START -->
```
agentic/
├── AGENTS.md                    # Repo-specific rules for future Codex/Copilot work
├── .claude-plugin/
│   └── marketplace.json          # Claude Code distribution catalog
├── .github/
│   ├── copilot-instructions.md   # Global Copilot instructions for this repo
│   └── plugin/
│       └── marketplace.json      # GitHub Copilot distribution catalog
└── plugins/
    ├── devcontainer/
    │   ├── plugin.json
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
    │   ├── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       ├── analyze-complexity/
    │       │   └── SKILL.md
    │       ├── blind-spot-coverage/
    │       │   └── SKILL.md
    │       ├── cause-effect-graphing/
    │       │   └── SKILL.md
    │       ├── combinatorial-testing/
    │       │   └── SKILL.md
    │       ├── compound/
    │       │   └── SKILL.md
    │       ├── cross-check/
    │       │   └── SKILL.md
    │       ├── decision-tables/
    │       │   └── SKILL.md
    │       ├── design-space-exploration/
    │       │   └── SKILL.md
    │       ├── equivalence-partitioning-bva/
    │       │   └── SKILL.md
    │       ├── flaky-build-investigation/
    │       │   └── SKILL.md
    │       ├── fmea/
    │       │   └── SKILL.md
    │       ├── operator-setup/
    │       │   └── SKILL.md
    │       ├── product-map/
    │       │   ├── SKILL.md
    │       │   └── references/
    │       │       ├── inventory.md
    │       │       ├── journeys.md
    │       │       ├── matrix.md
    │       │       ├── tree.md
    │       │       └── visual-chart.md
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
    │   ├── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── synouser/
    │           └── SKILL.md
    ├── ugacltool/
    │   ├── README.md
    │   ├── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── ugacltool/
    │           └── SKILL.md
    ├── aspire/
    │   ├── plugin.json
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── aspire-deploy-pipeline/
    │           ├── SKILL.md
    │           └── references/
    │               ├── adding-steps.md
    │               ├── gotchas.md
    │               ├── multi-step-factory.md
    │               ├── ordering-steps.md
    │               ├── parameters-and-config.md
    │               ├── pipeline-services.md
    │               ├── tagging-steps.md
    │               └── well-known-steps.md
    └── technical-writing/
        ├── README.md
        ├── plugin.json
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── ste-writing/
                ├── SKILL.md
                ├── LICENSE
                └── UPSTREAM.md
```
<!-- STRUCTURE_END -->

## Quick Reference

| Folder            | Purpose                                                 | File type              |
| ----------------- | ------------------------------------------------------- | ---------------------- |
| `.claude-plugin/` | Claude Code distribution catalog                       | `marketplace.json`     |
| `.github/plugin/` | GitHub Copilot distribution catalog                    | `marketplace.json`     |
| `plugins/`        | Portable Agent Plugins with a generated Claude adapter | `**/*.md`, `**/*.json` |

## Usage

Each `plugins/<name>/` directory is a portable Agent Plugins 1.0 package. Codex, GitHub Copilot CLI, and VS Code consume its root `plugin.json`. Only Claude Code uses a generated `.claude-plugin/plugin.json` compatibility adapter.

The [GitHub Copilot catalog](.github/plugin/marketplace.json) and [Claude Code catalog](.claude-plugin/marketplace.json) are separate distribution metadata. Follow the `release` skill before committing plugin, catalog, or adapter changes — it regenerates those files and the README tree, then validates.
