# Feature tree

Use a shallow functional hierarchy for orientation. Usually area, capability, and feature are sufficient. Avoid forcing a fixed number of areas or copying the navigation structure. Use descriptive feature names at leaves and link to their stable reference paths in a Markdown list when navigation is needed; put a shared feature in one primary area and cross-reference it elsewhere when useful.

## Example: Pocket Notes

```text
Pocket Notes
|-- Capture
|   `-- Create note
|-- Organize
|   `-- Tag note
|-- Retrieve
|   `-- Search notes
|-- Portability
|   `-- Export Markdown
`-- Recovery
    `-- Restore deleted note
```

The inventory contains limits such as title-only CLI search. Do not turn this into a checklist of future work. Check that every in-scope inventory feature has a home and that branch labels describe product purposes rather than code modules.
