# Assurance

How a run is checked, constrained, approved, and later debugged. Assurance primitives sit outside the draft. When the same pass both writes the deliverable and declares it good, you do not have one of these yet.

## Schema check

**Aliases:** validation, parse check, contract check

**Summary:** A parser accepts or rejects shape and returns a structured error.

### Explanation

A schema check is a non-model parser that accepts or rejects an output against a declared shape: types, required fields, enums, ranges, and simple cross-field constraints you can express without knowing the task. Failure returns a structured error a revision step can see. The check says nothing about whether the content is true, useful, or safe. A beautiful object can still be the wrong answer.

Put the check on every boundary where a later consumer would otherwise throw a worse error or, quieter, misread a field. Tool arguments, structured generation, child-agent results, and scratchpad writes are the usual boundaries. A check that runs only in evaluation will tell you the skill is drifting after users have already seen the drift.

Rejection should be specific: the field, the constraint, the value. "Invalid JSON" is enough for a parse failure and too coarse for a missing field you could have named. The loop that consumes the error needs to be able to change the output, not just retry the same generation.

Shape constraints that encode business truth ("status is always active") will force the model to lie in order to parse. Keep business truth in the oracle or the instruction. Keep the schema to the contract between steps.

### When to use

- Structured generation, tool arguments, or a delegated result cross a boundary.
- A downstream step would fail later, opaquely, on the same structure.
- You want evaluation to distinguish "wrong shape" from "wrong answer."

### When not to use

- As a stand-in for an oracle. Passing the schema is not passing the task.
- The output is prose whose quality is rhetorical. Check the few structural musts (a required section exists) and judge or exemplify the rest.
- You are adding fields to the schema so the check has more to do. Every required field will be filled.

### Pros

- Deterministic, cheap, and easy to explain in a trace.
- Turns a class of failures into revision input.
- Documents the contract between steps.

### Cons

- Only sees shape. Over-trusting it creates a green bar that means "parsed."
- Strict required fields encourage placeholders.
- Schemas drift from the consumers if more than one copy exists.

### Failure modes

- Placeholder strings pass a present-and-non-empty check.
- Two fields conflict and each field is valid alone.
- The error returned to the model omits the field name, so the revision perturbs the whole object.
- The check is duplicated in a prompt ("make sure you return JSON") and the parser is never run.
- A schema change without an evaluation-set update makes old fixtures fail for a reason nobody connects to the contract.

### Pairs with

[Structured generation](cognition.md#structured-generation), [Tool call](action.md#tool-call), [Revision](cognition.md#revision), [Oracle](#oracle)

### In a skill

Point at the schema. Say which boundary runs it. Require the error to name the field and the constraint. Say that a pass means "well shaped" and name the oracle or judgment that means "acceptable."

## Oracle

**Aliases:** verifier, test, checker, invariant

**Summary:** A decider of acceptability other than the model that produced the work.

### Explanation

An oracle decides whether an artifact is acceptable using something other than the opinion of the model that produced it. Tests, typecheckers, linters, diff rules, invariants, a query with an expected row, a second tool reading the effect of the first: all of these count when their result does not depend on the author's reasoning. The oracle returns pass or fail plus evidence. That pair goes into the scratchpad and the episode log, and it is what a revision loop consumes.

A model grading a draft is judgment, including when you label the pass "verifier." Judgment is legitimate when no oracle exists. Calling it an oracle lets a recipe pretend it has an independent check. If you use a second model as a judge, record it as judgment and keep its context separate from the author's deliberation.

Design the oracle so it can fail. A test that always passes, an invariant that checks a tautology, or a diff rule the procedure can satisfy by deleting the check, is not an oracle for the task. When the procedure can edit the oracle (the tests, the lint config), the recipe has to say whether that edit is in the allowed write set. Often the right split is: the procedure may add tests, and it may not weaken existing assertions. That rule itself needs a guardrail or a diff check, because it will not survive as a sentence in the instruction alone.

Oracle output should be specific enough to revise against. A boolean is enough for the stop condition and too little for the edit. Keep the failing lines.

### When to use

- You can state correctness independently of the draft: it compiles, the test fails then passes, the migration has a down, the output matches a fixture.
- A loop will revise until done. The oracle is what "until" means.
- You need evaluation to score behavior the model's self-report would inflate.

### When not to use

- You cannot build an independent check. Use judgment or confirmation, and say so in the skill. A fake oracle is worse than a named judgment because the trace will say "verified."
- The check requires taste and a rubric. That is judgment. You can still put an oracle in front of it for the mechanical musts.
- The oracle is so expensive or flaky that its result is not a progress signal. Fix the oracle, or stop gating the loop on it, before you tune the agent.

### Pros

- Independent of the author's fluency.
- Gives loops a real progress signal and stop conditions a real done.
- Catches regressions the procedure would otherwise describe as improvements.

### Cons

- Good oracles are harder to write than the skill text.
- A narrow oracle lets the procedure pass while missing the actual goal (the test suite covers the wrong case).
- Flaky or slow oracles poison the progress signal and the evaluation set.

### Failure modes

- The procedure weakens the test, deletes the assertion, or special-cases the fixture.
- The oracle checks a proxy (file exists, command exits 0) and the task required a behavior.
- Failure evidence is compacted to "tests failed," and revision guesses which test.
- The same model is asked "did the tests pass" after running nothing.
- An oracle that the procedure can edit is edited in the same change as the code, with no rule separating the two.

### Pairs with

[Loop](control.md#loop), [Revision](cognition.md#revision), [Stop condition](control.md#stop-condition), [Code execution](action.md#code-execution), [Judgment](cognition.md#judgment)

### In a skill

Name the oracle command or check, what it reads, and which part of its output is the evidence. Say whether the procedure may modify the oracle. Define pass, fail, and flake or infrastructure failure as different scratchpad values with different exits. Fail and flake should not share an exit.

## Guardrail

**Aliases:** policy check, allowlist, pre-execution hook

**Summary:** A check on a proposed action that allows, rewrites, or blocks it before it runs.

### Explanation

A guardrail inspects a proposed action and returns allow, rewrite, or block before any side effect. Typical checks are path allowlists, command denylists, size limits, "no push to the default branch," and redaction of a secret that was about to enter a tool argument. The guardrail should be narrower and more deterministic than the agent it constrains. A second full agent asked "is this okay?" is judgment wearing a guardrail's name, and it will fail open in ways you cannot replay.

Rewrite is for mechanical fixes: adding a required flag, redirecting a write into the allowed directory, stripping a secret from logs. The rewritten action is the one you run, and it is the one you confirm if confirmation is also in the recipe. A rewrite the trace does not show is a hidden action.

Block ends that attempt. The procedure should treat a block as a distinct observation, usually routing to escalation or to an alternative that stays inside the policy. A loop that treats a block as a generic error will probe nearby arguments until one slips through. That probing is a failure mode of the recipe, and the guardrail alone cannot fix it. The episode log has to record the block and the stop condition has to refuse to retry the same blocked class.

Put task policy that defines "good work" in the instruction and the oracle. Put action policy that defines "actions we will not take" in the guardrail. When the guardrail encodes the real goal ("the patch must be correct"), the agent learns the guardrail's wording instead of the goal, and you have built an oracle in the wrong place.

### When to use

- A tool or a runtime can do harm the skill does not need: arbitrary paths, network, push, send, delete.
- The boundary is expressible as allow, rewrite, or block on the action's arguments.
- You want a check you can replay without the model.

### When not to use

- The check is "is the work good?" Use an oracle or judgment.
- The guardrail always allows. Delete it. A decorative check teaches the wrong lesson in the trace.
- The policy is a one-off preference for this task. An ask or an instruction line covers it. A guardrail is for a boundary you want even when the prompt says otherwise.
- You would need the guardrail to understand the whole plan. Narrow the tool's privileges instead, so the forbidden action is not expressible.

### Pros

- Stops a class of side effects independent of how persuasive the prompt was.
- Deterministic rules are explainable and testable.
- Rewrite can make the safe action the easy action.

### Cons

- A narrow guardrail does not make the allowed actions wise.
- Rules on argument text are bypassed by equivalent forms (a different shell quoting, a relative path).
- Authors start to rely on the guardrail for task correctness, which it does not provide.

### Failure modes

- The check runs after the side effect, as a log.
- A block is retried with trivially different arguments until it passes.
- The rewrite changes the meaning of the action and the procedure does not look at the new arguments.
- Allowlists grow until they include the dangerous case they were added to stop.
- Two guardrails disagree and the runtime applies them in an order the skill does not document.

### Pairs with

[Tool call](action.md#tool-call), [Code execution](action.md#code-execution), [Confirmation](#confirmation), [Escalation](coordination.md#escalation)

### In a skill

Name the actions covered, the allow / rewrite / block rules, and the exit on block. Say that a rewrite replaces the proposal in the trace and in any confirmation. Say that a blocked class is not retried inside the loop.

## Confirmation

**Aliases:** human approval, human-in-the-loop gate, permission

**Summary:** A person approves one fully specified action before it runs.

### Explanation

Confirmation shows a person one proposed action and waits for approval before running it. The proposal includes the tool or command, the arguments, and the effect in words a person can check ("push current branch to origin", with the branch name). Approval covers that proposal. If a guardrail rewrites an argument, or the procedure changes its mind, the previous approval does not carry. Resume loads the checkpoint, shows the new proposal, and waits again.

Confirmation is permission. [Ask](action.md#ask) is how you get a missing fact or a goal decision. If the action is not fully specified, you cannot confirm it; you would be asking the person to approve a direction, which is an ask about the goal. Skills often need both at different points: an ask to choose the target, later a confirmation to send.

Granularity is the design choice. Confirming every file read trains the person to click through. Confirming an entire skill with one up-front "go ahead" does not approve the specific push the skill invents twenty minutes later, unless the skill's contract really is "you may take these classes of action without coming back," which is a different and explicit setting. Write the granularity down: which action classes wait, which proceed.

The wait is a checkpoint. The procedure does not keep working on a side effect "in the meantime." Read-only investigation while waiting is fine when it does not change the proposal. If it does, the proposal is rebuilt and confirmed again.

A default of proceed on silence is a side effect without approval. If the skill has a timeout, the timeout's exit is escalation or abandon, and the action does not run.

### When to use

- The action is hard or expensive to undo: send, delete, pay, push, migrate shared state, write to a shared system.
- The user asked to approve this class of action.
- A guardrail allowed the action and a person is still the right final check because the arguments require judgment.

### When not to use

- The action is a routine reversible read. Confirming it creates rubber-stamp fatigue.
- The proposal is incomplete. Ask until you can specify it, or keep investigating.
- The skill's contract already grants this class, and the user can see the trace. Extra confirms will be ignored, which trains a bad reflex. Revisit the contract if the class was drawn too wide.
- You are confirming a judgment ("is this prose good?") with a yes/no on the whole draft and no criterion. Show the draft and ask for the decision you actually need.

### Pros

- Puts a person on the irreversible edge, looking at the real arguments.
- Creates a clear record of who approved what.
- Composes with guardrails: the machine enforces the boundary, the person approves the instance.

### Cons

- Stops the run and depends on a person's attention.
- A vague proposal produces a vague yes.
- Too many confirms, and the yes stops meaning the person looked.

### Failure modes

- The proposal describes the intention and hides an argument (the destination, the flag, the path).
- Approval of an older proposal is reused after the arguments change.
- Silence, or a message about something else, is taken as approval.
- The procedure runs the action and then asks.
- The confirm UI shows a summary the procedure wrote and the summary does not match the arguments that will run.

### Pairs with

[Guardrail](#guardrail), [Ask](action.md#ask), [Checkpoint](control.md#checkpoint), [Tool call](action.md#tool-call)

### In a skill

List the action classes that require confirmation. Require the proposal to show the exact arguments and the effect. Say that any edit to the proposal invalidates the approval, that the run checkpoints and waits, and that timeout does not run the action.

## Evaluation set

**Aliases:** evals, golden set, regression cases

**Summary:** Fixed cases you run after every meaningful change to a skill.

### Explanation

An evaluation set is a fixed collection of inputs with expected outcomes, plus a way to run the procedure and score it. You change the skill, the instruction, the examples, the tools, or the model, and then you run the set. A single happy path is a demo. The set contains the cases the skill claims to handle, the cases it must refuse or escalate, and the cases that have gone wrong in real use.

Each case needs an input, the context assembly the case assumes, and a check that is as independent as you can make it. Exact match works for structured fields and fails for prose. For prose, score the properties you care about (mentions the constraint, cites a source that entails the claim, stays inside the write set) with an oracle where possible and a rubric where you must. Store the expected tool-call shape when "which tool" is the behavior under test, separate from the words of the final answer.

Runs vary. A case that flips between pass and fail without a skill change is a flaky case, and it will teach you to ignore the set. Fix the case or the oracle, or report the pass rate over repeats, before you treat a one-point move as a regression.

Start the set when the recipe stabilizes enough that a frozen input means something. Add a case for every production miss you decide is in scope. That is how the set stays connected to the skill's real failure modes. A set written entirely up front canonizes your first guesses.

Version the set with the skill. A change to the expected outcome is a product decision, visible in review, and it is different from a change that makes a previously failing case pass.

### When to use

- The skill will be edited more than once.
- Behavior is easy to regress: triggers, format, which tool is called, when the skill refuses, when it escalates.
- You are about to change the model, the instruction, or the examples and want to see what moved.

### When not to use

- You are still discovering the task. A frozen set would canonize a guess. Capture notes, and freeze a case once you believe it.
- You cannot say what a pass is. Build the oracle or the rubric first. An evaluation set without a check is a folder of anecdotes.
- The case requires live side effects against shared systems. Use a fixture or a dry environment. An eval that sends real messages will be turned off.

### Pros

- Makes skill edits reviewable as behavior changes.
- Stops example-driven tweaks from silently breaking last month's case.
- Gives you a place to put production misses so they stay fixed.

### Cons

- Cases take time to write and to keep honest.
- A set that under-represents refusals and edge cases produces a skill that only demos well.
- Model variance can drown a real regression if you look at a single run of a small set.

### Failure modes

- The expected output was copied from a model run the author liked, including its mistakes.
- Cases share a template the skill memorizes, and a slightly different real task fails.
- The set is never run after the first week.
- Scoring uses the same procedure as the skill, so both drift together.
- A production miss is fixed in the instruction and never added as a case, so the next edit restores it.

### Pairs with

[Oracle](#oracle), [Procedure load](memory.md#procedure-load), [Worked examples](context.md#worked-examples), [Trace](#trace)

### In a skill

Point at the set and the command that runs it. For each case, keep the input, the expected decision (tool, refusal, deliverable properties), and the check. When you change the skill because of a real miss, add the case in the same change. Note which cases are flaky and what repeat count you use.

## Trace

**Aliases:** observability, run log, audit log

**Summary:** A run record for the author, separate from the state the agent reads to continue.

### Explanation

A trace is the record of a run aimed at the person who maintains the procedure: procedure name and version, model, assembled instruction identity, tool names and arguments, observation handles or hashes, branch taken, stop reason, token and time and spend, confirmation decisions, and guardrail results. The agent does not need the trace to continue. The scratchpad and the episode log are what it reads. You need the trace to debug a run, to build the next evaluation case, and to explain a side effect after the fact.

Keep the trace complete enough to reconstruct the control flow, and keep payloads out by default when they are large or sensitive. Store a hash and a pointer with a retention rule. A trace that inlines every file read becomes a second datastore you did not mean to operate, and it will eventually get compacted by someone who needed disk, taking the debugging value with it.

Redact secrets at the source, before the trace write. A later scrub of the log store will miss the copy that landed in a compacted summary, a checkpoint, or a delegated child's brief. The guardrail and the trace share this job.

A trace nobody looks at is a cost. The minimum habit that makes it a primitive is: when a run goes wrong, the stop reason and the last few actions are where you look, and when you change the skill, you can compare a trace from before and after on the same evaluation case.

### When to use

- Any skill you expect to run more than once or that can have a side effect.
- Any time you delegate, confirm, loop, or spend, because those are the runs you will have to explain.

### When not to use

- You do not skip tracing for a skill you will keep. You do skip storing raw payloads and secrets.
- You are about to feed the trace back into the agent as its memory. That collapses the trace into the episode log and usually blows the context. Distill a log entry on purpose.

### Pros

- Makes runs debuggable and side effects explainable.
- Supplies the raw material for new evaluation cases.
- Lets you see which primitive actually fired (which branch, which stop).

### Cons

- Storage, retention, and redaction are real obligations.
- A noisy trace is as hard to read as no trace. Structure it around control flow.
- Traces can contain more sensitive data than the deliverable if you capture arguments carelessly.

### Failure modes

- The stop reason and the model identity are missing, so two unlike runs look comparable.
- Secrets and personal data land in arguments and observation bodies.
- Payload retention is forever, by default, with no owner.
- The trace is the only copy of a decision that should have been in the scratchpad, so the agent cannot see it on resume and the author can.
- Evaluation runs and production runs are not distinguished, and you "fix" the skill against a fixture artifact.

### Pairs with

[Episode log](memory.md#episode-log), [Stop condition](control.md#stop-condition), [Guardrail](#guardrail), [Evaluation set](#evaluation-set)

### In a skill

List the fields every run must record, including procedure version, stop reason, and the actions taken. Say what is stored by handle, what is redacted, and how long payloads live. Say that the agent continues from the scratchpad and the episode log, and that the trace is for the author.
