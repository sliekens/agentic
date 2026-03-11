# Repository Notes

## Copilot CLI plugins

When working on GitHub Copilot CLI plugins in this repository, keep the two manifest layers distinct:

- `plugin.json` is the manifest for one installable plugin.
- `.github/plugin/marketplace.json` is the catalog for many plugins published by this repository.

Reference:

- https://docs.github.com/en/copilot/reference/cli-plugin-reference

### `plugin.json`

Use `plugin.json` for per-plugin identity and runtime layout:

- `name`
- `description`
- `version`
- `author`
- `license`
- `keywords`
- component paths such as `skills`, `agents`, `hooks`, and `mcpServers`

Practical rule: `plugin.json` is the source of truth for what a plugin contains and where Copilot CLI should load it from.

### `marketplace.json`

Use `.github/plugin/marketplace.json` for marketplace identity and discovery metadata:

- marketplace `name`
- `owner`
- optional `metadata`
- `plugins[]` entries that point to installable plugin directories

Each `plugins[]` entry should describe how to find a plugin, not redefine the plugin's internal layout.

### Source path rule

Use explicit repo-root-relative `source` paths such as `plugins/devcontainer`. Do not add `metadata.pluginRoot` unless there is a concrete reason that outweighs the loss of readability.

### Update rule

When adding or reorganizing a plugin:

1. Update that plugin's `plugin.json`.
2. Update `.github/plugin/marketplace.json` if the plugin should be discoverable from this repository's marketplace.
3. Keep `plugin.json` operational and `marketplace.json` catalog-oriented.
4. If a marketplace entry duplicates fields such as `description` or `version`, keep those values in sync with the plugin's `plugin.json`.
5. Treat `plugin.json` as canonical when resolving any mismatch.
