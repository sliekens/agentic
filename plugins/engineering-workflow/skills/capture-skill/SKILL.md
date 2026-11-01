---
name: capture-skill
description: Capture a practice the user is introducing as one new skill, after testing that none of the skills they name already own it. Use when the user says they have skills for some jobs but something is missing, says a practice is not captured or is not covered, says nothing captures this, or introduces a workflow that should become a skill — including "we have skills for X, Y, and Z, but I'm missing something." Read the named skills first. If one owns the practice, name it and stop. If the gap is only a missing handoff sentence, patch that boundary and stop. Otherwise confirm the shape, write one skill whose description and steps send each neighboring job to its own skill, and add the return pointer on each neighbor. Do not use to record session friction into whatever instruction home fits (`compound`), to revise a skill the user already named, or to carry out the practice after the skill exists.
---

# Capture Skill

The user is introducing a practice and naming the skills around it. Give that practice one skill, or show that a skill already owns it.

## Authority boundary

- `/capture-skill`, or a statement that a practice is missing from the skills the user names, authorizes reading those skills, writing one new skill, and adding the boundary sentence on each neighbor the new skill touches.
- It does not authorize performing the practice. When the skill exists, stop. The user invokes that skill.
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

## 3. Confirm the shape

Show the shape and wait. Fill every line the files and the message already decide. Ask only where two shapes would produce different skills.

- **Name:** kebab-case. Name the practice, not the session.
- **Job:** one sentence.
- **Home:** the directory that holds the named neighbors. In this workspace that is `plugins/<plugin>/skills/<name>/`. Neighbors in different homes make the home a line the user must confirm. Follow a junction to the real file. Do not write into a plugin cache or a marketplace copy.
- **Use when:** the phrases the user actually uses.
- **Hands off when:** one line per neighbor, naming that skill.
- **Authority:** what invoking the skill allows, and which decisions it hands to the user or to another skill.
- **Steps:** the procedure. Each step states what is true when it is done.

A confirmation or an edit is the go-ahead. A redirect replaces the shape. Do not write the file before that.

Done when the user has confirmed the shape.

## 4. Write

Read the nearest neighbor's `SKILL.md` and match its section pattern. Required in every case:

- `name` matches the directory.
- The description states the job, when to use the skill, and when to hand off. It names each neighbor.
- Each step ends with what is true when the step is done.
- A handoff names the other skill and stops. The new skill does not contain that skill's procedure.

On each neighbor, add one sentence at the step where the new skill takes over, and one clause in that neighbor's description. Leave the neighbor's procedure as it was.

Done when the new skill and each neighbor boundary are written, and each handoff is named on both sides.

## 5. Check

Re-read the new skill against its description.

- The job in the description is the job the steps perform.
- No step repeats a neighbor's procedure.
- Every handoff is named on both sides.
- The name, the directory, and the description agree.

When the home is a plugin in this workspace, continue under `release`.

Done when the check holds, and `release` has the handoff or the home is outside this workspace.

## 6. Report

Lead with the skill name and the one-sentence job. Then list:

- the home path;
- each neighbor, and the sentence that sends work to it;
- whether a skill was written, a boundary was patched, or an owner was named;
- the release version, when `release` ran.
