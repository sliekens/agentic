# Upstream source

- Repository: https://github.com/woosal1337/blog
- Source: https://github.com/woosal1337/blog/tree/13c4143f778f7a7dc14299b7ddaec148e3a7f82e/videos/ep01-the-cure-for-ai-slop/asd-ste100
- Revision: `13c4143f778f7a7dc14299b7ddaec148e3a7f82e`
- Upstream skill version: 2.0.3 (ASD-STE100 Issue 9, January 2025)
- License: [MIT](LICENSE), copied from the upstream repository

ASD-STE100 is a registered EU trademark (No. 017966390) of ASD. This skill is
unofficial and not affiliated with ASD. The MIT license covers the upstream
project's own text, not the ASD-STE100 specification, which is available from
https://asd-ste100.org under ASD's own terms.

## Vendored files

| File | Upstream path | Source blob |
| --- | --- | --- |
| `SKILL.md` | `asd-ste100/SKILL.md` | `6b5bb66be1f3864fe065b0dc0084bcc2d4d32ab7` |
| `LICENSE` | `asd-ste100/LICENSE` | `60d713bb54d4aa23c92d86825cb60c321910e552` |
| `references/ste-recurring-errors.md` | `asd-ste100/references/ste-recurring-errors.md` | `9c4c9a7dbcd4477210a6698e82cd527beeddd9d0` |

## Local modifications

This package vendors the instructions only. Upstream also ships a Python
linter, a Node wrapper, Claude Code hooks, an installer, and an output style.
Those are deliberately not vendored, so the skill stays portable and needs no
runtime beyond the agent.

Applied to `SKILL.md`:

- Renamed the skill from `asd-ste100` to `ste-writing`, to keep the name this
  repository already uses and to satisfy the rule that a skill's frontmatter
  name matches its directory.
- Removed `metadata.replaces`, which named an upstream-only skill.
- Removed the "Lint before you send" section, the `ste-lint.py` command block,
  the post-send gate instructions, and the score-versus-shape note. All four
  depend on tooling this package does not ship.
- Promoted the manual checklist to the primary verification step, and dropped
  its "if you cannot run commands" qualifier, which is now the only path.
- Removed the note about a retired upstream `i-have-adhd` skill, which never
  existed here.

No rule, scope table, example, or guard was changed. Re-apply these edits when
refreshing from upstream.

## Refreshing

Compare the blob hashes above against the upstream paths. When they differ,
copy the new files and re-apply the local modifications listed above.
