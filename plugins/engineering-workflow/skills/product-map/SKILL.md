---
name: product-map
description: Create or update a product map, feature map, or capability map from an existing implementation. Use when no map exists, when documenting what a program does, or after code changes add, alter, or remove capabilities that an existing map must reflect. Produces current-state documentation that planning can consult; does not propose features or replace product planning.
---

# Product map

Document what the product can do today, for users, operators, and integrating systems. Write product descriptions at two levels: a high-level map and linked feature references. Keep one authoritative home for each level of detail and derive other views from it. A capability is an observable outcome; a button is an entry point and a class is implementation evidence.

The map describes existing capabilities. Proposed features, priorities, release slices, and acceptance criteria belong in planning documents. Update the map after implementation establishes behavior.

## Establish the baseline

Find existing feature documentation and project instructions before choosing a path, vocabulary, or format. Search for product, feature, and capability maps as well as documentation indexes. Read the relevant implementation rather than treating an old map or design document as proof.

Link the map from the project's existing documentation index when one exists.

Ground descriptions in concrete implementation, tests, or observations during research. Do not infer support from a dependency, enum member, method name, mock, or aspirational design alone.

For a new map, add a short scope note with the product boundary, intended readers, inspected version or revision, and covered interfaces. Include configuration assumptions only when they affect the mapped capabilities. Follow project documentation conventions; otherwise use `docs/product-map.md`. Default to a short product overview followed by feature sections grouped by product area. Read [Inventory](references/inventory.md) for the layout and an example. Ask only when an unresolved scope or audience choice materially affects the result.

For an update, read the existing map and the relevant implementation changes. Use a diff or supplied change description to locate affected behavior, then check callers, entry points, configuration, and tests in current code. If the change boundary is unknown, inspect the relevant area without implying a whole-product audit.

## Discover and substantiate capabilities

- Follow user and operator entry points through their behavior: pages, commands, API routes, integrations, configuration, scheduled work, recovery, and maintenance. A route list or sitemap helps check coverage but is not the feature taxonomy.
- Group by product purpose, not source folders. Name features with concise actions and objects.
- Describe what each feature does, how people or systems use it, how it behaves, and its limitations. Link its high-level summary to a descriptive reference path. Use headings and short paragraphs by default. Use descriptive file names such as `features/search-notes.md` as stable reference targets. Visible titles can change while links keep the same target. Reuse suitable existing references rather than adding numbered feature IDs.
- During research, distinguish evidence from availability in the relevant context. Tests support only the behavior they cover; code inspection does not prove live provider availability. Explain product conditions to readers without turning research classifications into mandatory documentation fields.

## Resolve research gaps

After the initial exploration, identify missing facts that affect an in-scope product description. Inspect the relevant entry points, callers, configuration, tests, or runtime behavior to resolve each gap. Revisit the description and repeat targeted exploration as needed. Missing evidence does not prove absence, and an unknown label does not complete the research.

If access or another concrete constraint prevents resolution, report the blocker and affected scope separately in the task response. Mark that scope incomplete. Do not present an unknown label, silently omitted capability, or narrowed scope as a completed map. Keep research gaps out of the product description and do not invent behavior to fill them.

## Make the map easy to read

Start with what the product does and who uses it. Add a linked area list when the document needs navigation. Put the main behavior first in each feature section, followed by meaningful limits and a link to the detailed product reference. Keep research mechanics out of the product description.

Describe meaningful conditions such as disabled options, platform restrictions, or unavailable interfaces in product terms. Do not include supporting-evidence links to implementation or tests in the generated map or feature references. Link to product documentation for further explanation.

Use tables for short, comparable values. When rows need paragraphs, several links, or long limitations, use feature sections instead of widening the table. Keep enough detail to explain the behavior without repeating empty labels or identical status fields on every feature. State shared product conditions once, and identify exceptions at the relevant feature.

Use progressive disclosure to keep the main map concise as the product grows. Describe each feature at a high level, independently of the detail in neighboring features. Link to detailed references in separate files for options, rules, examples, and product behavior, reusing existing documentation when suitable. Keep conditions that materially change the claimed outcome visible in the summary. Preserve stable reference paths and one authoritative home for each level of detail, without copying reference content into the map.

## Choose supporting views

Use these presentation defaults at each level. Areas can remain sections in the main map; this does not require a separate document for every area.

| Level | Default presentation | Reader purpose |
|---|---|---|
| Product | Short overview and linked area list | Understand the product and find an area |
| Area | Grouped, high-level feature summaries with links to detailed references | Discover related capabilities |
| Feature | Descriptive prose, examples, and short procedures where useful | Understand behavior, usage, and limitations |

Choose optional visuals by the behavior or reader question, not by document depth. Use a journey or flow diagram for activities in order, a state diagram for states and transitions, a comparison table for differences, or a relationship diagram for meaningful connections. Do not require a diagram at every level. Omit a tree or chart that only repeats the grouped headings, and avoid showing the same hierarchy in both forms without a distinct purpose.

Read only the references needed for the requested output. Their examples describe the same fictional notebook product and are illustrative, not evidence about the inspected application. Example documentation paths are placeholders. Replace them with real reference targets when mapping a product.

| Format | Use | Reference |
|---|---|---|
| Feature inventory | Authoritative descriptions grouped by area; compact tables when they remain readable | [Inventory](references/inventory.md) |
| Optional hierarchy view: tree or connected chart | Orientation and functional grouping when headings alone do not answer the reader question | [Tree](references/tree.md), [chart](references/visual-chart.md) |
| Journey/story map | Explain how existing features support a user goal | [Journeys](references/journeys.md) |
| Capability matrix | Compare availability across one explicit dimension | [Matrix](references/matrix.md) |

Keep the map authoritative for feature summaries and the linked references authoritative for detailed product behavior. Other views use the same feature names and reference paths rather than becoming independent catalogs. Label partial views with their scope. Add a tree, journey, matrix, or chart only when requested or when it answers a distinct reader question. The default map does not need every view.

Write a product reference, not a demonstration of these formats. Use concrete behavior, meaningful product-specific comparisons, and actual user/operator journeys. Supporting views should help readers understand the product rather than repeat the inventory or fill a matrix with empty comparisons.

## Reconcile an existing map

Preserve reference targets and vocabulary. Use new descriptive paths for distinct capabilities. Keep reference paths stable through ordinary title changes and regrouping. Never reuse a retired path for a different capability. Preserve existing numbered references that other documents still use. When migrating references or changing file paths, update known callers and preserve old targets with a forwarding note when needed. For splits or merges, preserve the reference of a clearly continuing capability and add new references only where needed. Explain changed references in the task summary, not a document changelog.

When a capability is removed, repair incoming references and respect the project's reference retirement convention when one exists.

Update affected feature summaries, detailed references, and supporting views together.

## Check the result

- Check that links reach the intended product references.
- Check that summaries and supporting views agree with the detailed descriptions, including limitations.
- Check that tables and diagrams remain readable in the intended viewer. Check diagram syntax and render locally when supported. Provide a text fallback for diagrams.
