# Find out why your mod is not working

[简体中文](../../zh-CN/tutorials/debugging.md) · [Index](../README.md)

“It builds, but nothing happens in the game” can have several causes. Find the earliest failed step before changing source, artwork and stage layout all at once.

This page uses [Your first mod](first-mod.md), [the fixed stage](stage.md) and [the relic reward](treasure.md) as examples. You only need your mod project and the game.

## 1. Start with what you can see

| Symptom | Check first | Next step |
| --- | --- | --- |
| The build fails | The first compiler error's file and line | Fix it, then build again |
| The relic is missing from the codex | Successful installation, enabled mod, full restart and search language | Use [loading diagnostics](../troubleshooting.md) |
| The relic is in the codex but not in chests | Character pool eligibility, or simply a random draw | Grant it directly with the encounter |
| You collect the relic but gain no shield | Whether you have entered the next stage | A relic collected after entry triggers on the next entry |
| You changed 2 to 4 but still see 2 | Saved source, incremented version and successful new installation | Fully exit, restart and start a new run |
| Hurting one wolf also strengthens the other | Shared objects or `static` fields storing state | Use each card's own state |

Find specific diagnostic codes in [Troubleshooting](../troubleshooting.md). Fix the first failure, then move on.

## 2. Isolate it in a small practice run

Use one character, one reward and one effect to check. Place the content in fixed columns instead of waiting for random draws. Record values before and after, for example:

```text
Before: 0 shield; one level-1 Wayfarer's Relic collected; BaseValue is 4.
Action: defeat the first guard, use the exit and enter stage two through preparation.
Expected: gain 4 shield on entry.
Actual: shield remains 0.
```

That narrows the question to the stage-entry effect. “Shield is wrong” leaves out whether you collected the relic, entered another stage or took damage that consumed shield.

For random stages, keep the seed, difficulty and action sequence too. The same seed with different actions need not produce the same later random results.

## 3. Choose checks that match the edit

| You changed… | Try in the game |
| --- | --- |
| A name or description | Both languages are readable, placeholders become numbers and text is not cut off |
| A value or formula | Description and effect agree; minimums and caps work |
| A counter or trigger | First trigger, last trigger, beyond the cap and entry to another stage |
| Enemy state | Two enemies change independently; new cards start from initial values |
| A paid option | Exactly enough gold, one gold short and no duplicate payment |
| A multi-stage route | Every exit is reachable, the adventure can end in victory and Continue Game resumes it |
| A page or assets | Buttons work, the original menu is reachable, images and sound work in the game |

You do not need to repeat the entire table for a name change. Pick the relevant checks. Increment the version before installing changed content, and fully restart for C# changes.

## 4. Ask another person or AI for help

Copy this short template:

```text
Lesson page and step:
Game/API version, mod package ID and version:
Files and code I changed:
Steps to reproduce:
Expected result:
Actual result, including values before and after:
First error with file and line, or "none":
```

Share only relevant source and necessary errors. Remove private paths, account details and other personal content. Do not send whole game DLLs or saves. For a failed build, the first `error CS...` is usually more useful than the final “build failed” line.

When asking AI to fix it, request an explanation followed by the smallest relevant edit. Check each fix in the game before moving on, rather than having it rebuild a project that already works. See [Making mods with AI](../ai-authoring.md) for prompts.
