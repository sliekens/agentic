# Context

What a turn can see, and the standing text that is present on every turn.

## Instruction

**Aliases:** system prompt, policy, standing orders

**Summary:** Standing rules and a definition of done that hold on every turn, independent of this task's data.

### Explanation

An instruction is the text you can write before you know the task. It names the role the procedure is playing, the invariants, the actions that are allowed, and the evidence that counts as done. It is loaded on every turn, including after compaction, and inside a delegated child when that child is still carrying out this procedure.

Task data stays out of it. The bug, the path, the user's latest sentence, and any retrieved passage change per run and belong in working context. An instruction that absorbs a task teaches the next run a stale goal.

Write invariants as conditions a later check can apply. "Be careful with migrations" does not change outputs in a way an evaluation set can catch. "A migration includes an up and a down, and the procedure runs the project's migration check before it stops" can become an oracle. Keep a single wording of each rule. The same rule copied into the instruction, the examples, and the oracle will drift, and the model will follow whichever copy sits closest to the decision.

### When to use

- The rule is true for every invocation of the procedure.
- A run that forgot the rule would look finished and be wrong.
- You can state the rule without looking at the task.
- A person should be able to change the procedure's behavior by editing this text and re-running the evaluation set.

### When not to use

- The content depends on this task. Assemble it into working context.
- The content is a document the procedure should find. Use retrieval, or a fresh lookup when you know which record.
- The content shows a format or a taste that is awkward to specify. Use a worked example.
- The rule exists to stop one specific side effect. Put that check in a guardrail on the action, and keep the instruction for rules that shape the whole run.

### Pros

- Stable across tasks, so a person can review it and a runtime can cache it.
- The place where behavior is changed on purpose.
- Gives later primitives a policy to point at. The oracle checks the invariants named here. The stop condition uses the definition of done named here.

### Cons

- It competes with the task for attention. Past a few screens, later rules get uneven compliance.
- Vague sentences feel like safety and leave behavior unchanged.
- A long instruction is hard to keep consistent with the evaluation set.

### Failure modes

- The instruction and the user goal disagree, the model picks one, and the trace looks like obedience.
- An example buried in the instruction is copied into an unrelated task, including its names and incidental numbers.
- Two loaded procedures disagree. The run follows the instruction closer to the decision.
- Done is described as a feeling ("make it good"), so no stop condition can fire on evidence.

### Pairs with

[Worked examples](#worked-examples), [Stop condition](control.md#stop-condition), [Oracle](assurance.md#oracle), [Procedure load](memory.md#procedure-load)

### In a skill

Put the instruction above the steps. Name the allowed write set, the invariants, and the evidence for done. If a sentence is only true for one step, move it to that step.

## Worked examples

**Aliases:** few-shot examples, demonstrations

**Summary:** Input and output pairs that show a result the rules only imply.

### Explanation

A worked example is a concrete input paired with a concrete output you endorse, placed in context so the model can match a shape, a level of detail, or a judgment that the instruction states only in the abstract. Examples teach format and edge handling faster than rules do. They also teach their accidents: the names you picked, the length, the hedging, the order of sections.

Two examples that differ in the way you care about are worth more than five that differ in window dressing. A bad example you include as a warning needs a label that says it is the case to avoid, and it still sometimes gets imitated. Prefer a good example that already handles the edge.

Examples are part of the procedure, so they belong in review the same way the instruction does. When the endorsed output changes, update the example in the same change as the rule. An example that is really a test fixture belongs in the evaluation set, and you may still put a short version in context if the model needs to see the shape.

### When to use

- The output has a shape you can show more reliably than you can specify.
- Reviewers disagree about the words of the rule and agree when they see a sample.
- The usual failure is right content in the wrong form.
- A boundary case (empty input, refusal, partial data) keeps getting handled in a way you have already rejected.

### When not to use

- A schema and an oracle already force the shape. An example that only repeats them spends context and can contradict them.
- You have one example. It will be copied, including parts you considered incidental.
- The example contains real customer data, secrets, or a long artifact. Describe the shape, or use a trimmed fixture.
- The example is longer than the task. The model answers the example's question.

### Pros

- Strong effect on format, granularity, and voice.
- Makes a subjective standard concrete enough to argue about.
- Cheap to add once you have a case you trust.

### Cons

- Surface features leak into unrelated tasks.
- Examples rot quietly after the rule changes.
- You cannot unit-test "what the model will generalize" from the example. You only see the damage in the evaluation set.

### Failure modes

- The model copies a name, a date, a count, or a file path out of the example and into the deliverable.
- A negative example is followed as a template.
- Examples disagree with the instruction, and the example wins because it is more specific.
- The set of examples covers the happy path only, so every unusual task is pulled back toward that path.

### Pairs with

[Instruction](#instruction), [Evaluation set](assurance.md#evaluation-set), [Structured generation](cognition.md#structured-generation)

### In a skill

Put examples after the instruction and before the task data. For each one, a one-line note should say which property it is there to show. Keep them short enough that the task still dominates the turn. When you add a case to the evaluation set because the skill missed it, decide whether a trimmed twin belongs here too.

## Working context

**Aliases:** prompt assembly, context window contents

**Summary:** The policy for what this turn can see, and in what order.

### Explanation

Working context is the assembled input for this turn: the goal, the constraints discovered so far, the observations the next decision depends on, any loaded procedure, and the scratchpad. The primitive is the assembly policy. The model's maximum window is a limit you design against, and it is a property of the runtime.

Every item in the assembly should have a reason tied to the next decision. "It might be relevant" is how transcripts, entire trees, and old tool dumps end up crowding out the goal. Order matters in practice: material at the very start and the very end is followed more reliably than material in the middle. Put the goal, the definition of done, and the active constraints in those positions. Put a large observation behind a short conclusion plus an identifier when the next step needs the conclusion, and include the raw observation when the next step will quote, edit, or dispute it.

Assembly is a procedure, so it can be wrong in a reviewable way. Write down what is always included, what is included by trigger, and what is replaced by a compaction or by a scratchpad field. After a delegation, a pause, or a compaction, re-assembly is how the next turn learns what is still true.

### When to use

- On every turn. The design work is the policy, and a skill that skips it has an implicit policy of "whatever is already in the transcript."
- When a child agent, a resumed checkpoint, or a new phase needs a brief that a stranger could act on.
- When you can name, for each included item, the decision that would go wrong without it.

### When not to use

- Growing the context to postpone a decision. If the next step is a lookup or a judgment, add the one observation that step needs.
- Including a second copy of state that the scratchpad already holds. The copies will diverge.
- Passing the parent's whole transcript into a delegated child. Assemble the child a brief: goal, constraints, inputs, done condition.
- Relying on an earlier message as the current value of a file, a ticket, or a schema. That is a fresh-lookup situation.

### Pros

- Makes "what the model knew" a design choice you can trace and evaluate.
- Keeps expensive observations out until a step needs them.
- Gives compaction and delegation a clear input contract.

### Cons

- A careful policy takes design time, and a sloppy one fails quietly.
- Over-trimming removes the constraint that would have prevented a bad action.
- Re-assembly rules themselves become a source of bugs when they drop an open loop.

### Failure modes

- The goal is present once at the top of a long run and is effectively gone by the time of the edit.
- A compacted summary and a raw observation disagree, and both are in context.
- Tool noise from an abandoned approach fills the middle of the window and the model resumes that approach.
- The same file is included three ways (chat mention, retrieval hit, fresh read) with three different contents.

### Pairs with

[Instruction](#instruction), [Compaction](#compaction), [Scratchpad](memory.md#scratchpad), [Fresh lookup](grounding.md#fresh-lookup), [Retrieval](grounding.md#retrieval)

### In a skill

Name the always-on items, the per-phase items, and the order. Name the maximum you will include for large observations (hit count, line range, log lines) and what you store instead when you omit the raw text. Say which scratchpad fields replace history.

## Compaction

**Aliases:** context summarization, rolling summary

**Summary:** A shorter stand-in for prior state that keeps decisions, constraints, and open loops.

### Explanation

Compaction replaces older turns, tool output, or files with a shorter text the next turn will treat as the record of what happened. Its job is to save room while keeping the state the recipe still needs: decisions and why, constraints, rejected options and why they were rejected, names and identifiers, and open loops. Chatter, superseded drafts, and raw tool noise can go once their conclusion is recorded somewhere the recipe reads.

A summary written for a person is a deliverable. Compaction is a different product: a stand-in for state, consumed by the procedure. Hold it to that standard. "We decided to use the existing parser" is incomplete if the decision was conditional. The condition is the part a later step will violate.

Write compaction at defined points (a phase boundary, a budget threshold, before a delegation) through a fixed set of headings, so the result is comparable across runs. The episode log and the scratchpad should already hold the structured version of the important facts. Compaction then becomes a rendering of those, which is much safer than asking the model to remember the transcript from scratch.

Exact strings the next edit will touch — paths, quotes, numbers, error text — belong in the scratchpad or in a fresh lookup, with the compaction pointing at them. A paraphrase of an error message is a good way to chase a bug that was never in the file.

### When to use

- The run is long enough that new observations are displacing the goal or the constraints.
- You are about to delegate, and the child needs a brief.
- The same facts are being re-read as raw tool output on every iteration of a loop.
- You are resuming from a checkpoint and the transcript is the wrong source of state.

### When not to use

- The next step will edit a region whose exact current text exists only in the history. Read the file.
- A number, a path, a quote, or an error string must stay exact and is stored only inside the text you are about to compact.
- The transcript itself is the deliverable, as in an evaluation of the conversation.
- The scratchpad already holds every field later steps read. Compaction would create a second, looser copy.

### Pros

- Lets a long procedure keep its constraints in view.
- Produces the brief a delegated child actually needs.
- Forces a moment where the run states what it believes.

### Cons

- Any stand-in can drop the one clause that mattered.
- Compaction spends a turn and can be wrong in the same ways as any other generation.
- Once the raw history is gone, you cannot audit the compaction against it unless the trace kept the original.

### Failure modes

- Rejected alternatives disappear, and a later step proposes them again.
- A conditional decision is stored as an unconditional one.
- The compaction cites a file, and later steps treat the citation's paraphrase as the file's contents.
- Open asks and failed attempts are summarized away, so the resumed run repeats them.

### Pairs with

[Working context](#working-context), [Scratchpad](memory.md#scratchpad), [Episode log](memory.md#episode-log), [Checkpoint](control.md#checkpoint), [Delegation](coordination.md#delegation)

### In a skill

Name the trigger (phase boundary, token threshold, before delegation). Name the headings the compaction must fill: decisions, constraints, rejected options, identifiers, open loops. Say which facts are copied from the scratchpad verbatim, and which raw artifacts remain reachable by fresh lookup.
