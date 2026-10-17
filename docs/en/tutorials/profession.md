# Give your character crystal upgrades

[简体中文](../../zh-CN/tutorials/profession.md) · [Index](../README.md)

Turn Lantern Ranger's profession into **Runesmith**, with five upgrades copied from Mage. Players buy them in the existing profession upgrade page using the same crystals as the built-in professions. Runesmith keeps its own upgrade levels.

You need the [character lesson](character.md) and a game whose generated SDK includes **API 1.11.0**. Update the game and regenerate its development references if `ProfessionUpgradeCurrency` or `CopyBuiltInProfession` is missing. Copying a signature into your project will not supply its implementation.

## Add the profession and bind the character

Copy [the profession source](../../../templates/en/18-crystal-profession.cs.txt) to `source/RunesmithProfession.cs`. Match its namespace to your existing entry. Register it inside your existing `ModEntry.Load`:

```csharp
registrar.AddContent(new RunesmithProfession());
```

Keep the existing Lantern Ranger, trait and move registrations. In `source/LanternRanger.cs`, add this property to `LanternRanger` and replace its existing `Role` property:

```csharp
public override string ProfessionId => ModEntry.PackageId + ".profession.runesmith";
public override string Role => ModText.Get(ModEntry.PackageId, "profession.runesmith.name", "Runesmith");
```

Merge `profession.runesmith.name` from the [English](../../../templates/en/localization.json) and [Chinese](../../../templates/zh-CN/localization.json) catalogs into your text files. Its values are `Runesmith` and `符文师`. Set `package.json.modApiVersion` to `"1.11.0"`, increase the package version, then build and install and fully restart the game.

`GameCrystals` selects the game's crystal wallet and crystal icon. With the default `ModCurrency`, upgrades instead spend this package's `CurrencyKey`, which defaults to `training_points`. `CurrencyName` and `CurrencyIconId` describe that independent resource. Give players a way to earn it before choosing that mode; see [persistent progress](#keep-your-own-progress).

## Buy a level and check the result

Select Trail Lab and Lantern Ranger. Open the character's existing profession upgrade page. It should show Runesmith, five nodes and your game crystal balance. At level 0, the starting-gold node costs **50 crystals**. Buy it and check that the balance decreases by 50 and that this node becomes level 1. A new run starts with **2 extra gold**. The built-in Mage's level stays unchanged.

Repeat the purchase with too few crystals: neither the level nor balance should change. A fully upgraded node accepts no further purchase. Fully restart the game to check persistence. Disabling and re-enabling the same package retains its levels; renaming its profession or upgrade IDs creates different nodes.

A run locks its upgrade snapshot when it starts. Buying an upgrade later affects a new run or a restart. Continuing an older saved run restores its older snapshot. Permanent crystal spending is not rolled back with the run.

Crystal purchases are handled by the game's upgrade button. Mod callbacks cannot grant or spend game crystals through `ModProgress`. Ordinary workshop-run rewards remain separate from official crystal rewards and achievements.

## Reuse a whole profession or mix individual nodes

To use Mage itself with its existing shared levels, set the character’s `ProfessionId` to `ProfessionIds.Mage` and keep its `Role` as Mage. Register your own profession when you want separate levels.

The fragment uses `CopyBuiltInProfession(ProfessionIds.Mage, Id)`. Change `Mage` to `Warrior`, `Ranger` or `Assassin` to copy that profession's full set. Each copy preserves effects, prices and level caps, and creates IDs under your profession. The original levels are never shared.

To choose individual nodes, replace the `Upgrades` property with:

```csharp
public override IReadOnlyList<ProfessionUpgradeConfig> Upgrades => new[]
{
    ProfessionUpgradeConfig.FromBuiltIn(Id + ".wisdom", ProfessionUpgradeIds.MageWisdom),
    ProfessionUpgradeConfig.FromBuiltIn(Id + ".boss_shield", ProfessionUpgradeIds.WarriorBossShield)
};
```

You can edit the returned configs' `costs`, `valuePerLevel`, `name`, `description` and `iconId`. `costs` lists the positive price for each level; its length is the cap, with at most 100 levels and 32 nodes per profession. Keep IDs in the profession's namespace. A standard `effectKind` may appear only once per profession. Copied names and current-level descriptions use the game's translations until you replace those fields. Custom descriptions support `{level}` and `{value}`, where value is level times `valuePerLevel`.

For a new mechanic, use `ProfessionUpgradeEffectKind.Custom`, implement it in your profession's normal rule events, and read `UpgradeLevel(e.State, upgradeId)`. Put its rule in the profession class. Do not add a special-case branch to the game engine.

## Keep your own progress

For experience, unlocks or an independent training currency, follow [Professions and persistent progress](profession-progress.md). That lesson covers `ModProgress`, successful-callback writes, read-only previews, data limits and reward deduplication. Permanent progress does not rewind with a run save.

Decide the currency mode before release: changing modes does not transfer balances or purchased levels.
