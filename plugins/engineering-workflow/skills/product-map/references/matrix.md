# Capability matrix

Compare one dimension at a time: interfaces, platforms, roles, editions, or operating modes. Do not mix provider and interface columns into a matrix that implies their combinations are supported. Use separate matrices when both matter.

## Example: Pocket Notes by interface

| Feature | Web | CLI |
|---|---|---|
| [Create note](features/create-note.md) | Supported | Supported |
| [Tag note](features/tag-note.md) | Supported | Unsupported: no command |
| [Search notes](features/search-notes.md) | Titles and bodies | Partial: titles only |
| [Export Markdown](features/export-markdown.md) | Partial: one note at a time | Single note or all notes |
| [Restore deleted note](features/restore-deleted-note.md) | Within retention period | Unsupported: no command |

Each cell describes the same feature and context as the inventory. Investigate unresolved availability through targeted follow-up before completing the matrix. An `Unknown` cell, blank cell, or unexplained dash does not complete that work. Use `Not applicable` only when the dimension does not apply. Explain meaningful differences in product terms and link to the detailed feature reference when needed. If a concrete blocker prevents resolution, report the affected comparison as incomplete separately from the product documentation.

For automatic work, distinguish a web control that enables a feature from a background process that executes it. Both can be present without being equivalent interfaces.
