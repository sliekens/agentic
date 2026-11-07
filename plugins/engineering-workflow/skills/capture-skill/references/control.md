# Control

How steps are arranged, repeated, split, and ended. Control primitives are the skeleton of a recipe. Cognition and action fill the steps.

## Sequence

**Aliases:** pipeline, fixed procedure

**Summary:** Steps in a fixed order the procedure does not revisit on its own.

### Explanation

A sequence is a list of steps in an order the procedure treats as given. Step N may assume that step N−1 produced its output. There is no loop and no return to an earlier step unless another primitive says so. That strictness is the value. A reader can see what will happen, and an evaluation can tell when a run skipped a step.

Many skills are sequences with one or two loops embedded, not loops with a sequence hiding inside. Read, then edit, then check is a sequence. "Repeat the edit until the check passes" is a loop around the middle. Write the outer shape first so you do not reach for a loop when the order is knowable in advance.

A step that says "if needed, do X" has already stopped being a sequence. Either the condition is a branch with a predicate you can name, or X is always part of the sequence and the step itself decides, internally, that there is nothing to do — and records that. Implicit optionality is where required checks get skipped.

### When to use

- The order is real: you must look before you edit, and check after you edit.
- You want the skill to be predictable, reviewable, and easy to evaluate.
- The number of steps is known before the run starts.

### When not to use

- The next step depends on what the previous observation contained, in a way you cannot write down as one branch. Use a loop whose body chooses the next action.
- You know you will return to an earlier step. That return is a loop or an explicit re-plan branch. A sequence that people "just go back on" has an unwritten loop.
- The steps are independent and wall time matters. Fan-out fits better, if the join is defined.

### Pros

- Easy to review, trace, and test.
- Each step has a clear input from the step before it.
- Failures have an obvious location.

### Cons

- Brittle when the world talks back in an unexpected shape.
- Tempting to overload a step with hidden conditions so the sequence stays looking linear.
- Wastes nothing on control, and also captures no new information between steps unless a step is itself a lookup.

### Failure modes

- A failed step is followed by the next step because the sequence has no failure edge. Give each step a failure edge into escalation or a branch.
- Optional-sounding steps are skipped under time pressure, including the check.
- The sequence encodes an order that the domain does not have, and later steps undo earlier ones.

### Pairs with

[Planning](cognition.md#planning), [Stop condition](#stop-condition), [Branch](#branch), [Oracle](assurance.md#oracle)

### In a skill

Write the steps as an ordered list. For each step, name its input and its output. Name the failure edge. If a step may no-op, say what it records when it does.

## Branch

**Aliases:** router, conditional, fork

**Summary:** A predicate on current state that picks which procedure runs.

### Explanation

A branch chooses among two or more procedures using a predicate on the scratchpad or on an observation. The predicate should be something you can compute or classify into a small enum: the oracle failed this way, the selection returned this procedure name, the file exists, the user chose this option. "If it seems appropriate" is deliberation with no record of the fork.

Each arm is a procedure with its own steps and its own way back to a common continuation, or its own stop. Arms that silently rejoin with different scratchpad shapes cause the continuation to guess which arm ran. Write the fields every arm must set.

A branch with many arms that are really different skills is a router, and it should select then procedure-load, keeping the router's instruction thin. A branch with many arms that share almost all their steps wants the shared part in the sequence and the fork pushed down to the one step that differs.

### When to use

- The skill handles more than one shape of task, and you can say how to tell them apart.
- An observation has a small set of outcomes (pass, fail, blocked) with different next procedures.
- A selection or a structured generation has produced an enum the control flow must obey.

### When not to use

- You are packing unrelated skills into one procedure so there is a single entry point. Split the skills, and route with procedure load.
- There is one path plus a step that sometimes has nothing to do. Keep the sequence and let that step record a no-op.
- The predicate depends on a fact you have not looked up. The branch will classify a guess.
- The set of arms changes every week. Drive the arm from a closed list the selection step reads, so adding an arm is data plus a procedure.

### Pros

- Makes case splits visible and testable.
- Pairs with structured generation so the predicate is an enum.
- Keeps each arm simpler than a procedure full of inline conditions.

### Cons

- Arms multiply, and shared behavior drifts between them.
- A wrong predicate fails closed-looking: some arm always runs.
- Deeply nested branches become unreadability the model also mishandles.

### Failure modes

- The predicate is re-derived in prose on every turn and disagrees with the recorded enum.
- An arm leaves a scratchpad field unset and the continuation reads a value from a previous task.
- The default arm catches everything the author did not imagine, including refusals and tool errors.
- Both arms can fire because two procedures load and each contains its own copy of the branch.

### Pairs with

[Selection](cognition.md#selection), [Structured generation](cognition.md#structured-generation), [Procedure load](memory.md#procedure-load), [Scratchpad](memory.md#scratchpad)

### In a skill

Write the predicate, the enum of arms, and the fields every arm sets before rejoining. Name the default arm and what reaches it. Keep the fork at one level unless a nested fork has its own reason to exist.

## Loop

**Aliases:** retry, iteration, ReAct loop, verifier loop

**Summary:** A body repeated against a progress signal and a budget.

### Explanation

A loop repeats a body until a stop condition fires. Every loop in a skill names four things: the body, the progress signal, the maximum number of iterations (or another budget), and the exit taken when the signal does not move. A loop missing any of the four will either run once in disguise or run until something outside the recipe kills it.

The progress signal is an observation you can compare across iterations: the oracle result, the number of unresolved defects, a search cursor, a diff. "The model feels closer" is not a signal. No-progress means the signal is unchanged after a body that was supposed to change it. The right exit is usually escalation or a switch of approach, which you should write down. Spending the remaining budget on identical retries hides the stuckness inside a timeout.

Retry is a narrow loop. The body is one call, the progress signal is "a non-ambiguous success or a definitive failure," and the budget is small. Ambiguous failures (timeouts on a non-idempotent side effect) are not automatic retries. The episode log is what lets the next iteration see the arguments that just failed, which is the difference between iterating and flailing.

The body of a loop should be short enough to re-read. A loop around an entire skill is a sign the stop condition belongs to the skill and the loop belongs around one phase.

### When to use

- The exit depends on an observation you cannot know in advance: tests go green, a search finds the record, a person accepts.
- Transient tool failures have a defined retry policy and the call is safe to repeat.
- Revision should continue while an oracle is red and the iterations are still changing the oracle result.

### When not to use

- You know the count. Use a sequence of that length, or a sequence whose steps are the real stages.
- The body has no progress signal. You will burn the budget.
- Each iteration performs a side effect you cannot undo and cannot deduplicate.
- One iteration's failure is deterministic. A second try with the same inputs will fail the same way. Change the inputs on purpose (a revision) or stop.

### Pros

- Handles tasks whose length depends on the world.
- With a progress signal, stuck runs end for a reason you can trace.
- Makes retry policy a visible part of the skill.

### Cons

- Multiplies cost and the chance of collateral edits.
- A weak signal (any diff at all) counts thrashing as progress.
- Loops are where procedures quietly exceed the write set the instruction named.

### Failure modes

- The same failing call is repeated with the same arguments until the budget ends.
- The progress signal is the model's summary of progress, so it moves every turn while the oracle does not.
- The loop counts a weakened check or a deleted assertion as progress.
- Side effects accumulate: comments, files, partial migrations, duplicate messages.
- The budget is the only stop, so a success on the last allowed iteration and a failure look similar in the trace if you do not record the reason.

### Pairs with

[Stop condition](#stop-condition), [Episode log](memory.md#episode-log), [Oracle](assurance.md#oracle), [Revision](cognition.md#revision), [Scratchpad](memory.md#scratchpad)

### In a skill

Name the body, the progress signal, the budget, and the no-progress exit. Say which scratchpad fields the body reads and writes. Say whether the body's side effects are safe to repeat. Record the stop reason from the loop into the trace.

## Fan-out

**Aliases:** parallel agents, map-reduce, scatter-gather

**Summary:** Independent units run at the same time, then combined by a defined join.

### Explanation

Fan-out runs the same procedure, or different ones, on units that do not share writable state, then joins their results. The join is part of the primitive. Union, first success, all-must-pass, and reduce-by-selection are joins. "The parent will look at what came back" is a hope that the parent has a second, unnamed procedure.

Independence is the precondition. Two units that edit the same checkout, the same migrating document, or the same ticket will clobber each other or produce a merge that is larger than the original task. If the units only share read-only inputs, say so, and give each unit its own assembled context. Copying the entire parent transcript into every unit spends cost and leaks constraints meant for the parent.

Best-of-n is fan-out over identical goals in isolated contexts, joined by selection or judgment. Map over files is fan-out over different inputs, joined by an all-must-pass oracle or a parent integration step. The isolation requirements differ, and the skill should say which one it is.

The parent keeps the original goal. A unit that returns a confident answer to a different question is a failed unit, and the join should be able to reject it.

### When to use

- Units do not share writable state, and you can state the join before they start.
- Wall time matters and the units are large enough to justify the overhead.
- You want diverse attempts at a generative task and a way to pick a winner.

### When not to use

- Units would edit the same files or the same record. Sequence them, or split the writable regions until they are independent.
- The join is undefined. Define it, or you have started work you cannot finish.
- The per-unit context overhead is comparable to doing the units in one sequence.
- A partial failure has no rule. Decide in advance whether one failure fails the fan-out, gets retried, or is omitted from the join.

### Pros

- Cuts wall time on independent work.
- Isolates a bad attempt so it does not poison a shared transcript.
- Makes diversity (best of n) a deliberate setting: unit count, temperature or procedure differences, and join.

### Cons

- Cost scales with units, including the bad ones.
- Joins drop contradictions unless the join is required to surface them.
- Operationally heavier: more traces, more checkpoints, more ways to strand a unit.

### Failure modes

- Duplicate side effects because the units were not actually independent.
- The join averages or pastes contradictory results into something that looks complete.
- A unit exceeds its brief and the join treats volume as authority.
- One slow or stuck unit blocks the join because there is no per-unit budget.
- The parent redoes each unit's work while integrating, so you paid for parallelism and then for the original task.

### Pairs with

[Decomposition](cognition.md#decomposition), [Delegation](coordination.md#delegation), [Selection](cognition.md#selection), [Judgment](cognition.md#judgment), [Working context](context.md#working-context)

### In a skill

Name the unit boundary, the isolation rule (separate context, separate checkout, read-only inputs), the per-unit budget, and the join. Say what a failed or late unit does to the join. Say what the parent is allowed to change during integration.

## Stop condition

**Aliases:** termination, done criteria, budget, halt

**Summary:** The endings of a run, and the evidence each ending requires.

### Explanation

A stop condition is the set of ways a procedure is allowed to end, plus the evidence each ending requires. Typical endings are done, blocked, out of budget, refused, and no progress. The set can be smaller. It cannot be "until the model decides," because that decision is one more generation with no evidence attached.

Done cites the deliverable and the check that accepts it: the oracle passed, the schema check passed, the person confirmed, the source bindings resolve. A narrative "I have finished" is deliberation, and it can be an input to the stop decision only when the recipe says the deliverable is a judgment.

Blocked and no-progress are successful uses of the procedure when they carry the episode log and the decision needed. They should route to escalation. Out of budget ends even if the model wants to continue. Budgets that matter are the ones that can actually run away: iterations, tool calls, time, and spend. Pick the ones this skill can blow.

Refused is the ending for work the instruction or a guardrail will not do. It is different from blocked. Blocked means the procedure could not see how to proceed. Refused means it will not take this request further. Mixing them up trains people to rephrase a refusal until it becomes a block you then "solve."

Every path out of a loop, a branch, a delegation, and a wait on a person should land in this set. An implicit ending is a path you have not reviewed.

### When to use

- Any procedure that loops, delegates, calls tools, or waits on a person.
- A one-shot transform, where the ending is "one schema-valid output or a parse failure." Say that, so success and failure stay distinct.

### When not to use

- You do not omit stop conditions. You omit endings you cannot detect. An undetectable "done" will be claimed rather than observed.
- You are adding endings that mean the same thing in your trace. Collapse them so evaluation can count.

### Pros

- Makes completion and giving up both explicit.
- Gives evaluation a label per run that is comparable across changes to the skill.
- Caps cost.

### Cons

- A tight budget cuts off runs that would have succeeded one step later. You learn this from the trace and adjust on purpose.
- Evidence for done that is too weak (any non-empty file) makes the stop fire on junk.
- Several overlapping budgets are hard to explain when one of them fires.

### Failure modes

- The model emits "done" and the procedure stops without checking the deliverable.
- Budget exhaustion is reported as a successful deliverable.
- No-progress is unmeasured, so the loop runs to the iteration cap every time it gets stuck.
- A refusal is retried under a reworded goal inside the same run.
- The stop reason is missing from the trace, so you cannot tell a pass from a cap.

### Pairs with

[Deliverable](action.md#deliverable), [Oracle](assurance.md#oracle), [Loop](#loop), [Escalation](coordination.md#escalation), [Trace](assurance.md#trace)

### In a skill

List the endings. For each, write the evidence and the next owner (the user, a parent procedure, nobody). Include the budgets that apply. Require the trace to store the ending's name and the evidence.

## Checkpoint

**Aliases:** snapshot, save state, resume point

**Summary:** Enough saved state to resume without replaying the transcript.

### Explanation

A checkpoint is a saved bundle sufficient to continue the procedure: the goal, the plan position, the scratchpad, where the deliverables live, open asks, and a pointer into the episode log. Resume loads that bundle and reassembles working context from it. The transcript may still be in the trace for the author. The agent does not need to replay it to know what is true.

Checkpoint at boundaries you can name: before a confirmation or an ask, before a delegation returns, at a plan step, before compaction throws away raw history. A checkpoint after every tool call is a trace with extra cost. The trace can hold the fine grain. The checkpoint holds the resume grain.

Anything in the checkpoint that is a copy of the world (file contents, ticket status) is stale the moment the world moves. Store identifiers and read them with a fresh lookup on resume. Store decisions, constraints, and the step position as themselves, because those are the procedure's own facts.

A resumed run should say, in the trace, which checkpoint it loaded and what the fresh lookup contradicted. Silent resume from a stale file copy is how a procedure overwrites newer work.

### When to use

- The run can be interrupted, wait on a person, or outlive one context window.
- Delegation returns later and the parent must still know what it asked.
- Compaction is about to drop raw history the procedure might otherwise need.

### When not to use

- The run is one shot and the deliverable is the only state worth keeping.
- You would be snapshotting derived text the repository already holds. Store the path and the version, and read it on resume.
- You want an audit log. That is the trace and the episode log. A checkpoint is the latest resume point, and it may replace the previous one.

### Pros

- Turns pauses into continuations.
- Gives compaction permission to drop raw history.
- Makes "where the run is" a concrete object.

### Cons

- A second source of truth that can lag the repo and the transcript.
- Resume logic is real code or a real procedure, and it needs its own tests.
- Checkpointing secrets or full tool payloads stores the wrong thing for a long time.

### Failure modes

- Resume trusts copied file contents and clobbers newer edits.
- The checkpoint has a plan position whose step no longer matches the deliverable on disk.
- Open asks are dropped, and the resumed run asks again or, worse, assumes the answer.
- Two resumes from the same checkpoint both believe they own the next side effect.

### Pairs with

[Scratchpad](memory.md#scratchpad), [Ask](action.md#ask), [Confirmation](assurance.md#confirmation), [Compaction](context.md#compaction), [Fresh lookup](grounding.md#fresh-lookup)

### In a skill

Name the resume fields and the boundaries that write a checkpoint. Say which fields are identifiers to re-read, and which are procedure facts taken as current. Say what a second resume of the same checkpoint should do if the first already continued.
