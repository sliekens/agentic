---
name: duh
description: >
  Before a choice-like turn, drop every option a recorded lock, the code,
  or a wait already decides. Continue when one option remains. Use on
  every choice-like turn where the answer might be obvious. That includes a
  turn that offers a choice, ranks options, or is about to end on a question.
  Also use when `grill-me` is about to ask, or when `fix-loop` is about to
  treat a choice as the user's. Do not use to interview the user (`grill-me`).
  Do not use to fix an issue (`fix-loop`). Do not use to write a
  `Decision fork:` line. That line is the parent's job after this skill
  returns `ask`.
---

# Duh

Before a choice-like turn, drop every option a recorded lock, the code, or a wait already decides. Continue when one option remains.

Call this skill before the choice, on every choice-like turn where the answer might be obvious.

## Authority boundary

- `/duh`, or a choice-like turn, authorizes a read of the locks, the code, and the docs.
- It authorizes the choice to continue with no question.
- It authorizes no file writes. The scratchpad and the trace stay in the task.
- A secret, a one-way door, or a choice only the user can make stays with the user.
- It does not interview the user. That job is `grill-me`, and only after `ask`.
- It does not fix an issue. That job is `fix-loop`.
- It does not write a `Decision fork:` line. The parent does that after `ask`.
- It does not take the parent's next action after `proceed`.

## Instruction

These rules hold on every turn of this skill.

- The write set is empty.
- Do not end the turn on a question when one option remains.
- A problem is a prompt. A wait for an event is not a choice.
- An unsourced claim that a lock decides the question does not drop an option.
- Done evidence is the stop record in the last step.

## Worked examples

Each example shows one property. Do not copy its names into the task.

### A lock already decided

Property: a recorded lock removes the question.

Input: an awaiting-release issue has a fix line outside the newest tag. The turn is about to ask whether to keep the label or to treat the issue as backlog. The lock says a fix line stays until a tag contains that commit. A future check time is a wait.

Output: `proceed`. The survivor is "keep the label until a tag contains that commit." Do not ask.

### Two real forks

Property: no lock names one option, so the user still chooses.

Input: the practice has two homes, and no lock names one home.

Output: `ask`. Name both homes, the consequence of each, and one recommendation.

## Scratchpad

Keep this in the task, not in a file. Start every field empty. A step that needs state reads it from here.

The parent writes one identifier for each option it was about to offer.

| Field | Initial | Writer | Reader |
| --- | --- | --- | --- |
| `proposed_options` | empty | Parent, at load | Selection |
| `recorded_decision` | empty | Fresh lookup | Selection, resume |
| `rejected` | empty | Selection | Stop |
| `survivor` | empty | Selection | Branch, Ask, Stop |
| `arm` | empty | Branch | Ask, Stop |
| `user_choice` | empty | Parent, on resume | Parent |

`recorded_decision` stores an identifier for a fresh read. On resume, re-read that path or message before you use the conclusion. The other fields are procedure facts.

## 1. Fresh lookup

Re-read the user's locks. Re-read the file or issue the choice would change. Re-read the neighbor section the choice would change.

A new user message, an edit, or a compaction invalidates the previous read.

Write `recorded_decision` as the path or the message, plus the conclusion. A completed read that finds no lock still writes the path and the conclusion `none`.

Failure edge: the authority does not open. Leave `recorded_decision` empty. That empty read is not the conclusion `none`.

This skill has no edit step. The parent reads the current bytes before it edits.

Done when `recorded_decision` is set, or the read is empty.

## 2. Source binding

Material claims are why an option dropped, and the claim that one option remains.

The identifier is a file and a line, or the user message that locked the claim.

Drop an unsourced "already decided" claim. The option stays.

Do not run a second pass to check entailment.

This skill has no revision step. Do not rewrite a bound sentence.

Done when each drop cites an identifier, or the option stayed.

## 3. Selection

The set is `proposed_options`, plus `recorded_decision` when the lookup found a lock.

The set is closed. Do not add an option at decision time.

Apply the criteria in this order.

1. Drop an option that contradicts a cited lock, the current code, or a wait for an event.
2. Drop an option that is not a real fork.

A real fork is a secret, a one-way door, or a choice only the user can make.

Tie-break: do not break a tie between real forks. Two real forks both survive.

Write `rejected` and `survivor`. Quote each survivor's identifier from the set.

Done when `survivor` lists the options that remain.

## 4. Branch

The predicate is the survivor count. The arms are `proceed`, `ask`, and `blocked`.

Every arm sets `arm`. There is no default arm. A tool error does not become `proceed`.

- Count `1` sets `arm` to `proceed`.
- Count `2` or more sets `arm` to `ask`.
- Count `0` sets `arm` to `blocked`.

Failure edge: `recorded_decision` is empty because the authority did not open. Repeat the fresh lookup one time. A second empty lookup sets `arm` to `blocked`.

The budget is that one re-read.

Done when `arm` is set.

## 5. Ask

Run this step only when `arm` is `ask`.

The decision to ask is the `ask` arm. Selection decides a `proceed` arm from its criteria. No default exists. Silence is not a choice.

The question names the decision, the surviving options, the consequence of each, and one recommendation.

The run waits. The parent stores the answer in `user_choice`.

When `arm` is not `ask`, record that this step did not ask.

Done when the question is asked, or the skip is recorded.

## 6. Stop

The trace stores the ending name and the evidence. The trace stays in the task. The budget is one re-read.

- `proceed`: evidence is the survivor and a source that entails it. The parent owns the next action. This skill stops.
- `ask`: evidence is two or more survivors, each with the reason only the user can choose. The user owns the next action. When the parent is an interview, `grill-me` asks that one question and recommends one option. When the parent is a fix unit, `fix-loop` writes the decision record, marks the issue blocked, and returns `needs-user`. This skill does not do that job.
- `blocked`: evidence is no survivor after one re-read. The parent owns the next action. The parent does not ask the rejected question.

Done when the trace has the ending and the evidence.
