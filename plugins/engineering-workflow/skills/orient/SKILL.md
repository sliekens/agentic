---
name: orient
description: Help the user fill a specific gap in their mental model of a system. Use this skill when the user asks "why doesn't X happen", "how does Y work here", "why is this method not called", "why does this text get clipped", or any question where they clearly understand most of the system but are stuck on one specific behavior or mechanism. They have most of the picture — one piece is missing or wrong. This skill always reads back an interpretation of the gap before answering, so misunderstandings get caught early. Activate eagerly on "why" or "how does this work" questions about specific behaviors.
---

The user has a working mental model with one gap. Find the missing piece and state it as concisely as possible.

## Step 1 — State your interpretation first

Before answering, write 1–2 lines:

> **You're asking:** [what the user wants to understand]
> **The gap:** [the assumption or fact that's missing or wrong in their model]

This gives the user a chance to catch a misread before investing time in an answer to the wrong question.

## Step 2 — Gather material

Scan broadly until you find the mechanism that explains the behavior:

- Nearby code: callers, callees, base classes, interfaces, configuration, event bindings
- Related files: CSS, templates, middleware, layout, generated code
- External sources: if a third-party library is involved, fetch its documentation or source

Stop when you've found the one thing that closes the gap.

## Step 3 — Answer

Lead with the key fact. Add one or two sentences of context only if they'd be non-obvious to someone who already understands the surrounding system.

No preamble. No summary. If one sentence answers it, use one sentence.

Assume the user knows the language, framework, and general system — skip anything they already know. Use their vocabulary.

## Step 4 — Suggest follow-up gaps (conditional)

After answering, consider whether the gap just filled is part of a cluster — where not knowing A makes it likely the user also hasn't encountered B or C. If so, offer 2–3 terse follow-up questions the user could ask next, phrased as they would ask them:

> **Where next?**
>
> - Why does X also affect Y?
> - How does Z get initialized in the first place?
> - What happens when this fails?

Only do this when the gaps are genuinely related and the user is likely to hit them. Skip it for isolated questions where the surrounding model is probably intact. The goal is to guide vertical exploration, not pad every answer with a menu.
