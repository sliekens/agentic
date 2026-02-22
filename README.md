# skill-issues

My personal collection of GitHub Copilot customizations — prompts, instructions, agents, and skills — tailored to my specific workflows and preferences.

> Inspired by [github/awesome-copilot](https://github.com/github/awesome-copilot).

## Structure

```
skill-issues/
├── .github/
│   └── copilot-instructions.md   # Global Copilot instructions for this repo
├── prompts/
│   ├── README.md                 # How to use prompt files
│   └── sample.prompt.md          # Template for new prompts
├── instructions/
│   ├── README.md                 # How to use instruction files
│   └── sample.instructions.md    # Template for new instructions
├── agents/
│   ├── README.md                 # How to define custom agents
│   └── sample/
│       └── README.md             # Template for a new agent
└── skills/
    ├── README.md                 # How to create skills
    └── sample/
        ├── README.md             # Template for a new skill
        └── sample.instructions.md
```

## Quick Reference

| Folder | Purpose | File type |
|---|---|---|
| `.github/` | Repo-level Copilot instructions | `copilot-instructions.md` |
| `prompts/` | Reusable, task-specific prompts | `*.prompt.md` |
| `instructions/` | Coding standards applied to matching files | `*.instructions.md` |
| `agents/` | Custom agent configurations (MCP / tools) | `README.md` per agent |
| `skills/` | Self-contained instruction bundles | folder + `*.instructions.md` |

## Usage

Copy any prompt or instruction file into the `.github/prompts/` or `.github/instructions/` directory of a target repository to activate it in that project. Skills can be copied in their entirety.

See the `README.md` inside each folder for detailed guidance and the format each file type expects.
