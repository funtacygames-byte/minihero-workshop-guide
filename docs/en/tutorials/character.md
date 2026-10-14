# Create a character, trait, and initial move

[简体中文](../../zh-CN/tutorials/character.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14 · [Validation scope](../reference/versions.md)

Goal: Trail Lab offers **Lantern Ranger** with base HP 24, attack 6, defense 1, and wisdom 2. Its only initial move is **Silver Bolt**. Combine three content types, then make the character eligible for a specific selection entry.

Prerequisites: [Your first mod](first-mod.md) and [A fixed stage](stage.md). Add `source/LanternRanger.cs`. Supply the three image files yourself, or first use the rules-only route below.

Before installing a changed build, increment `package.json.version` as in [the first lesson](first-mod.md#4-change-one-value-and-verify-again). Different contents cannot replace an installed package under the same version.

## 1. Register three classes

Copy the [character, trait, and initial-move fragment](../../../templates/en/02-character-trait-and-move.cs.txt), check the namespace, and add this to `Load`:

```csharp
registrar.AddContents(new LanternSight(), new SilverBolt(), new LanternRanger());
```

`LanternSight` is a separate trait; `SilverBolt` is a move; `LanternRanger` combines them through type lists. A class that exists in source but is not registered can cause a loading failure.

The fragment binds image paths. Supply `assets/icons/silver-bolt.png` (1:1), `assets/icons/lantern-ranger.png` (284×512 or that ratio), and `assets/portraits/lantern-ranger-avatar.png` (1:1). See [Assets and text](assets-and-text.md).

To check rules first, remove `, IModPresentationContent` from the `SilverBolt` and `LanternRanger` declarations and delete each entire `Presentation` property. This removes only custom art bindings. Do not leave bindings to missing files. Add your own art back afterward.

## 2. Add the character to the practice entry

In `PracticeAdventure.Difficulties`, use this `availableHeroIds` list:

```csharp
availableHeroIds = new List<string>
{
    ModEntry.PackageId + ".character.lantern_ranger"
}
```

Set `availableHeroIds` to the intended roster. You may keep the same ID in `PracticeStage.allowedCharacterIds` for consistent metadata, but that field does not enforce selection in the current C# runtime. `maxHeroCount = 1` is sufficient when this level offers one character.

To add a character to a built-in selectable level, use `AddCharacterToLevel`, available from API 1.7.0. See [Registration](../reference/entry.md). A source-stage pool ID is not a selectable level ID.

## 3. Verify through actions

Build and install, fully restart, and select Trail Lab. Check the character's name and base stats. On entering the board, confirm Silver Bolt is the initial move with 2 uses. Target the exposed guard and check damage and remaining uses.

Silver Bolt reads twice the current attack for its single hit; enemy damage still follows shared settlement. To test Lantern Sight's extra target, expose a second enemy. A one-enemy board cannot verify additional random targeting.

## 4. Check current starting-content limits

Only the first `StartingMoveTypes` entry becomes the initial move. Later entries are not automatically equipped in ordinary move slots. `StartingTreasureTypes` is stored and validated, but selection does not grant it. Use the [reward encounter](treasure.md) for a specific treasure.

The fragment includes `CharacterTreasurePoolTags.HealingLifeBuild` so the first character has an eligible treasure pool before custom treasures are added. Its additional tag `treasure_pool.your_package.lantern` matches the [character-treasure fragment](../../../templates/en/03-character-treasures.cs.txt). Pool matching uses any shared tag. If you later remove the life-build tag, first register eligible treasures for the remaining custom tag; an empty pool reports `AW_CHARACTER_EMPTY_TREASURE_POOL`. Change both sides when changing a custom tag. Use `GetPoolWeight` or character `SetWeight` for weights.

## Checks and next step

- All three content classes are registered, and difficulty and stage eligibility agree.
- The name and stats appear; the initial move hits and consumes a use.
- Extra targeting is tested with two exposed enemies, and unsupported starting grants are not promised.

Continue with [Enemies and instance state](enemy.md). See [Character and enemy reference](../reference/actors.md) for defaults and state boundaries.


Related extension: [custom page entry](custom-ui.md).


## Let one source file follow the selected language

The fragment now reads character, trait, move and role text with ModText. Merge entries from the [Chinese example catalog](../../../templates/zh-CN/localization.json) and [English example catalog](../../../templates/en/localization.json) into your existing files without replacing generated entries. Rules and IDs remain in one source file. Start a fresh test run after changing language and check names, descriptions and role text; see [assets and text](assets-and-text.md).
