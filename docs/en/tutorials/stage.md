# Make your first fixed stage

[简体中文](../../zh-CN/tutorials/stage.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14 · [Validation scope](../reference/versions.md)

Goal: **Trail Lab** appears in level selection. Its first column contains a guard above an exit; all other columns are empty. Defeat the guard, use the revealed exit, and finish with victory. Then change guard HP from 4 to 8 and see the new value after restarting.

Prerequisite: [Your first mod](first-mod.md). Add two complete content classes for this exercise; no finished adventure package is supplied. Edit `source/ModEntry.cs` and add `source/PracticeStage.cs`. No external classes, images, or music are needed.

Before installing a changed build, increment `package.json.version` as in [the first lesson](first-mod.md#4-change-one-value-and-verify-again). Different contents cannot replace an installed package under the same version.

## 1. Add the source stage and selection entry

Copy the [fixed-stage fragment](../../../templates/en/08-fixed-stage-lab.cs.txt) to `source/PracticeStage.cs`. Keep your generated namespace. It contains `PracticeStage` and `PracticeAdventure`, without a second mod entry.

Keep the relic registration in `ModEntry.Load` and add:

```csharp
registrar.AddContents(new PracticeStage(), new PracticeAdventure());
```

`StageContent` defines the board; `AdventureContent` creates its level-selection entry. Registering only the stage does not create that entry. This guard uses the public `ContentCards.Enemy` factory directly. After the [enemy lesson](enemy.md), you can register an `EnemyContent` and call its `CreateCard` instead.

## 2. Connect storage order to play order

![Fixed-column storage and exposure order](../../../images/fixed-column-order.svg)

`cards` stores cards from bottom to top. The last card is exposed. Adding the exit before the guard puts the guard in front of the player first. The loop creates the normal number of columns and adds cards only to the first; empty columns remain empty.

`appearancePool` includes an Exit template for compatibility with earlier validators. In the current C# validator, a fixed layout is checked for an exit in its fixed columns; a random layout is checked in its pool. With nonempty `fixedColumns`, runtime clones only the fixed columns and does not add random pool cards. That pool template will not create a second exit. See [Stage reference](../reference/stages.md).

## 3. Verify through player actions

Build and install, then fully exit and restart. Page through level selection to find Trail Lab, choose its only difficulty, and select Runehunter. The first column should expose the guard; the others should be empty.

Attack the guard. Once it is defeated, the exposed card should become the exit. Use the exit and check the victory result. Character upgrades can change the number of attacks needed; this lesson does not prescribe an exact count. Empty art fields use host fallback presentation for checking the rules. Add your own art before a finished release.

If the entry is absent, check adventure registration and `IncludeInSelection`. If the character cannot be selected, check the difficulty's `availableHeroIds` and host unlock rules. Use the stable public ID `BuiltInCharacterIds.RuneHunter`, not a localized name. The source's `allowedCharacterIds` is retained metadata rather than an enforced C# selection filter.

## 4. Change a visible value

In `ContentCards.Enemy`, change `hp: 4` to `hp: 8`. Rebuild, fully restart, and begin a new run. Guard maximum HP should become 8; card order and exit count should stay the same.

This proves the new DLL's content reaches the board. A successful build or registration count alone does not replace this check.

## Checks and next step

- The entry, its difficulty, and its permitted character are selectable.
- Normal column structure remains, only the first column is populated, and the guard is exposed first.
- The revealed exit can be used to finish the adventure, and the 4→8 source change takes effect.

Add the [treasure lesson's guaranteed reward](treasure.md), or continue with [Connecting stages](adventure.md). Random pools, bosses, graph routes, and loops remain in the [advanced overview](../02-content-creation.md).


Fragment names and descriptions now use ModText. Merge the sample entries as in [bilingual text](assets-and-text.md); without them, source fallbacks remain visible. Existing card/definition snapshots are not guaranteed to translate immediately, so check a fresh run after changing language.
