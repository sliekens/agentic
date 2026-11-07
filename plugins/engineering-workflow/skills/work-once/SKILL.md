---
name: work-once
description: Run one skill for one issue, write the returned next skill onto that issue, and exit. Use when a schedule wakes an agent, when the user runs /work-once, or when one tick should resume from the issue tracker. Prefer an open issue that already has next_skill and is not waiting on a person. Otherwise run `fix-loop` on the oldest actionable issue, one issue only. Do not load the returned next skill in this run. Do not use to burn down a backlog in one sitting (`fix-loop`), to plan a replacement (`yak-shave`), to perform parallel change (`expand-and-contract`), or to file a defect (`bug-report`), except as the single skill this tick was told to run.
---

# Work Once

One wake runs one skill for one issue, writes that skill's return onto the issue, and exits. The next wake starts empty and reads the issue.

The return is a [work result](../capture-skill/references/work-result.md): `stop_reason`, `issue_id`, and `next_skill`. `next_skill` is a request. This skill stores it. It does not load it.

## Authority boundary

- `/work-once`, or a scheduled wake that names this skill, authorizes one read of the issue-tracker record, one skill, and one cursor write.
- It does not authorize a second skill in the same run.
- It does not authorize burning down the backlog in one sitting. That is `fix-loop` in backlog mode.
- It does not authorize a schedule. The host starts the wake.

## 1. Read the tracker

Read the workspace issue-tracker record (`ISSUE_TRACKER.md` by default). This tick needs **List and search**, **Comment**, the blocked convention, and a `Cursor` section whose **Set** and **Find** are filled in.

When the file is missing, or those operations are still placeholders, or `Cursor` is missing, the one skill this tick is `workspace-setup`. Run it. Do not write a cursor. When it stops because only the user can answer, print `stop_reason=needs-user`. Otherwise print `stop_reason=tracker-missing`. In both cases `issue_id=none` and `next_skill=none`. Exit.

Done when the record can find a cursor and comment on an issue, or this tick has already exited.

## 2. Pick one issue

Use **Find**. Take the oldest open issue that has `next_skill` set, is not blocked, and has no open pull request of its own.

When none, take the oldest open issue that `fix-loop` step 1 would take: not blocked, no open pull request of its own, and not waiting on a release. Also skip an issue whose latest `work-once` comment has `stop_reason` `awaiting-release`. The skill for that issue is `fix-loop`, in tick mode.

When none, print `stop_reason=idle issue_id=none next_skill=none` and exit.

Done when one issue and one skill name are chosen.

## 3. Run that skill

Follow that one skill. The caller is `work-once`, so the skill uses tick mode and returns a work result. It must not load `next_skill`.

When the stored name is not a skill in this plugin, do not invent one. The result is `stop_reason: blocked`, `next_skill: none`, on that `issue_id`.

Do not start the skill named in the return.

Done when the return is recorded and no second skill has started.

## 4. Write the cursor and exit

A crash before this write leaves the previous cursor in place. The next wake runs that skill again.

When `issue_id` is `none`, do not invent an issue. Print the stop line and exit. A `next_skill` with no issue does not survive this process.

Otherwise write the cursor as [work result](../capture-skill/references/work-result.md) describes, then print one line and exit:

`stop_reason=<token> issue_id=<id> next_skill=<skill|none>`

Done when the issue matches the return, or there was no issue to write, and the process stops.
