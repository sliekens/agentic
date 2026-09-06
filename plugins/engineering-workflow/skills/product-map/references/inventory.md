# Flat inventory

Use this for enumeration and precise lookup. Keep one row per distinct behavior. For a small product, the table is enough; add linked detail sections only for significant rules. Evidence links should identify the implementing behavior, not just the repository root.

## Example: Pocket Notes

Scope: fictional web and CLI notebook application. These examples assume source inspection, not runtime verification. Paths below illustrate evidence labels; replace them with real links when mapping a product.

| ID | Area | Feature | Behavior | Entry / trigger | Limits | Evidence |
|---|---|---|---|---|---|---|
| F-001 | Capture | Create note | Store a title and body | Web editor; CLI `note add` | Title required | Code-supported: `notes/create` |
| F-002 | Organize | Tag note | Associate labels with a note | Web editor | No CLI entry point | Code-supported: `notes/tag` |
| F-003 | Retrieve | Search notes | Match text in titles and bodies | Web search; CLI `note search` | CLI searches titles only | Code-supported: both search handlers |
| F-004 | Portability | Export Markdown | Produce a Markdown file | Web note menu; CLI `note export` | Web exports one note; CLI also exports all | Code-supported: both export handlers |
| F-005 | Recovery | Restore deleted note | Return a deleted note to the notebook | Web trash | Only within retention period | Code-supported: restore handler |

A reported offline-editing feature has no supporting evidence in this example. Record it under unknowns; do not add it as supported to the inventory or imply it is absent.

IDs survive renaming and regrouping. Add availability or actor columns only when they clarify real differences. Avoid a vague `Done` column that conflates implementation, deployment, verification, and maturity.
