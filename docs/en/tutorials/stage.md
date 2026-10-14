# Build a small adventure you can finish

[简体中文](../../zh-CN/tutorials/stage.md) · [Index](../README.md)

Add **Trail Lab** to your mod. It has one guard with an exit hidden underneath. Defeat the guard, use the exit, then change the guard's HP from 4 to 8 to see your stage update.

**Before this lesson:** finish [Your first mod](first-mod.md) and keep its `ModEntry` and `StarterRelic`. You need no artwork or music.

| File | What you do |
| --- | --- |
| `source/PracticeStage.cs` | Create it and add the stage source |
| `source/ModEntry.cs` | Add a registration line inside `Load` |
| `package.json` | Increment the version before each changed installation |

## 1. Add the stage source

Use **Open Source** on your project's Workshop row. Create **`PracticeStage.cs`** inside `source` and paste all of [the fixed-stage source](../../../templates/en/08-fixed-stage-lab.cs.txt) into it.

If you used a different package ID from the first lesson, replace `namespace LocalAliceLanternTrailMod` with the namespace in your own `ModEntry.cs`. Keep `ModEntry.PackageId` elsewhere. You do not need a new entry class or a new project.

This file contains two classes: `PracticeStage` places cards on the board, and `PracticeAdventure` gives you an entry in level selection. Keep both.

In `source/ModEntry.cs`, find the existing `Load` method. Add the stage registration after the relic registration. The method should now be:

```csharp
public override void Load(IModRegistrar registrar)
{
    registrar.AddContent(new StarterRelic());
    registrar.AddContents(new PracticeStage(), new PracticeAdventure());
}
```

Replace only the existing `Load` method. Keep the rest of `ModEntry.cs`, including the `StarterRelic` class below it. Make sure the new file ends in `.cs`, not `.cs.txt`.

## 2. See why the guard covers the exit

Find these lines in `PracticeStage.cs`:

```csharp
columns[0].cards.Add(exit);
columns[0].cards.Add(guard);
```

The code places the exit first, then the guard. Cards are stored **bottom to top**, so the guard added last is exposed first. Defeat it to reveal the exit. `columns[0]` is the first column; `columns[1]` is the second.

![Cards are stored bottom to top; the guard is exposed before the exit](../../../images/fixed-column-order.svg)

The source already creates the full column structure and leaves the other columns empty. You do not need to fill them or change `appearancePool` or `cardsPerRound` yet. After playing the stage, you can look up those fields in the [stage reference](../reference/stages.md).

## 3. Play through it

1. Save both source files and increment the version in `package.json`.
2. Return to Workshop, choose **Build and Install**, and check that installation succeeds and the mod is enabled.
3. Fully exit and restart. From the main menu, open level selection and page through to **Trail Lab** (林径练习 in Chinese).
4. Choose its only difficulty and **Runehunter** (符刃猎手), then start.
5. The first column should expose a guard; the others should be empty. Click the guard to attack until it is defeated.
6. Click the revealed exit. The adventure should end in victory.

Existing character upgrades can change how many attacks defeat the guard. Check that the guard is defeated and the exit completes the adventure. The game's fallback artwork is enough for now; you can add your own later.

**No level-selection entry?** Check that `Load` registers both `PracticeStage` and `PracticeAdventure`. A board definition alone does not add a selectable adventure. Then check `IncludeInSelection` and the difficulty's `availableHeroIds` in [Troubleshooting](../troubleshooting.md). Keep `BuiltInCharacterIds.RuneHunter` as a code identifier rather than replacing it with a displayed name.

## 4. Give the guard 8 HP

In `PracticeStage.cs`, find `hp: 4` in the `ContentCards.Enemy(...)` call and change it to `hp: 8`. This changes HP without moving cards or exits.

Save, increment the version, build and install, fully restart and **start a new** Trail Lab run. The guard should now have 8 maximum HP. An old run already contains generated cards, so use a new run to check this change.

You can now create and modify a playable adventure. Continue with [Put your treasure in the stage](treasure.md) to see the starter shield take effect, or try [Connecting stages](adventure.md).

### Look this up later

The source keeps an exit template in `appearancePool` for older validators. A fixed layout does not add that template to the board, so you still have only one exit. See the [reference](../reference/stages.md) for fixed-column and random-pool constraints.

Names already use `ModText`. English source provides English fallback text. To display the corresponding Chinese names, follow [the text-merging steps](assets-and-text.md#merge-text-for-topic-fragments) for `stage.practice.*` and `adventure.practice.*`, then start a new run.
