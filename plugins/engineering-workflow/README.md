# Engineering Workflow Plugin

This plugin provides engineering skills for product mapping, flaky-build diagnosis, operator setup, session compounding, consistency auditing, conformance checking, test design, scenario analysis, complexity analysis, technical debt reviews, and controlled technical writing.

## Skills

- **Analyze Complexity**: Analyze a code path, system, workflow, or architecture to separate inherent complexity imposed by requirements and external constraints from accidental complexity introduced by the current implementation, then define the invariants a simplification must preserve. Use when the user asks what complexity is necessary or unavoidable, asks for inherent vs. accidental complexity, says a pipeline or subsystem feels too complex, wants to understand why something cannot be simpler, or wants a complexity map before refactoring. Also use before a technical-debt audit when unavoidable constraints and removable implementation complexity are mixed together. Do not use for exploring competing greenfield designs (`design-space-exploration`) or for a pure structural-debt inventory that does not need an invariant boundary (`technical-debt-audit`).
- **Blind Spot Coverage**: Analyzes a specific method to identify uncovered edge cases, error paths, and unusual inputs that existing tests miss. Focuses on pragmatic, high-value blind spots rather than achieving 100% line coverage. Activates on `/blind-spot-coverage` commands.
- **Compound**: End-of-session hill climb on the instruction surface. Encodes this session's friction into AGENTS.md, skills, or project docs so the next session does not pay the same tax.
- **Cross-Check**: Compare two representations of one subject — design and implementation, specification and analysis, reference architecture and code, API documentation and handlers, threat model and deployed controls — on a grid of subject units against comparison facets, classify every cell as agreement, refinement, divergence, or a one-sided gap, and propose a remediation for each discrepancy. Use when the user asks whether the code matches the design, whether a document still describes reality, where two artifacts have drifted apart, or wants a conformance or traceability matrix between a reference and its realization. Do not use for inconsistency among several implementations of one pattern inside a single codebase (`realign`), for single-sided current-state documentation with no reference artifact (`product-map`), or for a structural-problem inventory that needs no second side (`technical-debt-audit`).
- **Flaky Build Investigation**: Diagnose intermittent build, test, packaging, or CI pipeline outcomes by comparing equivalent runs and correlating logs, configuration, code, environment, ordering, and timing. Use when a build or test sometimes fails, a rerun passes, behavior depends on runner or execution order, or the user asks why the build is flaky. Default to a bounded read-only investigation. Do not use for consistently failing builds, unrelated runtime defects, or release and deployment execution.
- **Operator Setup**: Creates or updates a personal operator profile under `~/.agents/projects/` (index + `OPERATOR.md`) — who you are, skill calibration, and collaboration preferences for this project. Worktree-safe via main worktree path; wires only the current harness. Only invoked when the user explicitly runs `/operator-setup`.
- **Product Map**: Create or update a product map, feature map, or capability map from an existing implementation. Use when no map exists, when documenting what a program does, or after code changes add, alter, or remove capabilities that an existing map must reflect. Produces current-state documentation that planning can consult; does not propose features or replace product planning.
- **Realign**: Audit a codebase for divergent solutions to one recurring problem — several error-handling styles, competing HTTP clients, three ways to assemble the same query — by searching out every instance, clustering them by approach, electing a canonical form from what already exists, and proposing a migration for the outliers. Use when the user says the code is inconsistent, notices the same job done differently in two places, asks which approach is the real one, wants a pattern settled before building on it, or invokes `/realign`. Do not use for comparing an implementation against an external reference such as a design, specification, or architecture document (`cross-check`), for cataloguing current capabilities (`product-map`), or for structural problems that are not about inconsistency (`technical-debt-audit`).
- **Scenario Design**: Diagnoses the shape of a scenario-enumeration problem and routes to the right systematic technique below — used when the shape isn't obvious yet or when a problem spans multiple dimensions (e.g. a stateful entity with range-constrained fields) that need more than one technique. Confirms the plan with the user, then hands off to the matching technique skill(s) and ties multi-technique outputs together. Jump straight to a technique skill instead when it's already clear which one fits.
  - **Decision Tables**: Maps every combination of independent yes/no conditions to an outcome, flagging combinations nobody has specified — authorization rules, validation logic, discount/pricing stacking.
  - **Equivalence Partitioning + BVA**: Partitions an input's valid/invalid ranges into classes and probes the boundaries between them, where bugs disproportionately cluster — numeric ranges, string lengths, date windows, enums.
  - **Combinatorial Testing**: Shrinks an exponential combination space (feature flags, config options) down to a minimal pairwise/orthogonal-array test matrix that still guarantees every pair of values is covered.
  - **State Transition Testing**: Models a stateful entity as states and event-triggered transitions, finding missing transitions, unreachable states, trap states, and undefined invalid-transition handling.
  - **FMEA**: Enumerates failure modes for a system or process and scores each by severity, likelihood, and detectability into a prioritized risk register (RPN = S × O × D).
  - **Design Space Exploration**: Maps the dimensions along which an architectural or design decision can vary, places known options in that space, and surfaces unexplored regions before a decision locks in.
  - **Scenario Analysis**: Builds named, narrative scenarios — who does what under what conditions — to find requirements gaps and give stakeholders a shared vocabulary to validate against.
  - **Cause-Effect Graphing**: Builds a directed graph connecting causes to effects through AND/OR/NOT logic, then derives a decision table from it — for tangled conditional logic or stakeholder-facing visuals.
- **STE Writing**: ASD-STE100 Simplified Technical English, and the reply shape a reader with ADHD can act on. A standing style rule, not an on-request tool. Layer 1 governs the words of every text a human reads — chat replies, docs, READMEs, commit messages, PR text, code comments, error messages, release notes, tool descriptions, task trackers, wiki pages. Layer 2 governs the order of a reply to a person — the next action first, numbered steps, real time estimates, no preamble and no closer. Neither layer touches code, identifiers, or command syntax. Load it before you write prose, and also when asked to remove "AI slop", make writing clear or plain, enforce a controlled style, or review text for STE violations. Two word modes — strict (procedures, runbooks, safety text, error messages) and STE-flavored (general prose, the default).
- **Technical Debt Audit**: Identifies structural problems in a codebase and writes them up as technical debt documentation — one file per issue in a subfolder, plus an index. Surfaces concerns that make code hard to change, test, or reason about, producing actionable write-ups with concrete consequences and credible paths forward.

## Change Log

### v2.7.1

- Compound now carries its agent-writing guidance inline instead of deferring to skills that live outside this repository, so the procedure works wherever the plugin is installed
- Compound follows junctions to the source of truth and skips plugin cache and marketplace copies, so a delta lands on the real file rather than a copy that is regenerated later
- Compound treats `/compound` as authorizing the whole climb, and naming a skill as authorizing edits to that skill, resolving a body that claimed narrower authority than the command granted

### v2.7.0

- Added STE Writing, moved here from the now-deprecated technical-writing plugin along with its upstream MIT license and pinned source attribution, so the skills that reference it no longer depend on a separately installed package
- STE Writing now tracks upstream 2.0.3, which rewrites the skill as a standing style rule and adds a second layer governing the shape of a reply, and bundles the recurring-errors reference it cites
- STE Writing vendors the instructions only — the upstream Python linter, Node wrapper, and Claude Code hooks stay out, so the manual checklist is now the verification step and the skill needs no runtime beyond the agent

### v2.6.0

- Added Cross-Check for comparing two representations of one subject — design against implementation, specification against analysis, reference architecture against code — on a units-by-facets grid, with a correspondence step that matches elements by behavior before comparing, a refinement-versus-divergence distinction that keeps normal abstraction gaps out of the findings, a per-discrepancy direction-of-truth judgment, and a remediation for every discrepancy
- Realign now searches on behavior rather than names, separates deliberate variation from drift and records accepted exceptions so later passes stop re-reporting them, weighs an elected canonical on failure behavior and call-site clarity ahead of prevalence, reports migration risk and search coverage, and takes an optional rather than mandatory hint
- Realign's discovery metadata now states what it produces and routes explicitly to Cross-Check when an external reference exists, resolving a description that could not compete for invocation and a body that contradicted it by claiming slash-command-only activation

### v2.5.0

- Added Product Map to document implemented capabilities and maintain product maps, with five formats and explicitly connected visual charts.
- Planning and scenario skills now consult existing product maps, reference feature IDs, and keep proposed changes separate from current capabilities.

### v2.4.0

- Added Flaky Build Investigation for bounded, evidence-led diagnosis of intermittent local and CI build failures

### v2.3.0

- Added Compound for end-of-session hill climbing on the instruction surface (AGENTS.md, skills, project docs)

### v2.2.0

- Operator Setup now stores profiles under `~/.agents/projects/` with a path index (main worktree as canonical root), skill calibration menus instead of proficiency scores, minimal mid-session patches, and harness-only self-wiring — no workspace `OPERATOR.md` or repo `AGENTS.md` injection
- Operator Setup migrates and removes legacy workspace `.agents/OPERATOR.md` and the old repo `AGENTS.md`/`CLAUDE.md` operator-load blurb after a successful home-profile write

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
