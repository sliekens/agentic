---
name: workspace-setup
description: Install the workspace files that engineering-workflow skills depend on — the validation runbook (VALIDATION.md) that fix-loop reads, including whether changes land through pull requests or by direct push, and the issue-tracker record (ISSUE_TRACKER.md) that says where issues and work artifacts live — by copying bundled seed files into the workspace and fitting them to it from existing context, exploration, and a few easy-to-answer questions. Recommends an issue tracker from the evidence (such as the git remote), records the choice, and migrates open work that lives in committed markdown into that tracker, deleting the migrated files, unless the user chose repository files. Use when the user runs /workspace-setup, asks to set up or bootstrap the workflow in a repository, asks to move TODO, plan, or debt documents into the issue tracker, or when a skill such as fix-loop, bug-report, or work-once finds its workspace file missing. Re-running updates an existing install instead of overwriting it. Do not use for personal collaboration preferences (`operator-setup`).
---

# Workspace Setup

Copy each seed file this plugin carries into the workspace, then fit the copy to
the workspace so it holds workspace facts instead of placeholders. A seed
installed but not fitted is not done.

## Standing rule: questions

**Only ask questions that are easy to answer. Prefer questions that are hard to
ask.**

- **Easy to answer:** the user can answer in seconds, from memory, without
  looking anything up: a choice between concrete options, a yes or no, or a
  fact only they hold. Never ask what the workspace can answer; explore first.
- **Hard to ask:** the question could only be phrased after exploration. It
  names the evidence and the specific ambiguity: "CI runs 7 of the 21 test
  suites; is that deliberate?", not "Which tests should run?".

Ask these questions together, once, after exploration, and only where the answer
changes what gets written. When a question fails the rule, decide from the
evidence, write the result, and report it as an assumption.

## Seed files

| Seed | Default workspace path | Used by |
| --- | --- | --- |
| [references/VALIDATION.md](references/VALIDATION.md) | the workspace's agent-doc folder, for example `.agents/VALIDATION.md` or `docs/agents/validation.md` | `fix-loop` (steps 0, 4, 5, and 6) |
| [references/ISSUE_TRACKER.md](references/ISSUE_TRACKER.md) | the same folder, for example `.agents/ISSUE_TRACKER.md` or `docs/agents/issue-tracker.md` | `fix-loop`, `bug-report`, `work-once`, `technical-debt-audit`, `cross-check`, `realign`, and every scenario-design technique that publishes its output |

## Authority boundary

- `/workspace-setup` authorizes creating or editing the seed files listed above
  in the workspace, and adding one link to each from the workspace's agent
  instructions (`AGENTS.md`, `CLAUDE.md`, or the equivalent).
- Read anything in the workspace. Run only read-only commands and cheap,
  bounded checks whose writes stay in ordinary build output (for example,
  confirming that a test command exists with a list or help flag). Do not run
  full builds or test suites unless the user asks.
- Migration (step 5) is the only part that writes outside the workspace's
  files. Filing issues and deleting files needs the user's approval of the
  migration plan, given after the plan is shown. The approval covers that plan
  only. It does not extend to a later run.
- Do not commit, push, or change CI, source, or other docs, except for repairing
  links to files that migration deleted. Report a problem found during
  exploration instead of fixing it.

## 1. Locate

Find the workspace root and its agent instructions. Find where agent-facing
docs live (`.agents/`, `docs/agents/`, or files linked from the instructions),
and follow the existing naming style.

For each seed, check whether the workspace already has it, under the default
name or another one (for example a testing guide that already lists
per-change checks, or an `issue-tracker.md` that already says how to operate the
tracker).

Done when each seed has a target path and an install mode: **new**, **update**
(the file exists), or **merge** (the content exists elsewhere under another
name).

## 2. Explore

Collect the facts each seed needs. For VALIDATION.md:

- **completion gate:** build, lint, and format commands from the agent
  instructions, the README, package scripts, the Makefile or task runner, and
  the CI config;
- **kinds of change:** source and test layout, how test projects map to source,
  test runners and their filter syntax, UI test suites;
- **CI:** workflow files, which ones run on push or pull request, and what each
  covers;
- **integration:** whether changes land through pull requests or by direct
  push, the target branch, and who merges. Weigh the agent instructions and
  contributing guide, branch protection or rulesets on the target branch
  (read them with the forge CLI or API when available), recent history on the
  target branch (pull request merge or squash commits versus direct commits),
  pull request templates, `CODEOWNERS`, and the CI triggers. When the sources
  disagree, the disagreement becomes a question;
- **runtime evidence:** logging, error-tracking, or metrics tools named in the
  instructions or configuration;
- **gaps:** anything the evidence shows is not validated (for example test
  suites that exist but that CI does not run).

For ISSUE_TRACKER.md:

- **candidate trackers:** the host of each git remote and whether it offers
  issues (GitHub, GitLab, Gitea, Forgejo, Azure DevOps); a forge CLI that is
  installed and logged in (`gh`, `glab`, `tea`, `az`); issue tracker links in
  the agent instructions, README, contributing guide, or issue templates; an
  external tracker named there (Jira, Linear, and similar) or reachable through
  an available MCP server;
- **use so far:** whether the tracker has issues, and whether the instructions
  or history refer to issue numbers. A tracker with issues and references to
  them is already in use;
- **committed issue files:** directories or files that act as a tracker
  (`issues/`, `docs/issues/`, `TODO.md`, `BACKLOG.md`, `ROADMAP.md`);
- **operation:** the create, read, list, comment, label, and close commands of
  the candidate, checked with a help flag, and the grouping features it has
  (project, milestone, label) that can hold technical debt, and whether a label
  or a one-line body field can store one `next_skill`;
- **recommendation:** choose one candidate from this evidence. Prefer the
  tracker of the forge that hosts the `origin` remote when it has issues
  enabled and a working CLI. Prefer a tracker already in use over a better one
  that is not. Recommend repository files only when no tracker is reachable.

Done when every placeholder in each seed is backed by evidence or is on a
question list.

## 3. Ask

Apply the standing rule to the question list. Drop each question that
exploration answered, or that the user cannot answer at a glance. Rewrite the
rest so they name the evidence. Ask the remaining questions in one message.

Always ask where to track issues, because the choice is the user's. Put the
recommendation first and name its evidence, for example: "Track issues in
Gitea at gitea.example.com/owner/repo? It hosts `origin`, `tea` is logged in,
and it has 41 issues." Offer these options, each only when it can work:

- **Forge issues:** the recommendation, when one exists.
- **External tracker:** a tracker that is not the forge.
- **Repository files:** committed markdown files. Say that this keeps work in
  the repository and that migration will not run.
- **None:** work is reported in the conversation only.

Done when the answers are in, or no question passed the rule. The tracker
question always passes.

## 4. Install

- **new:** copy the seed and replace every placeholder with a workspace fact.
  For VALIDATION.md:
  - the purpose line says that validation depends on the change, that a reader
    runs every entry whose trigger matches, and that entries record reusable
    checks, not the steps run for one change;
  - fill `Integration` from step 2 with one mode, never both;
  - repeat the entry block once per kind of change found in step 2, with the
    completion gate first as the entry that applies to every change;
  - list each gap from step 2 under `Known gaps`, or leave the section with no
    items when there are none.

  For ISSUE_TRACKER.md:
  - record the mechanism the user chose, its location, tool, and the basis for
    the choice;
  - fill `Operations` with commands checked in step 2, not commands from
    memory;
  - fill `Cursor` from those same commands. When the tracker can label an
    issue, storage is one label `next:<skill>`, **Set** replaces that label,
    and **Find** lists open issues that have it, oldest first. When it
    cannot, storage is one line `next_skill: <skill>` at the top of the
    issue body. **Set** for `none` removes the label or the line;
  - fill `Grouping` with the project, milestone, or label that holds technical
    debt. When the tracker has none, offer to create one and create it only
    after the user agrees;
  - fill `Artifacts` so each kind has one destination. Keep durable
    current-state documents in the repository;
  - keep the `Repository files` section only when the user chose that
    mechanism, and delete it otherwise.
- **update:** keep the workspace's content. Add missing structure from the
  seed, such as the entry shape, a `Known gaps` section, or a `Cursor`
  section, and fill it from exploration. Do not remove entries the
  workspace wrote.
- **merge:** leave the existing file in place, create the seed at its target
  path from the existing content, and link the two. Never delete or move the
  existing file.

Add one link to each installed file from the agent instructions, next to the
related docs. Keep existing links.

Done when no `<placeholder>` remains, and each file is linked once.

## 5. Migrate open work into the tracker

Skip this step when the mechanism is **repository files** or **none**, and say so
in the report. Files that the user chose to keep are not migration candidates.

### Inventory

Find committed markdown that holds open work:

- backlog and plan files (`TODO.md`, `ROADMAP.md`, `BACKLOG.md`, `plans/`,
  `docs/plans/`, `docs/issues/`);
- technical debt indexes and their per-item write-ups;
- analysis documents (`docs/analysis/`, FMEAs, design spaces, scenario sets)
  with open questions, next steps, deferred items, or unresolved findings;
- migration or rollout checklists, and any file marked proposed, draft, or in
  progress;
- unchecked task lists (`- [ ]`) and sections titled open questions, remaining
  work, follow-up, deferred, or known gaps.

Do not treat these as work: product maps, architecture decision records,
runbooks, reference docs, changelogs, and documents that describe current
behavior. Those stay.

### Classify

For each candidate decide with evidence, by reading the code or history when
the file claims a status:

- **whole file is open work:** file it, then delete the file.
- **file mixes open work with lasting content:** file only the open part, delete
  only that section, and leave one line that names the issue number.
- **work is already done:** do not file it. List the file as a deletion
  candidate and let the user decide.
- **work already has an issue:** link the existing issue and do not duplicate
  it. Search closed issues too.
- **grouped debt:** items that are structural debt go into the `Grouping`
  entry from step 4, not into a new index file.

### Plan and approve

Show one table before touching anything: file or section, class, resulting
issue title, group, and what is deleted. Mark each row that deletes content with
no copy elsewhere. Get the user's approval of the table. Apply changes the user
removes or edits, and nothing else.

### Apply

1. File each issue with the tracker's create command. The body carries the full
   open content, not a summary, plus the source path and the commit hash it was
   read at, so the original stays recoverable from history. Add it to its group.
2. Record each issue number against its table row.
3. Delete the files and sections the table names. Where a lasting file keeps a
   pointer, write the issue number.
4. Repair every link and instruction that pointed at a deleted file: search the
   repository, the agent instructions, and skill or prompt copies. Point them at
   the group or issue. Keep mirrored copies identical.
5. Verify: search for each deleted path and heading and find no dangling
   reference, and confirm each filed issue reads back with its full body.

Done when every approved row is applied, no reference to a deleted file remains,
and the user has the list of issue numbers.

## 6. Report

List each installed file with its path and mode, the integration mode found
and its evidence, the issue tracker chosen with the evidence and whether the
user confirmed it or you assumed it, the assumptions you made
instead of asking, and the gaps you recorded. Report the migration: issues
filed with their numbers, files and sections deleted, rows the user declined,
and references repaired, or why migration was skipped. Suggest filing an issue
for each gap. The files are left uncommitted unless the user asked for a commit.
