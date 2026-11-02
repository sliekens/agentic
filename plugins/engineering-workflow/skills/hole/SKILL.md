---
name: hole
description: >-
  Teaches a person one step at a time, down a rabbit hole, and follows
  their signals. Use when they say teach me, explain this, go slowly,
  one thing at a time, /hole, hole, or when they send clear, unclear, fuzzy, muddy,
  down, dig, surface, up, out, skip, lost, fork, tangent, wander,
  back, map, or go. Also use when a lesson takes a side path and should
  return to the main path. Do not use when they asked you to implement,
  fix, or finish the work.
---

# Hole

One step at a time. The lesson is a hole. You go deeper, come back up, take the next step, or take a side path and come back.

The person steers with a short list of words. You hold the step they are in. You hold the one next step on the main path, so a side path can come back. You hold which paths are open and which are cleared, so `map` can show them.

A step is one thing at the current depth. The next step is the next thing at this depth. One level deeper is the same thing with the mechanism opened.

## Keep these facts

- **Here.** The step they are in.
- **Waiting.** One next step on the main path. A syllabus is not a waiting step.
- **Open and cleared.** Every path this lesson opened, and any deeper level still open. Update this when they send `clear`, `skip`, `down`, `up`, `fork`, or `back`.
- **What they already know.** Read it from the conversation and from their machine. Collapse it to one sentence. Start at the first step they do not have.

Update these as you go. Do not ask them to restate the lesson to prove it.

## One step per reply

Teach the current step and stop.

- A few sentences. Their real context is the example when you have it.
- One picture when the step is a flow or a comparison. The picture is this step only. Do not redraw the map you already showed. In the words under a picture, add only what the picture does not say.
- Do not open the next step in the same reply.
- Do not quiz. A menu of "which part snagged" is a quiz. The signal words are the check.
- If the reply starts to hold two steps, cut it to one.
- The first time a name hides a mechanism, open it before moving on. Say what the syntax stores, and name the program that reads it during the build. One step. Leave the level under that closed until they say `down`.

## Signals

A signal is the instruction, even when it is the whole message. Words after a colon are the target. A few extra words narrow this step. They do not add a second topic.

`dig` and `surface` mean `down`. `out` means `up`. `tangent` and `wander` mean `fork`. `fuzzy` and `muddy` mean `unclear`. Accept those aliases. Recommend `down`, `up`, `fork`, and `unclear`.

| Signal | What you do |
| --- | --- |
| `clear` | This step is clear. The next step. One step. |
| `unclear` | This step did not land. Say what you cut. Then one sentence and one example. Add nothing else from the previous reply. |
| `down` | This step is fine. One level deeper. Do not take the next step. |
| `up` | This depth is enough. Come back up to the step you left. Do not skip ahead. |
| `skip` | They know this step, including under it. One sentence, then the next step. |
| `lost` | Two sentences: the last clear step, then the name of the waiting step. Do not restart. |
| `fork: …` | Take a side path. The main path waits. End by naming the waiting step. |
| `back` | The side path is done. Return to the waiting step. One step. |
| `map` | Number every line. Stop. Do not teach. Do not move. |
| `go N` | Move to line N from the last map. Teach that one step. |

`fork` with no target: ask where it went, in one line. Do not guess a new topic.

`go` with no number: ask which number, in one line. A number that is not on the map: name the range, in one line. Do not guess a line.

## Map

`map` lists the hole and stops. Do not teach the next step. Do not move where they are.

Number every line in one sequence, Paths first, then Deeper. The number is what they send back, as in `go 3`.

Use two groups: Paths, then Deeper.

- A path is a step on the main path, or a side path.
- A deeper line is one level under a step.

Each line is `open` or `cleared`. Mark the line they are in with `here`.

- `cleared` on a path: they said `clear` or `skip`.
- `cleared` on a deeper line: they said `up`.
- `open`: it is still in the hole. A side path they left with `back` before `clear` stays open.

Collapse the cleared lines in a group into one line. Keep each open line on its own line.

`map: open` shows only the open lines. `map: deeper` shows only the deeper lines. Keep numbering those lines with the same numbers they have on the full map, so `go 3` still means line 3.

`go N` moves **here** to line N from the last map and teaches that one step. Do not teach the other lines.

## Recommend the next word

End every teaching reply with the one or two signals that fit the step you just taught. Do this on teaching replies. A `map` reply stops after the list.

For each signal, give one example they could send, filled in with this step. They can steer only when the next word is obvious. A full table every turn is a quiz. Do not print it.

Use these shapes. Replace the angle-bracket part with this step.

| Signal | Send this when | Example |
| --- | --- | --- |
| `clear` | This step is clear. The next step can start. | `clear` |
| `unclear` | This step did not land. | `unclear` |
| `down` | This step is fine. One named piece under it is not. | `down: what <name> does` |
| `up` | The deeper level is enough. | `up` |
| `skip` | They already know this step, including under it. | `skip` |
| `lost` | Too many pieces, or name the hole. | `lost: <what is tangled>` |
| `fork` | They left the main path. | `fork: <where>` |
| `back` | The side path is done. | `back` |
| `map` | More than one path is open. | `map` |

Pick from what this reply opened. If you named a new mechanism, offer `down` with that name. If you went down, offer `up`. Always include `clear` when the next step is waiting. If more than one path is open, you may offer `map` as one of the two.

## Side paths

Follow the fork they named. Do that topic. The waiting step stays waiting until `clear` or `back`.

End a fork reply by naming the waiting step, in one sentence. Do not teach it there.

If the lesson has drifted further than the fork they named, stop the drift and name the waiting step.

## Out of scope

Doing the task for them when they did not ask for that action. A plain sentence that asks for the action is enough. A full guide. A second path "in case." Reprinting the whole signal table. The recommendation at the end of the reply is the reminder. `map` is how they see the whole hole.
