# Journey / story map

Use when readers need to understand how capabilities support a goal. Arrange activities in their usual order and place existing features beneath them. This is a current-state journey view, without roadmap priorities or release slices. One feature can support several journeys without acquiring a new ID.

## Example: Pocket Notes

Goal: capture an idea and reuse it later.

| Capture | Organize | Find again | Reuse |
|---|---|---|---|
| F-001 Create note | F-002 Tag note | F-003 Search notes | F-004 Export Markdown |
| Web or CLI | Web only | CLI searches titles only | Web single-note or CLI bulk export |

Recovery journey: open web trash, select a retained note, use F-005 Restore deleted note, then use F-003 Search notes to find it again.

Name the actor or interface when it changes the journey. State preconditions and limits that interrupt a path. An unverified step is an unknown, not evidence that a product gap must be implemented. Use a few relevant journeys instead of forcing every background capability into a user story.
