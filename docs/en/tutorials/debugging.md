# Build reproducible gameplay checks and reports

[简体中文](../../zh-CN/tutorials/debugging.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14


Goal: split “build succeeds but nothing happens” into six checks: registration, appearance, trigger, measurement, settlement and reset. Prerequisite: [first mod](first-mod.md). Use a [fixed stage](stage.md) and [specified reward](treasure.md) with only necessary content. This is a test in your workshop source project; no Unity project is required.

## 1. Fix inputs and record deltas

Choose a fixed character, board, reward, level and quality. Remove unrelated treasures. Record HP, shield, attributes, gold, turn, columns and counters before and after. Separate display results from actual state. “Total shield is 10” cannot show whether this treasure added 3.

## 2. Minimum coverage by content

| Content | Cover at least |
| --- | --- |
| Treasure | Acquisition, level, quality values, repeated preview, stacking, cap, new stage, restore |
| Move | Uses 0/1/cap, no target, multiple targets, automatic activation, restored uses |
| Enemy | Independent counters for two instances, defense, zero HP damage, death and boss reward |
| Item | Direct/targeted use, exposed target, healing modifiers, removal and notification |
| Choice | No effects on opening, payment, repeated clicks, rollback, chained cancellation, restore |
| Adventure | Selection entry, character list, every exit, preparation, final victory, loop termination/continuation failure |
| Page/assets | Original-menu fallback, missing files, language switch, original font/layout, cropping, global audio settings |

Minimums, caps and exact affordability versus one short often reveal more than ten additional normal cases. Fix seeds and record actions for random content; the same seed with different actions need not yield the same result.

## 3. Locate the first failed layer

For compilation, inspect the first compiler error. For loading, inspect package ID, full entry point, API, hashes and duplicates. For appearance, check pool/stage placement after registration. For triggers, check the event and real action. For numbers, check requested, shared accumulators and rounding. For a second-attempt failure, inspect instance state, caps and resets. Use [troubleshooting](../troubleshooting.md) for symptoms.

## 4. Copyable report

```text
Guide revision / API / package version:
Lesson and step:
Seed / character / difficulty / quality / level:
Files changed and registered IDs:
Action sequence:
Before -> expected -> actual:
First diagnostic code and location:
Build / load / gameplay / save / UI / Steam: passed, failed, or not run
```

Share only relevant source and diagnostics, removing private paths, accounts, saves and development references. Include the code, not just the final “failed” line. Local installation, same-process reload, full restart and Steam submission require separate results.

## 5. Recheck according to the change

Text changes need bilingual and layout checks. Number changes need descriptions, boundaries and effects. Event/state changes need preview, reset and restoration. Entry/reference changes need full restart and registration. Increment the version for each rebuilt installation. Maintainers may run documentation tools, but link checks do not verify gameplay. Unity checks use only the already-open formal Editor; guide readers need neither Unity installation nor project copies.
