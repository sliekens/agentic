---
name: compound
description: End-of-session hill climb on the instruction surface. Encodes this session's friction into AGENTS.md, skills, or project docs so the next session does not pay the same tax.
disable-model-invocation: true
argument-hint: "[optional friction hint]"
---

End-of-session *climb* on the instruction surface. Turn this session's *friction* into a *delta* at its *home*, so the next session does not pay the same tax.

`/compound` authorizes the climb for local project deltas. A hint, if given, is the primary event; still mine the rest.

The target is the instruction surface — skills, AGENTS.md / CLAUDE.md, pointers, project docs, or a discoverable environment. Not product code, not a session diary.

## 1. Mine

From this session only, list every *friction* event that has evidence:

- User correction, undo, or re-statement
- Retry or wrong path
- Repeated lookup for a fact that should have been a pointer
- Procedure invented by hand that should be a skill
- Instruction that was wrong, stale, or missing
- Work that existed only because the instruction surface was incomplete (*yak*)

Skip: hypothetical future pain, thoroughness that simply took time, facts already encoded that the agent merely failed to follow for no pointer reason (those still count if the pointer itself was too weak to fire).

Done when the list is numbered with one-line evidence each, or the list is empty — then stop and say `no movement`.

## 2. Home

For each event, pick one *home* (narrowest that would have fired) and one *kind*.

Scope, narrowest first:

1. Environment — script, config, `--help`, layout. Prefer a discoverable environment over a cached instruction.
2. Project doc the next session will already read
3. Project skill
4. Project `AGENTS.md` / `CLAUDE.md` — a pointer, not an essay
5. User skill (`~/.agents/skills`)
6. User-global instruction
7. `OPERATOR.md` — only for how to work with this operator

Kind: *prune*, *pointer*, *fact*, *skill*, *environment*.

*Counterfactual* gate: if this *delta* had existed at turn 0, the event would not have happened. Drop anything that fails.

Encode the class of problem, not the instance. When the *home* is a skill or `AGENTS.md`, follow `writing-for-agents`. When creating or editing a skill, also follow `skill-design-principles`. When the *home* is a vault note marked for STE, follow `ste-writing`.

Done when every surviving event has a home, a kind, a one-sentence delta, and a one-sentence counterfactual.

## 3. Rank

This is a climb, not a backlog. Rank by tax saved, then by how local the delta is.

Prefer: prune over add, pointer over inline, skill over always-loaded essay, project over user.

Cap this run at three deltas, and at one delta per home. Leftovers stay on the table as one-liners.

## 4. Apply

Apply ranked local deltas (project AGENTS.md / docs, existing skill edits, environment facts in-repo).

Pause and wait before:

- Creating a new skill
- User-global instruction (`~/.agents`, harness instruction files)
- A vault note
- A large prune

Canonical new user skills live in `~/.agents/skills/<name>/`. After creating one, junction it to `~/.claude/skills/<name>` and `~/.grok/skills/<name>` the same way `teach` is wired.

Done when each applied file has been re-read, each fact has one home, and the counterfactual still holds.

## 5. Report

```
Moved:
- <friction> → <home> (<kind>)
  counterfactual: <one line>

Left on the table:
- <one line each, or none>
```
