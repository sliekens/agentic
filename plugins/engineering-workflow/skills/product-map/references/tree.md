# Feature tree

Use a shallow functional hierarchy for orientation. Usually area, capability, and feature are sufficient. Avoid forcing a fixed number of areas or copying the navigation structure. Reference inventory IDs at leaves; put a shared feature in one primary area and cross-reference it elsewhere when useful.

## Example: Pocket Notes

```text
Pocket Notes
|-- Capture
|   `-- F-001 Create note
|-- Organize
|   `-- F-002 Tag note
|-- Retrieve
|   `-- F-003 Search notes
|-- Portability
|   `-- F-004 Export Markdown
`-- Recovery
    `-- F-005 Restore deleted note
```

The inventory contains limits such as title-only CLI search. Do not turn this into a checklist of future work. Check that every in-scope inventory feature has a home and that branch labels describe product purposes rather than code modules.
