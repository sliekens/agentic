# Plugins

This folder contains installable GitHub Copilot CLI plugins. Each plugin has its own `plugin.json` manifest and can bundle one or more skills, plus any supporting references, agents, hooks, or MCP/LSP configs.

## Structure

```
plugins/
└── <plugin-name>/
    ├── plugin.json
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── references/        # optional
```

## Creating a new plugin

1. Create `plugins/<plugin-name>/plugin.json`.
2. Create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`.
3. Keep the plugin name, skill name, and marketplace entry aligned.
4. Add `references/` only when the root skill needs to stay concise and delegate details.

## Publishing in this repo

If you want the plugin to be installable from this repository's marketplace, add an entry to [`.github/plugin/marketplace.json`](../.github/plugin/marketplace.json).
