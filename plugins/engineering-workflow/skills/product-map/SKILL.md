---
name: product-map
description: Create or update a product map, feature map, or capability map from an existing implementation. Use when no map exists, when documenting what a program does, or after code changes add, alter, or remove capabilities that an existing map must reflect. Produces current-state documentation that planning can consult; does not propose features or replace product planning.
---

# Product map

Document what the product can do today, for users, operators, and integrating systems. Use a flat inventory as the reference list and derive other views from it. A capability is an observable outcome; a button is an entry point and a class is implementation evidence.

## Establish the baseline

Find existing feature documentation and project instructions before choosing a path, vocabulary, or format. Search for product, feature, and capability maps as well as documentation indexes. Read the relevant implementation rather than treating an old map or design document as proof.

For a new map, establish the product boundary, intended readers, inspected version or revision, interfaces, and configuration assumptions. Follow project documentation conventions; otherwise use `docs/product-map.md`. Default to an inventory and tree in one document. Ask only when an unresolved scope or audience choice materially affects the result.

For an update, read the existing map and the relevant implementation changes. Use a diff or supplied change description to locate affected behavior, then check callers, entry points, configuration, and tests in current code. If the change boundary is unknown, inspect the relevant area without implying a whole-product audit.

## Discover and substantiate capabilities

- Follow user and operator entry points through their behavior: pages, commands, API routes, integrations, configuration, scheduled work, recovery, and maintenance. A route list or sitemap helps check coverage but is not the feature taxonomy.
- Group by product purpose, not source folders. Name features with concise actions and objects. Keep granularity comparable; retain small options as limitations or subfeatures unless they provide a distinct outcome.
- Record one row per feature with a stable ID, area, behavior, entry points or automatic trigger, limitations, and evidence. Reuse an established ID scheme; otherwise use area-independent IDs such as `F-001` so regrouping does not renumber features.
- Separate **evidence** (observed, code-supported, documented-only, unknown) from **availability** (supported, conditional, unsupported, unknown in a specified context). Tests support only the behavior they cover; code inspection does not prove live provider availability.
- Link to concrete implementation, tests, or observations. Explain meaningful conditions such as disabled flags, platform restrictions, or missing entry points. Do not infer support from a dependency, enum member, method name, mock, or aspirational design alone.
- Record unresolved claims as unknowns instead of inventing behavior or treating missing evidence as proof of absence. State what was inspected and what was not; avoid claiming exhaustive coverage from a partial pass.

## Choose views, from flat to visual

Read only the references needed for the requested output. Their examples describe the same fictional notebook product and are illustrative, not evidence about the inspected application.

| Format | Use | Reference |
|---|---|---|
| Flat inventory | Precise, traceable list; basis for the other views | [Inventory](references/inventory.md) |
| Feature tree | Orientation and functional grouping | [Tree](references/tree.md) |
| Journey/story map | Explain how existing features support a user goal | [Journeys](references/journeys.md) |
| Capability matrix | Compare availability across one explicit dimension | [Matrix](references/matrix.md) |
| Connected capability chart | Visual hierarchy with explicit connections from product to areas to features | [Visual chart](references/visual-chart.md) |

Keep the inventory authoritative for feature identity and behavior. Other views reference its IDs rather than becoming independent catalogs. Label partial views with their scope. Add short feature detail sections only when behavior or limitations do not fit a readable row.

Write a product reference, not a demonstration of these formats. Use concrete behavior, meaningful product-specific comparisons, and actual user/operator journeys. Supporting views should help readers understand the product rather than repeat the inventory or fill a matrix with empty comparisons.

## Reconcile an existing map

Preserve IDs, vocabulary, and unrelated content. Add new IDs for distinct capabilities; keep IDs for renames and moves. Never reuse a removed ID for a different capability. For splits or merges, preserve the ID of a clearly continuing capability and assign new IDs only where needed; explain changed references in the task summary, not a document changelog.

Confirm removals against current behavior, including alternate entry points. Remove confirmed obsolete capabilities from current-state views and repair references. If removal is uncertain, retain an explicitly uncertain claim pending verification. Respect an existing external reference or retirement convention when one exists.

Update affected inventory rows, tree branches, journeys, matrix cells, and visual nodes together. Do not regenerate unaffected sections merely to impose this skill's preferred format. Report the scope of the update and outstanding unknowns in the task response.

## Contract with planning

The map is an input to planning, not a plan. Make it easy to find through the project's existing documentation index when one exists. Planning skills should read the map to understand current capabilities and reference feature IDs, verifying relevant implementation when the map may be stale. Proposed features, priorities, release slices, and acceptance criteria belong in planning artifacts. Update the map after implementation establishes behavior.

Starting a planning task does not itself require map regeneration. A missing or demonstrably stale map can warrant a separate documentation pass. Do not change other planning skills or implement missing product features as part of mapping unless requested.

## Check the result

Check that each claim has appropriate evidence, IDs are unique, every cross-view reference resolves, and all displayed limitations agree with the inventory. Check local links and diagram syntax where tools are available; provide the text fallback even when Mermaid rendering is unavailable. Keep the artifact about current state, with no speculative features or change history. Summarize coverage and verification limits honestly.
