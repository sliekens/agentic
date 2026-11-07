# Agent primitives

The block list for Capture Skill. A primitive is one block a skill can include or leave out. A skill is a recipe: which primitives, in what order, which state they read and write, and which evidence ends the run.

Capture Skill reads this index first, then the group file for each primitive it might keep. It writes a skill only from primitives in this catalog. The [later list](#left-for-later) names blocks this cut does not have. A practice that needs one of them stops until that primitive exists.

Architectures are recipes, and they live in [Recipes](#recipes). ReAct, plan-and-execute, RAG, and reflection stay out of the block list so a skill can swap one primitive and keep the same job.

A skill that `work-once` can run returns a [work result](work-result.md) when it stops. That file is the return protocol, not a primitive.

## How to read an entry

Each entry has the same parts:

| Part | What it decides |
| --- | --- |
| Summary | The primitive in one or two sentences. The tables below repeat this line. |
| Explanation | What it is, what it owns, and the choice you are actually making. |
| When to use | Situations where the recipe gets worse without it. |
| When not to use | Situations where it adds cost, noise, or a false sense of control, and which primitive fits instead. |
| Pros / Cons | Costs you accept even when you use it well. |
| Failure modes | How it goes wrong in practice. |
| Pairs with | Primitives that usually show up in the same recipe. |
| In a skill | What the skill text should name so the primitive is real and not a vibe. |

Aliases are industry names, included so you can find an entry from the name you already use.

## Index

### [Context](context.md)

What a turn can see, and the text that is present every time.

| Primitive | Summary |
| --- | --- |
| [Instruction](context.md#instruction) | Standing rules and a definition of done that hold on every turn, independent of this task's data. |
| [Worked examples](context.md#worked-examples) | Input and output pairs that show a result the rules only imply. |
| [Working context](context.md#working-context) | The policy for what this turn can see, and in what order. |
| [Compaction](context.md#compaction) | A shorter stand-in for prior state that keeps decisions, constraints, and open loops. |

### [Cognition](cognition.md)

What the model does before it commits to an action or an answer.

| Primitive | Summary |
| --- | --- |
| [Deliberation](cognition.md#deliberation) | A reasoning pass whose product is a commitment to the next action or the final answer. |
| [Structured generation](cognition.md#structured-generation) | Model output shaped so a parser can accept it. |
| [Planning](cognition.md#planning) | An inspectable list of steps, produced before those steps run. |
| [Decomposition](cognition.md#decomposition) | Subgoals that each have an input, an output, and a done condition. |
| [Selection](cognition.md#selection) | One choice from a closed set, judged against stated criteria. |
| [Judgment](cognition.md#judgment) | A verdict on an artifact that leaves the artifact unchanged. |
| [Critique](cognition.md#critique) | A defect list specific enough for a revision to apply. |
| [Revision](cognition.md#revision) | An edit that addresses known defects and leaves the rest of the artifact alone. |

### [Action](action.md)

How the procedure touches something outside the prompt.

| Primitive | Summary |
| --- | --- |
| [Tool call](action.md#tool-call) | A typed action whose result comes back as an observation the next step must use. |
| [Code execution](action.md#code-execution) | A program run by a runtime, which is the authority on what the program did. |
| [Deliverable](action.md#deliverable) | The object that must exist when the procedure says it is done. |
| [Ask](action.md#ask) | A pause for a specific fact or decision only a person can supply. |

### [Control](control.md)

How steps are arranged, repeated, split, and ended.

| Primitive | Summary |
| --- | --- |
| [Sequence](control.md#sequence) | Steps in a fixed order the procedure does not revisit on its own. |
| [Branch](control.md#branch) | A predicate on current state that picks which procedure runs. |
| [Loop](control.md#loop) | A body repeated against a progress signal and a budget. |
| [Fan-out](control.md#fan-out) | Independent units run at the same time, then combined by a defined join. |
| [Stop condition](control.md#stop-condition) | The endings of a run, and the evidence each ending requires. |
| [Checkpoint](control.md#checkpoint) | Enough saved state to resume without replaying the transcript. |

### [Memory](memory.md)

State the procedure writes on purpose, for later steps or later runs.

| Primitive | Summary |
| --- | --- |
| [Scratchpad](memory.md#scratchpad) | Structured fields later steps read, so they depend on declared state. |
| [Episode log](memory.md#episode-log) | An append-only record of attempts, so the run can avoid repeating them blindly. |
| [Durable memory](memory.md#durable-memory) | Facts kept for later runs, each with a source and a time. |
| [Procedure load](memory.md#procedure-load) | Bringing a stored how-to into context because its trigger matched. |

### [Grounding](grounding.md)

How claims stay tied to an authority outside the model.

| Primitive | Summary |
| --- | --- |
| [Retrieval](grounding.md#retrieval) | Bounded, identified search hits from a corpus, placed into working context. |
| [Source binding](grounding.md#source-binding) | Each material claim points at the observation that supports it. |
| [Fresh lookup](grounding.md#fresh-lookup) | A read from the system of record at the moment of the decision. |

### [Assurance](assurance.md)

How a run is checked, constrained, approved, and debugged.

| Primitive | Summary |
| --- | --- |
| [Schema check](assurance.md#schema-check) | A parser accepts or rejects shape and returns a structured error. |
| [Oracle](assurance.md#oracle) | A decider of acceptability other than the model that produced the work. |
| [Guardrail](assurance.md#guardrail) | A check on a proposed action that allows, rewrites, or blocks it before it runs. |
| [Confirmation](assurance.md#confirmation) | A person approves one fully specified action before it runs. |
| [Evaluation set](assurance.md#evaluation-set) | Fixed cases you run after every meaningful change to a skill. |
| [Trace](assurance.md#trace) | A run record for the author, separate from the state the agent reads to continue. |

### [Coordination](coordination.md)

How ownership of a goal moves between agents and people.

| Primitive | Summary |
| --- | --- |
| [Delegation](coordination.md#delegation) | A bounded subgoal given to another agent. The parent keeps the original goal. |
| [Handoff](coordination.md#handoff) | Ownership of the remaining goal moves, and the sender stops acting on it. |
| [Escalation](coordination.md#escalation) | A deliberate stop that reports the blocker, the evidence, and the decision needed. |

## Recipes

A recipe names the primitives and the order. It also names the scratchpad fields that carry state between them. If a step's input is "the conversation so far," the recipe is unfinished.

### Answer from a corpus

Use when the authority is a body of text larger than the context, and the user will act on the answer.

1. [Procedure load](memory.md#procedure-load), when a skill defines the corpus, the refusal rules, and what counts as a material claim.
2. [Retrieval](grounding.md#retrieval) with a query built from the question, a hit limit, and identifiers on every hit.
3. [Working context](context.md#working-context): the question, the hits, and the definition of done. Leave the rest of the corpus out.
4. [Structured generation](cognition.md#structured-generation) or prose, plus [source binding](grounding.md#source-binding).
5. [Schema check](assurance.md#schema-check) when the output is a record.
6. [Stop condition](control.md#stop-condition): one bound answer, or [escalation](coordination.md#escalation) when nothing in the hits supports a material claim.

Swap retrieval for a [fresh lookup](grounding.md#fresh-lookup) when you know the record's identity. Search is the wrong tool for "open this file."

### Change the repo until the check passes

Use when correctness is something a program can decide.

1. [Instruction](context.md#instruction): allowed write set, invariants, evidence for done.
2. [Fresh lookup](grounding.md#fresh-lookup) of the failing command and the files it names.
3. [Scratchpad](memory.md#scratchpad): hypothesis, files touched, last oracle result.
4. A patch or an edit as the [deliverable](action.md#deliverable). Use [code execution](action.md#code-execution) when the oracle is a command.
5. [Oracle](assurance.md#oracle). Its output is the defect list. Add a [critique](cognition.md#critique) pass only when the oracle output is too coarse to revise against.
6. [Revision](cognition.md#revision) inside a [loop](control.md#loop).
7. Stop on pass, on no progress, or on budget. On no progress, [escalate](coordination.md#escalation) with the [episode log](memory.md#episode-log).
8. [Trace](assurance.md#trace) the run.

This is the reflection / verifier-loop recipe. The oracle is what makes the loop honest. A model grading its own patch is [judgment](cognition.md#judgment), and the recipe should say so.

### Plan, then do

Use when the work has several dependent steps, a person may want to see the approach, or the run may resume later.

1. [Fresh lookup](grounding.md#fresh-lookup) wide enough to write a plan that names real files and real checks.
2. [Planning](cognition.md#planning), stored as a [deliverable](action.md#deliverable) or in the [scratchpad](memory.md#scratchpad).
3. Optional [confirmation](assurance.md#confirmation) of the plan when later steps are expensive or hard to undo.
4. [Sequence](control.md#sequence) through the steps. Each step's done test comes from the plan.
5. [Checkpoint](control.md#checkpoint) at step boundaries if the run can pause.
6. A re-plan point, written into the recipe, where an observation is allowed to replace the rest of the plan. That point is a [branch](control.md#branch) back into planning.

A plan that cannot survive contact with the first observation is deliberation with extra paperwork. Re-plan, or start with a shorter plan.

### Side effect a person must approve

Use when the action sends, deletes, pays, pushes, or is otherwise hard to undo.

1. [Fresh lookup](grounding.md#fresh-lookup) of the object the action will touch.
2. Build the [tool call](action.md#tool-call) and hold it.
3. [Guardrail](assurance.md#guardrail): allow, rewrite, or block.
4. [Confirmation](assurance.md#confirmation) of the exact arguments. A change to the arguments invalidates the approval.
5. Run the tool call.
6. Fresh lookup again, to confirm the effect matches the proposal.
7. [Trace](assurance.md#trace), including the proposal, the decision, and the observed effect.

[Ask](action.md#ask) is the wrong gate here if the action is already fully specified. Ask is for a missing fact. Confirmation is for permission.

### Split the work

Use when the goal breaks into pieces a stranger could check separately.

1. [Decomposition](cognition.md#decomposition) with a done condition per piece.
2. [Fan-out](control.md#fan-out) or [delegation](coordination.md#delegation) per piece. Delegation when a piece needs its own context, model, or checkout. Fan-out when the parent can hold the join.
3. A join you can state before the pieces start: all must pass an oracle, first success, or selection against criteria.
4. The parent writes the integrated [deliverable](action.md#deliverable). Integration is its own step.
5. [Checkpoint](control.md#checkpoint) before the join if children return later.

### Best of n

Fan-out of the same goal in isolated contexts, then [selection](cognition.md#selection) or [judgment](cognition.md#judgment), and the winner is the deliverable. Use when the task is generative and a person or a rubric can compare results. Leave it out when the attempts would share a checkout, or when one attempt plus an oracle is cheaper and stricter.

### Route to a procedure

[Selection](cognition.md#selection) or [structured generation](cognition.md#structured-generation) over a closed set of procedure names, then a [branch](control.md#branch) into [procedure load](memory.md#procedure-load). The router produces an enum, and the loader is the only thing that brings the procedure in. A router that also tries to do the task has two jobs and will do one of them badly.

### ReAct-shaped run

[Deliberation](cognition.md#deliberation), then a [tool call](action.md#tool-call), then the observation is appended, inside a [loop](control.md#loop), until a [stop condition](control.md#stop-condition). Useful when you cannot see the next action until you see the last observation. Add a [scratchpad](memory.md#scratchpad) and an [episode log](memory.md#episode-log) as soon as the loop can repeat a failed call. Add an [oracle](assurance.md#oracle) as soon as "the model thinks it is done" is the only stop you have.

## Adding an entry

Capture Skill does not add a primitive in the same run as a new skill. When a practice needs a block this catalog does not have, the capture stops. Add the primitive in its own change.

Copy [template.md](template.md). Link the entry from the index in this file, and keep the summary line identical in both places. If the new behavior is a common combination of primitives that already exist, add a recipe instead.

A new primitive earns an entry when it has its own when-to-use. When the guidance would always say to use two primitives together, write a recipe.

## Left for later

Named here so the next pass can extend the catalog on purpose:

- Idempotency keys and compensation after a side effect lands wrong
- Dry run, where the action is fully specified and then explained with no side effect
- Redaction and secret handling as their own primitive, beyond a note on traces and memory
- Caching of tool results, and the invalidation rule that must come with it
- Rollback of a deliverable to a named earlier state
- Sampling policy (temperature and related knobs) as a procedure setting
- Spend, latency, and tool-call budgets once a single stop-condition budget is too coarse
- A stored model of a specific user's preferences, which is a sharper and riskier form of durable memory
- Multimodal observation (screens, images, audio) as an input type with its own failure modes
- Queue and priority, when more than one goal is active

Debate and voting are expressible today as fan-out plus judgment or selection. They can become named recipes when a real skill needs a join rule spelled out.
