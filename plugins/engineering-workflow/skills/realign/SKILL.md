---
name: realign
description: Audit a codebase for divergent solutions to one recurring problem — several error-handling styles, competing HTTP clients, three ways to assemble the same query — by searching out every instance, clustering them by approach, electing a canonical form from what already exists, and proposing a migration for the outliers. Use when the user says the code is inconsistent, notices the same job done differently in two places, asks which approach is the real one, wants a pattern settled before building on it, or invokes `/realign`. Do not use for comparing an implementation against an external reference such as a design, specification, or architecture document (`cross-check`), for cataloguing current capabilities (`product-map`), or for structural problems that are not about inconsistency (`technical-debt-audit`).
---

# Realign

One problem, several solutions, and no reference to judge them against. The canonical form is elected from what the codebase already does rather than imported from outside. The goal is convergence, with deliberate exceptions recorded so they stop being reported as drift on every future pass.

## Input and output mode

- **Scope**: a file or directory where the inconsistency was noticed. It anchors the search and does not bound it. Infer the anchor from the conversation when the user does not name one.
- **Hint**: an optional short description of what they noticed, such as "error handling" or "volume migration". Without a hint, derive candidate patterns from the operations the anchor repeats and confirm which one to chase before searching wide.
- Report in the task by default. Change code only after the user approves a specific canonical form and a specific set of call sites.

## 1. Understand the anchor

Read the scope and identify the operation the user noticed. Understand not only how the anchor solves it but what shaped that solution — the surrounding layer, its failure requirements, its age.

Treat the anchor as one data point. It is where the problem became visible, not the standard the rest should meet, and assuming otherwise biases every later step toward whatever the user happened to be reading.

## 2. Search the whole repo

Search on behavior rather than names. The same problem appears under different vocabulary, through different libraries, and at different layers, so searching for the anchor's identifiers finds only its relatives. Work outward from what the operation must accomplish.

Include the places that solve the problem by not solving it: the call site with no error handling, the path that skips validation. An absent instance is part of the spread.

Record what was searched and what was not. A confident claim to have found every instance is almost always wrong, and the next reader will rely on it.

## 3. Cluster by approach

Group instances by approach, never by directory. Two kinds of inconsistency are worth reporting:

- **Structural** — the same goal reached through different sequences of steps or different data flows.
- **Abstraction choice** — the same operation performed through different tools, libraries, primitives, or levels of indirection, such as ORM against raw SQL, or declarative configuration against an imperative script.

Do not report formatting, quoting, or casing; linters own those. Do not report naming unless the names reflect a structural difference.

A cluster of one matters in both directions. It may be the outlier among six, or the single modern instance that the other six predate.

## 4. Separate drift from deliberate variation

Before proposing convergence, ask of each cluster whether it had a reason. A different approach is deliberate when its context differs in a way the canonical could not serve: a hot path that cannot afford the abstraction, a boundary with different failure semantics, a module under a constraint the others do not carry.

Look for the evidence — a comment, a commit message, a test that pins the behavior, an architecture decision record. Absence of evidence is not proof of drift. Say which one you found.

Record deliberate variation as **accepted**, with its reason, so later passes stop re-reporting it. When the reason exists only in your analysis, propose writing it down next to the code, because an undocumented exception gets "fixed" by the next person who runs this audit.

## 5. Elect a canonical

Elect from what exists. Introduce a new approach only when every existing option is genuinely poor, and say plainly that you are doing so.

Weigh the candidates roughly in this order: correctness under failure, then clarity at the call site, then fit with the wider repo and its ecosystem, then how many instances already use it. Prevalence is the weakest argument available — the majority approach is frequently just the oldest one.

Give the reasoning in a sentence, and name what the losing approaches did better if anything. That is precisely what will be missed after migration, and saying it up front is how you find out the election was wrong.

## 6. Report

For each cluster give a short name for the inconsistency, then each approach with a brief excerpt and a clickable `[file:line](path#Lline)` link so the user can reach the surrounding context, then what varies across them, then the elected canonical and why, then any accepted exceptions.

````markdown
## Error handling in service calls

Three approaches, plus one call site with none.

**Try/catch with logger** — [src/services/payments/charge.ts:42](src/services/payments/charge.ts#L42)

```ts
try {
  await stripe.charge(amount);
} catch (err) {
  logger.error(err);
  throw err;
}
```

**Result type** — [src/services/payments/refund.ts:18](src/services/payments/refund.ts#L18)

```ts
const result = await safeCall(() => stripe.refund(chargeId));
if (!result.ok) return { error: result.error };
```

**Unhandled** — [src/services/payments/webhook.ts:31](src/services/payments/webhook.ts#L31)

**Canonical:** the result type, because it makes the failure visible in the signature. The try/catch style logs more context at the point of failure, which the migration must preserve.

**Accepted:** the retry loop in `sync.ts` swallows transient errors deliberately — reason recorded at line 88.
````

Follow the clusters with a migration note: which call sites move, in what order, which moves are mechanical and which need judgment, and what could break. Pay attention to behavior that differs subtly between approaches, such as which exception type escapes, how null is treated, or whether ordering is preserved. Order clusters by the consequence of leaving them alone, not by how easy they are to fix.

## 7. Confirm and converge

Ask which clusters to standardize and whether the elected canonical is right, and continue conversationally from there rather than offering menus.

Migrate only what the user approves. Take the most mechanical cluster first and let them verify one converted call site before converting the rest, because a canonical that looked right in the report sometimes reads badly in place.

## Relationship to adjacent skills

- Use `cross-check` when an external reference exists — a design, specification, or architecture document — and the question is whether the code matches it rather than whether the code agrees with itself.
- Use `product-map` when the goal is an inventory of what the system does rather than how consistently it does it.
- Use `analyze-complexity` when the variation may be justified by constraints that are not visible at the call sites, and the inherent requirements need separating from the implementation choices first.
- Use `technical-debt-audit` when the migration is too large to carry out now and should be tracked as debt.
- Use `design-space-exploration` when no existing approach deserves to win and a new one has to be chosen deliberately.
