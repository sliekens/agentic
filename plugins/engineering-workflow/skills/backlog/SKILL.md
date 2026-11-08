---
name: backlog
description: Front door to the workspace backlog. Walk the blocked issues with the user one at a time, or add a new item by routing it to the skill that owns that kind of item. A walk re-investigates each fork first. A fork with one good option, or a two-way door, is decided and unblocked without a question. Only a real fork (several good options, or none) or a one-way door is explained to the user with recommended options and a question. Each decision goes on the issue, `blocked` comes off, and the issue gets a `next:fix-loop` or `next:expand-and-contract` cursor. Use when the user runs /backlog, asks to walk, review, or triage the backlog or the blocked issues, asks what is waiting on them, or asks to add something to the backlog. A defect goes to `bug-report`, structural debt with no failing behavior to `technical-debt-audit`, and a missing issue-tracker record to `workspace-setup`. Do not use to fix an issue (`fix-loop`), or from `work-once`: this skill needs a person.
---

# Backlog

One entry point for the backlog. A walk turns blocked issues back into work
that `fix-loop` can take. An add files a new item through the skill that owns
its kind. This skill does not fix anything.

## Authority boundary

- `/backlog`, or a request to walk or add to the backlog, authorizes reading
  the issue-tracker record, the issues, and the code; commenting on issues;
  removing the blocked marker; writing the cursor; and creating one issue for
  an item that is neither a defect nor debt.
- It does not authorize a fix, a commit, a close, or a contract step the user
  has not approved. The fix is `fix-loop`. The contract step is
  `expand-and-contract`.
- It does not authorize choosing a tracker. A missing record stops the run
  for `workspace-setup`.
- `work-once` does not run this skill. A walk waits on a person.

## Walk state

Keep this in the task, not in a repository file. Steps read these fields and
do not invent replacements.

| Field | Initial | Writes it | Reads it |
| --- | --- | --- | --- |
| `tracker_path` | empty | step 1 | every write |
| `ops` | empty | step 1 | every write |
| `mode` | empty | step 2 | step 2 |
| `queue` | empty list | step 4 | step 5 |
| `issue_id` | empty | step 5 | step 5 |
| `class` | empty | step 5 | step 5 |
| `options` | empty list | step 5 | step 5 |
| `decision` | empty | step 5 | step 5 |
| `results` | empty list | step 5 | step 6 |
| `stop_reason` | empty | the ending step | the report |

`ops` holds the **List and search**, **Read**, **Comment**, **Label**,
**Create**, blocked convention, and **Cursor Set** operations, taken from the
record as it reads now. A user turn invalidates any issue read before it.

## 1. Read the tracker record

Read `ISSUE_TRACKER.md` from the workspace's agent-doc folder. Store the path
and `ops`.

Failure edge: the file is missing, an operation is still a placeholder, or
`Cursor` is missing. Set `stop_reason` to `tracker-missing` and stop. The next
owner is `workspace-setup`. Do not guess a host or a command.

Done when `tracker_path` and every `ops` entry are set from the file.

## 2. Choose the mode

The predicate is the user's message. The arms are:

- `add` — the message names an item to add.
- `walk` — anything else, including a bare `/backlog`. This is the default.

Done when `mode` is set.

## 3. Add

Classify the item into one kind. Criteria, in order:

1. `defect` — it states expected and actual behavior, or something is broken.
   Hand off to `bug-report` with the user's words. Set `stop_reason` to
   `handed-off` and stop.
2. `debt` — a structural problem with no failing behavior. Hand off to
   `technical-debt-audit` with the user's words. Set `stop_reason` to
   `handed-off` and stop.
3. `other` — a feature, a task, or a chore. Continue.

For `other`, run **List and search** for open issues with the item's words.
When one already states the same goal, set `stop_reason` to `duplicate`, name
it, and stop. Otherwise call **Create** once with a one-line title and a body
of two sections, `## Goal` and `## Done when`, taken from the user's words.
Ask one question when the done condition is missing; there is no default.
Create is a side effect and is not safe to retry. On an unclear error, search
once for the title, and stop as `blocked` when the issue is not there.

Done when the item is handed off, named as a duplicate, or created with the
id the tracker returned. Set `stop_reason` to `filed` and go to step 6.

## 4. List the blocked issues

Run **List and search** for open issues with the blocked convention. Read
every page. Sort oldest first and store the ids in `queue`.

When `queue` is empty, set `stop_reason` to `walked` and go to step 6.

Done when `queue` holds every blocked open issue.

## 5. Walk the queue

A loop over `queue`. The progress signal is the number of ids left. The
budget is one visit per issue. Each visit writes its result to the tracker
before the next visit starts, so a stopped walk loses nothing.

Read ahead before you ask. Decide every issue that needs no question first.
Then ask the remaining questions together, up to four independent questions
per turn. One question covers every issue that shares the same fork, and
names each id.

For each `issue_id`:

1. **Read it fresh** with **Read**, including comments. Take the fork from the
   latest comment that set the blocked marker.
2. **Investigate the fork.** Test each option on the issue against the code,
   the runtime evidence, the repository's patterns and restrictions, and the
   issue history. Reject an option that breaks an invariant or a restriction,
   misses the issue's goal, or only defers the problem. Write each rejection
   with its reason into `options`. Do not add facts that only the reasoning
   holds.
3. **Classify** into one `class`:
   - `one-good` — one option is left after step 2.
   - `two-way` — several good options are left, and a revert undoes any of
     them without data loss and without a lasting effect outside the
     repository.
   - `one-way` — a revert cannot undo the choice (data the user owns is
     deleted or rewritten, a destructive migration, a production change, an
     external commitment), or the repository instructions restrict it. Also
     a fork with no good option left.
   - `access` — the block is a standing approval rule, not a choice.
   - `tooling` — the block is a missing tool, MCP server, credential, or
     route for one agent on one host.
   - `resolved` — the code or the evidence shows the problem is gone.
4. **Act on the class:**
   - `one-good`, `two-way`, `resolved`: take the remaining option, or the
     simplest good one. Do not ask. Comment the decision, the rejected
     options with their reasons, and how to revert. Remove the blocked marker
     and set the cursor to `fix-loop`, which confirms a resolved issue and
     closes it. Tell the user in one line.
   - `one-way`: ask. Name what is blocked, why, and the evidence. Give each
     option with its consequence, recommendation first, plus `skip` and
     `stop`. When the expand part of `expand-and-contract` can be built
     without walking through the door, say so as an option. Wait for the
     answer.
   - `access`: ask. Name the rule, every queued issue it holds, and the
     smallest grant that would do. The options are the grant, `skip`, and
     `stop`. Wait for the answer.
   - `tooling`: do not ask. A tooling problem is open work. File it, or
     comment on the existing one, where the tracker record groups tooling
     problems, with the agent and host it affects. On the issue, replace the
     blocked marker with a line naming that tooling issue, agent, and host,
     and set the cursor to `fix-loop`.
5. **Store the answer** in `decision` with its source `(user)`:
   - an option: comment the decision and the options that were on the table,
     remove the blocked marker, and set the cursor to `fix-loop`. When the
     option approves a contract step, set it to `expand-and-contract`.
   - a grant: comment it, remove the blocked marker, and set the cursor to
     `fix-loop`.
   - an answer that changes a standing rule (an approval rule, a restriction,
     an access assumption): change the rule in the repository instructions
     first, then classify every remaining issue in `queue` against the new
     rule before the next question.
   - `skip`: change nothing on the issue.
   - `stop`: set `stop_reason` to `stopped` and go to step 6.

Append `issue_id`, `class`, and the outcome to `results`, then clear the
per-issue fields.

Done when every id in `queue` has a result, or the user said `stop`. Set
`stop_reason` to `walked` when the queue is empty.

## 6. Stop

| Ending | Evidence | Next owner |
| --- | --- | --- |
| `walked` | one result per blocked issue | `fix-loop` or `work-once`, through the cursors |
| `stopped` | the results so far | the user, on the next `/backlog` |
| `filed` | the id from **Create** | `fix-loop` |
| `duplicate` | the existing id | the user |
| `handed-off` | the receiving skill | `bug-report` or `technical-debt-audit` |
| `tracker-missing` | the missing operation | `workspace-setup` |
| `blocked` | the tracker error | the user |

Report the ending. For a walk, list each issue with its class and outcome:
decided without a question, decided by the user, granted, skipped. Then name
the issues still blocked.

Done when the report matches `results` and the tracker.
