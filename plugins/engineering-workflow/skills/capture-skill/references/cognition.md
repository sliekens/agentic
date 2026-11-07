# Cognition

What the model does on a turn before it commits to an action or an answer. These primitives describe the product of the turn. They leave the side effect to [Action](action.md) and the arrangement of turns to [Control](control.md).

## Deliberation

**Aliases:** chain of thought, reasoning, scratch reasoning

**Summary:** A reasoning pass whose product is a commitment to the next action or the final answer.

### Explanation

Deliberation is a pass that looks at the observations already in context and produces the next commitment: which tool to call, which option to pick, or what the answer is. The reasoning can stay private to the model or be written into the scratchpad. What makes it this primitive, and a defined step, is that the commitment is supposed to depend on the observations.

A plan is an artifact you can tick, revise, and resume. Deliberation can contain a sketch of steps and then disappear into the action. Use deliberation when you need a careful next step. Use planning when the sequence itself must be reviewed or followed later.

Deliberation is a poor substitute for a missing fact. A fluent reason about the contents of a file is still a guess. If the commitment depends on current state, the previous primitive in the recipe is a fresh lookup or a tool call, and deliberation starts from the observation.

### When to use

- The next action is expensive, shared, or hard to undo, and more than one observation bears on it.
- The task has a common wrong answer that a moment of comparison would reject.
- Intermediate claims need to be visible so a later critique or a person can check them.
- The recipe is a ReAct-shaped loop and the action should follow from the latest observation.

### When not to use

- The step is a mechanical transform with a schema check. Deliberation adds tokens and a place for invented justification.
- The missing piece is a current fact in a system of record. Look it up, then deliberate if a decision remains.
- Latency dominates and the step is a routing choice over a small enum. Structured generation into that enum is enough.
- You would be deliberating because the recipe has no oracle. Add the check, and keep deliberation for the step that proposes a fix.

### Pros

- Catches some inconsistencies before a side effect.
- Makes intermediate claims available to critique, trace, and evaluation.
- Pairs naturally with a loop that must choose the next tool from new evidence.

### Cons

- Spends tokens and time on every use, including easy turns.
- Confident reasoning about absent evidence looks like evidence to later steps.
- Private reasoning cannot be reviewed. Written reasoning that nobody checks becomes a story the rest of the run trusts.

### Failure modes

- The reasoning cites a constraint that was never in context, and the action follows the citation.
- A long deliberation ends by ignoring the observation it was meant to use.
- The model states a conclusion first and produces reasons for it, which the trace records as analysis.
- Written deliberation is compacted into "we concluded X," and the observations behind it are gone.

### Pairs with

[Fresh lookup](grounding.md#fresh-lookup), [Tool call](action.md#tool-call), [Scratchpad](memory.md#scratchpad), [Planning](#planning)

### In a skill

Say whether the reasoning is written down, and if so into which scratchpad field. Say which observations the commitment must account for. Forbid the step from introducing facts that are only in the reasoning.

## Structured generation

**Aliases:** structured output, JSON mode, schema-constrained decoding

**Summary:** Model output shaped so a parser can accept it.

### Explanation

Structured generation asks the model for an output a parser can accept: an object matching a schema, a tool-argument record, or a value from an enum. The model still produces it. Acceptance is a separate step, the schema check. Keeping the two apart matters because a model can look constrained and still return a shape the downstream code will misread.

Use a schema when the next consumer is code, a branch, a record, or a tool. The fields should be ones you are willing to handle in that consumer. A field nobody reads becomes a place for the model to park a guess that later looks official.

Prose for a person often wants a looser shape: headings you name in the instruction, plus a worked example. Forcing that prose through a deep object schema flattens emphasis and invites filler keys. When you need both a human-readable note and a machine-readable verdict, emit both as named fields, and say which one the next step is allowed to trust.

### When to use

- The next step branches on the output, stores it, or passes it to a tool.
- You need an enum (procedure name, stop reason, verdict) and free text would require another parser.
- Evaluation compares outputs field by field.

### When not to use

- The deliverable is prose whose structure is rhetorical. Specify the sections in the instruction and show one worked example.
- You do not yet know the fields. A premature schema invents categories the procedure then has to honor.
- The schema duplicates an oracle. Emitting `{"tests_pass": true}` does not make the tests pass.

### Pros

- Gives branches, joins, and tool calls a stable input.
- Makes evaluation and traces comparable across runs.
- Failures become parse errors the loop can show back to a revision step.

### Cons

- Schema design becomes part of the procedure's real interface, and a bad field is a standing bug.
- Models fill required fields with plausible placeholders when they lack the fact.
- Strict schemas are awkward for outputs that are legitimately partial. You need an explicit way to say "unknown."

### Failure modes

- A required string is filled with "N/A" or a hedged sentence, and the schema check passes.
- Two fields disagree (verdict pass, defect list non-empty) and the consumer reads only one.
- The schema allows free-text fields long enough to hide an unstructured answer, and every caller uses those fields.
- A downstream step treats a successful parse as a successful task.

### Pairs with

[Schema check](assurance.md#schema-check), [Selection](#selection), [Branch](control.md#branch), [Tool call](action.md#tool-call)

### In a skill

Include the schema or point at it. For every field, say what consumes it. Include an explicit empty or unknown value where partial answers are allowed. Say which field is authoritative when two fields can conflict.

## Planning

**Aliases:** plan-and-execute, task list

**Summary:** An inspectable list of steps, produced before those steps run.

### Explanation

A plan is an ordered artifact: steps, the dependency between them, and a way to tell that a step is done. You produce it before the side effects it describes. A person can read it, the procedure can tick it, and a later turn can throw the rest of it out. Deliberation may sketch the same steps and then lose them inside the answer. If you need the sketch tomorrow, it had to be a plan.

Plans rot as soon as the environment answers back. The useful plan says where re-planning is allowed: after which observation the remaining steps may be replaced. A recipe with no re-plan point will keep executing step four after step two failed. A recipe that re-plans every turn never had a plan; it has a ReAct loop wearing a list.

The grain of a step should match something you can check. "Handle the backend" cannot be ticked. "Add a failing test for the empty-cart case and run it" can. Detail past that grain turns the plan into a second implementation, and the implementation then drifts from the plan.

### When to use

- The work has more than a few dependent steps.
- A person needs to see or approve the approach before expensive steps run.
- The run may pause, and resume must know which step is current.
- Some steps are risky enough that you want them visible while they are still proposals.

### When not to use

- The task is a single tool call or a single edit. Write the call.
- The environment changes faster than a long plan can track. Plan only the next phase, with a fresh lookup at the boundary.
- Planning is standing in for a lookup you have not done. The plan will name files and failures that a read would have settled.
- The steps have no done test. You have a motive, and the loop will not know when to advance.

### Pros

- Makes the approach reviewable before side effects.
- Gives checkpoints, confirmation, and escalation a shared notion of progress.
- Surfaces missing information at plan time, when changing course is cheap.

### Cons

- Takes a turn up front, which is waste on small tasks.
- A stale plan confidently walks into a world that has moved.
- Over-detailed plans duplicate the work and then diverge from it.

### Failure modes

- Steps are not checkable, so the procedure marks them done by assertion.
- A failed step is followed by the next step as if the failure were a note.
- The plan is never updated, and the scratchpad's "current step" points at work that was abandoned.
- Re-planning happens silently inside deliberation, and the written plan no longer describes the run.

### Pairs with

[Sequence](control.md#sequence), [Checkpoint](control.md#checkpoint), [Confirmation](assurance.md#confirmation), [Fresh lookup](grounding.md#fresh-lookup), [Decomposition](#decomposition)

### In a skill

Say where the plan is stored, what a step must contain (action, dependency, done test), and which observations authorize replacing the unread steps. Say whether a person confirms the plan.

## Decomposition

**Aliases:** task breakdown, subgoals

**Summary:** Subgoals that each have an input, an output, and a done condition.

### Explanation

Decomposition cuts one goal into pieces that can be specified on their own. A piece has an input, an output, and a done condition someone who never saw the parent transcript could check. Sequencing the pieces is planning. Running them together is fan-out. Giving one to another agent is delegation. You can also decompose and then run the pieces one after another in a single context, when the reason to split was to understand the goal.

Split along a boundary you can name: a file, a failing test, a user journey, a record, a module. The parent must be able to integrate the outputs. If the only integration story is "the model will merge it," the decomposition is unfinished. Pieces that share a writable checkout, a single migrating schema, or an invariant neither piece can see are one piece that has been drawn as two.

Decomposition is also how a goal that does not fit in one working context becomes tractable. Each child gets a brief assembled for that subgoal. The parent keeps the original goal, the interface between the pieces, and the join.

### When to use

- The goal is naturally several deliverables, or one deliverable with independent regions.
- You want fan-out or delegation, and you can state a done condition per unit.
- One context cannot hold every artifact the job touches.
- The parent needs to understand the shape of the work before committing to an approach.

### When not to use

- The pieces share an invariant, and splitting creates integration work larger than the task.
- You cannot say how you would know a piece is done.
- The split follows a team boundary or a directory boundary that cuts through the change.
- The task is small enough that the brief for each piece would repeat the whole parent context.

### Pros

- Makes large goals delegable and parallel.
- Forces done conditions into the open before the work starts.
- Localizes failure: one bad piece does not require redoing the others, if the join says so.

### Cons

- Integration is real work and is easy to leave unnamed.
- Over-splitting spends more context on briefs than the pieces were worth.
- Pieces drift from the parent goal when a constraint lived only in the parent's transcript.

### Failure modes

- Two pieces both "fix" the same lines and the join silently picks one.
- A piece succeeds at a narrower goal than the parent asked, because the brief dropped a constraint.
- The parent has no join rule and pastes the child outputs together.
- Decomposition is redone on every turn, so the pieces never stabilize enough to execute.

### Pairs with

[Planning](#planning), [Fan-out](control.md#fan-out), [Delegation](coordination.md#delegation), [Working context](context.md#working-context)

### In a skill

Say what boundary a piece is cut on, the brief each piece receives, the done condition, and the join that integrates outputs. Say which state pieces may write, and which state only the parent may write.

## Selection

**Aliases:** routing, choice, classification over a closed set

**Summary:** One choice from a closed set, judged against stated criteria.

### Explanation

Selection picks one element from a set that is listed in the context. The set is closed: the procedure does not get to add an option at decision time. The criteria are stated. The output is the chosen element and the criterion it satisfied. If you also want a full ranking or a score, that is judgment, and selection can be the last step that turns the top of the ranking into the choice the branch will take.

An open-ended "pick a good approach" is generation. Calling it selection hides the fact that the model invented the candidate set, which is the actual decision. When the candidates are not known up front, add a step that proposes them, check that they are real (they name a tool that exists, a file that was read, a procedure you ship), and only then select.

Ties need a rule you write down: prefer the reversible option, prefer the option the oracle can check, or escalate. A model left to break a tie will produce a reason that looks better than the rule you would have chosen on purpose.

### When to use

- Routing to a procedure, a tool, a template, or a candidate fix.
- Choosing the winner of a best-of-n fan-out.
- Any branch whose predicate you want written as "which of these."

### When not to use

- The set is open. Add a proposal step, or call the activity what it is: generation of an approach.
- You have no criteria. The model will supply one that fits the choice it already likes.
- A single option survives your constraints. Take it, and record the constraints.
- You need every fitting option preserved. Selection discards the rest. Use judgment with a keep-list, or keep the set for a join.

### Pros

- Turns a fuzzy fork into an enum the branch and the trace can record.
- Makes criteria explicit enough to argue with and to evaluate.
- Composes cleanly with structured generation.

### Cons

- A closed set can omit the option the task actually needed, and the selector will still pick.
- Criteria that overlap produce unstable choices across runs.
- The stated reason can be a rationalization of a choice made on surface similarity to a worked example.

### Failure modes

- The model names an option that was not in the set, and a loose parser accepts it.
- All options are weak and selection still returns a winner with high confidence.
- The criterion cited does not distinguish the winner from the runner-up.
- Selection is re-run after new evidence and the recipe has no rule for sticking with or replacing the previous choice.

### Pairs with

[Structured generation](#structured-generation), [Branch](control.md#branch), [Judgment](#judgment), [Procedure load](memory.md#procedure-load)

### In a skill

List the allowed options or say which runtime list is the set (installed procedures, discovered tools). Write the criteria in order, including the tie-break. Require the output to quote the chosen option's identifier from the set.

## Judgment

**Aliases:** rubric scoring, critique-free evaluation, LLM-as-judge

**Summary:** A verdict on an artifact that leaves the artifact unchanged.

### Explanation

Judgment applies criteria to an artifact and returns a verdict: a score, a rank, or a pass/fail, with each point tied to a criterion. It does not modify the artifact. Critique lists defects for someone to fix. An oracle decides from something other than a model's opinion. Judgment is the model's opinion, made comparable by a rubric.

The useful form is a second pass with a different procedure, and when you can afford it a different model, that sees the artifact and the criteria and does not see the author's deliberation. Same-model judgment of a draft the model just wrote tends to defend the draft. Use it when you have no oracle and the cost of another pass matters less than a completely unreviewed output, and record in the trace that the judge was the author.

Scores need anchors. "Rate quality from 1 to 5" drifts. A rubric line that says what a 1 looks like and what a 5 looks like, ideally with a worked example, drifts less. A pass/fail judgment should name the criterion that failed. A bare "fail" gives revision nothing to apply and gives the evaluation set nothing to regress on.

### When to use

- You are comparing options that an oracle cannot score (tone, structure of an explanation, fit to a brief).
- You need a gate before a person sees the work, and you can write criteria a second pass can apply.
- The verdict must be recorded without changing the artifact, so the author can respond.

### When not to use

- A test, a typechecker, a diff rule, or a query with an expected answer can decide. That is an oracle, and it is stricter.
- The criteria are taste and you have no anchored rubric or examples. The verdict will be arbitrary and stable-looking.
- You already know the defects and need them fixed. Critique plus revision does that job. A score in between adds a number nobody uses.
- The judge would be the same pass that wrote the draft, on a high-stakes deliverable. Get a second procedure or a person.

### Pros

- Applies to outputs no program can fully decide.
- Produces a record you can calibrate against people over time.
- Leaves the artifact intact, so the verdict can be disputed.

### Cons

- It is an opinion, and it inherits the model's biases and the rubric's blind spots.
- Unanchored scales feel quantitative.
- Author-as-judge inflates pass rates in a way a rising score will not reveal.

### Failure modes

- The judge rewards resemblance to the worked example, including irrelevant features.
- Pass/fail hides which criterion failed, and revision churns on the wrong axis.
- Scores creep upward across iterations of one draft without the draft changing on the criteria.
- The judge treats fluent prose as evidence that the underlying claim was checked.

### Pairs with

[Worked examples](context.md#worked-examples), [Selection](#selection), [Oracle](assurance.md#oracle), [Evaluation set](assurance.md#evaluation-set)

### In a skill

Write the rubric with anchors. Say who judges (author pass, second procedure, different model, person) and which context the judge must not see. Require each point of the verdict to name a criterion. Say what a failing verdict triggers: revision, escalation, or another sample in a best-of-n join.

## Critique

**Aliases:** reflection, defect list, review comments

**Summary:** A defect list specific enough for a revision to apply.

### Explanation

A critique names defects in an existing artifact. Each defect says where it is, which criterion it fails, and what change would remove it. The critique does not declare the work finished and does not apply the change. That split is the point: a defect list can be checked, trimmed, or handed to a person before anyone rewrites the artifact.

An oracle that already points at a line and a rule is a better defect list than a model's critique of the same failure. Use the oracle output directly as the input to revision. Add a critique pass when the oracle is silent or coarse ("command failed," "the explanation is hard to follow") and a revision needs a sharper target.

Critiques expand to fill the request. If you ask for issues, you will get issues, including nits that a correct artifact did not need. Bound it: defects that violate a named criterion, or the single defect that blocks the done condition. Everything else waits.

### When to use

- Revision is a separate step, or a person will accept the defect list before any edit.
- The failure signal is real and too coarse to edit against.
- You want a record of what was wrong, separate from the next version of the artifact.

### When not to use

- The oracle output is already a location plus a rule. Feed that to revision.
- The artifact passed its oracle and meets the brief. A critique pass will invent nits and feed a loop that churns.
- You have no artifact yet. You would be critiquing a plan or a hypothesis, which is deliberation or judgment.
- The same author immediately critiques its own draft with no new evidence. The list will track the draft's own doubts, which are a weak sample of its faults.

### Pros

- Gives revision a target and the episode log a reason.
- A person can edit the list before any rewrite.
- Easier to spot a wrong critique than to spot a wrong silent rewrite.

### Cons

- Adds a turn, and unbounded critiques create work.
- Suggested changes can be wrong and still get applied because they are specific.
- Nitpicking a passing artifact makes the procedure look busy while quality stays flat or drops.

### Failure modes

- Defects have no location ("the design is unclear"), so revision rewrites at random.
- The suggested change contradicts an invariant or a passing check.
- The list restates the oracle in vaguer words and loses the line number.
- Old defects stay in the list after they are fixed, and the next revision "fixes" them again.

### Pairs with

[Revision](#revision), [Oracle](assurance.md#oracle), [Judgment](#judgment), [Episode log](memory.md#episode-log)

### In a skill

Say what may appear in the list (which criteria, which artifacts) and the maximum number of defects you will act on per iteration. Require location, criterion, and a concrete change. Say whether a person sees the list first. Drop defects the latest oracle no longer supports.

## Revision

**Aliases:** rewrite, patch, self-refine

**Summary:** An edit that addresses known defects and leaves the rest of the artifact alone.

### Explanation

Revision takes an existing artifact plus a defect list or a failed check, and produces a new version that addresses those defects. The rest of the artifact stays. That preservation is the difference between revision and generating the artifact again. A fresh generation can be the right move when the structure is wrong. Calling that move a revision implies a continuity you should then check with a diff.

The input list bounds the edit. A revision that also "cleans up" neighboring code will fix the note and break a part that was passing, and the next oracle failure will be new. When you want a wider cleanup, make it a separate task with its own done condition.

Revision without a record of the defect is a request to try again. The procedure will change something, and you will not be able to tell whether the change answered the failure. Point the revision at the oracle output or the critique, and record in the episode log what you asked it to change.

### When to use

- A previous version is mostly right, and you have a concrete defect list or a failing oracle.
- You can diff the result and see that the edit stays inside the defect.
- The artifact is a document, a patch, or a plan you want to keep stable for the steps that already passed.

### When not to use

- The structure of the artifact is the problem. Local edits will preserve the wrong structure. Generate a new candidate, then select.
- You have no defect record. You are sampling another attempt. Fan-out or a fresh generation describes that honestly.
- The oracle failure is environmental (missing dependency, wrong machine). A revision of the artifact will not move the signal. Escalate or fix the environment as its own step.
- The defect list is untrusted and untrimmed. Apply a checked list.

### Pros

- Preserves work that already passed.
- Makes iteration legible: defect in, diff out.
- Lets a loop stop for no progress when the diff stops touching the defect.

### Cons

- Local edits accumulate into a design nobody chose.
- Each revision spends a turn and can introduce a defect outside the list.
- Preserving the artifact is the wrong bias when the first version committed to a bad approach early.

### Failure modes

- The wording of the critique is satisfied and the underlying fault remains.
- A passing behavior regresses because the edit was wider than the defect.
- The revision and the previous version are not diffed, so "addresses the defect" is an assertion.
- The loop revises against a stale defect list and reintroduces a fixed bug.

### Pairs with

[Critique](#critique), [Oracle](assurance.md#oracle), [Loop](control.md#loop), [Episode log](memory.md#episode-log)

### In a skill

Name the artifact, the allowed edit region, and the only inputs that may justify a change (oracle output, accepted critique). Require a diff or an equivalent check that unrelated regions stayed put. In the loop, define no-progress as a revision that does not change the oracle result.
