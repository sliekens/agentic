---
name: operator-setup
description: Create or update .agents/OPERATOR.md in the current workspace — a personal profile that tells AI models who you are, your skill levels, and how you like to collaborate. Only invoke when the user explicitly runs /operator-setup. Do not auto-trigger based on context.
---

# Operator Setup

Interview the operator to create `.agents/OPERATOR.md` in the current workspace. This file is gitignored and loaded at the start of every session to help models calibrate explanation depth, autonomy level, and communication style.

## Before starting

Check if `.agents/OPERATOR.md` already exists. If it does, tell the user what it currently contains and ask if they want to update specific sections or start fresh.

## Tech stack detection

Read `AGENTS.md` (or `CLAUDE.md`) and scan the project root for signals:

- `*.csproj` → C# / .NET
- `package.json` → JavaScript / TypeScript
- `*.py` → Python
- `*.go` → Go
- `Dockerfile` / `docker-compose.yml` → Docker / containers
- `*.tf` → Terraform

You'll use the top 2–4 technologies to ask targeted skill-level questions.

## Interview (one question at a time)

Ask questions one at a time. If a tool for presenting structured questions is available (e.g. `AskUserQuestion`), prefer it. Otherwise ask in plain text. Do not ask the next question until the previous one is answered.

**Q1 — Role**
What is their primary role on this project? Ask as an open question; do not constrain to a fixed list. Common examples: Solo owner, Lead developer, Solution Architect, Backend developer, Frontend developer, Full-stack developer, Test Analyst, DevSecOps engineer, DevOps engineer. Use the answer to infer decision authority and what kinds of concerns they care about.

**Q2 — Autonomy**
How autonomous should the model be?
Options:

- Fully autonomous — act on reasonable assumptions, minimal check-ins
- Checkpoint on approach — agree on plan before implementing, then execute
- Frequent check-ins — confirm at key decision points
- Depends on risk — autonomous for low-risk, check in for architectural or destructive changes

**Q3 — Verbosity**
How much explanation do they want?
Options:

- Minimal — code and diffs, very little prose
- Brief rationale — one sentence on why, then the change
- Explain trade-offs — surface alternatives and reasoning before committing
- Teach me — explain what's happening, especially in unfamiliar areas

**Q4 — Working mode**
How do they focus when working with an AI?
Options:

- I direct, you implement — clear picture of what they want; model executes
- Collaborative problem-solving — think through the problem together before committing
- Review-driven — they write or sketch, model reviews and improves
- Exploration-first — use the model to understand options before deciding

**Q5 — Skill levels (repeat for each detected technology)**
For each significant technology from the detection step, ask:

> How would you rate your [Technology] skill level?
> Options: Expert | Proficient | Functional | Beginner

Expert = deep knowledge, no need to explain idioms
Proficient = comfortable day-to-day, occasional gaps in advanced topics
Functional = gets things done, not a primary domain
Beginner = still building foundational knowledge

Limit to the 2–4 most relevant technologies. Don't ask about every library.

## Generate .agents/OPERATOR.md

Create `.agents/` if it doesn't exist, then write `.agents/OPERATOR.md` in the workspace root:

```
# OPERATOR.md

Context about the human operator working with this codebase. Use this to calibrate
explanation depth, autonomy, and collaboration style.

## Role

[Role + decision authority. E.g. "Solo owner/developer. Full decision authority — no
approvals needed from stakeholders or teammates."]

## Autonomy

[One paragraph describing when to act vs. check in, based on their answer.]

## Communication Style

- **Verbosity:** [Their choice + one-line description]
- **Working mode:** [Their choice + one-line description]

## Skill Levels

| Area | Level | Notes |
|------|-------|-------|
[One row per technology. Notes column: what to skip explaining / what to surface.]
```

## Wire up the repository AGENTS.md / CLAUDE.md

Find the repo-level instructions file: prefer `AGENTS.md` at the repository root, fall
back to `CLAUDE.md`. If neither exists, create `AGENTS.md`.

Add the following block if it isn't already present — don't overwrite anything else:

```
At the start of every session, read `.agents/OPERATOR.md` for context about the
operator (role, skill levels, collaboration style). If the file does not exist, end
your first response with:

> No operator profile found. Run `/operator-setup` to create one.
```

## Protect OPERATOR.md from being committed

If the current directory is a git repository, add `.agents/OPERATOR.md` to `.gitignore`
(under a "User-specific files" comment if one exists, otherwise at the top). This
prevents the personal profile from being accidentally committed to a shared repo.

## Confirm

Tell the user the file was written and that it will be loaded automatically in future sessions in this workspace.
