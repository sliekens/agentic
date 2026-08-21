# Agent Plugins 1.0 Migration

## Decision

Agent Plugins 1.0 is the canonical package format. Each plugin uses root `plugin.json`, immediate-child skills under `skills/`, and root `mcp.json` when MCP configuration is present.

Codex, GitHub Copilot CLI, and VS Code consume the portable package directly. Only Claude Code retains a generated manifest because its installation flow requires a client-specific location. Marketplace catalogs remain distribution metadata outside individual plugin packages.

## Source format and target clients

The repository previously stored identical OpenPlugin metadata in `.plugin/plugin.json` and `.claude-plugin/plugin.json`. Its skills already used the portable `skills/<name>/SKILL.md` layout. Two identical marketplace catalogs served GitHub Copilot and Claude Code.

The migrated packages target:

- Agent Plugins 1.0 conforming clients through root `plugin.json`.
- Codex through the portable root package, as verified by the repository's installed use.
- GitHub Copilot CLI and VS Code through the portable root package.
- Claude Code through generated `.claude-plugin/plugin.json` adapters and its repository catalog.

## Artifact mapping

| Original artifact | Classification and outcome |
| --- | --- |
| `plugins/aspire/.plugin/plugin.json` | Removed legacy OpenPlugin manifest; replaced by portable `plugins/aspire/plugin.json`. |
| `plugins/devcontainer/.plugin/plugin.json` | Removed legacy OpenPlugin manifest; replaced by portable `plugins/devcontainer/plugin.json`. |
| `plugins/engineering-workflow/.plugin/plugin.json` | Removed legacy OpenPlugin manifest; replaced by portable `plugins/engineering-workflow/plugin.json`. |
| `plugins/synouser/.plugin/plugin.json` | Removed legacy OpenPlugin manifest; replaced by portable `plugins/synouser/plugin.json`. |
| `plugins/technical-writing/.plugin/plugin.json` | Removed legacy OpenPlugin manifest; replaced by portable `plugins/technical-writing/plugin.json`. |
| `plugins/ugacltool/.plugin/plugin.json` | Removed legacy OpenPlugin manifest; replaced by portable `plugins/ugacltool/plugin.json`. |
| Each `plugins/*/.claude-plugin/plugin.json` | Retained as a generated Claude Code compatibility adapter. Metadata comes from the matching root portable manifest. |
| Each `plugins/*/.codex-plugin/plugin.json` created during the initial migration | Removed as redundant. Codex already consumes the portable root package in this repository. |
| Each `plugins/*/skills/<name>/SKILL.md` | Retained as portable core. The 19 skill directories are immediate children of their package's `skills/` directory. |
| `plugins/*/skills/*/references/`, `evals/`, `LICENSE`, and `UPSTREAM.md` | Retained as skill-relative supporting resources. They are package content, not additional portable component types. |
| `plugins/engineering-workflow/skills/analyze-complexity/agents/openai.yaml` | Retained as Codex UI metadata for one skill. It is not presented as an Agent Plugins component. |
| `.github/plugin/marketplace.json` | Retained as GitHub Copilot distribution metadata. Source paths are repository-root-relative. |
| `.claude-plugin/marketplace.json` | Retained as Claude Code distribution metadata. It is no longer described as canonical plugin metadata. |
| `.agents/skills/release/SKILL.md` | Updated repository tooling to version root portable manifests and regenerate the Claude Code adapter. |
| `.claude/skills/release/SKILL.md` | Updated Claude Code compatibility copy of the repository release workflow. |
| `agents/workbench-color-agent.md` | Retained unchanged as a repository customization outside the installable plugin packages. |

No plugin contained MCP servers, hooks, plugin-level custom agents, commands, LSP servers, authentication declarations, executable scripts, secrets, or UI assets that required migration into a portable component or another adapter.

## Generated and intentionally omitted files

`scripts/sync-plugin-metadata.py` generates each Claude Code adapter and duplicated marketplace descriptions from the root portable manifests. The GitHub and Claude catalogs remain separate files because they belong to different distribution systems.

Added files are the six root portable manifests, the metadata synchronization script, the repository validator, and this report. The six Claude Code adapters and both marketplace catalogs remain in their existing locations. No package content moved outside its plugin root.

The migration intentionally omits:

- `.plugin/plugin.json` compatibility copies, because no target client in this repository requires them.
- `.codex-plugin/plugin.json` compatibility copies, because installed Codex use verifies that the portable root packages work without them.
- Client fields in root `plugin.json`, because the Agent Plugins 1.0 schema is closed.
- A client extension namespace, because no target client documents a namespace needed by these skills-only packages.
- Root `mcp.json`, because none of the packages contains an MCP server.
- Marketplace metadata inside plugin packages.

## Validation and smoke tests

Run from the repository root:

```text
python scripts/sync-plugin-metadata.py --check
python scripts/validate-agent-plugins.py
```

Results on 2026-08-22:

- Metadata synchronization check passed.
- Repository validation passed for 6 portable packages and 19 independently discoverable skills.
- Package containment, generated Claude adapter equality, marketplace synchronization, removal of all six obsolete OpenPlugin manifests, and absence of `.codex-plugin` adapters passed.
- `claude plugin validate` passed for all 6 Claude Code adapters and the Claude marketplace catalog.
- `claude --plugin-dir <path> plugin details <name>` loaded all 6 packages and discovered the expected 19 skills, with no hooks, plugin-level agents, MCP servers, or LSP servers.
- Codex exposes installation and marketplace commands but no non-mutating plugin validation command. The repository's installed Codex use is the behavior evidence for loading the portable packages without `.codex-plugin` adapters.
- GitHub Copilot CLI smoke validation could not run because the local WinGet executable link is not launchable in this execution context. Root manifests and the GitHub marketplace were validated statically against the repository's portable-format rules.

## Remaining client-specific risks

- Claude Code still depends on its adapter location. Re-run the metadata generator after every portable metadata change.
- A release should smoke-test installation in each available client. Static validation does not prove marketplace installation, UI rendering, or skill activation.
- Official OpenAI documentation still shows a `.codex-plugin/plugin.json` layout. This repository intentionally follows its verified installed behavior instead. Reassess if Codex plugin discovery changes.
