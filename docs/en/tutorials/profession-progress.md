# Add profession upgrades and permanent training points

[简体中文](../../zh-CN/tutorials/profession-progress.md) · [Index](../README.md)

Give Lantern Ranger 1 training point for each enemy defeated. Spend those points on Vitality in the existing character upgrade page: +2 starting max health per level, two levels, costing 2 and 3 training points.

Complete [the character lesson](character.md) and regenerate development references with a game supporting **Mod API 1.9.0** or later. Keep the character's current trait, move and selection roster.

## 1. Register a profession and bind the character

Save the [profession fragment](../../../templates/en/17-profession-progress.cs.txt) as `source/LanternTraining.cs`, matching your entry's namespace. Add this before the character registration in your existing `ModEntry.Load`:

```csharp
registrar.AddContent(new LanternTraining());
```

Add `ProfessionId` to your existing `LanternRanger` class and replace its existing `Role` property with the one below. Keep only one `Role`:

```csharp
public override string ProfessionId => ModEntry.PackageId + ".profession.trailwarden";
public override string Role => ModText.Get(ModEntry.PackageId, "profession.trailwarden.name", "Trailwarden");
```

Set the manifest's `modApiVersion` to `1.9.0`; use `1.10.0` if you also call the difficulty-copy API. Merge the `profession.trailwarden.` entries from both sample catalogs using the [text-merging steps](assets-and-text.md#merge-text-for-topic-fragments). Increment the package version, build/install and fully restart.

## 2. Earn points and buy a level

Enter a practice stage with guards as Lantern Ranger, defeat enemies, then return to the character upgrade page. Training should increase. Once you have 2 points, buy Vitality level 1: it spends 2 and sets the level to 1. Start a new run; base max health 24 plus 2 gives 26. Earn another 3 points and buy level 2; a new run starts with max health 28, and no further level is available.

A profession's `Upgrades` returns its definitions. Each `costs` entry prices the next level, and the array length sets the cap; no extra tiers are inferred. A profession has 1–32 upgrades, each with 1–100 levels and positive prices. Upgrade IDs start with the profession ID plus a dot. This example uses `StartingMaxHp` through shared settlement. For custom behavior, use `Custom`, keep the effect in the profession's own event callbacks and read the run's locked level through `UpgradeLevel(e.State, upgradeId)`.

Upgrade prices use that profession's `CurrencyKey`, which defaults to `training_points`. Spending and gaining a level are saved together by the host and cannot consume official crystals. Profession and upgrade definitions stay stateless. Use short, natural profession and upgrade names that fit the existing font sizes and text boxes.

## 3. Store your own permanent flags

Other chapter unlocks and resources can use this package's scalar data:

```csharp
var progress = ModProgress.ForPackage(ModEntry.PackageId);
int defeated = progress.GetInt("enemies_defeated", 0);
bool accepted = progress.AddInt("enemies_defeated", 1);
```

Write from successful gameplay actions or screen `OnOpen/OnAction` callbacks. Content queries, battle previews, status projection, screen `OnUpdate/OnClose` and save restoration cannot commit permanent changes; write methods return `false`. Failed actions and exceptions discard their changes. Background threads cannot commit.

The host stores data under the package ID without granting the Mod a disk path or file-write permission. Keys use semantic ASCII identifiers and may include digits, dots, hyphens and underscores; keys beginning with `__` are reserved. Each string is limited to 16 KiB, each package to 512 entries and 256 KiB of values. Use `GetString/GetInt/GetBool`, `SetString/SetInt/SetBool`, `AddInt/Remove/TrySpend`. A write's return value says whether the change was accepted.

Upgrades are locked into a snapshot when a run starts. Purchases outside battle do not change an existing run; continuing a save restores its old levels, while new runs use current ones. Permanent resources do not roll back with a save. Authors must track stable chapter or reward IDs when a reward should not be farmed repeatedly. Disabling or reinstalling the same package ID keeps its data; a new package ID uses separate progress.

Check that points and levels survive a restart, then compare a continued save with a fresh run. See the [API index](../reference/api-surface.md#professioncontent) for declarations.
