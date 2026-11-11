# Feature inventory and detailed references

Keep one authoritative summary per feature in the map and one authoritative home for its detailed product description. Group summaries under product-area headings, with descriptive titles and stable links to feature references.

Start the map with a short explanation of the product and its readers. Add a short scope note with the covered interfaces and inspected revision. For a long map, add links to the area headings.

Keep each summary at a high level: what the feature does and any limitation that materially changes that outcome. Link to a detailed product reference in a separate file. Reuse suitable existing documentation.

## Write the detailed reference

Describe the feature as part of the product. Explain what it does, how someone uses it, how it behaves, and what limits or conditions apply. For automatic capabilities, explain what starts them and what happens next. “How it works” means behavior the reader needs to understand, including useful underlying concepts. Source structure does not determine the description.

Choose headings that suit the feature. Natural descriptions, examples, and short procedures can explain more than a repeated set of fields. Include options, interactions, results, and failure or recovery behavior when they matter. Describe only behavior established by the research.

Implementation and test inspection support accuracy during research. The reference itself serves readers who want to understand the product. Do not include supporting-evidence links to source code or tests, or an index of handlers, classes, or evidence labels. Link to related product documentation when it helps explain behavior.

## Example: Pocket Notes map excerpt

This fictional web and CLI notebook illustrates the document layout. Its paths and behavior are illustrative. Replace them with real product descriptions and reference targets. A real map also identifies the inspected revision.

```markdown
# Pocket Notes product map

Pocket Notes lets people capture ideas, organize notes, and find them later through a web app and command line.

Scope: web app and CLI, for people who manage personal notes.

## Capture

### Create note

Store a note with a title and body through the web editor or `note add`. A title is required.

[About note creation](features/create-note.md)

## Retrieve

### Search notes

Find notes through web search or `note search`. CLI search covers titles only.

[How search works](features/search-notes.md)
```

This excerpt shows two features, not the full fictional product.

## Example: detailed search reference

The file `features/search-notes.md` describes the product capability:

```markdown
# Search notes

Search helps you find a note when you remember words from its title or content.

## Search in the web app

Enter your search text in the search field. Web search matches text in both note titles and bodies.

For example, searching for `meeting` can find a note titled “Meeting notes” or a note that contains “meeting” in its body.

## Search from the command line

Use `note search` to find notes by title. A word that appears only in a note body will not produce a match through the CLI.

## Limitations

The web app and CLI search different parts of a note. Use web search when you need to search note bodies.
```

This example describes only established fictional behavior. A real reference explains matching options or other rules only after the implementation establishes them.

## When a table fits

For a small inventory with short descriptions, a compact table can replace feature sections. Group tables by area when that avoids a repeated area column. Put detailed product behavior in linked references in separate files rather than expanding cells.

| Feature | Behavior and limits |
|---|---|
| [Create note](features/create-note.md) | Store a title and body. Title required. |
| [Search notes](features/search-notes.md) | Web searches titles and bodies. CLI searches titles only. |

Reference paths survive title changes and regrouping. Explain availability when it differs by context. Avoid a vague `Done` field that conflates implementation, deployment, verification, and maturity.
