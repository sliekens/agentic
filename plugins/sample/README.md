# Sample Plugin

<!--
  Replace "Sample Plugin" with the name of your plugin.
  Fill in each section below and delete this comment.
-->

## Description

Briefly describe what this plugin provides and when it should be installed.

## Contents

| File | Purpose |
|---|---|
| `plugin.json` | Copilot CLI plugin manifest |
| `skills/sample/SKILL.md` | Core skill instructions |

## Creating a new plugin from this template

Copy this folder to `plugins/<your-plugin-name>/`, then:

1. Rename `skills/sample/` to the real skill name.
2. Update `plugin.json`.
3. Replace the placeholder content in `skills/<skill-name>/SKILL.md`.
4. Add references or other plugin components only when needed.

## Notes

Keep the root workflow concise. Move variant-specific details into `references/` when the plugin needs more than one operating mode.
