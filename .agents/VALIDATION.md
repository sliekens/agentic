# VALIDATION.md

Which checks prove a change works depends on the change. Run every entry whose trigger matches the change. Entries record reusable checks, not the steps run for one change.

## Integration

- **Mode:** direct push
- **Target branch:** `main`
- **Merge:** none
- **CI:** none. The repository has no workflow files, so nothing runs after a push. Run every check locally before the push.

## Every change (completion gate)

- **Trigger:** any change
- **Run:** `python scripts/validate-agent-plugins.py`, then `git diff --check`
- **Passes when:** the validator exits 0 and prints "Validated ... Agent Plugins v1 packages", and `git diff --check` prints nothing
- **Pitfalls:** the validator checks structure only (manifests, adapters, catalogs, frontmatter, README markers). It does not check skill behavior, SemVer choice, or changelog accuracy

## Plugin package, adapter, or catalog

- **Trigger:** changes under `plugins/`, `.claude-plugin/`, or `.github/plugin/`
- **Run:** follow the `release` skill (`.agents/skills/release/SKILL.md`). It runs `python scripts/sync-plugin-metadata.py` and `python scripts/sync-readme-structure.py`, then the completion gate
- **Passes when:** `python scripts/sync-plugin-metadata.py --check` and `python scripts/sync-readme-structure.py --check` exit 0, the version changed in `plugins/<name>/plugin.json`, and the plugin README has a matching change log entry
- **Pitfalls:** never hand-edit generated files (`plugins/<name>/.claude-plugin/plugin.json`, catalog `description` and `source`, the README structure tree). The sync scripts run repository-wide

## Skill or agent content

- **Trigger:** changes to `plugins/*/skills/**` or `agents/`
- **Run:** the completion gate, then read the skill's `SKILL.md` against its own frontmatter description. When behavior changed, invoke the skill once in a session
- **Passes when:** the validator accepts the frontmatter and the skill behaves as its description says in the session
- **Pitfalls:** the validator passes on any non-empty description, so it cannot catch wrong instructions. An installed plugin cache (`~/.claude/plugins/cache/`) holds the released copy, not the working tree

## Validation scripts

- **Trigger:** changes to `scripts/*.py`
- **Run:** `python scripts/validate-agent-plugins.py`, `python scripts/sync-plugin-metadata.py --check`, `python scripts/sync-readme-structure.py --check`
- **Passes when:** all three exit 0 on the unchanged tree, and a deliberately stale adapter or catalog makes the matching script fail
- **Pitfalls:** no tests exist for the scripts, so a script that always passes looks the same as a working one

## Known gaps

- No CI runs the validation scripts, so a push that skips them is not caught
- No tests cover `scripts/*.py`
- No automated check covers skill behavior or SemVer and changelog accuracy
