# Action

How a procedure touches something outside the prompt, and the two pauses that are themselves actions: producing the thing the task was for, and asking a person for something the procedure cannot supply.

## Tool call

**Aliases:** function call, action, tool use

**Summary:** A typed action whose result comes back as an observation the next step must use.

### Explanation

A tool call invokes a declared capability with typed arguments. A runtime executes it and returns an observation: a payload, an error, or a side effect plus its result. The next step treats that observation as evidence. The model's expectation of what the tool would return is not evidence, and it should not survive into the scratchpad once the observation is back.

The tool's description and schema are part of the procedure's interface. Models call what the description appears to promise. A vague description ("handles files") produces systematically wrong calls that still validate. A description that names the one job, the arguments that change behavior, and the errors the caller must handle is doing as much work as the instruction.

Prefer a tool that already expresses the operation over generated code that reimplements it. The tool has a narrower argument list, a clearer trace, and a place to hang a guardrail. Code execution is the right primitive when the operation is specific to this task or when the thing you want back is the behavior of a program.

Side effects want an idempotency story. A retry of "create," "send," or "pay" is a second action unless the tool treats a repeated key as the same action. Read-only tools can be retried. Say which class each tool is in.

### When to use

- The fact lives outside the model, or the step changes the world.
- The operation is stable enough to name, describe, and schema-check.
- You want the action and its observation in the trace as a pair.

### When not to use

- You are transforming text you already hold. That is generation, revision, or compaction.
- The "tool" is a prompt in disguise. That is another cognition step or a delegation, and wrapping it as a tool hides the second model call inside an observation.
- The side effect is hard to undo and the recipe has no guardrail or confirmation on it.
- A fresh lookup or an existing read-only tool returns the fact, and the proposed call would shell out to rediscover it.

### Pros

- Grounds the run in observations and makes actions auditable.
- Schemas constrain the action space the model can express.
- Errors come back as data the loop can branch on.

### Cons

- The real design work moves into tool descriptions and schemas.
- Large observations crowd out the goal unless working-context policy trims them.
- A rich tool list causes confident calls to the wrong tool.

### Failure modes

- The model calls a tool to look busy, including reads of files it already has.
- Arguments parse and still name the wrong object, account, or environment.
- A non-idempotent call is retried after an ambiguous timeout and happens twice.
- The description's promise is trusted over a contradictory observation.
- An error payload is summarized away, and the retry repeats the same arguments.

### Pairs with

[Structured generation](cognition.md#structured-generation), [Schema check](assurance.md#schema-check), [Guardrail](assurance.md#guardrail), [Fresh lookup](grounding.md#fresh-lookup), [Episode log](memory.md#episode-log)

### In a skill

For each tool the skill may call, say what it is for, whether it is read-only or a side effect, and whether a retry is safe. Say what the caller must do with each documented error. If the tool list is discovered at runtime, say how selection chooses among the discovered set.

## Code execution

**Aliases:** interpreter, sandbox, REPL, shell

**Summary:** A program run by a runtime, which is the authority on what the program did.

### Explanation

Code execution means the model writes or selects a program, a runtime runs it, and the stdout, stderr, files, and exit status come back as the observation. The runtime is the authority on what happened. The model's prediction of the output is a hypothesis that the observation replaces.

This is the empirical primitive. Use it when the question is "what does this data do," "does this parse," or "does the check pass," and when the transformation is precise in a way prompts are not (a rename across a tree, a calculation, a migration dry run). The program is also a deliverable when the skill's job is to produce code. Then execution is the oracle, and the program remains the thing you keep.

Generated code has a wider action space than a tool call. The guardrail here is the runtime's privilege, filesystem, and network, plus any command policy you add. A sandbox that can do everything the developer can do is not a boundary. Match the privilege to the step: read the repo, run the test, or, separately and under confirmation, touch shared state.

Reading the observation is part of the primitive. A successful exit status says the process exited cleanly. It does not say the answer is correct, the right test ran, or the assertion was meaningful. The recipe should say which outputs count as the oracle and which are logs.

### When to use

- The question is settled by running something: a test, a query, a repro, a parser.
- The transformation is awkward or unsafe to do by editing from memory.
- You need a reproducible command a person can re-run, and that command is part of the deliverable or the trace.

### When not to use

- A tool already performs the operation with a narrower schema. Call the tool.
- The code would need privileges you would not give a new hire for this step.
- The task is a judgment, a summary, or a message. Execution will be a detour into incidental scripts.
- You are executing to discover a fact a read-only lookup returns directly.

### Pros

- Turns guesses about behavior into observations.
- Handles precise transforms that prompts garble.
- Produces commands and scripts a person can replay.

### Cons

- The action space is as wide as the privileges you granted.
- Generated scripts accumulate hidden assumptions about the machine.
- Debugging the script can hijack the original task.

### Failure modes

- The model edits the code toward a green exit without reading the failure.
- The check is weakened until it passes, and the exit status is reported as success.
- A script depends on local state the trace does not record, so the run cannot be replayed.
- Execution is used where a file read belonged, and the command is broader than the question (a recursive delete dressed as a search).

### Pairs with

[Oracle](assurance.md#oracle), [Guardrail](assurance.md#guardrail), [Tool call](#tool-call), [Confirmation](assurance.md#confirmation), [Trace](assurance.md#trace)

### In a skill

Say which runtime, which paths it may read and write, and whether it has a network. Say which command is the oracle and what in its output counts as pass or fail. Require the procedure to record the command and the result in the trace, and to read the failure output before the next edit.

## Deliverable

**Aliases:** artifact, work product, definition of done object

**Summary:** The object that must exist when the procedure says it is done.

### Explanation

The deliverable is the object the procedure promises to leave behind: a patch, a file, a decision record, a sent message, a test that failed and then passed, a plan a person accepted. Naming it before the work starts separates "the model talked about the task" from "the task produced a thing you can point at." The stop condition's done branch should cite the deliverable and the evidence on it, such as an oracle result or a confirmation.

Some procedures produce an intermediate deliverable per phase (a plan, then a patch). Name each one, and say which is the product of the skill and which is scaffolding the scratchpad can drop at the end. Scaffolding that escapes into the repository is a delivery bug.

A decision inside a larger procedure often needs no separate document. The deliverable of a selection is the chosen identifier recorded in the scratchpad. Insisting on a writeup for every intermediate choice creates paperwork the next step does not read. Match the weight of the artifact to the weight of the decision.

### When to use

- The skill claims to finish something a person or another procedure will use.
- You need a clear target for the oracle, the diff, and the evaluation set.
- Delegation needs a contract for what the child hands back.

### When not to use

- The step's product is a choice or a verdict that the scratchpad can hold. A document would duplicate that field.
- You are naming a deliverable you cannot check. Tighten it until an oracle, a schema, or a person can accept it.
- The run is exploratory and the honest product is an episode log of what you tried. Call that the deliverable, and stop promising a fix.

### Pros

- Makes done observable.
- Gives delegation and handoff a contract.
- Gives the evaluation set an object to score.

### Cons

- A prematurely frozen deliverable shape distorts the task (every question becomes a memo).
- Producing the artifact can detach from the goal if the oracle checks the artifact's shape and misses its effect.
- Multiple unnamed outputs appear anyway (files, comments, follow-up tasks) if the skill only names one of them.

### Failure modes

- The procedure stops after describing the deliverable, and the object does not exist.
- The object exists and does not satisfy the reason the task was opened.
- Side files and drive-by refactors ship alongside the named deliverable with no check.
- An intermediate plan is treated as the final deliverable and the implementation never starts.

### Pairs with

[Stop condition](control.md#stop-condition), [Oracle](assurance.md#oracle), [Delegation](coordination.md#delegation), [Revision](cognition.md#revision)

### In a skill

Name the deliverable, where it lives, and the evidence that accepts it. Name scaffolding that must not remain. If there are required companion outputs (a test, a changelog line, a migration), list them as part of the same deliverable.

## Ask

**Aliases:** clarification, elicitation, question to the user

**Summary:** A pause for a specific fact or decision only a person can supply.

### Explanation

Ask stops the procedure and requests one missing input from a person. A useful ask names the decision, the options when you have them, what will change based on the answer, and the default you will take if the skill allows a default. Then the procedure checkpoints and waits. The answer is written into the scratchpad and treated as an input, with its source, so later steps can see why the goal changed shape.

Ask is for facts and goal-shaping decisions the procedure cannot look up and was not given: which of two product behaviors is intended, a credential the user must provide through a secret channel, a scope choice that is genuinely theirs. Confirmation is a different pause. It approves an action you have already fully specified. If you cannot yet write the action, you are asking. A yes/no prompt in that situation hides the missing piece.

Questions have an order. Ask the one that can delete the rest of the plan. A batch of questions is justified when the answers are independent and you would otherwise pay a round trip per question. Even then, each question should be one you would still need after any answer to the others.

The procedure should do the investigation a person would need in order to answer. "What should I do?" after no lookup is a handoff of the original task. An ask that follows a fresh lookup can say what you found and what remains ambiguous.

### When to use

- Two reasonable next actions differ in a way the user owns, and the rest of the recipe changes with the choice.
- The fact is private or only exists in someone's head, and no tool has it.
- Continuing on your best guess could spend the budget on the wrong goal.

### When not to use

- The fact is one lookup away. Read it.
- You already have criteria that decide the question. Apply them and record the decision.
- You are asking permission for a fully specified action. Use confirmation.
- The user cannot answer without the investigation the skill was supposed to do. Do the investigation, then ask the residual question.
- You are asking in order to avoid a reversible attempt the skill was asked to make.

### Pros

- Prevents a long run aimed at the wrong goal.
- Leaves a record of a human decision and the options that were on the table.
- Pairs with checkpoint so the wait is a pause, and the run can resume cleanly.

### Cons

- Each ask costs a round trip and breaks flow.
- Questions can become a way to push judgment back to the user.
- Badly posed options anchor the user on a framing you chose too early.

### Failure modes

- The question is open-ended and the answer cannot be written into a scratchpad field.
- The procedure asks and, in parallel or earlier, already did the thing.
- A batch includes questions the first answer would have made irrelevant.
- The default fires accidentally because the ask did not say what "no reply" means.
- The ask requests a secret in the transcript. The secret belongs in a private input channel, and the scratchpad stores only a reference.

### Pairs with

[Checkpoint](control.md#checkpoint), [Confirmation](assurance.md#confirmation), [Escalation](coordination.md#escalation), [Scratchpad](memory.md#scratchpad)

### In a skill

Say which decisions must be asked, which may be decided from named criteria, and whether a default exists. Require the question to include the options, the consequence of each, and where the answer is stored. Say that the run waits.
