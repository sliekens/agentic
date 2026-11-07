# Coordination

How ownership of a goal moves between agents and people. The parent, the child, and the person need the same story about who is allowed to act and who is waiting.

## Delegation

**Aliases:** subagent, child agent, spawned task

**Summary:** A bounded subgoal given to another agent. The parent keeps the original goal.

### Explanation

Delegation hands another agent a subgoal, the minimum context it needs, the tools it may use, a budget, and the shape of the result you will accept. The parent keeps the original goal, integrates the result, and remains responsible for the deliverable. The child does not inherit the parent's transcript, the parent's open asks, or the parent's permission to touch everything the parent can touch. It inherits what the brief states.

The brief is a working-context assembly for a stranger: the subgoal, the constraints, the inputs (as identifiers plus the contents the child must see), the done condition, and the output schema. "Here is my whole conversation, please handle the backend" is a transfer of confusion. If you cannot write the done condition, you are not ready to delegate. You are ready to decompose further or to keep the work in the parent.

The parent checks the child's result against the contract. A confident narrative is not a result. Schema-check the output, run the oracle the contract named, or reject the result and send a tighter brief. Integrating by pasting the child's prose into the parent's deliverable imports the child's misunderstandings.

Children that share a writable checkout will overwrite each other. Give them disjoint write sets, or sequence the ones that touch the same files, or give each an isolated checkout and make integration an explicit parent step. Isolation is fan-out's precondition, and delegation is how a unit of fan-out actually runs when it needs its own context or model.

Delegation has a budget and a stop. A child that runs until it feels done will spend the parent's whole allowance on one subgoal. The child's stop reasons (done, blocked, budget) return as data. Blocked is something the parent handles: a new brief, a different decomposition, or an escalation. It is not a cue for the parent to adopt the child's goal and abandon its own.

### When to use

- A subgoal needs a fresh context because the parent's is full or contaminated by abandoned approaches.
- A subgoal benefits from a different model, a different tool set, or a different procedure.
- Fan-out units need isolation from each other.
- The subgoal is checkable on its own, and the parent can say what it will do with the result.

### When not to use

- The subgoal is one tool call. Call the tool. A child wrapped around a single read adds a summary that can be wrong.
- You cannot check the result. You will integrate fiction.
- The integration work is comparable to the original task. Keep it in one procedure.
- The units would need to negotiate while they run. They are not independent. Redesign the boundary or sequence them.
- You are delegating because the task is unclear. Clarifying it is the parent's job, sometimes via an ask.

### Pros

- Fresh context, specialized procedure, and bounded tools.
- A bad child attempt can be discarded without poisoning the parent transcript.
- Makes parallelism possible under an explicit join.

### Cons

- Briefs drop constraints, and children then "succeed" at the wrong task.
- Cost multiplies, including children that return unused work.
- The parent can lose the plot while supervising, or rubber-stamp results to finish.

### Failure modes

- The child redoes the parent's investigation because the brief contained motives and no facts.
- Two children edit the same files.
- The parent passes its permissions through, including confirms it meant to keep.
- The child's blocked stop is ignored and the parent continues as if the subgoal were done.
- The brief includes a compacted guess about file contents, and the child never does a fresh lookup.
- A child is delegated the original user goal, so two agents now own it.

### Pairs with

[Decomposition](cognition.md#decomposition), [Working context](context.md#working-context), [Fan-out](control.md#fan-out), [Schema check](assurance.md#schema-check), [Checkpoint](control.md#checkpoint)

### In a skill

Specify the brief fields, the child's allowed tools and write set, the output schema, the budget, and the stop reasons the parent handles. Say how the parent checks the result before integration. Say that the parent keeps the user-facing goal and the confirmation duties the skill assigned to it.

## Handoff

**Aliases:** transfer, takeover, escalate-and-release

**Summary:** Ownership of the remaining goal moves, and the sender stops acting on it.

### Explanation

A handoff transfers ownership of the remaining goal to another actor, who may be a person or another procedure in another session. The sender passes the checkpoint, the deliverable so far, the open questions, and the constraints, then stops acting on that goal. Stop is what makes it a handoff. If the sender keeps editing, reviewing, or "just finishing one thing," the receiver is not the owner, and you have a delegation with two writers.

The package is for a stranger who was not in the transcript. It states the goal in the user's terms, what is already true and how you know (oracle results, files written, decisions confirmed), what remains, and what the sender is unsure about. A package that argues for the sender's last plan hides the uncertainty the receiver most needs.

Handoff is the right edge when the skill's scope ends: a specialist procedure takes the next phase, a person takes a decision the skill must not make, or the session ends and another session will continue. The stop condition should include this ending, so "I handed it off" is a recorded stop and not an abandonment.

The receiver needs permission to change the plan. A handoff that says "continue step 4 exactly as I would have" is a delegation that dropped the return channel. If you need the work done your way and brought back, delegate.

After a handoff to a person, the agent does not sit in a loop refreshing to see if it can take the goal back. The goal is theirs until a new invocation says otherwise.

### When to use

- The next actor is better placed: a person, a specialist procedure, a new session with a clean context.
- The current procedure's scope ends at a boundary you defined in advance.
- Continuing would require authority or knowledge the sender does not have, and there is a named receiver.

### When not to use

- You still want the result back and you will check it. That is delegation.
- There is no receiver. Stopping with a report for the user may be escalation. Calling it a handoff implies someone accepted the goal.
- The sender will keep a background loop that also writes. Two owners will clobber each other.
- The package would be the raw transcript. Assemble a checkpoint a stranger can resume from.

### Pros

- Makes a single owner at every moment.
- Gives the receiver a resume package instead of a transcript.
- Lets a skill end at a clean scope boundary.

### Cons

- Context that lived only in the sender's head is gone if it missed the package.
- The receiver may restart work the sender had already done well.
- A premature handoff dumps the hard part on someone who expected a finished deliverable.

### Failure modes

- The sender keeps writing after the handoff.
- The package states the sender's plan as if it were the user's goal.
- Open asks and failed attempts are omitted, so the receiver repeats them.
- The handoff points at stale file contents instead of paths to re-read.
- Nobody is the owner for an interval, and both sides assume the other is working.

### Pairs with

[Checkpoint](control.md#checkpoint), [Delegation](#delegation), [Escalation](#escalation), [Stop condition](control.md#stop-condition)

### In a skill

Name the scope boundary where ownership moves, who the receiver is, and the package fields (goal, what is true, evidence, what remains, uncertainties, paths to re-read). Say that the sender's stop reason is handoff and that the sender does not keep acting. Distinguish this boundary from delegation inside the skill.

## Escalation

**Aliases:** raise, blocker, abort with report

**Summary:** A deliberate stop that reports the blocker, the evidence, and the decision needed.

### Explanation

Escalation stops the procedure because it cannot proceed responsibly, and it reports that fact to a person or a parent procedure. The report contains the blocker, what was tried (the episode log, bounded), the evidence (oracle output, guardrail block, contradictory sources), and the decision or action needed from the receiver. Then the procedure ends in the blocked, refused, or no-progress stop. It does not keep poking the same blocker while it waits.

Escalation is a successful use of a stop condition. A crash, an empty message, or a confident deliverable that dodges the hard part are the alternatives, and they are worse. A skill that can only end "done" will call a stuck run done.

The receiver should be able to act on the report without replaying the run. "It's complicated, what do you want?" is an ask that skipped the investigation. A good escalation names the smallest decision that would unblock the next step, with the options you actually see. If you do not know the options yet, the next step is more investigation, if budget remains, and the escalation says what you still cannot see.

Some blockers are refusals: the request asks for something the instruction or a guardrail will not do. Report those as refusals, with the rule that fired. Rephrasing the goal inside the same run to get past a refusal is a failure mode, not persistence.

Parents receiving a child's escalation integrate it. They do not paste it to the user automatically, and they do not ignore it. The parent's recipe says which child stops are retried with a new brief, which change the plan, and which become the parent's own escalation.

### When to use

- A guardrail block, a missing authority, or a contradictory oracle means continuing would be a guess or a violation.
- The loop's no-progress exit fired.
- The budget will run out before a responsible done, and a person should know where things stand.
- The goal changed shape in a way the skill's contract does not cover.

### When not to use

- The next step is a lookup or a reversible attempt you have not made. Do the step. Escalating the original task back to the user is a handoff you did not earn.
- You are escalating to avoid a judgment the skill gave you criteria for. Make the judgment, record it, and proceed.
- The situation is an ask: you know the question and the options, and the run should wait and then resume. Escalation ends the run. An ask pauses it. Pick the one you mean.
- You would attach the raw trace and no decision. Distill the report.

### Pros

- Turns stuckness into a specific request for a decision.
- Preserves the attempts so the next owner does not repeat them.
- Gives evaluation a way to score "escalated correctly," which is different from "failed to finish."

### Cons

- A hair-trigger escalation trains people to expect unfinished work.
- A late escalation wastes the budget and then asks for a decision you could have asked up front.
- Writing the report is a generation, and it can soften a hard blocker into something that sounds handled.

### Failure modes

- The report says the work is done and mentions the blocker as a footnote.
- Attempts are omitted, so the next run repeats them.
- A refusal is escalated as a technical blocker, inviting the user to help bypass the rule.
- The procedure escalates and also keeps a loop running.
- The parent swallows a child's escalation and ships the rest of the deliverable as if the subgoal had passed.

### Pairs with

[Stop condition](control.md#stop-condition), [Episode log](memory.md#episode-log), [Ask](action.md#ask), [Guardrail](assurance.md#guardrail), [Delegation](#delegation)

### In a skill

Name the blocker classes that escalate (guardrail block, no progress, contradictory oracle, missing authority, out of scope). For each, name the receiver and the report fields: blocker, attempts, evidence, decision needed. Say that escalation is a stop, and that the deliverable is the report. In a parent skill, say how child escalations are handled.
