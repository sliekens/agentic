# Work result

A skill that `work-once` runs returns this record and stops. The record is the only handoff that survives the process. The next wake starts with an empty conversation and reads the issue.

This file is the return protocol. It is not a catalog primitive.

## Fields

| Field | Meaning |
| --- | --- |
| `stop_reason` | Why this run stopped. A short token, specific to the skill. |
| `issue_id` | The issue this run used. `none` when there is no issue. |
| `next_skill` | One skill name, or `none`. A request. The caller decides whether a later wake runs it. |

`next_skill` is one name. A list is not a result. The skill that produced the name does not load it in tick mode.

## Tick mode

The caller is `work-once`, or the user asked for one issue and no continuation.

- Do the skill's own job for that issue.
- At a handoff, put that skill in `next_skill` and stop. Do not load it.
- A step that waits on the user returns `needs-user` and `next_skill: none`. The issue is marked blocked with the tracker's blocked convention.
- A skill used for a judgment stays inside the run. It is not `next_skill`. That includes `analyze-complexity`, `blind-spot-coverage`, `product-map`, and `design-space-exploration`.

## Backlog mode

A person ran the skill and asked it to continue. The skill follows its own "continue under" lines. It does not write a cursor while it still has work to do in this sitting.

## Who writes the cursor

The finisher writes the cursor once, at the exit.

- When `work-once` started the run, it is the finisher. The skill it ran does not write the cursor.
- When the user started the skill and that skill is now exiting, that skill is the finisher.

Write only when `issue_id` is an issue. A `next_skill` with no issue is not stored. The printed line dies with the process.

Read `Cursor` in the workspace issue-tracker record (`ISSUE_TRACKER.md` by default).

1. Set `next_skill` with that section's **Set** operation. Remove the cursor when the value is `none`.
2. Comment with **Comment**. The comment is these three lines, then one sentence. No log body, stack trace, or trace payload.

```
work-once:
stop_reason: <token>
next_skill: <skill|none>
```

3. When `stop_reason` is `needs-user`, mark the issue blocked.
4. Do not mark the issue blocked for `awaiting-merge` or `awaiting-release`.

## Resume

The next `work-once` searches with **Find**. It runs the stored skill when the issue is open, has `next_skill` set, is not blocked, and has no open pull request of its own.

A pull request that waits on a merge stores `next_skill` as the skill that was in progress. The open pull request keeps the next wake off that issue. When the pull request merges, the stored skill runs again.

A checkpoint that waits on production evidence stores `next_skill: none` and `stop_reason: awaiting-release`. When the evidence is later written on the issue, that session sets `next_skill` to the skill that stopped, using **Set**, so the next wake resumes it.

`filed` and `duplicate` store `next_skill: none`. The next wake takes the oldest actionable issue. Filing does not jump the queue.
