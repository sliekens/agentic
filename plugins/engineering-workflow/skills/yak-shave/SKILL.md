---
name: yak-shave
description: Plan a replacement before Parallel Change. Sniff out a bad system or a feature the current architecture cannot hold, inventory what that system does, decide which capabilities to retain, retire, or introduce, and design the interface for that set. Then enter `expand-and-contract`. Use when the user says yak shave or yak shaving, when a new feature does not fit the architecture, when `scenario-design` finds a scenario the architecture cannot hold, or when `fix-loop` stops because the architecture is unsound. Do not use to harden a sound architecture that already fits the goal (`fix-loop`), to build, migrate, and delete once the interface is confirmed (`expand-and-contract`), or to untangle the whole codebase in one pass rather than replace one system (`untangle-codebase`). When `work-once` runs this skill, return the next skill at a handoff and do not enter it.
---

# Yak Shave

The path from a bad system, or from a feature the current architecture cannot hold, to a new interface, and then into Expand and Contract. A natural entry is `scenario-design`: scenarios come first, and an architecture obstacle found there is the handoff.

## Authority boundary

- `/yak-shave`, a handoff from `scenario-design` or `fix-loop`, or a request to replace a system authorizes the sniff, the inventory, the recommendation, and the interface design inside the boundary.
- Retain, retire, and introduce change what the product does. Show the dispositions and wait for the user before designing the interface or entering `expand-and-contract`.
- It does not authorize building the new structure. That work is `expand-and-contract`.
- It does not authorize hardening a sound architecture whose current structure can hold the goal. That work is `fix-loop`.
- It does not authorize untangling the whole codebase in one pass. That work is `untangle-codebase`.

## Tick

When `work-once` is the caller, this run is tick mode. Return a [work result](../capture-skill/references/work-result.md) at the handoff and stop. Do not load the next skill. Do not write the cursor. `analyze-complexity`, `product-map`, and `design-space-exploration` stay inside this skill.

- Step 1, the architecture is sound: `stop_reason: sound`, `next_skill: fix-loop`.
- Step 3, the set is not confirmed: write the proposed table on the issue as unconfirmed. Return `stop_reason: needs-user`, `next_skill: none`. Do not wait in this session.
- Step 5: `stop_reason: interface-ready`, `next_skill: expand-and-contract`.

## 1. Sniff

Run `analyze-complexity` on the boundary the user named, or on the pain site. Read **Stacking complexity**. Scenarios passed from `scenario-design` are the pain site and the goal. Do not repeat that scenario pass.

Continue this skill when either is true:

- the architecture is unsound;
- the goal needs a capability the current structure cannot provide without a new interface.

When the architecture is sound and the current structure can hold the goal, stop and hand the work to `fix-loop`. In tick mode, return `sound` / `fix-loop` and do not load `fix-loop`.

Done when the class is named, the inherent invariants are named, and the reason to continue or stop is one sentence.

## 2. Inventory

Read the product map for this boundary. When the map is missing or stale for the boundary, create or update it with `product-map`. Map the boundary, not the whole product.

The map records current behavior only. Retain, retire, and introduce stay out of it.

Done when every current capability in the boundary has an ID on the map.

## 3. Choose the set

Assign one disposition to each capability, and introduce any capability the goal needs that the map does not have.

| ID | Capability | Disposition | Why |
| --- | --- | --- | --- |
| F-001 | Current capability | retain or retire | The reason, tied to an inherent invariant or to the goal |
| new | Capability the map lacks | introduce | Why the goal needs it, and why the current structure cannot hold it |

Retiring a capability that drops an inherent invariant is not valid. Move that invariant onto a retained or introduced capability.

Show the table and wait. The user confirms or edits the set. In tick mode, do not wait. Write the proposed table on the issue as unconfirmed, return `needs-user` / `none`, and do not publish it as confirmed.

Publish the sniff and the confirmed set to the issue tracker. When the user confirms a set that an earlier tick left blocked, clear the blocked mark first. Read the workspace issue-tracker record (`ISSUE_TRACKER.md` by default) for the mechanism. File one issue titled `Yak shave: <boundary>`, or extend the open issue for that boundary. Write `docs/analysis/<boundary>-yak-shave.md` only when the record names repository files. When no record exists and the project has an issue tracker, use that tracker and suggest `/workspace-setup`. When it has none, keep the table in the conversation and ask where it should go.

Done when the user has confirmed the set and the issue holds that set.

## 4. Design the interface

Design one interface that exposes the confirmed set and nothing else. For each retained or introduced capability, name the operation, its inputs, and its outputs. A retired capability has no operation. The interface preserves the inherent invariants from the sniff.

When more than one interface shape can express that set, run `design-space-exploration`, then choose. Record the chosen shape and the rejected shapes on the same issue.

Done when the issue holds the interface.

## 5. Enter Expand and Contract

Continue under `expand-and-contract` with the confirmed set, the interface, and the inherent invariants. In tick mode, return `interface-ready` / `expand-and-contract` and do not enter `expand-and-contract`.

Done when `expand-and-contract` has that handoff, or tick mode has returned the work result.
