---
name: add-marketplace-skill
description: Add a new skill to a marketplace plugin. Updates READMEs, bumps versions, and syncs directory structure. Invoke with /add-marketplace-skill or describe adding a new skill.
---

# Add Marketplace Skill

Automates the workflow for adding a new skill to any plugin in the `plugins/` directory and keeping all documentation and versioning in sync.

## When to invoke

Invoke this skill when the user has added a new skill directory to any plugin under `plugins/<plugin-name>/skills/` and needs to:
- Add the skill to the plugin's README
- Bump the plugin version
- Update the root README structure
- Ensure all plugin.json files are in sync

The user can trigger this with `/add-marketplace-skill` or by describing that they added a new skill to a plugin.

## Input

The skill path in the format `<plugin-name>/<skill-name>` or `<plugin-name>/skills/<skill-name>`. 

If not provided, prompt the user for:
1. The plugin name (directory under `plugins/`)
2. The skill name (directory under `plugins/<plugin-name>/skills/`)

Alternatively, if the user has only one plugin with untracked skill directories, auto-detect it.

## Steps

### 1. Detect or prompt for plugin and skill

**If skill path provided:** Parse `<plugin-name>/<skill-name>` or `<plugin-name>/skills/<skill-name>`

**If not provided:**
- List all plugins under `plugins/` that have a `skills/` directory
- For each, list untracked skill directories
- If exactly one plugin has untracked skills, use that plugin and first untracked skill
- Otherwise, prompt the user to select

### 2. Validate the skill exists

Check that `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` exists. If not, error and ask the user to create it first.

### 3. Read the skill's SKILL.md

Extract the name and description from the frontmatter to use in documentation.

### 4. Update plugin README

If `plugins/<plugin-name>/README.md` exists:

- **Skills/Agents section**: Find the section listing skills or agents and add a new bullet point in alphabetical order
  Format: `- **{Skill Name}**: {description from frontmatter}`
  
- **Change Log section**: Add a new version entry or append to the latest unreleased version
  - Check the current version in `plugins/<plugin-name>/.plugin/plugin.json`
  - If the latest changelog version matches the current plugin version, append to it
  - Otherwise, create a new version entry (incrementing the minor version: 1.X.0 → 1.(X+1).0)
  - Format: `- Added the {Skill Name} skill for {purpose}`

If the plugin has no README.md with a Skills section, skip the README update but still bump the version.

### 5. Bump plugin versions

Increment the minor version in:
- `plugins/<plugin-name>/.plugin/plugin.json`
- `plugins/<plugin-name>/.claude-plugin/plugin.json`

If the current version is `A.B.C`, the new version should be `A.(B+1).0`.

If a plugin.json file doesn't exist in one of the locations, only update the ones that do exist.

### 6. Sync root README

Run the sync script: `python3 scripts/sync-readme-structure.py` from the repo root.

This updates the directory tree in the root README.md automatically.

### 7. Verify changes

Review all changes with `git diff` and `git status` to ensure:
- The skill appears in the plugin README (if applicable)
- The version was bumped consistently in all plugin.json files
- The root README structure is updated
- No unintended files were modified

### 8. Report completion

Tell the user what was changed and ask if they want to commit the changes.

## Output format

When complete, provide a summary:

```
## Changes Made for {Plugin Name} - {Skill Name}

### Files Modified:
- plugins/{plugin-name}/README.md (added skill description and changelog)
- plugins/{plugin-name}/.plugin/plugin.json (version {old} → {new})
- plugins/{plugin-name}/.claude-plugin/plugin.json (version {old} → {new})
- README.md (structure synced)

### Files Added:
- plugins/{plugin-name}/skills/{skill-name}/SKILL.md

Version bumped: {old_version} → {new_version}
```

If README wasn't updated (no Skills section):
```
## Changes Made for {Plugin Name} - {Skill Name}

### Files Modified:
- plugins/{plugin-name}/.plugin/plugin.json (version {old} → {new})
- plugins/{plugin-name}/.claude-plugin/plugin.json (version {old} → {new})
- README.md (structure synced)

### Files Added:
- plugins/{plugin-name}/skills/{skill-name}/SKILL.md

Version bumped: {old_version} → {new_version}
```

## Notes

- Always prefer alphabetical ordering when adding to lists
- Use the description from the skill's frontmatter for consistency
- The version bump should always be a minor version increment (X.Y.Z → X.(Y+1).0)
- If there are other untracked skill directories in the same plugin, offer to process them all
- Do not commit changes automatically; let the user review first
- Handle both `.plugin/` and `.claude-plugin/` directory structures gracefully
- Some plugins may only have one or the other; only update what exists
