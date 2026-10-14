# TreasureContent: quality, level, and pools

[简体中文](../../zh-CN/reference/treasures.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14

Purpose: define treasures, create runtime treasure instances, and respond to shared rule events. Baseline: 1.8.0. See [Public declarations](api-surface.md) and [Treasure lesson](../tutorials/treasure.md).

## Common properties and defaults

| Member | Type/default | Meaning |
| --- | --- | --- |
| `Id` | `string`, set by constructor | Stable content ID, not display name |
| `Name` | `string` | Player-facing name, usually overridden |
| `Rank` | `TreasureRank` | Default/highest quality; distinct from current `Quality` in variants |
| `BaseValue` | `int` | Definition's effect value; level multiplication is a content rule |
| `Describe(int level)` | `string`, abstract | Accurate description for this level |
| `SellGold` | `int = 1` | Base recycling value |
| `MaxLevel` | `GameRules.TreasureMaxLevel` | Upgrade limit |
| `Exclusive` | `Rank == Legendary` | Legendary is exclusive by default |
| `IncludeInDefaultChestPool` | `!Exclusive` | Default chest eligibility, still subject to other conditions |
| `CategoryTags` | Defaults to `PoolTags` | Legacy fallback; declare categories explicitly for new content |
| `PoolTags` | Empty list | Character-pool tags |
| `GetPoolWeight(string poolTag)` | `float = 1f` | Relative weight within a pool |
| `FunctionTags` | Empty list | Build search, separate from categories and pools |
| `ActivationKind` | `Passive` | Passive/active entry |
| `MaxUses` | 0 passive, otherwise 1 | Active uses per stage |
| `CreateState(int level = 1)` | `TreasureState` | Clamp level and create runtime state |

`Quality` and `EffectValue` belong to multi-quality runtime instances and have protected setters. Do not confuse maximum `Rank` with current instance quality. `IMultipleVariantEffect.GetVariants()` returns the variants actually supplied. Five/four/three/two values start at Common/Uncommon/Rare/Epic respectively and end at Legendary. Do not invent missing values. See the [content overview](../02-content-creation.md).

Ordinary content that neither implements `IMultipleVariantEffect` nor overrides `GetStateVariants()` supplies all five qualities by default; `Exclusive` content defaults to Legendary only. Writing `Rank => Common` alone does not limit that list to Common or generate different effect values per quality. The first lesson therefore shares one formula across qualities. The codex initially selects the highest available quality, and its quality arrows do not change treasure level. Supply explicit variants to restrict qualities or assign separate values.

## Events and state

```csharp
public abstract string Describe(int level);
public virtual TreasureState CreateState(int level = 1);
public virtual void OnStageEntered(StageEnteredEvent gameEvent);
public virtual void OnSceneReset();
public virtual GameActionResult Execute(TreasureState treasure, TreasureActivationContext context);
```

These are reference signatures. Stage entry and scene reset are inherited from the shared content base. `SourceLevel` identifies this treasure's level; `Runtime` supplies shared settlement. Default `Execute` fails with `passive_treasure`; passive treasures need no override. Failed active execution does not consume a use.

Use `[System.Serializable]` and a public parameterless constructor. Store progress, stacks, pending rewards, and budgets on the concrete runtime instance, resetting temporary state at new stages by default. Avoid static state. Simple value fields clone with the instance; mutable reference collections require explicit cloning/save checks. `CloneRuntime()` does not prove that every nested collection is independent.

## Categories, pools, and appearance

`CategoryTags` describes gameplay categories. Any intersection between `PoolTags` and allowed character tags forms pool eligibility. `RequiredAppearanceTags` applies additional appearance conditions. Character Include/Exclude overrides, quality, exclusivity, and appearance can still affect final candidates. Eligibility does not guarantee a random draw.

The current life category includes shield, maximum HP, healing, and their cycles. Move enhancement uses shared move events. Reading attack does not automatically make a life effect general-purpose. Weights are numeric; do not add a second tag to represent a multiplier.

## Validation

Check level 1 and maximum level, every supplied quality, caps, stage changes, saves, preview/execution, and stacked percentages. Share description and execution formulas. Use the [treasure lesson](../tutorials/treasure.md) for a deterministic grant and the [testing overview](../04-testing-and-publishing.md) for full conditions.
