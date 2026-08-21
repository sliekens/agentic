# Repository Notes

## Agent plugins

Agent Plugins 1.0 is the canonical package format in this repository. Keep portable packages, the Claude Code adapter, and distribution catalogs distinct:

- `plugins/<name>/plugin.json` is the canonical portable manifest for one installable plugin.
- `plugins/<name>/skills/` contains its portable Agent Skills.
- `.claude-plugin/plugin.json` is a generated Claude Code adapter.
- `.github/plugin/marketplace.json` and `.claude-plugin/marketplace.json` are client-specific distribution catalogs for many plugins.

Reference:

- https://docs.github.com/en/copilot/reference/cli-plugin-reference

### Portable `plugin.json`

Use the root manifest for portable identity and metadata:

- `$schema` set to `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`
- `name`
- `description`
- `version`
- `author`
- `license`
- `keywords`

Do not put `skills`, `agents`, `hooks`, `mcpServers`, or other client fields at the top level. Portable skills are discovered from the fixed `skills/` directory. Portable MCP configuration, when present, belongs in root `mcp.json`.

GitHub Copilot CLI and VS Code use this root portable manifest. Do not create `.plugin/plugin.json` OpenPlugin manifests.

### Client compatibility

Claude Code uses a generated `.claude-plugin/plugin.json` compatibility adapter. Treat it as an adapter, not an alternative source of truth.

Codex, GitHub Copilot CLI, and VS Code use the root portable package in this repository. Do not create `.codex-plugin/plugin.json`.

Run `python scripts/sync-plugin-metadata.py` after changing a root portable manifest. Do not bundle duplicate skills in the Claude Code adapter.

### `marketplace.json`

Use each marketplace catalog only for marketplace identity and discovery metadata:

- marketplace `name`
- `owner`
- optional `metadata`
- `plugins[]` entries that point to installable plugin directories

Each `plugins[]` entry should describe how to find a plugin, not redefine the plugin's internal layout. Marketplace catalogs are not portable components of an individual plugin.

### Source path rule

In `.github/plugin/marketplace.json`, use explicit repo-root-relative `source` paths such as `plugins/devcontainer`. Do not add `metadata.pluginRoot` unless there is a concrete reason that outweighs the loss of readability.

### Update rule

When adding or reorganizing a plugin:

1. Update that plugin's `plugin.json`.
2. Run `python scripts/sync-plugin-metadata.py` to regenerate the Claude Code adapter and duplicated catalog metadata.
3. Update the appropriate marketplace catalog only when plugin discovery or distribution policy changes.
4. Keep `plugin.json` operational and marketplace catalogs distribution-oriented.
5. Run `python scripts/validate-agent-plugins.py`.
6. Treat root `plugin.json` as canonical when resolving any mismatch.
