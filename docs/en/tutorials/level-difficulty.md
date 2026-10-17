# Add a difficulty to an existing level

[简体中文](../../zh-CN/tutorials/level-difficulty.md) · [Index](../README.md)

Copy a Twilight Beyond difficulty into Deepwood Trail, adjust enemy bonuses and the crystal multiplier, then add it as a new selectable tier without creating another map.

Complete [the first lesson](first-mod.md) and generate development references with a game supporting **Mod API 1.10.0**. If an older game lacks these methods, update it and regenerate references; changing the manifest version alone does not add an API. Unlock the target map through normal play first.

## 1. Add a registration helper

Save the [difficulty fragment](../../../templates/en/16-level-difficulty.cs.txt) as `source/ExtraDifficulty.cs`, using your entry's namespace. Add this to your existing `ModEntry.Load`:

```csharp
ExtraDifficulty.Register(registrar);
```

Keep your other registrations and single entry. Set `package.json.modApiVersion` to `1.10.0` and increment the package `version`.

The fragment uses `GetLevels()` to inspect loaded levels and their full difficulty data, then chooses the target's maximum tier plus 1. The default target has six tiers, so it adds VII. If another Mod already appended tiers, the actual maximum applies.

## 2. Edit the copy

`CopyLevelDifficulty("challenge_starlit_expedition", 3, next)` reads an independent copy of Twilight Beyond III and assigns the new number. The example sets extra enemy attack to 8, extra health to 20 and the crystal multiplier to 1.8. It retains the other copied settings.

| Method | Purpose |
| --- | --- |
| `GetLevels()` | Inspect level IDs, names and difficulties |
| `GetLevelDifficulty(levelId, difficulty)` | Read an independent difficulty copy |
| `CopyLevelDifficulty(sourceLevelId, sourceDifficulty, newDifficulty)` | Read a copy and assign its new number |
| `AddLevelDifficulty(id, targetLevelId, definition)` | Append the edited copy to the target map |

Source and target may be the same level or another loaded Mod's level. Declare dependencies so other Mods load first. Your package can register an adventure before extending it, and can read a tier registered earlier in the same `Load` call.

Copies include heroes and count, rule IDs, stat bonuses, rewards, section growth arrays, item whitelists and segment settings. Lists, arrays and segment settings are independent, and registration copies them again. Editing the new tier does not alter its source. The target retains its own layout, card pools and base scaling, so identical difficulty parameters can produce different enemy stats on different maps.

To borrow only numeric tuning, explicitly replace or clear copied `adventureRuleIds`, hero lists and item restrictions. A `null` or empty section-growth array inherits its rule; `new[] { 0 }` explicitly disables that growth. An enabled segmented item pool needs six distinct ordinary adventure item IDs.

## 3. Check it in the game

Merge `difficulty.starlight.description` from the [English catalog](../../../templates/en/localization.json) and [Chinese catalog](../../../templates/zh-CN/localization.json), following the [text-merging steps](assets-and-text.md#merge-text-for-topic-fragments). Build/install, fully exit and restart.

Find the new tier in Deepwood Trail. Check its description and the original tiers, then enter battle to inspect the enemy bonuses. Save and continue to check the tier number. Maps with sequential unlocking require the previous number to be cleared, so keep added tiers consecutive. Maps that already expose all tiers retain that behavior. Test mode can enter every tier but does not record Mod selection progress.

Mod selection clears are stored separately for unlocks and clear markers while Mods are enabled. Added tiers use their stable registration IDs. Disabling Mods hides these records and additional tiers; Mod runs do not increase official clears, character progression, achievements or crystals. The example's 1.8 is a difficulty parameter, not a promise of official crystal rewards for Mod runs.

Missing templates or targets, duplicate tier numbers, missing references and invalid values produce load diagnostics. Registration IDs must be unique and belong to your package. Use the large level's ID rather than a region, stage or card-pool ID. Fix the first diagnostic in source, rebuild and restart.
