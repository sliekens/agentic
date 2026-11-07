# ISSUE_TRACKER.md

<purpose: where this workspace tracks issues and the work artifacts that become issues, and how skills reach it. State that skills read this file before they publish anything.>

## Mechanism

- **Tracker:** <forge issues | external tracker | repository files | none>
- **Location:** <host and project, for example `gitea.example.com/owner/repo`; for repository files, the directory that holds them>
- **Tool:** <CLI, API, or MCP tools that operate it, with the login or flag they need>
- **Basis:** <user's choice, or the evidence behind the recommendation, for example the git remote host>

## Operations

- **Create:** <command>
- **Read:** <command, including comments>
- **List and search:** <command; how to include closed issues>
- **Comment:** <command>
- **Label or assign:** <command>
- **Close:** <command; whether it takes a comment>
- **Blocked convention:** <label, status, or `Blocked by:` line>

## Cursor

`work-once` writes this at the end of a wake. The next wake reads it. One issue has at most one `next_skill`.

- **next_skill storage:** <one label `next:<skill>`, or one line `next_skill: <skill>` at the top of the issue body>
- **Set:** <command that replaces any existing next_skill; delete the label or the line when the value is `none`>
- **Find:** <command that lists open issues that have a next_skill, oldest first>
- **Comment shape:** use **Comment**. The comment is three lines, `work-once:`, `stop_reason: <token>`, `next_skill: <skill|none>`, then one sentence. No log or trace body.

## Grouping

- **Technical debt:** <the project, milestone, or label that holds debt issues, and how to add an issue to it; `none` when the tracker cannot group>
- **Other groups:** <one line per group skills must use, or `none`>

## Artifacts

| Artifact | Destination |
| --- | --- |
| Analysis results (decision tables, scenarios, FMEA, state models, design spaces) | <one issue per analysis, or the file path pattern in repository-files mode> |
| Technical debt findings | <one issue per finding, added to the debt group> |
| Conformance and consistency findings (`cross-check`, `realign`) | <one issue per report, with one issue per approved remediation> |
| Durable current-state documents (product maps, ADRs, runbooks, reference docs) | <repository docs; the tracker holds work, not reference> |

## Repository files (only when the user chose this mechanism)

- **Directory:** <path>
- **Naming:** <pattern>
- **Status:** <how a file records open or closed, for example front matter>
- **Index:** <path of the index file, if any>
