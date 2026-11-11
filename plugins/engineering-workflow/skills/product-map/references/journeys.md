# Journey / story map

Use when readers need to understand how capabilities support a goal. Arrange activities in their usual order and place existing features beneath them. This is a current-state journey view, without roadmap priorities or release slices. One feature can support several journeys with the same reference target.

## Example: Pocket Notes

Goal: capture an idea and reuse it later.

| Capture | Organize | Find again | Reuse |
|---|---|---|---|
| [Create note](features/create-note.md) | [Tag note](features/tag-note.md) | [Search notes](features/search-notes.md) | [Export Markdown](features/export-markdown.md) |
| Web or CLI | Web only | CLI searches titles only | Web single-note or CLI bulk export |

Recovery journey: open web trash, select a retained note, use [Restore deleted note](features/restore-deleted-note.md), then use [Search notes](features/search-notes.md) to find it again.

Name the actor or interface when it changes the journey. State preconditions and limits that interrupt a path. Investigate an unverified step through targeted follow-up before completing the journey. If a concrete blocker prevents resolution, report that journey as incomplete separately. Do not treat a research gap as a product gap to implement. Use a few relevant journeys instead of forcing every background capability into a user story.
