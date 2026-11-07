---
name: bug-report
description: File one reported defect as an issue in the workspace issue tracker, with expected behavior, actual behavior, a repro or an explicit `none`, and evidence as identifiers rather than log or trace payloads. Use when the user reports a bug, says something is broken, or asks to file or write a bug report, and that defect is not already an issue. Search open issues first and stop when one states the same actual behavior. Stop when the new issue exists. Do not fix it (`fix-loop`). When the issue-tracker record is missing, stop and use `workspace-setup`. When `work-once` is the caller, return the stop record and do not write the cursor. Do not use for a structural-debt inventory with no failing behavior (`technical-debt-audit`), or to diagnose an intermittent build (`flaky-build-investigation`).
---

# Bug Report

File one reported defect as an issue, then stop. The issue is input for
`fix-loop`. This skill does not confirm the defect against the code and does
not change the code.

## Authority boundary

- `/bug-report`, or a request to file a bug, authorizes reading the
  issue-tracker record, searching open issues, and creating one issue.
- It does not authorize a fix, a commit, a close, or an edit to any other
  issue. The fix is `fix-loop`.
- It does not authorize pasting logs, stack traces, or trace payloads into
  the issue. Evidence is an identifier.
- It does not authorize choosing a tracker. A missing record stops the run
  for `workspace-setup`.

## Draft

Keep this in the task, not in a repository file. Steps read these fields and
do not invent replacements.

| Field | Initial | Writes it | Reads it |
| --- | --- | --- | --- |
| `tracker_path` | empty | step 1 | steps 2 and 5 |
| `search_op` | empty | step 1 | step 2 |
| `create_op` | empty | step 1 | step 5 |
| `duplicate_id` | empty | step 2 | stop |
| `expected` | empty | step 3 | steps 4 and 5 |
| `actual` | empty | step 3 | steps 4 and 5 |
| `repro` | `none` | step 3 | steps 4 and 5 |
| `evidence` | empty list | step 3 | steps 4 and 5 |
| `body` | empty | step 4 | step 5 |
| `issue_id` | empty | step 5 | stop |
| `stop_reason` | empty | the ending step | the report |
| `next_skill` | `none` | the ending step | the report |

`tracker_path` is an identifier. A wait on step 3 invalidates `create_op`
until step 5 re-reads the record.
`expected`, `actual`, and `repro` are procedure facts taken from the user.
`issue_id` and `duplicate_id` are identifiers returned by the tracker.

## Issue shape

The create call sends a title and a body. The title is one line taken from
`actual`, with no stack frame and no log line. The body is:

```markdown
## Expected

<sentence, or the field is missing and step 3 must ask>

## Actual

<sentence>

## Repro

<steps, or `none`>

## Evidence

- <kind>: <identifier>
```

`kind` is one of `query`, `time-range`, `trace-id`, `path`, `commit`, `url`.
Zero evidence items is allowed. Write `none` under the heading in that case.

Each of `expected`, `actual`, and `repro` is at most 12 lines. An evidence
item is one line. There is no field for a payload.

Material claims are the expected sentence, the actual sentence, and any
sentence that says why the defect happens. Each one ends with a source mark
`(user)` or `(<evidence kind>:<identifier>)`. A sentence with no source is
dropped. `actual` is the authority for the title when the title and `actual`
disagree.

A schema pass means the body matches this shape. It does not mean the defect
is real. `fix-loop` confirms that.

## 1. Read the tracker record

Read `ISSUE_TRACKER.md` from the workspace's agent-doc folder. Take
`search_op` from **List and search** and `create_op` from **Create**. Store
the path.

Failure edge: the file is missing or those two operations are still
placeholders. Set `stop_reason` to `tracker-missing` and stop. The next owner
is `workspace-setup`. Do not guess a host or a command.

Done when `tracker_path`, `search_op`, and `create_op` are set from the file
as it reads now.

## 2. Search open issues

Run `search_op` for open issues. The call is read-only and safe to retry.

The branch predicate is the search result. The arms are:

- `duplicate` — an open issue states the same actual behavior. The same
  component is not enough. When several match, keep the oldest id. Set
  `duplicate_id` and `stop_reason`.
- `blocked` — the search errors. Leave `duplicate_id` empty. Set
  `stop_reason` to `blocked`. Do not create.
- `continue` — no open issue states the same actual behavior. This is the
  default. Leave `duplicate_id` empty and go to step 3.

When the arm is `duplicate`, stop. The next owner is the user, who may run
`fix-loop` on that id.

Done when the arm is chosen and the fields that arm sets are written.

## 3. Fill the draft

Take `expected`, `actual`, and `repro` from the user's message. Take
`evidence` from identifiers they already named. When they pasted a log, a
stack, or a trace body, do not copy it. Keep an identifier if they named one.
Otherwise leave `evidence` empty.

`repro` stays `none` when they gave no steps. Do not ask for steps.

Ask when `expected` or `actual` is empty. One question. Name the empty field.
The options are a sentence for that field, or stop. A sentence is stored on
that field and the run continues. Stop stores nothing and sets `stop_reason`
to `refused`. There is no default. The run waits until they answer.

Done when `expected` and `actual` are each stored as a sentence, or the run
has stopped as `refused`.

## 4. Write the body

Build `title` and `body` from the draft only, including the source mark on
each material sentence. Check the body against the issue shape. On failure,
the error names the field and the constraint. Rebuild once from the draft,
re-applying the source marks. The rebuild has no side effect.

The loop budget is two builds. The progress signal is a schema pass. When the
second build still fails, stop with `stop_reason` `blocked` and the error.
Do not create.

Done when `body` has passed the shape check.

## 5. Create the issue

Re-read `tracker_path` and take `create_op` from the file as it reads now.

Call `create_op` once with `title` and `body`. The call is a side effect and
is not safe to retry.

On timeout or an unclear error, run `search_op` once for the title. When that
search returns the issue, store its id and stop as `filed`. When it does not,
stop as `blocked`. Do not call create again.

A documented create error stops as `blocked` with that error.

Done when `issue_id` is the id the tracker returned.

## 6. Stop

Set `stop_reason`, `issue_id`, and `next_skill`. Record them in the task.
Record the operation names, not response payloads. This is a [work result](../capture-skill/references/work-result.md). This skill does not write the cursor. When `work-once` is the caller, it writes the cursor. `filed` and `duplicate` use `next_skill: none`, so the next wake takes the oldest actionable issue.

| Ending | `issue_id` | `next_skill` |
| --- | --- | --- |
| `filed` | the id from create, or from the single search after an unclear create | `none` |
| `duplicate` | `duplicate_id` | `none` |
| `tracker-missing` | `none` | `workspace-setup` |
| `refused` | `none` | `none` |
| `blocked` | the id when one exists, otherwise `none` | `none` |

Report the ending, the id when there is one, and that this skill does not
fix the defect.

Done when the report matches the ending and no second issue was created.
