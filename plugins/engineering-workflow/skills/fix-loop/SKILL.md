---
name: fix-loop
description: Work an issue backlog in a loop — fix one issue, validate every phase against a repository validation runbook, file every out-of-scope problem found along the way as a new issue, then take the next issue — until only blocked issues remain or a release is needed to verify more. Use when asked to fix an issue, work the backlog, burn down issues, or run the fix loop, or when the user runs /fix-loop, optionally with a starting issue. Do not use for a single exploratory investigation with no fix (`flaky-build-investigation`, `analyze-complexity`), or for cutting or deploying releases.
---

# Fix Loop

Burn down an issue backlog one issue at a time. Every fix is also an audit:
whatever the work turns up that is out of scope becomes a new issue, and new
issues feed the next round. A problem noticed and not filed is lost.

Every phase ends with validation. What validates a change depends on the
change, `validation = f(change)`, so derive the checks from the repository's
validation runbook, and improve that runbook when the work shows a better
check.

## Authority boundary

- `/fix-loop`, or a request to work issues, authorizes: reading issues, fixing
  them within the repository's normal change process, commenting on and
  labeling issues, filing new issues, and editing the validation runbook.
- It does not authorize: product decisions, new architectural patterns, or
  other choices that repository instructions reserve for the user;
  production releases or deployments; closing an issue before its fix is
  verified. Stop and hand these to the user.
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

## 0. Locate the tooling

Read the repository's agent instructions. Find:

- **the issue tracker** and how to operate it (CLI, API, or MCP tools);
- **the blocked convention**: a label, a status, or a `Blocked by:` line;
- **the release process**, only to know what it needs; never run it here;
- **runtime evidence**: logs, error tracking, or metrics for dev and
  production;
- **the validation runbook**, and its `Integration` section: pull request or
  direct push mode, the target branch, who merges, and which CI runs.

If the repository has no validation runbook, or the runbook has no
`Integration` section, run `workspace-setup` to install or update it before
step 1. Do not guess the integration mode; step 6 depends on it.

Done when each item is found, or recorded as absent.

## 1. Pick

Start with the issue the user named. Otherwise take the oldest open issue that
is not blocked (no blocked label or status, no open issue in its `Blocked by:`
line), has no open pull request of its own, and is not waiting on a release.

Read it with its comments. Check the repository's technical-debt notes for the
area, if it keeps any.

Done when one issue is chosen and its history is read.

## 2. Confirm

Check the issue's claims against the code, and against runtime evidence when
the claim is about runtime behavior. Issues age: if the problem is already
gone, comment with the evidence, close the issue, and go back to step 1.

Prefer a failing test as the reproduction. It becomes the regression test in
step 4.

Done when the defect is reproduced in code, runtime evidence, or a failing
test.

## 3. Decide

Separate engineering choices from the user's choices.

- **Engineering choice** (mechanism, structure, which of several fixes): pick
  the simplest option that follows the repository's existing patterns. Record
  the choice and the rejected options on the issue before writing code.
- **User's choice** (product behavior, data the user owns, new architectural
  patterns, anything the repository instructions restrict): comment with the
  options and a recommendation, mark the issue blocked, and go back to step 1
  with the next issue.

Done when the approach is written on the issue, or the issue is marked blocked.

## 4. Fix

Make the smallest change that resolves the issue, with a regression test for
the triggering case when the change has testable behavior. Update docs that
describe the changed behavior.

Before editing, list the validation plan: every runbook entry whose trigger
matches the files and behavior the change touches. Validate in the inner loop:
after each edit, run the narrowest check that can fail (compile, then a
filtered test run) before moving on.

While working, write down every problem you notice outside the issue's scope:
bugs, swallowed errors, misleading logs, missing tests, doc drift, validation
gaps. Do not fix them here.

Done when the change and its regression test are written, and the narrow
checks pass.

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
  the target branch, not from the unmerged branch.

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

Done when every noted problem is an issue or a comment on one.

## 8. Repeat

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
