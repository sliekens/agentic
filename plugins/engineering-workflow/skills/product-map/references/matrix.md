# Capability matrix

Compare one dimension at a time: interfaces, platforms, roles, editions, or operating modes. Do not mix provider and interface columns into a matrix that implies their combinations are supported. Use separate matrices when both matter.

## Example: Pocket Notes by interface

| Feature | Web | CLI |
|---|---|---|
| F-001 Create note | Supported | Supported |
| F-002 Tag note | Supported | Unsupported: no command |
| F-003 Search notes | Titles and bodies | Partial: titles only |
| F-004 Export Markdown | Partial: one note at a time | Single note or all notes |
| F-005 Restore deleted note | Within retention period | Unsupported: no command |

Each cell describes the same feature and context as the inventory. Use `Unknown` when coverage was not established, and `Not applicable` only when the dimension does not apply. A blank cell or an unexplained dash cannot distinguish these cases. Link evidence in the inventory; add cell-specific evidence when the inventory does not substantiate the difference.

For automatic work, distinguish a web control that enables a feature from a background process that executes it. Both can be present without being equivalent interfaces.
