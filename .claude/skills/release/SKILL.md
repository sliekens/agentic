---
name: release
description: Release a new version of a plugin in this repo. Bumps the canonical portable manifest, writes the changelog entry, updates the plugin README when needed, regenerates the Claude adapter and catalogs, and validates the packages. Invoke with /release or when the user asks to bump, publish, or version a plugin.
---

# Release Plugin

Publish a new version of a plugin after changes have been made to it.

## Step 1 — Identify the plugin

If the plugin name is not stated, infer it from context (the last file edited, the last skill or agent mentioned). If genuinely ambiguous, ask.

Read the current version from canonical `plugins/<name>/plugin.json`.

## Step 2 — Detect what changed

Check `git status` and `git diff HEAD` for the plugin directory to understand what was modified. This determines both the version bump type and the changelog wording.

Classify the change:

| Change type | Version bump |
|---|---|
| New skill or agent added | minor (x.Y.0) |
| New feature or meaningful behavioral change | minor (x.Y.0) |
| Existing content updated (catalog entry, wording, bug fix) | patch (x.y.Z) |
| Breaking change to the plugin's interface or workflow | major (X.0.0) |

If it's not clear, default to patch and mention what you assumed.

## Step 3 — If a new skill or agent was added, update the README

Open `plugins/<name>/README.md`.

**For a new skill**: find the `## Skills` section and add a bullet in alphabetical order:
```
- **{Skill Name}**: {description from SKILL.md frontmatter}
```

**For a new agent**: find the `## Agents` section and add a bullet in alphabetical order:
```
- **{Agent Name}**: {description from the agent file}
```

Skip this step if nothing new was added — an existing skill or agent updated in place does not get a new bullet.

## Step 4 — Bump the version

Update the `"version"` field in `plugins/<name>/plugin.json`. Do not edit the generated Claude Code adapter directly.

## Step 5 — Add the changelog entry

In `plugins/<name>/README.md`, insert a new section immediately after `## Change Log`:

```markdown
### vX.Y.Z

- <one-line description of what changed>
```

One bullet per logical change. Describe what was added or fixed, not the steps taken to do it.

## Step 6 — Run the sync scripts

```bash
python3 scripts/sync-plugin-metadata.py
python3 scripts/sync-readme-structure.py
```

Run from the repo root. The first command regenerates the Claude Code adapter plus duplicated marketplace fields from the portable manifest. The second updates the directory tree in the top-level `README.md`.

## Step 7 — Verify and report

Run `git diff` and confirm:
- Version changed in the root portable manifest and synchronized Claude adapter
- Changelog entry present
- README Skills/Agents section updated if applicable
- Root README structure updated

Run `python3 scripts/validate-agent-plugins.py` and stop if it fails.

Tell the user the new version number and the one-line changelog summary. Ask if they want to commit.
