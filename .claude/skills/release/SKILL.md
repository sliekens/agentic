---
name: release
description: >
  Prepare a changed Agent Plugin in this repository for release: select the SemVer bump, update canonical metadata and changelog, regenerate adapters and catalogs, and validate the result.
  Use for /release, plugin versioning, preparing to publish, or before committing changes under plugins/, .claude-plugin/, or .github/plugin/. This skill prepares local release state; it does not push, tag, publish, or deploy.
---

# Prepare Plugin Release

Turn already-authorized plugin changes into a complete, validated local release diff. A short prompt such as `/release` is sufficient: infer routine details, preserve the working state, and carry the release preparation through verification. The user retains authority for the feature change, any commit not already requested, and every external release action.

## Authority and release state

- `/release` authorizes release-metadata edits and local synchronization and validation for the affected plugin. It does not authorize feature changes or unrelated cleanup.
- Edit canonical `plugins/<name>/plugin.json`, the plugin README, and a missing minimal catalog entry when required. Use repository generators for generated files; never hand-edit their derived content.
- Preserve all pre-existing and unrelated changes. Never clean, stash, reset, checkout, or revert the worktree to make the release easier.
- Commit only when the user already explicitly requested or accepted a commit for these changes. Never push, tag, create a hosted release, publish to a marketplace or package registry, deploy, change credentials, or contact people under this skill.

Keep a compact release state in the task: target plugin, baseline branch and HEAD, pre-existing changes, current version, classified authored changes, selected bump and rationale, expected release files, validation status, and commit authority. Recheck the worktree and generated-file freshness after resuming.

## 1. Establish scope and baseline

Read the repository instructions. Inspect `git status` and `git diff HEAD`, including the contents of relevant untracked files reported by status. Separate authored plugin changes from prior release metadata, generated output, and unrelated work.

Infer the affected plugin from canonical package paths when it is clear; shared generated catalogs or the root README alone are not enough. Process multiple affected plugins independently when the request plainly covers them and each release decision is unambiguous. Ask only when changes cannot be assigned safely or choosing the release scope would materially change the outcome.

Read the current version from canonical `plugins/<name>/plugin.json`. If matching version, changelog, and generated changes already exist for the current authored work, treat them as partial release state and continue verification; do not bump the same change twice.

## 2. Select the version bump

Classify the underlying authored change, not generator churn or the version line itself.

| Change type                                                | Version bump  |
| ---------------------------------------------------------- | ------------- |
| New skill or agent added                                   | minor (x.Y.0) |
| New feature or meaningful behavioral change                | minor (x.Y.0) |
| Existing content updated (catalog entry, wording, bug fix) | patch (x.y.Z) |
| Breaking change to the plugin's interface or workflow      | major (X.0.0) |

Choose the smallest bump supported by the diff. Decide ordinary patch-versus-minor cases without asking and record the reason. If no breaking signal exists but the distinction remains uncertain, use patch and report the assumption. Stop for a real fork when the evidence plausibly indicates a breaking change or materially different release scopes.

## 3. Update canonical release content

Update `"version"` in `plugins/<name>/plugin.json`. Keep the canonical plugin description and keywords accurate when the authored capability changed, but do not rewrite them merely for a release.

Use `plugins/<name>/README.md` as the release record. If it is absent, create only the minimal structure needed here: plugin title, canonical description, applicable `## Skills` or `## Agents` inventory, and `## Change Log`. Add new skills or agents to their section in alphabetical order:

**For a new skill**: in `## Skills`, add a bullet in alphabetical order:

```
- **{Skill Name}**: {description from SKILL.md frontmatter}
```

**For a new agent**: in `## Agents`, add a bullet in alphabetical order:

```
- **{Agent Name}**: {description from the agent file}
```

Skip the listing update when no skill or agent was added. Insert the new changelog entry immediately after `## Change Log`:

```markdown
### vX.Y.Z

- <one-line description of what changed>
```

Use one bullet per logical change. Describe the user-visible addition or correction, not the file operations.

## 4. Synchronize generated files

Ensure the plugin appears exactly once in both `.github/plugin/marketplace.json` and `.claude-plugin/marketplace.json`, in the same plugin order. For a new plugin, add the minimal `name` and `source` entry only to each catalog where it is missing; do not duplicate an existing entry.

- GitHub source: `plugins/<name>`
- Claude source: `./plugins/<name>`

After the canonical changes, run from the repository root:

```bash
python scripts/sync-plugin-metadata.py
python scripts/sync-readme-structure.py
```

Those commands own these files — do not hand-edit them:

- `plugins/<name>/.claude-plugin/plugin.json`
- `.github/plugin/marketplace.json` (`description` and `source`)
- `.claude-plugin/marketplace.json` (`description` and `source`)
- Root `README.md` structure tree (`<!-- STRUCTURE_START -->` … `<!-- STRUCTURE_END -->`)

These generators operate repository-wide. Do not discard concurrent work in their outputs. If generation would overwrite a change that cannot be reproduced from canonical sources, stop and report the conflict rather than forcing synchronization.

## 5. Verify the release diff

Run:

```bash
python scripts/validate-agent-plugins.py
git diff --check
```

The plugin validator checks stale Claude adapters, catalogs, package containment, basic frontmatter, and the root README marker block. It does not validate the SemVer decision, changelog or inventory accuracy, or authored behavior. Check those manually and run or verify the applicable change-specific checks separately.

Inspect final `git status` and the complete diff, including untracked files. Confirm:

- Version changed in the root portable manifest
- Changelog entry present
- Plugin README Skills/Agents section updated if a skill or agent was added
- Generated adapter, both catalogs, and root README tree updated by the sync scripts
- Applicable change-specific checks and both release checks passed
- Pre-existing and unrelated changes remain intact and are excluded from any commit

Fix failures only when the correction is release-related and within this authority. Stop with the preserved release state when validation exposes an unrelated defect, missing access, or a change that needs broader authority.

## Decision gates and completion

Before escalating, restate the intended release outcome, inspect the current state, try safe in-scope corrections, and identify the smallest unresolved fork. Ask one focused question only when the target or release scope is genuinely ambiguous, a possible breaking change changes the required bump, synchronization would overwrite concurrent work, or completion needs authority not granted above.

The release is complete only when canonical metadata, changelog and listings, generated files, and validation evidence agree on the same version and logical changes. Report only the plugin name, old and new version with bump rationale, changelog summary, checks run, preserved conflicts or blockers, and commit status. Keep routine generator output in the background.

If a commit was already authorized, stage only task-scoped paths, inspect the exact staged diff, commit after all checks pass, and leave unrelated work untouched. When HEAD is detached, report the exact commit identity and detached state without implying branch integration. Otherwise leave the validated release diff uncommitted and report that fact without asking the user to make an optional decision.
