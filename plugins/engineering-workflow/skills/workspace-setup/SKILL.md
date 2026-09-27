---
name: workspace-setup
description: Install the workspace files that engineering-workflow skills depend on — currently the validation runbook (VALIDATION.md) that fix-loop reads, including whether changes land through pull requests or by direct push — by copying bundled seed files into the workspace and fitting them to it from existing context, exploration, and a few easy-to-answer questions. Use when the user runs /workspace-setup, asks to set up or bootstrap the workflow in a repository, or when a skill such as fix-loop finds its workspace file missing. Re-running updates an existing install instead of overwriting it. Do not use for personal collaboration preferences (`operator-setup`).
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

## Authority boundary

- `/workspace-setup` authorizes creating or editing the seed files listed above
  in the workspace, and adding one link to each from the workspace's agent
  instructions (`AGENTS.md`, `CLAUDE.md`, or the equivalent).
- Read anything in the workspace. Run only read-only commands and cheap,
  bounded checks whose writes stay in ordinary build output (for example,
  confirming that a test command exists with a list or help flag). Do not run
  full builds or test suites unless the user asks.
- Do not commit, push, or change CI, source, or other docs. Report a problem
  found during exploration instead of fixing it.

## 1. Locate

Find the workspace root and its agent instructions. Find where agent-facing
docs live (`.agents/`, `docs/agents/`, or files linked from the instructions),
and follow the existing naming style.

For each seed, check whether the workspace already has it, under the default
name or another one (for example a testing guide that already lists
per-change checks).

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

Done when every placeholder in each seed is backed by evidence or is on a
question list.

## 3. Ask

Apply the standing rule to the question list. Drop each question that
exploration answered, or that the user cannot answer at a glance. Rewrite the
rest so they name the evidence. Ask the remaining questions in one message.

Done when the answers are in, or no question passed the rule.

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
- **update:** keep the workspace's content. Add missing structure from the
  seed, such as the entry shape or a `Known gaps` section, and fill it from
  exploration. Do not remove entries the workspace wrote.
- **merge:** leave the existing file in place, create the seed at its target
  path from the existing content, and link the two. Never delete or move the
  existing file.

Add one link to each installed file from the agent instructions, next to the
related docs. Keep existing links.

Done when no `<placeholder>` remains, and each file is linked once.

## 5. Report

List each installed file with its path and mode, the integration mode found
and its evidence, the assumptions you made
instead of asking, and the gaps you recorded. Suggest filing an issue for each
gap. The files are left uncommitted unless the user asked for a commit.
