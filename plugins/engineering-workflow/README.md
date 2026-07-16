# Engineering Workflow Plugin

This plugin provides engineering skills for operator setup, consistency auditing, test design, scenario analysis, complexity analysis, and technical debt reviews.

## Skills

- **Analyze Complexity**: Analyze a code path, system, workflow, or architecture to separate inherent complexity imposed by requirements and external constraints from accidental complexity introduced by the current implementation, then define the invariants a simplification must preserve. Use when the user asks what complexity is necessary or unavoidable, asks for inherent vs. accidental complexity, says a pipeline or subsystem feels too complex, wants to understand why something cannot be simpler, or wants a complexity map before refactoring. Also use before a technical-debt audit when unavoidable constraints and removable implementation complexity are mixed together. Do not use for exploring competing greenfield designs (`design-space-exploration`) or for a pure structural-debt inventory that does not need an invariant boundary (`technical-debt-audit`).
- **Operator Setup**: Creates or updates `.agents/OPERATOR.md` in the current workspace — a personal profile that tells AI models who you are, your skill levels, and how you like to collaborate. Only invoked when the user explicitly runs `/operator-setup`.
- **Realign**: Identifies and reports inconsistencies in code patterns across the codebase, helping to maintain a coherent engineering workflow.
- **Blind Spot Coverage**: Analyzes a specific method to identify uncovered edge cases, error paths, and unusual inputs that existing tests miss. Focuses on pragmatic, high-value blind spots rather than achieving 100% line coverage. Activates on `/blind-spot-coverage` commands.
- **Scenario Design**: Diagnoses the shape of a scenario-enumeration problem and routes to the right systematic technique below — used when the shape isn't obvious yet or when a problem spans multiple dimensions (e.g. a stateful entity with range-constrained fields) that need more than one technique. Confirms the plan with the user, then hands off to the matching technique skill(s) and ties multi-technique outputs together. Jump straight to a technique skill instead when it's already clear which one fits.
  - **Decision Tables**: Maps every combination of independent yes/no conditions to an outcome, flagging combinations nobody has specified — authorization rules, validation logic, discount/pricing stacking.
  - **Equivalence Partitioning + BVA**: Partitions an input's valid/invalid ranges into classes and probes the boundaries between them, where bugs disproportionately cluster — numeric ranges, string lengths, date windows, enums.
  - **Combinatorial Testing**: Shrinks an exponential combination space (feature flags, config options) down to a minimal pairwise/orthogonal-array test matrix that still guarantees every pair of values is covered.
  - **State Transition Testing**: Models a stateful entity as states and event-triggered transitions, finding missing transitions, unreachable states, trap states, and undefined invalid-transition handling.
  - **FMEA**: Enumerates failure modes for a system or process and scores each by severity, likelihood, and detectability into a prioritized risk register (RPN = S × O × D).
  - **Design Space Exploration**: Maps the dimensions along which an architectural or design decision can vary, places known options in that space, and surfaces unexplored regions before a decision locks in.
  - **Scenario Analysis**: Builds named, narrative scenarios — who does what under what conditions — to find requirements gaps and give stakeholders a shared vocabulary to validate against.
  - **Cause-Effect Graphing**: Builds a directed graph connecting causes to effects through AND/OR/NOT logic, then derives a decision table from it — for tangled conditional logic or stakeholder-facing visuals.
- **Technical Debt Audit**: Identifies structural problems in a codebase and writes them up as technical debt documentation — one file per issue in a subfolder, plus an index. Surfaces concerns that make code hard to change, test, or reason about, producing actionable write-ups with concrete consequences and credible paths forward.

## Change Log

### v2.1.0

- Added Analyze Complexity for separating required invariants from removable implementation complexity before refactoring or technical-debt analysis

### v2.0.0

- Removed the Distiller, Technical Analyst, Implementer, and Technical Writer agents, making the plugin skills-only
- Removed the Orient skill and updated plugin discovery metadata to reflect the remaining engineering skills

### v1.9.0

- Split Scenario Design's eight specification-based techniques into standalone skills (Decision Tables, Equivalence Partitioning + BVA, Combinatorial Testing, State Transition Testing, FMEA, Design Space Exploration, Scenario Analysis, Cause-Effect Graphing) so a technique can be jumped to directly instead of always routing through Scenario Design
- Scenario Design is now a lean pivot: it diagnoses problem shape and hands off to the matching technique skill(s), rather than embedding every technique's procedure itself
- Decision Tables now gives each rule column a short descriptive name and a one-line plain-English summary, not just a numbered Y/N grid
- Scenario Analysis now explicitly considers adversarial/misuse actors, not just legitimate ones

### v1.8.0

- Technical Debt Audit now links the index from the repo's `AGENTS.md` (or `CLAUDE.md`) after writing it, so any agent working in the repo later — not just this skill — knows to check it before changing code in a covered area

### v1.7.3

- Extended the Technical Debt Audit issue catalog with a new archetype: non-local coupling (code whose correctness cannot be assessed locally because effects, preconditions, or decisions are scattered across files or layers)

### v1.7.2

- Extended the Technical Debt Audit issue catalog with a new archetype: silent error suppression (an error is caught and discarded, causing a misleading loud failure downstream that points away from the real source)

### v1.7.1

- Expanded the Technical Debt Audit issue catalog with two archetypes: misplaced responsibility / leaky layer (a generic component bakes in narrower domain policy) and contract divergence / hidden behaviour (an implementation does more or less than its signature and docs promise)
- Added a short remediation hint to each archetype in the catalog ("usually points to ...") as a starting direction to confirm during solution design

### v1.7.0

- Added the Operator Setup skill for creating or updating `.agents/OPERATOR.md` to capture operator profile, skill levels, and collaboration preferences

### v1.6.0

- Added the Technical Debt Audit skill for identifying structural problems in a codebase and documenting them as actionable technical debt write-ups

### v1.5.0

- Added the Blind Spot Coverage skill for identifying uncovered edge cases, error paths, and unusual inputs in a specific method
- Added the Scenario Design skill for systematic scenario enumeration and gap detection using specification-based techniques

### v1.4.0

- Refactored workflow to use linear flow with bounded subagent delegation instead of circular handoffs
- Removed circular handoffs between Implementer ↔ Technical Analyst and Technical Writer ↔ Implementer/Technical Analyst
- Technical Analyst and Implementer now delegate documentation tasks to Technical Writer as subagents
- Technical Writer no longer has handoffs back to other agents
- Added the Blind Spot Coverage skill for identifying pragmatic test coverage gaps in specific methods

### v1.3.0

- Added the Orient skill for targeted mental-model gap-filling

### v1.2.0

- Added the Technical Writer agent and documentation-aware workflow loops
- Documented contributor-facing documentation responsibilities and handoff boundaries

### v1.1.1

- (Hopefully) fix agent handoffs, tighten responsibilities and boundaries

### v1.1.0

- Added the Realign skill

### v1.0.1

- Renamed agents

### v1.0.0

- Initial version with Distiller, Technical Analyst, and Implementer agents
