---
name: fix-loop
description: Harden a sound architecture one issue at a time — fix one issue, validate every phase against a repository validation runbook, file every out-of-scope problem found along the way as a new issue, then take the next issue — until only blocked issues remain or a release is needed to verify more. A simple bug gets the smallest change. A larger change, including a module rewrite, is in scope when it removes local accidental complexity instead of stacking it. Use `analyze-complexity` before choosing the shape. Use when asked to fix an issue, work the backlog, burn down issues, or run the fix loop, or when the user runs /fix-loop, optionally with a starting issue. Do not use when the architecture is unsound or the goal needs a capability the architecture cannot hold (`yak-shave`), for a single exploratory investigation with no fix (`flaky-build-investigation`, `analyze-complexity`), for untangling the whole codebase in one pass instead of issue by issue (`untangle-codebase`), or for cutting or deploying releases. When the user describes a defect that is not yet an issue, stop and use `bug-report`. When `work-once` runs this skill, finish one issue, return a WorkResult, and do not load the next skill or take another issue.
---

# Fix Loop

Harden a system whose architecture is already sound. Burn down an issue
backlog one issue at a time. Every fix is also an audit:
whatever the work turns up that is out of scope becomes a new issue, and new
issues feed the next round. A problem noticed and not filed is lost.

Every phase ends with validation. What validates a change depends on the
change, `validation = f(change)`, so derive the checks from the repository's
validation runbook, and improve that runbook when the work shows a better
check.

## Authority boundary

- `/fix-loop`, or a request to work issues, authorizes: reading issues,
  hardening a sound architecture within the repository's normal change
  process, commenting on and labeling issues, filing new issues, and editing
  the validation runbook. Step 3 chooses the size of the change.
- It does not authorize replacing an unsound architecture. That work is
  `expand-and-contract`.
- It does not authorize a whole-codebase refactor in one pass. That work is
  `untangle-codebase`.
- It does not authorize: product decisions, or other choices that repository
  instructions reserve for the user; production releases or deployments;
  closing an issue before its fix is verified. Stop and hand these to the
  user.
- Follow the repository's instructions for branching, commits, pull requests,
  CI, and the issue tracker. Where they are silent, prefer the least
  surprising option and say which one you chose.
- Never use auto-close keywords (`fixes #n`, `closes #n`) in commits or
  pull requests. An issue closes on verification, not on merge.

## Keep a compact loop state

Keep this in the task, not in a repository file:

- the current issue, its phase, and its decided approach;
- the validation plan for the current change and the result of each check;
- problems noted outside the current issue's scope, not yet filed;
- fixed issues awaiting merge, fixed issues awaiting release, closed issues,
  filed issues, blocked issues;
- failing checks proven to fail without the change.

After resuming, recheck the worktree, the branch, and each open issue's state
before using the prior state.

## Tick

Backlog mode is the default for `/fix-loop` and for a request to work the backlog, including a request that names a starting issue and then continues. Tick mode is when the caller is `work-once`, or the user asked for one issue and no continuation.

In tick mode, do steps 0 through 7 for one issue. Return a [work result](../capture-skill/references/work-result.md) and stop. Do not run step 8. Do not load `next_skill`. When `work-once` is the caller, it writes the cursor. When this skill is the top of the session, write the cursor before exiting.

| Stop | `stop_reason` | `next_skill` |
| --- | --- | --- |
| Record or runbook missing | `tracker-missing` | `workspace-setup` |
| A defect is described and no issue exists | `needs-issue` | `bug-report` |
| Unsound, or the goal does not fit | `needs-replacement` | `yak-shave` |
| The job is the whole codebase | `whole-codebase` | `untangle-codebase` |
| A choice the user must make | `needs-user` | `none` |
| The pull request waits on a merge | `awaiting-merge` | `fix-loop` |
| A release must happen before more can be verified | `awaiting-release` | `none` |
| The issue is closed | `done` | `none` |
| No actionable issue | `idle` | `none` |

`analyze-complexity` and `blind-spot-coverage` stay inside this skill. They are not `next_skill`.

When tick mode is given an issue whose fix has already landed, do not change the code again. Return `awaiting-release` / `none` when runtime verification still needs a release. When step 6's close rule is already met, close the issue and return `done` / `none`.

## 0. Locate the tooling

Read the repository's agent instructions. Find:

- **the issue tracker** and how to operate it (CLI, API, or MCP tools), from
  the workspace's issue-tracker record (`ISSUE_TRACKER.md` by default), which
  also names the group that holds technical debt;
- **the blocked convention**: a label, a status, or a `Blocked by:` line;
- **the release process**, only to know what it needs; never run it here;
- **runtime evidence**: logs, error tracking, or metrics for dev and
  production;
- **the validation runbook**, and its `Integration` section: pull request or
  direct push mode, the target branch, who merges, and which CI runs.

If the repository has no issue-tracker record, no validation runbook, or the
runbook has no `Integration` section, run `workspace-setup` to install or update it before
step 1. Do not guess the integration mode; step 6 depends on it. In tick mode,
return `tracker-missing` / `workspace-setup` and do not run `workspace-setup`.

Done when each item is found, or recorded as absent.

## 1. Pick

Start with the issue the user named. When they describe a defect and no issue
exists yet, stop and use `bug-report`. Do not invent the issue inside this
loop. In tick mode, return `needs-issue` / `bug-report` and do not run
`bug-report`. When the job is the whole codebase, stop and use
`untangle-codebase`. In tick mode, return `whole-codebase` /
`untangle-codebase` and do not load it. When no issue was named, take the oldest open issue that
is not blocked (no blocked label or status, no open issue in its `Blocked by:`
line), has no open pull request of its own, and is not waiting on a release.

Read it with its comments. Check the repository's technical-debt notes for the
area, if it keeps any. In tick mode, when no issue is actionable, return
`idle` / `none`.

Done when one issue is chosen and its history is read.

## 2. Confirm

Check the issue's claims against the code, and against runtime evidence when
the claim is about runtime behavior. Issues age: if the problem is already
gone, comment with the evidence, close the issue, and go back to step 1.
In tick mode, return `done` / `none` and do not go back to step 1.

Prefer a failing test as the reproduction. Step 4 decides whether that test
stays in the suite.

Done when the defect is reproduced in code, runtime evidence, or a failing
test.

## 3. Decide

Separate engineering choices from the user's choices.

Run `analyze-complexity` on the boundary this issue touches. Read **Stacking
complexity** there and class the architecture before choosing a shape.

- **Sound architecture.** Harden it. A simple bug gets the smallest change.
  Choose a larger change, including a module rewrite, when it removes local
  accidental complexity. Record the choice and the rejected options on the
  issue before writing code. Name a stacked change as a rejected option when
  one was available.
- **Unsound architecture, or a goal the structure cannot hold.** Stop this
  issue in the loop. A patch would stack complexity. Continue the same issue
  under `yak-shave`. In tick mode, return `needs-replacement` / `yak-shave`
  and do not load `yak-shave`.
- **User's choice** (product behavior, data the user owns, anything the
  repository instructions restrict): comment with the options and a
  recommendation, mark the issue blocked, and go back to step 1 with the
  next issue. In tick mode, return `needs-user` / `none` and do not go back
  to step 1.

Done when the approach is written on the issue, the issue has moved to
`expand-and-contract`, or the issue is marked blocked. A fix-loop approach
names the class from the analysis, the change, and the options rejected.

## 4. Fix

Make the change step 3 recorded. A simplification named there is in scope
for this issue. Update docs that describe the changed behavior.

Read **What deserves a test** in `blind-spot-coverage` before adding or
keeping a test, and obey that section.

Before editing, list the validation plan: every runbook entry whose trigger
matches the files and behavior the change touches. Validate in the inner loop:
after each edit, run the narrowest check that can fail (compile, then a
filtered test run) before moving on.

While working, write down every problem you notice outside the issue's scope:
bugs, swallowed errors, misleading logs, missing tests, doc drift, validation
gaps. Do not fix them here.

Done when the change is written, every test that deserves to exist is
written, and the narrow checks pass.

## 5. Validate

Run the whole validation plan: the repository's completion gate plus every
matching runbook entry. Judge each check by its pass criterion. Failing checks
that predate the change stay unfixed. Prove that they also fail without the
change, and name them in the report.

Then review the validation itself. Update the runbook when one of these is
true:

- a check missed a defect that a later check or CI caught;
- a check gave a false result (flaky, environmental, stale);
- a cheaper check would have found the same defect sooner;
- the change matched no entry, or an entry was missing a pitfall that cost
  time.

### Runbook format

The runbook is a quick reference keyed by kind of change, not a diary. Each
entry has this shape:

```markdown
## <Kind of change>

- **Trigger:** what the change touches (paths, components, behavior).
- **Run:** the commands or queries, general enough for the next change of this kind.
- **Passes when:** the evidence that proves the change works.
- **Pitfalls:** what gives false results or costs time.
```

Record reusable knowledge, never the steps taken for one issue. Merge a new
finding into the entry it belongs to before adding an entry. Keep an
`## Integration` section that states how changes land, one entry that applies
to every change (the completion gate), and a `## Known gaps`
section for validation that needs code or CI work; file an issue for each
gap in step 7.

Done when every planned check passes, and the runbook reflects anything the
validation taught.

## 6. Integrate

Land the change as the runbook's `Integration` section says. Commit runbook
changes separately from the fix.

- **Direct push:** commit on the target branch, push, and follow the triggered
  CI to green. The change has landed.
- **Pull request:** branch from the current target branch, open a pull request,
  and follow its CI to green. Merge it only when the `Merge` line lets you;
  otherwise the issue waits on a merge, and the next issue starts again from
  the target branch, not from the unmerged branch. In tick mode, do not start
  the next issue.

Comment on the issue with the commit or pull request, what changed, and how to
verify it in production. Leave the issue open:

- a fix with runtime behavior closes only after it is released and verified in
  production;
- a fix with no runtime behavior (tests, dead code, docs, CI) closes once it has
  landed on the target branch and CI is green there.

Done when CI is green, the change has landed or its pull request waits on a
merge, and the issue has a progress comment.

## 7. Log

File each problem noted in steps 4 and 5 as a new issue. Search first,
including closed issues, and comment on a match instead of duplicating it.
Each new issue states:

- `Found while working #<n>.` on the first line;
- what happens, with file:line or runtime evidence;
- the consequence;
- candidate directions, marked as not decided.

Add an issue that reports structural debt rather than a defect to the debt group
named in the issue-tracker record.

Done when every noted problem is an issue or a comment on one.

## 8. Repeat

Skip this step in tick mode. Return the **Tick** row for the outcome of step 6: `awaiting-merge`, `awaiting-release`, or `done`.

Go back to step 1. The newly filed issues are candidates like any other.

Stop when either:

- no open issue is actionable (all remaining are blocked or wait on a merge
  or a release), or
- a production release is needed before more progress can be verified.

## 9. Report

Lead with what the user must do next (usually: review and merge, release, or
decide on a blocked issue). Then list:

- issues fixed, with pull requests, awaiting merge;
- issues fixed, with commits, awaiting release;
- issues closed, with the verification evidence;
- issues filed, one line each;
- issues blocked, with the decision each one needs;
- runbook entries added or changed;
- failing checks that predate the work.

After the user releases, verify each fixed issue with runtime evidence,
comment the evidence, and close it.
