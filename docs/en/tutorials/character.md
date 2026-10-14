# Create a character with a starting move

[简体中文](../../zh-CN/tutorials/character.md) · [Index](../README.md)

Replace the selectable character with **Lantern Ranger**: base HP 24, attack 6, defense 1 and wisdom 2, with the Lantern Sight trait and 2 uses of Silver Bolt. Get the character and move working first, then add your own artwork.

**You need:** the project from [Your first mod](first-mod.md) and [A fixed stage](stage.md). The source uses the game's fallback artwork, so you can start without image files.

**Files:** create `source/LanternRanger.cs`; edit `source/ModEntry.cs` and `source/PracticeStage.cs`. After saving, increment `package.json.version`, build and install, then fully restart.

## 1. Register three classes

Copy the [character, trait, and initial-move source](../../../templates/en/02-character-trait-and-move.cs.txt) into `source/LanternRanger.cs`. Add this inside the existing `Load` in `ModEntry.cs`:

```csharp
registrar.AddContents(new LanternSight(), new SilverBolt(), new LanternRanger());
```

`LanternSight` defines the trait, `SilverBolt` the move and `LanternRanger` the character. Register all three so the character can find its trait and move.

The source has no custom image bindings, so it can build as copied. Once the character works, follow [Assets and text](assets-and-text.md#add-character-and-enemy-artwork) to add a move icon, character art and avatar. Leave out paths to files you have not added yet.

## 2. Add the character to the practice entry

Open `source/PracticeStage.cs` and find the `Difficulties` property in `PracticeAdventure`. Replace its `availableHeroIds` list, which currently contains only Runehunter, with:

```csharp
availableHeroIds = new List<string>
{
    ModEntry.PackageId + ".character.lantern_ranger"
}
```

Set `availableHeroIds` to the intended roster. You may keep the same ID in `PracticeStage.allowedCharacterIds` for consistent metadata, but that field does not enforce selection in the current C# runtime. `maxHeroCount = 1` is sufficient when this level offers one character.

To add a character to a built-in selectable level, use `AddCharacterToLevel`, available from API 1.7.0. See [Registration](../reference/entry.md). A source-stage pool ID is not a selectable level ID.

## 3. Select the character and try the move

Build and install, fully restart, and select Trail Lab. Check the character's name and base stats. On entering the board, confirm Silver Bolt is the initial move with 2 uses. Hold it, drag it onto the exposed guard and release. Check the damage and that its uses decrease from 2 to 1.

Silver Bolt deals damage equal to twice your current attack to one target; the game then applies its usual damage rules. To test Lantern Sight's extra target, add the block below before `PracticeStage.CreateDefinition` returns. It exposes another guard in column two. Use an attack on either guard and check damage to both; Silver Bolt should still hit only one target.

```csharp
CardState secondGuard = guard.Clone();
secondGuard.id = Id + ".guard.two";
columns[1].cards.Add(secondGuard);
```

## 4. Check current starting-content limits

Only the first `StartingMoveTypes` entry becomes the initial move. Later entries are not automatically equipped in ordinary move slots. `StartingTreasureTypes` is stored and validated, but selection does not grant it. Use the [reward encounter](treasure.md) for a specific treasure.

The fragment includes `CharacterTreasurePoolTags.HealingLifeBuild` so the first character has an eligible treasure pool before custom treasures are added. Its additional tag `treasure_pool.your_package.lantern` matches the [character-treasure fragment](../../../templates/en/03-character-treasures.cs.txt). Pool matching uses any shared tag. If you later remove the life-build tag, first register eligible treasures for the remaining custom tag; an empty pool reports `AW_CHARACTER_EMPTY_TREASURE_POOL`. Change both sides when changing a custom tag. Use `GetPoolWeight` or character `SetWeight` for weights.

## Try it in the game, then continue

- Lantern Ranger is selectable in Trail Lab with base HP 24, attack 6, defense 1 and wisdom 2.
- Silver Bolt hits the selected enemy and goes from 2 uses to 1.
- With two exposed enemies, an attack also hits the other; Silver Bolt still has one target.

Continue with [Enemies and instance state](enemy.md). See [Character and enemy reference](../reference/actors.md) for defaults and state boundaries.

## Let one source file follow the selected language

The fragment now reads character, trait, move and role text with ModText. Merge entries from the [Chinese example catalog](../../../templates/zh-CN/localization.json) and [English example catalog](../../../templates/en/localization.json) into your existing files without replacing generated entries. Rules and IDs remain in one source file. Start a fresh test run after changing language and check names, descriptions and role text; see [assets and text](assets-and-text.md).
