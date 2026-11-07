# Memory

State the procedure writes on purpose. Working context is what a turn can see. Memory is how that state is kept so a later step or a later run can load it without reconstructing it from chat.

## Scratchpad

**Aliases:** agent state, working memory, blackboard

**Summary:** Structured fields later steps read, so they depend on declared state.

### Explanation

A scratchpad is a small schema the procedure writes on purpose: current hypothesis, files touched, last oracle result, remaining subgoals, the option the user picked. Later steps read fields. They do not infer those facts from the transcript. That is the whole difference between a scratchpad and "it's in the conversation."

Keep the schema tight. A scratchpad that can hold anything becomes a second transcript with none of the transcript's order. Each field should have a writer (which step sets it) and a reader (which step requires it). A field with no reader is a diary. A step that needs a fact stored in no field will invent one from the conversation, which is the failure the scratchpad exists to prevent.

The scratchpad holds current belief. History belongs in the episode log. When a hypothesis is replaced, overwrite the field and append the old value to the log if you will need to know what was tried. Two "current hypotheses" in one pad means the schema is missing a slot.

Initialize the pad at the start of the run, even with empty values, so a step can tell "not yet known" from "missing because we forgot to write the field."

### When to use

- The procedure has more than one step, or any loop.
- A branch predicate or a stop condition needs a value more precise than prose.
- You will compact or delegate and still need the current facts.

### When not to use

- The procedure is a single generation whose output is the deliverable. The deliverable is the state.
- You are copying every tool observation into the pad. Store the conclusion and an identifier, and leave the payload in the trace.
- A field would duplicate the system of record. Store the identifier and use a fresh lookup.

### Pros

- Later steps have a contract.
- Branches, stops, and resumes can key off fields.
- Makes "what the agent currently believes" inspectable.

### Cons

- Another schema to design and to keep in sync with the skill.
- Stale fields are trusted because they look structured.
- If steps can write the same field freely, the pad stops being an explanation of the run.

### Failure modes

- A step reads a field the previous step never set and treats the empty value as a real answer.
- The pad and the repo diverge, and the pad wins.
- The hypothesis field is appended to forever, so every abandoned theory stays "current."
- A delegated child returns a different schema and the parent maps it by guesswork.

### Pairs with

[Episode log](#episode-log), [Checkpoint](control.md#checkpoint), [Branch](control.md#branch), [Working context](context.md#working-context)

### In a skill

Write the field list, the initial value of each, which step writes it, and which step reads it. Say which fields are identifiers for a fresh lookup on resume. Require a step that needs state to take it from the pad.

## Episode log

**Aliases:** attempt history, trajectory, reflection memory

**Summary:** An append-only record of attempts, so the run can avoid repeating them blindly.

### Explanation

An episode log is append-only. Each entry is one attempt: the action taken, a summary of the observation or a handle to it, and the decision that followed. The agent reads the log to avoid repeating a failed attempt. A person reads it when the trace is too low-level to see the story of the run.

The log is history. The scratchpad is current state. Mixing them produces a pad you are afraid to overwrite and a log that pretends to be current. When the procedure changes its mind, the log gets a new entry and the pad gets a new value.

Entries should be specific enough to recognize a repeat: tool name and the arguments that mattered, or the defect the revision was aiming at, plus the outcome. "Tried a fix, tests still failed" will not stop the next iteration from trying the same fix. You also do not need every token. Raw observations live in the trace. The log stores the decision and a handle.

Loops, search, and revision are where the log pays for itself. A single-pass sequence can rely on the trace alone, because nothing in the procedure will look back and choose differently.

### When to use

- A loop can repeat a failed attempt.
- The procedure searches, revises, or retries, and "what we already tried" changes the next action.
- Escalation should show a person the attempts, separate from raw logs.

### When not to use

- You would be logging every token or every file read. Store decisions and handles.
- Nothing in the recipe reads the log. You wanted a trace.
- The log is being used as the system of record for a fact that lives in a file or a ticket.

### Pros

- Stops identical retries from looking like progress.
- Gives escalation and compaction a ready-made history of decisions.
- Survives working-context trimming if the log itself is kept and re-injected in bounded form.

### Cons

- A long log becomes the thing you must compact, one level up.
- Poor entries create false confidence that an approach was tried.
- Writing the log costs a schema and a habit of filling it in. Optional logs stay empty.

### Failure modes

- Entries omit the arguments, so a repeat with the same arguments looks new.
- The log is rewritten or truncated by compaction and loses the rejected alternatives.
- The procedure reads only the latest entry and cycles between two failures.
- A failed attempt is logged as a conclusion about the world ("this API cannot do X") from one error string.

### Pairs with

[Loop](control.md#loop), [Scratchpad](#scratchpad), [Revision](cognition.md#revision), [Escalation](coordination.md#escalation), [Compaction](context.md#compaction)

### In a skill

Define the entry schema: action, arguments or target, observation handle, decision. Say when an entry is written (every loop iteration, every tool error, every abandoned hypothesis). When you inject the log back into context, say the bound (last N, or only entries for the current subgoal) and the headings compaction must preserve.

## Durable memory

**Aliases:** long-term memory, user memory, cross-session memory

**Summary:** Facts kept for later runs, each with a source and a time.

### Explanation

Durable memory is a store later runs load on purpose: preferences the user stated, project facts that are expensive to rediscover, decisions the user asked you to remember. A write is an explicit step. A read happens during context assembly, under the working-context policy, as a claim with a source and a time. A paragraph the model felt like keeping is not a memory. It is an unreviewed write.

Memory is the wrong shelf for anything a system of record can answer. A file, a ticket, a schema, and a config will change, and a remembered copy will win until it causes a visible bug. Store "the migration check command is in package.json" only if you have decided that rediscovering it is worth less than the risk of staleness — and even then, store the pointer, and look up the command.

Secrets, credentials, and one-task facts do not belong here. One-task facts belong in the scratchpad or the checkpoint. A secret belongs in a secret store, and the memory may hold the fact that a secret exists and how the procedure obtains a reference to it.

Contradictions need a rule: newest user statement wins, or the memory is flagged and the procedure asks, or a fresh lookup wins over memory always. Pick one. The default if you pick none is that whichever sentence was assembled closer to the decision wins, which is an accident of order.

Forget is part of the primitive. A memory you cannot delete or supersede becomes policy.

### When to use

- The user corrected the same thing across separate runs and asked, in substance, that it stick.
- A stable fact is expensive or easy to miss, and you store a pointer plus the source.
- A preference changes how many skills should behave, and it has an owner who can edit it.

### When not to use

- The fact is in a system of record you can read. Use a fresh lookup.
- The fact is true for this task only. Use the scratchpad.
- The fact may be a secret or personal data the procedure does not need in the prompt.
- You want to remember the model's own conclusion from a previous run. That writes a guess into policy. Remember user-stated decisions and verified pointers.

### Pros

- Removes repeated corrections the user can see.
- Carries stable preferences into new runs without a longer base instruction.
- A sourced, dated memory can be audited and deleted.

### Cons

- Stale memories override fresher evidence when the recipe lets them.
- The store accumulates contradictions and near-duplicates.
- People cannot see why a run behaved oddly when the cause is a memory they forgot existed.

### Failure modes

- A hallucinated conclusion is written as a memory and followed later.
- An old preference beats a newer instruction or a newer user message.
- A memory about one project loads into another.
- Deleted facts remain in compacted summaries and traces that get reloaded.
- The procedure asks the user the same question it already stored, or the reverse: it never asks because a wrong memory answered.

### Pairs with

[Working context](context.md#working-context), [Fresh lookup](grounding.md#fresh-lookup), [Instruction](context.md#instruction), [Ask](action.md#ask)

### In a skill

Say whether the skill may read durable memory, which keys it reads, and whether it may write. A write names the source (user statement, with a pointer) and the time. State the precedence: fresh lookup, then the current user message, then memory, unless you have a reason to order it differently. Say how a memory is superseded.

## Procedure load

**Aliases:** skill invocation, playbook, prompt module

**Summary:** Bringing a stored how-to into context because its trigger matched.

### Explanation

Procedure load brings a stored procedure's instruction, examples, and recipe into working context because the current situation matched its trigger. The trigger is a rule or a selection over a closed set of procedure names. The load is what makes a skill actually fire. Until the load, the skill is a file on disk the model has not been asked to follow.

Load one procedure for the current goal unless the loaded procedure itself says to load another. Eagerly loading every skill that might apply crowds out the task and creates contradictory instructions. A router recipe — select a name, then load that procedure — keeps the choice and the instructions separate.

A loaded procedure is allowed to be specific and long in ways the base instruction should not be. That is the bargain. In exchange, the procedure names its own deliverable, stop conditions, and tools. A procedure that only contains advice, with no recipe, is an instruction fragment. Those belong inside a real procedure or in the base instruction, and loading them as if they were skills makes the run sound guided while no step is specified.

Triggers overlap in practice. Two procedures that both claim "when the user asks for a test" will both want to load. The trigger text is part of the design, and overlaps are bugs in the catalog of procedures, fixed by narrowing the triggers or by an explicit priority in the router.

Unloading matters at phase boundaries. Once the procedure's deliverable is accepted, drop its examples and step text so they do not keep steering the next phase.

### When to use

- The how-to is reusable and longer than the base instruction should be.
- Different situations need different recipes, tools, or definitions of done.
- You want the behavior under version control, review, and an evaluation set of its own.

### When not to use

- The procedure is a few lines that always apply. Put them in the instruction.
- Triggers overlap and you have no router. Narrow them before adding another load.
- You are loading a procedure "in case," without a matched trigger. Assemble the task.
- The stored text is reference material the procedure should search. That is retrieval, and the procedure that uses it is what you load.

### Pros

- Keeps the base instruction small and the specialized behavior reviewable.
- Lets different tasks carry different tools, budgets, and done tests.
- Gives evaluation a unit: this procedure, these cases.

### Cons

- Trigger mistakes load the wrong recipe with confidence.
- Loaded text can contradict the user goal or another loaded procedure.
- A large procedure load leaves little room for the observations the procedure needs.

### Failure modes

- Two procedures load and the model blends their steps.
- The trigger matches on vocabulary ("test") and the situation was a question about an existing test.
- The procedure's examples dominate a task that is a poor fit, and the task is pulled toward the example.
- A child agent is delegated the goal and is not given the procedure the parent was following, or is given two.

### Pairs with

[Instruction](context.md#instruction), [Selection](cognition.md#selection), [Working context](context.md#working-context), [Evaluation set](assurance.md#evaluation-set)

### In a skill

Write the trigger as a situation, including a situation that should not fire it when the two are easy to confuse. Keep the body to instruction, examples, and a recipe that names its primitives. Say which tools and budgets come in with the load, and when the load is dropped.
