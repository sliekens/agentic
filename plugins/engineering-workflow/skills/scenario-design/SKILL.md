---
name: scenario-design
description: Use this skill for systematic scenario analysis — whenever a problem involves multiple variables, states, conditions, or failure modes and the user needs to enumerate the scenario space to find gaps, validate assumptions, or ensure coverage. Activate eagerly when the user asks "what cases should I handle?", "what could go wrong?", "am I missing any scenarios?", "how do I systematically test/model this?", or when they describe a decision table, state machine, input space, feature flag combination, risk matrix, or any artifact where multiple interacting variables might produce unexpected outcomes. Also use for non-testing contexts: config-flag interactions, requirement gap-finding, risk registers, design tradeoffs, business rule validation. This skill selects the right systematic technique, explains its reasoning, confirms with the user, and produces a structured markdown output for gap detection in code, requirements, design docs, or business rules.
---

# Scenario Design

Activate when the user needs to systematically enumerate scenarios for a problem with multiple interacting variables — to find gaps, validate assumptions, or produce structured test cases or a risk/coverage model.

## How this works

1. Understand the problem space
2. Diagnose the problem shape and select a technique (or combination) using the guide below
3. Explain your reasoning and proposed approach; ask the user to confirm
4. Apply the technique by reading the relevant reference file
5. Write the output to a markdown file

When multiple techniques could apply, recommend the simplest one that covers the gap — don't stack techniques for the sake of completeness.

## Technique selection guide

The central question is: **what is the shape of the problem?**

| Problem shape | Technique | Reference |
|---|---|---|
| Conditional rules with discrete outcomes ("if A and B then X") | Decision table | `references/decision-tables.md` |
| Input parameters with valid/invalid ranges (integers, strings, dates) | Equivalence partitioning + BVA | `references/equivalence-partitioning-bva.md` |
| Many parameters where the combination space is too large to enumerate exhaustively | Orthogonal array / combinatorial testing | `references/orthogonal-array-testing.md` |
| System with states and transitions (workflows, protocols, state machines) | State transition testing | `references/state-transition-testing.md` |
| Risk-driven: what can fail, how likely, how severe? | FMEA | `references/fmea.md` |
| Competing design options or unexplored parameter space | Design space exploration | `references/design-space-exploration.md` |
| Narrative-driven scenarios with stakeholder context | Scenario analysis | `references/scenario-analysis.md` |
| Causal chains: which inputs drive which outputs, and how? | Cause-effect graphing | `references/cause-effect-graphing.md` |

**Notes on overlap** — some techniques are closely related; knowing the distinctions prevents choosing redundantly:

- **Decision tables vs. cause-effect graphing**: Same analysis, different presentation. A cause-effect graph is a decision table drawn as a directed graph. Use decision tables — they're more directly actionable and easier to turn into test cases.
- **EP + BVA always go together**: Equivalence partitioning divides the input space into classes; BVA zooms in on the class boundaries. You rarely apply one without the other.
- **Orthogonal arrays vs. all-pairs**: Both belong to the combinatorial family. All-pairs (pairwise testing) is the practical subset you reach for first; orthogonal arrays when you need higher-strength interaction coverage.
- **FMEA vs. scenario analysis**: FMEA is quantitative (severity × probability → risk priority); scenario analysis is narrative and contextual. Use FMEA when you need a risk register; use scenario analysis when you need stakeholder-facing narratives.

## Procedure

### 1. Read the problem

Understand what the user is working with:
- What artifact is being analyzed? (code, requirements, design, business rules, architecture, configuration)
- What variables or dimensions are involved?
- What is the user's goal? (test cases, gap report, risk register, coverage model, design decision)

If the context is ambiguous, ask one focused question before proceeding.

### 2. Diagnose the shape

Map the problem to the technique selection guide. State which technique(s) fit and why in 2–3 sentences. If the problem has multiple distinct dimensions (e.g., input validation *and* stateful transitions), name both and explain how you'll handle each.

### 3. Explain and confirm

Present your technique selection to the user:
- Which technique(s) you're recommending and why they fit this problem shape
- What the output will look like (table, state matrix, FMEA register, etc.)
- Rough scope: how many rows/scenarios to expect

Ask: "Does this approach make sense, or would you like to adjust?"

Proceed after the user confirms. If the user redirects to a different technique, follow their lead — they may know constraints you don't.

### 4. Apply

Read the relevant reference file(s) for the selected technique. Each reference file contains:
- A step-by-step application guide
- The output format/template to use

Apply methodically. As you build the scenario matrix:
- Flag impossible or undefined combinations inline
- Highlight rows that represent gaps (no corresponding test, no spec coverage, etc.)
- Note any unresolved assumptions that need domain input

Keep scope focused: thorough coverage over a narrow, well-defined scope beats thin coverage over everything.

### 5. Save and summarize

Write the output to a markdown file. Suggested default path: `docs/analysis/<artifact-name>-scenarios.md`. Ask the user if they want a different path before writing.

After writing, summarize:
- Number of scenarios identified
- Notable gaps or unresolved questions
- Suggested next steps (e.g., "5 of these have no corresponding tests — `/blind-spot-coverage` on `X` would address them")
