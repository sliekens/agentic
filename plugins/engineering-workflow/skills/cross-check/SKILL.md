---
name: cross-check
description: Compare two representations of one subject — design and implementation, specification and analysis, reference architecture and code, API documentation and handlers, threat model and deployed controls — on a grid of subject units against comparison facets, classify every cell as agreement, refinement, divergence, or a one-sided gap, and propose a remediation for each discrepancy. Use when the user asks whether the code matches the design, whether a document still describes reality, where two artifacts have drifted apart, or wants a conformance or traceability matrix between a reference and its realization. Do not use for inconsistency among several implementations of one pattern inside a single codebase (`realign`), for single-sided current-state documentation with no reference artifact (`product-map`), or for a structural-problem inventory that needs no second side (`technical-debt-audit`).
---

# Cross-check

Compare two representations of one subject and report where they agree, where they conflict, and what only one side knows. Neither side is presumed correct. Decide direction of truth per discrepancy, with a stated reason, and attach a remediation to every discrepancy. The goal is realignment, not a verdict on who was wrong.

## Output mode

- Report the comparison in the task by default and modify nothing.
- When the user asks to document it, write one artifact under `docs/`; prefer `<subject>-cross-check.md`. Stamp it with both sides and their revisions so a later run can diff against it instead of starting over.
- Propose every remediation before changing anything. Execute only what the user approves, including implementation-side changes, in approved batches rather than as one sweep. An approved remediation authorizes that change and nothing adjacent.

## 1. Fix the two sides and the subject

Name each side precisely: the artifact, its revision (commit, document version, or date), its intended audience, and its level of abstraction. Compare exactly two sides. When three or more artifacts exist — specification, tests, and code — run pairwise and choose the pairs that carry the real question; a three-column grid makes correspondence quadratically harder and stops being readable.

State the subject both sides are describing and the boundary around it: what is in scope, and what belongs to neither side. Record the abstraction gap explicitly. A reference architecture sits far above code; an OpenAPI document sits directly on top of its handlers. The size of that gap decides how much one-sided detail is normal rather than suspicious.

Read both sides before deriving any axis. Never let one side's table of contents stand in for reading the other, and never treat an older document as evidence about current behavior.

## 2. Build the correspondence map before comparing

Match on identifiers alone and every row reads as a gap. Establish which element on each side corresponds to which on the other by behavior and responsibility, not by name.

Handle these relations explicitly:

- **One-to-one** — the straightforward pair.
- **Split** — one element on one side realized as several on the other. This is a match with a structural note, not a gap.
- **Merge** — several elements collapsed into one.
- **Unmatched** — a genuine one-sided element, recorded only after searching for the same behavior under a different name.

Record each pair with the evidence that justifies it and a confidence. Resolve or flag low-confidence pairs before building the grid, because an unstable correspondence invalidates every cell that rests on it. Renames are themselves a finding: divergent vocabulary between a design and its implementation costs every future reader, even where behavior agrees.

## 3. Derive the axes

Rows are **units of the subject** — the things both sides are trying to describe: components, requirements, endpoints, states, flows, or controls. Choose the granularity at which both sides actually commit to something, and aim for roughly 8 to 15 rows. Fewer and the cells are mush; more and nobody reads the grid. Name units after what a reader recognizes, not after files.

Columns are **facets of comparison** — the dimensions along which two descriptions can disagree. Derive them from what these particular artifacts argue about, drawing on: existence and structure; behavior and control flow; data and schema; error and failure handling; lifecycle and state; interfaces and contracts; vocabulary; and non-functional constraints such as security, performance, and operability.

Include a facet only when at least one side commits to it. Mark inapplicable cells as not applicable instead of inventing content for them. A grid that is mostly empty means the axes are wrong — re-derive them rather than filling them in.

## 4. Judge each cell

| Verdict | Meaning |
| --- | --- |
| Agree | Both sides commit to compatible content. |
| Refines | One side adds detail consistent with the other. Expected, not a defect. |
| Diverge | Both sides commit, incompatibly. A real conflict. |
| Gap | One side commits and the other is silent where it was obliged to speak. Record which side is silent. |
| Unverifiable | The evidence does not settle it. |
| N/A | The facet does not apply to this unit. |

The line between **refines** and **diverge** carries the whole technique. Refinement is compatible until it violates a constraint the other side states or clearly implies. "Persist the order" realized as Postgres with an outbox table is refinement. The same requirement realized as an in-memory cache is divergence, because durability was implied. Without this distinction every abstraction gap reads as drift and the report drowns in noise.

Silence is neither agreement nor automatically a gap. Silence is a gap only where the silent side's own purpose and level of abstraction obliged it to say something.

Every verdict cites a location on each side that commits to content — `file:line` for code, a heading or anchor for prose. An agreement supported by a citation on only one side is unverifiable; write it that way. Do not manufacture agreement out of plausibility, and do not let a matching name stand in for matching behavior.

## 5. Decide direction of truth per discrepancy

Do not declare one side authoritative for the whole comparison. It is normally a mixed bag, and a blanket rule produces confident wrong remediations. For each divergence and gap, state which side should change and why, in one sentence.

Apply these as priors rather than rules:

- Running code is authoritative about what happens and never about what should happen.
- A specification is authoritative about intent inside its own scope and stale outside it.
- A reference architecture is authoritative about the constraints it imposes, not about details it deliberately omits.
- The more recent artifact is not automatically right. Establish whether the change was a decision or an accident.

When the priors conflict, ask which side someone would be harmed by trusting.

Flag separately the discrepancies where the reference never anticipated the case and the implementer improvised. Neither side is wrong; a decision was never made. These are the most valuable findings the technique produces and they must not be resolved by quietly editing a document. Name the open question and its owner instead.

## 6. Propose a remediation for every discrepancy

Every divergence and gap resolves to one of four moves:

1. **Change the implementing side** to match the reference.
2. **Change the describing side** to match reality. Frequently the correct move and almost always the cheapest.
3. **Record the deviation deliberately** as an architecture decision record or known-deviation note, so a later run stops re-reporting it. Requires a stated reason; an undocumented deviation is not an accepted one.
4. **Escalate an undecided decision**, naming the question, the options, and who owns it.

For each remediation give the move, the concrete change (which file or section, and what it should say or do), its size, its risk, and anything that depends on it landing first. Order remediations by the consequence of leaving them alone, not by how easy they are. Keep one discrepancy to one move; do not bundle unrelated fixes because they touch the same file.

## 7. State coverage honestly

Report which units and facets were inspected and which were not, which cells are unverifiable and what evidence would settle them, and which correspondences remain low-confidence. Never imply an exhaustive comparison from a partial pass. When the result is documented, record both revisions compared, because a cross-check is accurate only against the revisions it was run on.

## Canonical document shape

```markdown
# <Subject> cross-check

| | |
| --- | --- |
| Side A | <artifact, revision, abstraction level> |
| Side B | <artifact, revision, abstraction level> |
| Subject | <the one thing both describe> |
| Boundary | <in scope / out of scope> |

## Correspondence map

| Side A | Side B | Relation | Confidence | Evidence |
| --- | --- | --- | --- | --- |

## Verdict grid

| Unit | <facet> | <facet> | <facet> |
| --- | --- | --- | --- |

## Findings

### <ID> <short name> — <verdict>

- **Side A:** <what it commits to> — <citation>
- **Side B:** <what it commits to> — <citation>
- **Judgment:** <which side should change, and why>
- **Remediation:** <move, concrete change, size, risk>

## Undecided decisions

## Accepted deviations

## Coverage and limits
```

## Relationship to adjacent skills

- Use `realign` when the inconsistency is among several implementations of one pattern inside one codebase and there is no second artifact to compare against.
- Use `product-map` to build a current-state side when only the implementation exists; its feature IDs make good rows for the grid.
- Use `analyze-complexity` when the divergence is that the implementation is far more complicated than its design, and the real question is how much of that is unavoidable.
- Use `technical-debt-audit` when implementation-side remediations are large enough to track as debt instead of fixing now.
- Use `design-space-exploration` when the conclusion is that neither side describes the right design.
