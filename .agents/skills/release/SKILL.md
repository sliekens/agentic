---
name: release
description: >
  Release a plugin in this repo — version bump, changelog, generated adapters/catalogs/README tree, validate.
  Use when committing changes under plugins/, .claude-plugin/, or .github/plugin/; when bumping, publishing, or versioning a plugin; or when the user runs /release.
---

# Release Plugin

Publish a new version of a plugin after it has changed. If the user already accepted a commit of this work, still complete this skill, then commit. Do not push.

## Step 1 — Identify the plugin

If the plugin name is not stated, infer it from the changed files. If genuinely ambiguous, ask.

Read the current version from canonical `plugins/<name>/plugin.json`.

## Step 2 — Detect what changed

Check `git status` and `git diff HEAD` for the plugin directory. That determines the version bump and the changelog wording.

| Change type                                                | Version bump  |
| ---------------------------------------------------------- | ------------- |
| New skill or agent added                                   | minor (x.Y.0) |
| New feature or meaningful behavioral change                | minor (x.Y.0) |
| Existing content updated (catalog entry, wording, bug fix) | patch (x.y.Z) |
| Breaking change to the plugin's interface or workflow      | major (X.0.0) |

If it's not clear, default to patch and mention what you assumed.

## Step 3 — If a new skill or agent was added, update the plugin README

Open `plugins/<name>/README.md`.

**For a new skill**: in `## Skills`, add a bullet in alphabetical order:

```
- **{Skill Name}**: {description from SKILL.md frontmatter}
```

**For a new agent**: in `## Agents`, add a bullet in alphabetical order:

```
- **{Agent Name}**: {description from the agent file}
```

Skip if nothing new was added.

## Step 4 — Bump the version

Update `"version"` in `plugins/<name>/plugin.json` only. Do not hand-edit generated files.

## Step 5 — Add the changelog entry

In `plugins/<name>/README.md`, insert immediately after `## Change Log`:

```markdown
### vX.Y.Z

- <one-line description of what changed>
```

One bullet per logical change. Describe what was added or fixed.

## Step 6 — Synchronize generated files

If this plugin is missing from either catalog, append a `plugins[]` entry to **both** `.github/plugin/marketplace.json` and `.claude-plugin/marketplace.json` with `name` and `source` only. Keep the same plugin order in both files.

- GitHub source: `plugins/<name>`
- Claude source: `./plugins/<name>`

Then from the repo root, after the version bump:

```bash
python scripts/sync-plugin-metadata.py
python scripts/sync-readme-structure.py
```

Those commands own these files — do not hand-edit them:

- `plugins/<name>/.claude-plugin/plugin.json`
- `.github/plugin/marketplace.json` (`description` and `source`)
- `.claude-plugin/marketplace.json` (`description` and `source`)
- Root `README.md` structure tree (`<!-- STRUCTURE_START -->` … `<!-- STRUCTURE_END -->`)

Done when both commands have run against the bumped manifest.

## Step 7 — Verify and report

Run `python scripts/validate-agent-plugins.py` and stop if it fails. That check includes stale Claude adapters, catalogs, and the root README tree.

Confirm in `git diff`:

- Version changed in the root portable manifest
- Changelog entry present
- Plugin README Skills/Agents section updated if a skill or agent was added
- Generated adapter, both catalogs, and root README tree updated by the sync scripts

Tell the user the new version number and the one-line changelog summary. If they already accepted a commit of this work, commit. Otherwise ask if they want to commit.
