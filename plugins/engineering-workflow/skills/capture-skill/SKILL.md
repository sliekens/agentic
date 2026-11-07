---
name: capture-skill
description: >
  Capture a practice the user is introducing as one new skill built from the primitive catalog, after testing that none of the skills they name already own it. Use when the user says they have skills for some jobs but something is missing, says a practice is not captured or is not covered, says nothing captures this, or introduces a workflow that should become a skill — including "we have skills for X, Y, and Z, but I'm missing something." Read the named skills first. If one owns the practice, name it and stop. If the gap is only a missing handoff sentence, patch that boundary and stop. Otherwise select the smallest set of primitives that can do the practice, confirm that recipe, and write one skill whose steps are those primitives and whose description sends each neighboring job to its own skill. Add the return pointer on each neighbor. If the catalog has no primitive for a part of the practice, stop and name the gap. Do not use to record session friction into whatever instruction home fits (`compound`), to revise a skill the user already named, to add a primitive to the catalog, or to carry out the practice after the skill exists.
---

# Capture Skill

The user is introducing a practice and naming the skills around it. Give that practice one skill built from the primitive catalog, or show that a skill already owns it.

A primitive is one building block. The catalog is [primitives](references/primitives.md). The new skill is a recipe: which primitives, in what order, what each one must name, and the evidence that ends the run. The written skill stands on its own. It does not point back at this catalog.

## Authority boundary

- `/capture-skill`, or a statement that a practice is missing from the skills the user names, authorizes reading those skills, reading this catalog, writing one new skill, and adding the boundary sentence on each neighbor the new skill touches.
- It does not authorize performing the practice. When the skill exists, stop. The user invokes that skill.
- It does not authorize a new primitive. A practice the catalog cannot express stops this run. Adding an entry is a separate change, from [template](references/template.md).
- It does not authorize a commit, a push, or a publish. When the home is a plugin in this workspace, continue under `release`. That prepares the version, changelog, and catalogs, and it stops before a commit unless one was already requested.
- Friction accumulated across a session, with no practice being introduced, belongs to `compound`.

## 1. Hear the practice

Take the skills the user named as the neighbors. Take the practice from what they said it does.

When they named the neighbors and did not say what the practice does, ask one question. Name each neighbor's job in the question, and ask what the practice does that those jobs do not. The answer is a boundary, not a topic.

When the message already states the practice, keep that statement. Do not ask them to restate it.

One introduction produces one skill. A second practice waits until the first skill exists, so the boundary against it is real.

Done when the practice is one sentence and the neighbor list is explicit.

## 2. Test ownership

Read the description and the handoff sections of each named skill, and of any skill those sections already point to. Search the skill directories for the practice's words.

Choose one:

- A skill already owns the practice. Stop. Name the skill and the section.
- The practice is a missing handoff between skills that already exist. Add that sentence on both sides. Do not add a skill.
- The practice has its own trigger, its own done condition, and a job none of the neighbors perform. Continue.

Done when one outcome is chosen, and the evidence is the skills that were read.

## 3. Select the primitives

Read the index in [primitives](references/primitives.md), including the recipes. A recipe there is a pattern. It is not a step you can paste as one block.

Choose the smallest set of primitives that can do the practice. For each primitive you keep, and for each one you almost kept, read that entry in its group file. Use "When to use", "When not to use", and "In a skill". Do not load every group file.

Keep a primitive only when the recipe gets worse without it. A handoff to a neighbor is not a primitive. It stays a boundary.

When a part of the practice has no entry, and it is not a handoff, stop. Name the missing primitive. Do not hide that part in a custom step, and do not add the catalog entry in this run. The [later list](references/primitives.md#left-for-later) is a list of gaps, not a list of blocks you may use.

Done when the ordered primitives, the stop evidence, and the primitives you left out are explicit, or when a missing primitive stopped the run.

## 4. Confirm the recipe

Show the recipe and wait. Fill every line the files and the message already decide. Ask only where two recipes would produce different skills.

- **Name:** kebab-case. Name the practice, not the session.
- **Job:** one sentence.
- **Home:** the directory that holds the named neighbors. In this workspace that is `plugins/<plugin>/skills/<name>/`. Neighbors in different homes make the home a line the user must confirm. Follow a junction to the real file. Do not write into a plugin cache or a marketplace copy.
- **Use when:** the phrases the user actually uses.
- **Hands off when:** one line per neighbor, naming that skill.
- **Authority:** what invoking the skill allows, and which decisions it hands to the user or to another skill.
- **Primitives:** the kept primitives, in order. Under each one, the names its "In a skill" section requires: fields, limits, evidence, and who writes them.
- **Stop:** the ending, and the evidence that ending requires.
- **Left out:** each primitive you considered and did not keep, in one line.

A confirmation or an edit is the go-ahead. A redirect replaces the recipe. Do not write the file before that.

Done when the user has confirmed the recipe.

## 5. Write

Read the nearest neighbor's `SKILL.md` and match its section pattern. Required in every case:

- `name` matches the directory.
- The description states the job, when to use the skill, and when to hand off. It names each neighbor.
- Each step is one confirmed primitive, or a handoff.
- The step states the names that primitive's entry requires, and what is true when the step is done.
- A handoff names the other skill and stops. The new skill does not contain that skill's procedure.
- A skill that `work-once` can run ends in a [work result](references/work-result.md) in tick mode. It names `next_skill` and does not load it. A direct request from a person may still continue into the next skill when the procedure says so.
- The new skill does not tell its operator to open this catalog.

On each neighbor, add one sentence at the step where the new skill takes over, and one clause in that neighbor's description. Leave the neighbor's procedure as it was.

Done when the new skill and each neighbor boundary are written, and each handoff is named on both sides.

## 6. Check

Re-read the new skill against its description and against each kept primitive's entry.

- The job in the description is the job the steps perform.
- Every step is a primitive from the confirmed recipe, or a handoff.
- The names that primitive's "In a skill" section requires appear in the step.
- No step repeats a neighbor's procedure.
- Every handoff is named on both sides.
- A skill that `work-once` can run returns a work result in tick mode and does not load `next_skill` there.
- The name, the directory, and the description agree.
- Nothing in the new skill depends on this catalog.

When the home is a plugin in this workspace, continue under `release`.

Done when the check holds, and `release` has the handoff or the home is outside this workspace.

## 7. Report

Lead with the skill name and the one-sentence job. Then list:

- the home path;
- the primitives, in order;
- the primitives left out;
- each neighbor, and the sentence that sends work to it;
- whether a skill was written, a boundary was patched, an owner was named, or a missing primitive stopped the run;
- the release version, when `release` ran.
