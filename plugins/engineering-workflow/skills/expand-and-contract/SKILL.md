---
name: expand-and-contract
description: Replace a system with Parallel Change, also called Expand and Contract. Build the new structure beside the old one, migrate existing usages, then delete the old structure. A later slice waits until production has reached its checkpoint. An additive migration must be in production before code that uses the new schema deploys. A version that has stopped using the old schema must be the running version before a destructive migration removes it. Use when `yak-shave` has confirmed the capability set and the interface, or when the user asks for parallel change or expand-and-contract and that set is already decided. Do not use to choose which capabilities to retain, retire, or introduce (`yak-shave`), to harden a sound architecture (`fix-loop`), to choose among greenfield designs (`design-space-exploration`), or to release or deploy.
---

# Expand and Contract

Parallel Change. Build the new structure, migrate existing usages, then delete the old structure, in that order. A slice lands on its own when the next slice is unsafe until production shows a checkpoint. An agent prepares a slice quickly. It does not release. A patch that leaves the old structure in place stacks complexity. The capability set and the interface come from `yak-shave`.

## Authority boundary

- `/expand-and-contract`, a handoff from `yak-shave`, or a request to run Parallel Change authorizes the three steps inside the analyzed boundary, within the repository's normal change process.
- With a confirmed set, Expand builds that interface. Retired capabilities disappear in Contract. Introduced capabilities appear in Expand.
- Without a confirmed set, the new structure keeps current product behavior. A retain, retire, or introduce decision stops the work. Continue under `yak-shave`.
- It does not authorize hardening a sound architecture whose current structure can hold the goal. That work is `fix-loop`.
- It does not authorize production releases or deployments. A checkpoint stops the skill until the user supplies production evidence. Reaching that checkpoint is a release. This skill does not run it.

## 1. Judge

Run `analyze-complexity` on the boundary. Read **Stacking complexity** and class the architecture.

- A confirmed capability set and interface are in hand. Keep going. Expand builds that interface.
- The set is missing, and the architecture is unsound or the goal needs a capability the structure cannot hold. Stop and run `yak-shave`.
- The architecture is sound and the current structure can hold the goal. Stop and hand the work to `fix-loop`.

Done when one of those three is chosen and the inherent invariants are named.

## Checkpoints

A checkpoint is a fact in production that the next slice depends on. Write every checkpoint on the issue before Expand. Each one names the fact, the slice it gates, and the evidence that proves the fact.

Do not start the gated slice until that evidence is on the issue. Comment the evidence when it arrives. This skill does not release or deploy to produce it.

When the change splits a schema into an additive migration and a destructive migration, the issue includes these two checkpoints:

1. The additive migration has run in production before any deploy of code that uses the new schema.
2. Production is running a version that does not read or write the old schema before the destructive migration that removes that schema.

Any other pair of slices that production applies separately gets a checkpoint of the same shape. When production cannot observe a gap between two slices, those slices may land as one change. The issue says why no checkpoint is required.

Done when the issue lists every checkpoint, or states why the slices are one change.

## 2. Expand

Build the new structure beside the old one. Existing usages keep calling the old structure. The new structure preserves each inherent invariant and leaves the accidental structure out. When `yak-shave` confirmed an interface, Expand builds that interface.

Existing tests stay green. Do not add a test whose only subject is the old structure.

Land each slice under **Validate and land**. Code that uses a new schema is a later slice than the migration that adds that schema. Stop when a checkpoint gates the next slice.

Done when the new structure is in the codebase, nothing has migrated, the old path still behaves as before, and every open checkpoint is named on the issue.

## 3. Migrate

Start only when every checkpoint that gates this phase has evidence on the issue.

Move existing usages to the new structure. Both structures stay until the last usage has moved. Update tests that covered a moved usage so they cover the new structure.

Read **What deserves a test** in `blind-spot-coverage` for the new structure. A behavior earns a test only under that section.

The version that stops reading and writing the old structure lands as its own slice when a destructive removal follows. Stop at that checkpoint.

Done when the codebase has no remaining use of the old structure, that version has landed, and Contract's checkpoint is either evidenced or named as the stop.

## 4. Contract

Start only when every checkpoint that gates this phase has evidence on the issue.

Delete the old structure. Remove tests that exist only to lock it. A destructive migration is its own slice. It does not ride in the deploy that still has callers of the old schema.

Done when nothing in the codebase references the old structure, the destructive slice has landed, and the narrowest check that can fail is green.

## Validate and land

Each slice uses this section. Run the repository validation runbook for the files and behavior the slice touches, the same completion rule `fix-loop` uses. Land the slice as that runbook's `Integration` section says. Comment the slice and the next checkpoint on the issue. Leave the issue open while a checkpoint is unmet.

When the change came from `yak-shave`, update the product map with `product-map` after Contract, so the map matches the new current behavior.

Done for a slice when the planned checks pass and the slice has landed, or its pull request waits on a merge. Done for the skill when Contract meets its done line and no checkpoint is still open.
