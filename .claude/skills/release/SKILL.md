---
name: release
description: Release a new version of a plugin in this repo. Handles the full release workflow — bumps both plugin.json files, writes the changelog entry, updates the Skills or Agents section of the plugin README when something new was added, and runs the sync scripts. Invoke with /release or whenever the user says "bump version", "release plugin", "add changelog", "run sync", or asks to publish or version a plugin after making any kind of change.
---

# Release Plugin

Publish a new version of a plugin after changes have been made to it.

## Step 1 — Identify the plugin

If the plugin name is not stated, infer it from context (the last file edited, the last skill or agent mentioned). If genuinely ambiguous, ask.

Read the current version from `plugins/<name>/.plugin/plugin.json`.

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

Update the `"version"` field in both:
- `plugins/<name>/.plugin/plugin.json`
- `plugins/<name>/.claude-plugin/plugin.json`

Both must match. If only one exists, update whichever is present.

## Step 5 — Add the changelog entry

In `plugins/<name>/README.md`, insert a new section immediately after `## Change Log`:

```markdown
### vX.Y.Z

- <one-line description of what changed>
```

One bullet per logical change. Describe what was added or fixed, not the steps taken to do it.

## Step 6 — Run the sync script

```bash
python3 scripts/sync-readme-structure.py
```

Run from the repo root. This updates the directory tree in the top-level `README.md`.

## Step 7 — Verify and report

Run `git diff` and confirm:
- Version bumped consistently in both plugin.json files
- Changelog entry present
- README Skills/Agents section updated if applicable
- Root README structure updated

Tell the user the new version number and the one-line changelog summary. Ask if they want to commit.
