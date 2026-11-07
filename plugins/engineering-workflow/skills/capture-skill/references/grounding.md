# Grounding

How a claim or a decision stays tied to an authority outside the model. Generation can sound grounded. These primitives are how the recipe makes that dependence real.

## Retrieval

**Aliases:** RAG, search, semantic search

**Summary:** Bounded, identified search hits from a corpus, placed into working context.

### Explanation

Retrieval searches a corpus and inserts a bounded number of hits into working context, each with an identifier the rest of the recipe can cite. The query, the corpus, the bound, and what counts as a hit are the design. The model's prior knowledge of the topic is still available to it, and the instruction has to say whether retrieved text outranks that prior. If it does not say, the two voices blend.

The query is part of the procedure. A query that copies the user's sentence works when the corpus uses the same words and fails when it does not. A query built from the terms the corpus actually uses, sometimes after one round of looking at section titles, is a different and often better step. That second round is a loop with a small budget, ending in the hits you will actually bind to.

Retrieval finds text that looks relevant. It does not find "the" record. When you know the identity — this path, this ticket id, this symbol — a fresh lookup is exact and search is a way to almost find it. Use retrieval for "where do we describe refunds," and a fresh lookup for "open docs/refunds.md."

Hits need a bound. The top of a wide search includes passages that share vocabulary and contradict the answer. Putting all of them in context and asking for a synthesis produces a compromise the corpus never stated. Prefer fewer hits, identifiers, and source binding on anything the answer claims.

Empty results are an outcome. The stop condition should say whether the procedure answers from prior knowledge, says it found nothing, or escalates. Leaving that implicit means the model will answer anyway and the citations will be decorative.

### When to use

- The authority is a corpus larger than the working context, and the answer depends on it.
- You can accept a ranked approximation and then bind claims to specific hits.
- You do not yet know which document holds the answer.

### When not to use

- You know the record's identity and can read it. Use a fresh lookup.
- The corpus is small enough to include under the working-context policy.
- The question is about current runtime or repository state. A document search returns a description of that state, often an old one.
- You need every matching record, not a top few. That is a query against an index with an explicit filter, closer to a tool call than to semantic retrieval.

### Pros

- Makes a large corpus usable without loading it.
- Gives source binding something to point at.
- A bad query is visible and improvable, unlike a vague instruction to "use the docs."

### Cons

- Relevance is not support. Hits can be adjacent to the question and still miss the constraint that changes the answer.
- The corpus can be wrong or stale, and retrieval will faithfully return it.
- Query and ranking behavior is another system to evaluate.

### Failure modes

- The answer uses a hit's vocabulary and ignores its condition ("only for annual plans").
- Citations point at hits that were in context and do not contain the claim.
- A failed search is followed by an ungrounded answer that still looks cited.
- Two corpora are mixed (public docs and an internal ticket) and the answer does not say which one a sentence came from.
- The hit limit cuts off the passage that contained the exception.

### Pairs with

[Working context](context.md#working-context), [Source binding](#source-binding), [Fresh lookup](#fresh-lookup), [Stop condition](control.md#stop-condition)

### In a skill

Name the corpus, who may update it, the query inputs, and the hit limit. Say whether retrieved text outranks parametric knowledge. Say what an empty result does. Require identifiers on hits that source binding can use.

## Source binding

**Aliases:** citations, attribution, grounded generation

**Summary:** Each material claim points at the observation that supports it.

### Explanation

Source binding attaches each material claim in the output to the identifier of the observation that supports it: a retrieval hit, a file and line from a fresh lookup, a tool result, a user message. A reader, or a later check, can open that source. The instruction says what happens to a claim that has no source. The usual choices are to mark it as inference or to leave it out. Those are different products, and the skill should pick one.

"Material" is a decision you write down. A number, a path, a policy, a name, and a cause-and-effect claim about the system are material in most skills. Connective prose is not. Binding every adjective produces noisy citations that train readers to ignore them. Binding only the convenient sentences produces confident gaps.

The binding has to be checkable. A citation that exists and does not entail the sentence is worse than a missing citation, because it borrows the source's credibility. When the stakes justify the cost, add a check: a second pass or a mechanical check that the cited span contains the terms of the claim. When they do not, still require the identifier, so a person can do that check.

Bind to the observation, not to a compaction of it. A summary that says the file "handles retries" is not a source for a claim about the retry limit. If the summary is all you still have, the claim's source is the summary, and the wording should show that.

### When to use

- A person will act on the answer, or another agent will treat it as a fact.
- The corpus or the tools can be wrong, and the consumer needs a way to check.
- You will grade the skill later and need to score support, separate from style.

### When not to use

- The deliverable is code a compiler or a test will accept or reject. The oracle is the binding that matters. Cite an external behavior only when the code is implementing a sourced rule.
- The output is a short UI string or a commit subject, where bindings destroy the form. Keep the bindings in the scratchpad or the trace.
- You cannot name what is material. Decide that before adding citation syntax the model will sprinkle everywhere.

### Pros

- Makes unsupported claims visible.
- Gives evaluation a hook: fraction of material claims whose source entails them.
- Teaches consumers where to go to verify.

### Cons

- Citation syntax can be gamed: the model cites a nearby span that shares a noun.
- Checking entailment is real work, model-based or human.
- Over-binding makes the deliverable harder to read than the sources were.

### Failure modes

- The citation resolves and does not support the sentence, including by omitting a condition.
- The source is a compacted paraphrase, and the original observation is gone.
- Inference is written in the same tone as sourced claims, with no mark.
- Bindings point at a whole long document, which is equivalent to no location.
- A later revision keeps the citation after changing the sentence.

### Pairs with

[Retrieval](#retrieval), [Fresh lookup](#fresh-lookup), [Judgment](cognition.md#judgment), [Trace](assurance.md#trace)

### In a skill

Define material claims for this deliverable. Say the identifier format, the rule for unsourced claims (mark or drop), and whether a second pass checks entailment. Tell revision to re-bind any sentence it changes.

## Fresh lookup

**Aliases:** read-through, system of record, read before write

**Summary:** A read from the system of record at the moment of the decision.

### Explanation

A fresh lookup reads the current value from the authority that owns it, at the time you are about to decide or claim: the file on disk, the ticket, the schema, the test output, the directory listing. An earlier mention in the conversation, a memory, a retrieved doc, or a plan is a hint about where to look. It is not a copy of the value.

This is the primitive that keeps long runs honest. Files change under you. Delegated children edit. Pauses last long enough for a person to commit. A procedure that treats its transcript as the tree will "fix" code that is already different and report facts that were true an hour ago.

Look up the thing you will act on, and look up the neighbors the action depends on (the test that should fail, the interface you will implement, the config key you will name). A lookup of an unrelated area is curiosity, and it belongs under the working-context budget like any other observation.

You do not need to re-read a value that cannot have changed since the last read in this same step. The scratchpad can hold a hash, an mtime, or a revision id that justifies skipping. After any boundary where something else could have written — a delegation, a confirmation wait, another process, a compaction that dropped the raw text — the next use re-reads.

Write the result into the scratchpad as an identifier plus the conclusion you will rely on, and keep the raw text available to the edit that needs it. A conclusion with no identifier cannot be checked. Raw text with no conclusion will be re-summarized differently on the next turn.

### When to use

- Before any claim about the repository, the config, the ticket, or the world.
- Before any edit, so the edit applies to the current bytes.
- After a pause, a delegation, a user turn, or any other boundary where the authority could have changed.
- When durable memory or retrieval offers a value the system of record also holds. The record wins.

### When not to use

- You read it in this step, nothing since then could have written, and the scratchpad holds a revision id you trust for this step only.
- The authority is a person. That is an ask, and repeating the lookup will not surface it.
- You are searching because you do not know the identity yet. Retrieval or a search tool comes first. The fresh lookup is how you open what you found.

### Pros

- Prevents decisions based on stale transcripts, memories, and docs.
- Makes the observation time a fact in the trace.
- Narrows edits to the current text, which keeps diffs smaller and conflicts visible.

### Cons

- Repeated reads of the same large file spend context and time.
- A lookup of the wrong identity (similar filename, old ticket) is freshly wrong.
- The system of record can itself be mid-update. A single read is current, and it is not a lock.

### Failure modes

- The procedure quotes a file from memory after a long run and edits the quote.
- A retrieved document answers a question about current code.
- Durable memory supplies a command or a path that no longer exists, and the procedure does not check.
- Two reads straddle a write the procedure did not make, and the scratchpad keeps the first.
- A directory listing is treated as file contents.

### Pairs with

[Tool call](action.md#tool-call), [Retrieval](#retrieval), [Durable memory](memory.md#durable-memory), [Checkpoint](control.md#checkpoint), [Working context](context.md#working-context)

### In a skill

Name the authorities the skill must re-read (files it will edit, checks it will cite, records it will update) and the boundaries that invalidate a previous read. Say what the scratchpad stores (path, revision, conclusion) and that an edit step reads the current bytes as its input.
