# Plugins

This folder contains portable Agent Plugins 1.0 packages. Each package has a canonical root `plugin.json` and one or more Agent Skills. Codex, GitHub Copilot CLI, and VS Code use the portable package directly. A generated Claude Code manifest adapts the package for that client's required manifest location.

## Structure

```
plugins/
└── <plugin-name>/
    ├── plugin.json                # canonical Agent Plugins 1.0 manifest
    ├── .claude-plugin/
    │   └── plugin.json            # generated Claude Code adapter
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── references/        # optional
```

## Creating a new plugin

1. Create `plugins/<plugin-name>/plugin.json` with the Agent Plugins 1.0 schema.
2. Add each skill at `skills/<skill-name>/SKILL.md`.
3. Add root `mcp.json` only when the package includes a portable MCP server configuration.
4. Follow the `release` skill so both marketplace catalogs get an entry, generated files are synchronized, and validation runs.

Do not create `.plugin/plugin.json` or `.codex-plugin/plugin.json`. Hooks, custom agents, commands, LSP servers, UI resources, and marketplace entries are not portable Agent Plugins 1.0 components.

## Publishing in this repo

If you want the plugin to be installable from this repository's marketplaces, follow the `release` skill. It adds the catalog entries and fills duplicated metadata from root `plugin.json`.

The GitHub and Claude marketplace catalogs are distribution metadata outside the individual plugin packages. Root `plugin.json` remains canonical for duplicated name, description, and version metadata.
