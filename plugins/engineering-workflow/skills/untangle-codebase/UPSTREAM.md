# Upstream source

- Repository: https://github.com/caldoai/skills
- Source: https://github.com/caldoai/skills/tree/f3cf47774975a7d9fca45730babf4ff7ad765ada/skills/untangle-codebase
- Revision: `f3cf47774975a7d9fca45730babf4ff7ad765ada`
- License: [MIT](LICENSE), Copyright (c) 2026 Maze, copied from the upstream repository

## Vendored files

| File | Upstream path | Source blob |
| --- | --- | --- |
| `SKILL.md` | `skills/untangle-codebase/SKILL.md` | `102ff57803e504876f6eb9b412e4eb0f6c576350` |
| `LICENSE` | `LICENSE` | `0f255b7e8b17e994384d1b981fc1a2d4a27d7bde` |

## Local modifications

Applied to `SKILL.md`:

- Extended the `description` with when to use the skill and a handoff to each
  neighboring engineering-workflow skill: `technical-debt-audit`,
  `analyze-complexity`, `realign`, `fix-loop`, and `yak-shave`.
- Added a `license` frontmatter field that points to `LICENSE` and this file.
- Added a "Relationship to adjacent skills" section at the end.
- Fixed the typo "a workaround om the codebase" to "a workaround in the codebase".

No step, rule, or example was changed. Re-apply these edits when refreshing
from upstream.

## Refreshing

Compare the blob hashes above against the upstream paths. When they differ,
copy the new files and re-apply the local modifications listed above.
