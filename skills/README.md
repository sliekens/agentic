# Skills

This folder contains **skills** — self-contained bundles of instructions and supporting resources that can be dropped into any project to give Copilot specialized knowledge.

## What is a skill?

A skill is a folder that combines:
- One or more `.instructions.md` files with scoped coding guidance.
- Optionally, `.prompt.md` files for related tasks.
- A `README.md` that explains the skill and how to install it.

## Structure

```
skills/
└── <skill-name>/
    ├── README.md                  # What the skill does and how to install it
    ├── <name>.instructions.md     # The core instructions
    └── <name>.prompt.md           # (optional) companion prompts
```

## Creating a new skill

1. Copy the `sample/` folder and rename it.
2. Edit `README.md` to describe the skill.
3. Replace the placeholder content in `sample.instructions.md` (and any `.prompt.md` files) with real rules.

## Installing a skill in a project

Copy the skill folder contents into the target project:

```
.github/
  instructions/
    <skill-name>.instructions.md
  prompts/
    <skill-name>-<task>.prompt.md   # if the skill includes prompts
```

See [`sample/README.md`](sample/README.md) for a ready-to-copy template.
