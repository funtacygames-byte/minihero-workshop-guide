# 02 Content creation

[简体中文](../zh-CN/02-content-creation.md) · [Guide index](README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14

Start with [Your first mod](tutorials/first-mod.md). This page is a manual; use the [task index](README.md) for guided steps.

This chapter covers gameplay content: how definitions connect, which event a treasure should use, how quality differs from level, and how to reset counted effects. Code fragments share the Chinese guide's technical identifiers and formulas; their display strings are translated into English.

**Author gameplay in C#.** Treasures, characters, stages and events are concrete content classes registered in `Load`; the workshop compiles them into your mod DLL. The generated `package.json` describes the package, localization files supply displayed text, and save files store progress. These auxiliary files do not replace C# behavior, and the player workflow does not ask you to submit gameplay JSON.

## Contents

1. Registration and stable IDs
2. A treasure class, explained
3. Turning a requirement into an event
4. Common treasure events and recipes
5. Quality, level, and variants
6. Counters, stage resets, and permanent state
7. Characters, traits, moves, and treasure pools
8. Enemies, enemy traits, and stages
9. Items and encounters
10. Registration checklist

## 1. Registration and stable IDs

Each content class must be `public`, instantiable, have a public parameterless constructor, use a unique stable ID, and be registered in `Load`. Begin IDs with the current package ID and a dot:

```text
local.alice.lantern-trail.treasure.amber_lantern
local.alice.lantern-trail.character.lantern_ranger
local.alice.lantern-trail.enemy.moss_wolf
```

Display names can change independently of IDs. Character and stage references depend on IDs or C# types; arbitrary ID changes break bindings in saves and other content.

An entry-point registration fragment:

```csharp
public override void Load(IModRegistrar registrar)
{
    registrar.AddContents(
        new LanternSight(),
        new SilverBolt(),
        new AmberLantern(),
        new MoonGlassBottle(),
        new LanternRanger(),
        new WoundedRage(),
        new MossWolf(),
        new MoonDewPotion(),
        new TwilightMeadowStage(),
        new WhisperingGroveStage(),
        new LanternRuinsStage(),
        new LanternExpedition());
}
```

## 2. A treasure class, explained

```csharp
[System.Serializable]
public sealed class AmberLantern : TreasureContent, IModPresentationContent
{
    public AmberLantern()
        : base(ModEntry.PackageId + ".treasure.amber_lantern") { }

    public override string Name => ModText.Get(
        ModEntry.PackageId, "treasure.amber_lantern.name", "Amber Lantern");
    public override TreasureRank Rank => TreasureRank.Rare;
    public override int BaseValue => 3;
    public override int SellGold => 4;
    public override int MaxLevel => 3;
    public override IReadOnlyList<string> CategoryTags =>
        new[] { TreasureCategoryTags.Shield };
    public override IReadOnlyList<string> PoolTags =>
        new[] { "treasure_pool.local.alice.lantern" };

    public override string Describe(int level) =>
        $"Gain {BaseValue * level} shield when entering a stage.";

    public override void OnStageEntered(StageEnteredEvent e)
    {
        e?.Runtime?.AddShield(BaseValue * e.SourceLevel);
    }

    public ModPresentation Presentation =>
        ModAssets.Icon("assets/icons/amber-lantern.png");
}
```

- The constructor sets the stable ID; it should not read the current save.
- `Rank` declares the default/highest quality.
- `BaseValue` is the base effect value. Multiply it by level only when the rule requires that.
- `SellGold` is the base recycling value.
- `MaxLevel` is the upgrade limit.
- `CategoryTags` describe collection/build categories; they do not determine character draw pools.
- `PoolTags` determine pool eligibility. Any shared tag with the character's allowed tags is sufficient.
- `Describe(level)` and execution must use the same formula.
- `SourceLevel` is this treasure's current level. `Runtime` provides shared settlement for shield, healing, damage, dodge, and permanent stats.
- `Presentation` binds package-local artwork.

## 3. Turning a requirement into an event

Before implementing a treasure, define its functional fingerprint:

1. **Trigger:** stage entry, damage taken, healing, defeating an enemy, clearing a column, using an item, or using a move?
2. **Input:** base stats, healing amount, damage actually dealt, column position, or a counter?
3. **Main benefit:** healing, shield, stats, gold, move uses, or damage?
4. **State:** immediate, ongoing, accumulated within a stage, reset on stage entry, or permanent for the run?
5. **Target:** the player, a random enemy, the enemy with the most HP, one column, or all enemies?
6. **Limits and costs:** uses per stage, quality, a cap, HP loss, or another drawback?

For example:

> After each potion heal, gain shield equal to 30% of the healing amount. Trigger at most 3 times per stage and reset when entering a new stage. Make it eligible only for the potion character pool.

This specifies the trigger, input, benefit, state, cap, and pool. Compare all six dimensions with existing treasures before creating another item with the same decision value.

## 4. Common treasure events and recipes

| Requirement | Event | Key fields/interfaces |
| --- | --- | --- |
| Flat or percentage stats | `OnTreasureStats` | `attackFlat`, `defenseFlat`, `maxHpFlat`, `wisdomFlat`, percentage fields |
| Stage-entry reward | `OnStageEntered` | `Runtime.Heal/AddShield/GainDodge` |
| Healing increase | `OnBeforeHealing` | `bonusFlat/bonusPercent` |
| After healing settles | `OnAfterHealing` | `requested/actual/overflow/potion` |
| Modify incoming damage | `OnBeforePlayerDamage` | `bonusPercent` |
| Damage-taken result | `OnPlayerDamageTaken` | `damage/absorbed/hpDamage` |
| Enemy defeat | `OnEnemyKilled` | `columnIndex/allEnemiesDefeated/restoreMoveUses` |
| Move capacity | `OnMoveCapacity` | `baseMaxUses/bonusMaxUses` |
| Before a move resolves | `OnBeforeMoveResolved` | `targetCount/damagePercent/damageFlat/preferHighestHp` |
| After a move resolves | `OnAfterMoveResolved` | `automatic/totalDamage/defeatedEnemies/shield` |
| Item enhancement | `OnBeforeItemEffect` | `bonusPercent/extraUseCount` |
| After an item is used | `OnItemUsed` | `item/potion/restoreMoveUses` |
| Basic attack | `OnNormalAttackResolved` | `damageDealt/hits/restoreMoveUses` |
| Clear an entire column | `OnColumnCleared` | `columnIndex/automaticInitialMoveTriggers` |

Flat attack:

```csharp
public override void OnTreasureStats(TreasureStatsEvent e)
{
    e.attackFlat += 2 * e.SourceLevel;
}
```

Increase healing by 20%:

```csharp
public override void OnBeforeHealing(BeforeHealingEvent e)
{
    e.bonusPercent += 20;
}
```

Percentages of the same kind add together before the base value is settled. Do not repeatedly multiply them in individual treasure classes.

Restore move uses after defeating an enemy:

```csharp
public override void OnEnemyKilled(EnemyKilledEvent e)
{
    e.restoreMoveUses += Math.Min(2, e.SourceLevel);
}
```

Add one move target:

```csharp
public override void OnBeforeMoveResolved(BeforeMoveResolvedEvent e)
{
    e.targetCount += 1;
}
```

Gain shield based on maximum HP:

```csharp
public override void OnStageEntered(StageEnteredEvent e)
{
    int maxHp = Math.Max(0, e?.State?.player?.maxHp ?? 0);
    int shield = e?.Percent(maxHp, 10) ?? 0;
    e?.Runtime?.AddShield(shield);
}
```

`Percent` uses the game's shared rounding rule. Use event fields and `Runtime` for effects; directly editing scene objects, UI, or enemy HP would bypass shared preview, execution, and stacking rules.

### Clearing columns and automatic moves

`OnColumnCleared(ColumnClearedEvent e)` fires when a column's entire `cards` list becomes empty. Removing an enemy with an encounter, exit, or other card below it does not clear the column. The core compares empty-column counts before and after an action and dispatches for the net increase, at most once per newly cleared column in that settlement. A refilled column can trigger again when cleared later. `columnIndex` identifies the cleared column.

`automaticInitialMoveTriggers` starts at 0 and accumulates requests for automatic starting moves. The core attempts them after all column-cleared listeners finish. It is a request count, not a success count, and is not overwritten with the result. Attempts stop early when there is no starting move or legal target. Count successful automatic resolutions in `OnAfterMoveResolved` with `automatic == true`; this does not identify which column-clear request caused them.

An automatic starting move has no player-selected column: internally it uses `-1`. `MoveTargetKind.Enemy` requires an explicit column and cannot select an enemy in this call. Use `MoveTargetKind.RandomEnemy` when the move must automatically choose an exposed enemy, and test both available and absent targets. Manual targeted moves may still use `Enemy`.

`OnAfterMoveResolved.shield` is a shared accumulator, applied after listeners finish. Use `e.shield += amount`. Also calling `Runtime.AddShield(amount)` for the same reward would grant it twice. Combine this accumulator with `automatic` to reward successful automatic moves.

### Damage and healing amounts

For damage taken, `damage` is the total after mitigation, including shield absorption; `absorbed` is the amount shield absorbed; `hpDamage` is HP lost.

For healing, `requested` is the complete healing amount after modifiers settle, including healing at full HP and overflow. Healing-related rules read it. `actual` is the HP-bar increase, used only for resources and presentation. Use `overflow` only for an effect explicitly converting overflow. Player-facing descriptions normally say “healing amount.”

## 5. Quality, level, and variants

| Display quality | Code enum |
| --- | --- |
| Common | `Common` |
| Uncommon | `Uncommon` |
| Rare | `Rare` |
| Epic | `Epic` |
| Legendary | `Legendary` |

Quality identifies the treasure's tier and base-value variant. Level is the within-run upgrade, usually read through `SourceLevel`. A fixed formula with no quality tiers can be a single Legendary version. Five tiers start at Common, four at Uncommon, three at Rare, and two at Epic; all end at Legendary. Implement `IMultipleVariantEffect` only when the design specifies multiple values, and do not invent missing tiers.

Descriptions should state the input, level relationship, cap, duration, and trigger count. Temporary treasure state resets on entering a new stage by default; descriptions need not repeat that default. State any cross-stage retention explicitly. Share the value source between descriptions and execution so a preview of 6 does not grant only 3.

## 6. Counters, stage resets, and permanent state

```csharp
[System.Serializable]
public sealed class TinkerAbacus : TreasureContent
{
    public int itemUses;
    public int rewardsThisScene;

    public TinkerAbacus()
        : base(ModEntry.PackageId + ".treasure.tinker_abacus") { }
    public override string Name => "Tinker Abacus";
    public override TreasureRank Rank => TreasureRank.Rare;
    public override int BaseValue => 4;
    public override IReadOnlyList<string> CategoryTags => new[] { TreasureCategoryTags.Shield };
    public override IReadOnlyList<string> PoolTags => new[] { CharacterTreasurePoolTags.HealingLifeBuild };
    public override string Describe(int level) =>
        $"Every 3 item uses, gain {BaseValue * level} shield; at most 2 triggers per stage.";

    public override void OnItemUsed(ItemUsedEvent e)
    {
        itemUses++;
        if (itemUses < 3 || rewardsThisScene >= 2) return;
        itemUses -= 3;
        rewardsThisScene++;
        e.Runtime?.AddShield(BaseValue * e.SourceLevel);
    }

    public override void OnSceneReset()
    {
        itemUses = 0;
        rewardsThisScene = 0;
    }
}
```

Store counters in the runtime treasure instance. Public fields let Unity JSON save this example's progress; `[Serializable]` does not save unmarked private fields automatically. Simple public fields work with the two generated game references without adding a Unity reference. Clear stage-local fields in `OnSceneReset`. For permanent run stats, use `Runtime.AddPermanentAttack`, `AddPermanentDefense`, or `AddPermanentMaxHp`. Leaving a temporary counter unreset is not a permanent-stat mechanism.

Accumulating healing amount:

```csharp
public int accumulatedHealing;
public int rewardsThisScene;

public override void OnAfterHealing(AfterHealingEvent e)
{
    if (e == null || e.requested <= 0) return;
    CountAmount(
        ref accumulatedHealing,
        ref rewardsThisScene,
        e.requested,
        10,
        2,
        () => e.Runtime?.AddPermanentMaxHp(1));
}

public override void OnSceneReset()
{
    accumulatedHealing = 0;
    rewardsThisScene = 0;
}
```

The example reads `requested`, accumulates in steps of 10, and grants at most 2 rewards per stage. The accumulated progress and reward quota reset; maximum HP already granted as a permanent resource remains.

## 7. Characters, traits, moves, and treasure pools

```csharp
public sealed class LanternRanger : CharacterContent
{
    public LanternRanger()
        : base(ModEntry.PackageId + ".character.lantern_ranger") { }
    public override string Name => "Lantern Ranger";
    public override string Role => "Hunter";
    public override string School => "Woodland Watch";
    public override string Description => "Protects travelers with a lantern and light crossbow.";
    public override PlayerState BaseStats => new PlayerState
    { hp = 24, maxHp = 24, attack = 6, defense = 1, wisdom = 2 };

    public override IReadOnlyList<Type> TraitTypes =>
        new[] { typeof(LanternSight) };
    public override IReadOnlyList<Type> StartingMoveTypes =>
        new[] { typeof(SilverBolt) };
    // The current runtime does not grant StartingTreasureTypes on selection:
    // public override IReadOnlyList<Type> StartingTreasureTypes => new[] { typeof(AmberLantern) };
    public override IReadOnlyList<string> TreasurePoolTags =>
        new[] { "treasure_pool.local.alice.lantern" };
}
```

- `TraitTypes` binds character traits.
- `StartingMoveTypes` declares starting moves. Currently only the first is loaded as `State.initialMove`; later entries do not fill ordinary move slots. Declare one usable starting move.
- `StartingTreasureTypes` is stored and validated as `CharacterDefinition.startingTreasureIds`, but character selection does not grant those treasures. Do not promise a starting reward from this declaration.
- `TreasurePoolTags` determines allowed pools for later treasure chests.
- Any intersection with a treasure's `PoolTags` makes it eligible. `CategoryTags` does not affect this check.
- `GetPoolWeight(poolTag)` adjusts relative weight: 1 by default, for example 2 for a specialty treasure.

Use `TreasurePoolTags` for ordinary characters. For small exceptions, override `TreasurePool`: `Exclude` removes otherwise eligible treasures, `Include` forces specified IDs into the pool, and `SetWeight` overrides a treasure's weight for this character only. These operations do not change the treasure's `PoolTags`.

```csharp
public override TreasurePoolDefinition TreasurePool =>
    base.TreasurePool
        .Exclude(
            "goblin_brass_scale",
            "veterans_wrap")
        .Include(
            ModEntry.PackageId + ".treasure.lantern_compass")
        .SetWeight(
            ModEntry.PackageId + ".treasure.lantern_compass",
            2f);
```

To start with a built-in character's complete pool, copy it by stable ID and adjust it:

```csharp
public override TreasurePoolDefinition TreasurePool =>
    TreasurePoolDefinition.FromBuiltInCharacter("grove_alchemist")
        .Exclude("sundered_vambrace")
        .Include(ModEntry.PackageId + ".treasure.lantern_compass")
        .SetWeight(ModEntry.PackageId + ".treasure.lantern_compass", 2f);
```

This copies Groveheart's (`grove_alchemist`) current tags, inclusions, exclusions, and individual weights. Changes affect only the new character; its definition's `treasurePoolTags` reflects the copied tags. Register both the character and any custom included treasure. The base pool is read when creating the character definition, so game updates to that pool are inherited.

For a short explicit list, create the pool directly:

```csharp
public override TreasurePoolDefinition TreasurePool =>
    TreasurePoolDefinition.Create()
        .Include(
            "goblin_brass_scale",
            ModEntry.PackageId + ".treasure.lantern_compass");
```

An ID cannot be both included and excluded. A `SetWeight` reference to missing content or a treasure outside the final pool fails mod-load validation.

Character traits derive from `TraitContent` and respond to shared events. Moves derive from `MoveContent`. An enemy-targeted move requires dragging onto a specific enemy; `MaxUses` is its uses per stage. Use `MoveEffectKind.Damage` for one damage settlement.

Use `MoveEffectKind.MultiHit` only for a true sequence whose presentation supports separate hit feedback, with `hitCount`, `percentValue`, and `stopWhenTargetDies`. If presentation plays only once, combine the total into one `Damage` node. Use shared move events for multiple targets, additional damage, and post-move rewards.

For structured `MultiHit`, each hit starts with `flatValue + attack × percentValue / 100`, rounded down before shared damage bonuses. Each positive incoming hit calls `OnBeforeDamaged`; each hit that actually removes HP calls `EnemyTraitContent.OnAfterDamaged`. Immunity, final zero damage, and no HP removal do not trigger the latter. The lethal hit's after-damage callback runs before death handling.

The node keeps its original target instance. After death, remaining hits do not move to a newly exposed enemy in the column. `stopWhenTargetDies = true` stops immediately; `false` still cannot retarget and stops when the original target cannot be found. `MoveUsed` fires once for the move, not for each hit. Count damaging hits using `OnAfterDamaged`.

## 8. Enemies, enemy traits, and stages

```csharp
public sealed class WoundedRage : EnemyTraitContent
{
    public WoundedRage()
        : base(ModEntry.PackageId + ".enemy_trait.wounded_rage") { }
    public override string Name => "Wounded Rage";
    public override string Description => "After taking damage, gain 1 attack.";
    public override void OnAfterDamaged(EnemyTraitEvent e)
    {
        if (e?.Owner != null) e.Owner.enemyTraitAttackDelta += 1;
    }
}

public sealed class MossWolf : EnemyContent
{
    public MossWolf() : base(ModEntry.PackageId + ".enemy.moss_wolf") { }
    public override string Name => "Moss Wolf";
    public override string Description => "A magical wolf lurking in woodland moss.";
    public override int Attack => 6;
    public override int Defense => 1;
    public override int MaxHp => 18;
    public override int RewardGold => 5;
    public override string EnemyTraitId =>
        ModEntry.PackageId + ".enemy_trait.wounded_rage";
}
```

Enemy traits can handle static stats, player attacks, before/after damage, round start/end, death, other enemy deaths, and countdowns. The trait object is a shared content definition. Store individual enemy changes on `e.Owner`, its own `CardState`.

`CardState` exposes serializable, instance-specific fields: `enemyTraitCounter` (main counter), `enemyTraitSecondaryCounter` (second counter), `enemyTraitPhase` (phase), `enemyTraitTriggered` (one-time flag), `enemyTraitAttackDelta`, and `enemyTraitDefenseDelta`. There is no general mod-defined key/value dictionary API. `enemyStatuses` stores actual status effects rather than arbitrary data.

Each card has one `enemyTraitId`, and `EnemyContent.EnemyTraitId` returns one ID. For several effects, put them in one `EnemyTraitContent` subclass and override multiple callbacks. Its definition may be shared across enemies; keep counters, stacks, and accumulated stats on `e.Owner`.

The following trait gains one attack stack after every 3 damaging hits, up to 3 stacks, and gains defense at the enemy response phase. `OnAfterDamaged` fires only after actual HP loss. `OnRoundStart` occurs after the player's basic attack, before enemy intent/retaliation, once for each participating enemy still exposed. Defeated enemies are skipped. This callback does not run on every stage entry, item use, or move use.

```csharp
using System;
using MiniAdventureWorld.Core;

public sealed class CinderplateAwakening : EnemyTraitContent
{
    public CinderplateAwakening()
        : base(ModEntry.PackageId + ".enemy_trait.cinderplate_awakening") { }

    public override string Name => "Cinderplate Awakening";
    public override string Description => "Every 3 damaging hits, gain 1 attack for this enemy's lifetime, up to 3 stacks. At each enemy response phase, gain another 1 defense per stack.";

    public override void OnAfterDamaged(EnemyTraitEvent e)
    {
        CardState owner = e?.Owner;
        if (owner == null || owner.enemyTraitSecondaryCounter >= 3) return;
        owner.enemyTraitCounter++;
        if (owner.enemyTraitCounter < 3) return;
        owner.enemyTraitCounter = 0;
        owner.enemyTraitSecondaryCounter++;
        owner.enemyTraitAttackDelta++;
    }

    public override void OnRoundStart(EnemyTraitEvent e)
    {
        CardState owner = e?.Owner;
        if (owner != null)
            owner.enemyTraitDefenseDelta += Math.Max(0, owner.enemyTraitSecondaryCounter);
    }
}
```

Defense accumulates by the current stack count on each applicable response phase. At 3 stacks, every callback adds another 3 defense. For a fixed cap, plan a state transition using an appropriate serializable field, such as `enemyTraitPhase` or `enemyTraitTriggered`; do not store individual counters on the shared definition.

This simpler trait counts each damaging hit and gains 1 attack every 3 hits, up to 3 attack:

```csharp
using System;
using MiniAdventureWorld.Core;

public sealed class ThreefoldRage : EnemyTraitContent
{
    public ThreefoldRage()
        : base(ModEntry.PackageId + ".enemy_trait.threefold_rage") { }

    public override string Name => "Threefold Rage";
    public override string Description => "Every 3 damaging hits, gain 1 attack, up to 3 attack.";

    public override void OnAfterDamaged(EnemyTraitEvent e)
    {
        CardState owner = e?.Owner;
        if (owner == null || owner.enemyTraitSecondaryCounter >= 3) return;

        owner.enemyTraitCounter++;
        if (owner.enemyTraitCounter < 3) return;

        owner.enemyTraitCounter = 0;
        owner.enemyTraitSecondaryCounter++;
        owner.enemyTraitAttackDelta++;
    }

    public override string GetRuntimeStatus(CardState owner) =>
        $"[Hit progress {Math.Max(0, owner?.enemyTraitCounter ?? 0)}/3 | Attack bonus {Math.Max(0, owner?.enemyTraitSecondaryCounter ?? 0)}/3]";

    public override bool TryGetRuntimeStatusCount(CardState owner, out int count)
    {
        count = Math.Max(0, owner?.enemyTraitSecondaryCounter ?? 0);
        return true;
    }
}
```

When `Countdown > 0`, the countdown system also advances `enemyTraitCounter` and clears it on triggering. Reserve that field for the countdown; use `enemyTraitSecondaryCounter` for another counter, with one meaning per field. `CardState.Clone()` and saves preserve instance fields. Newly created enemies start from initial values and do not inherit old enemies' counters in a new stage. `EnemyTraitContent` has no `OnSceneReset`. Override `TryGetRuntimeStatusCount` for a displayed count and `GetRuntimeStatus` for text.

### Fixed and random stage layouts

`appearancePool` supplies random card candidates. `fixedColumns` is a `List<CardColumnState>` containing bottom-to-top `cards: List<CardState>`.

With nonempty `fixedColumns`, the core uses the entire fixed layout: column count is `fixedColumns.Count`, cards are cloned in list order, and empty columns stay empty. It does not add random cards from `appearancePool`; configured `columnCount` and `generatedCardCount` do not determine the layout. Runtime total card count becomes the sum of the fixed cards. You currently cannot combine a fixed left column with random remaining columns in one definition. For random dealing, leave `fixedColumns` empty; for a fixed layout, provide every card.

Current C# workshop validation checks for `CardType.Exit` in the fixed columns when `fixedColumns` is nonempty; for random layouts, it checks `appearancePool`. Missing an exit in the applicable layout reports `AW_STAGE_EXIT_MISSING`. A pool Exit template may be retained for earlier-version compatibility; it is ignored by the fixed-layout runtime.

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(
    ModEntry.PackageId + ".enemy.moss_wolf");
CardState ignoredPoolExit = ContentCards.Card(
    Id + ".ignored_pool_exit", CardType.Exit, "Exit Template", "Ignored by the fixed layout.");
ignoredPoolExit.appearanceWeight = 1f;

return new StageDefinition
{
    id = Id,
    name = Name,
    subtitle = Subtitle,
    columnCount = GameRules.ColumnCount,
    appearancePool = new List<CardState> { ignoredPoolExit },
    fixedColumns = new List<CardColumnState>
    {
        new CardColumnState
        {
            cards = new List<CardState>
            {
                ContentCards.Card(Id + ".exit", CardType.Exit, "Forest Exit", "Leave the forest."),
                ContentCards.Card(Id + ".altar", CardType.Encounter, "Grove Altar", "Inspect the altar."),
                wolf.CreateCard(Id + ".wolf")
            }
        },
        new CardColumnState { cards = new List<CardState>() },
        new CardColumnState { cards = new List<CardState>() },
        new CardColumnState { cards = new List<CardState>() },
        new CardColumnState { cards = new List<CardState>() }
    }
};
```

The first list item is at the bottom, and the last is exposed first. In this fragment, defeat the wolf first, then inspect the altar, and finally reach the exit. Put the exit earlier in the list than its guard to require combat before leaving. The core has no per-column card cap, and the UI can create additional layers; test very tall columns at the actual resolution. `allowedCharacterIds` is retained and its references are validated, but the current C# runtime does not use it to restrict selection. Configure the adventure difficulty's `availableHeroIds` for the actual selection roster.

### Adding a mod character to a built-in level

Since API 1.7.0, `IModRegistrar.AddCharacterToLevel` can append an already registered character from the current package to a selectable level. It keeps the original roster. Pass the stable ID of the level-selection entry, rather than a component stage or enemy pool.

```csharp
registrar.AddContent(new LanternRanger());
registrar.AddCharacterToLevel(
    "challenge_wild_corruption_nest",
    ModEntry.PackageId + ".character.lantern_ranger");
```

The built-in level's ID in this fragment is `challenge_wild_corruption_nest`. A third argument such as `2` limits the addition to that difficulty; omitting it or passing `0` covers all difficulties. Register the character before this call, and keep its ID within the current package.

For an independent adventure, `registry.Get<StageContent>("wilderness_beasts")` does not retrieve a built-in stage implemented in the UI assembly. Create your own `StageContent`, create card instances with `ContentCards.Enemy/Card`, and assign built-in `contentId` and `icon` values when reusing existing card art. Your `AdventureContent` steps reference your Stage IDs; use `StageGenerationProfiles.Layered` for layered generation.

You can thus add a character to a built-in level and independently create an adventure with custom enemies, pools, or story.

### Boss cards, source stages, and adventure steps

Three distinct boss flags have separate roles:

- `CardState.isBoss = true` marks the enemy itself for targeting, boss defeat, and card filtering. A higher `enemyTier` alone does not make a boss. Tier 5 is a suggested value for high-tier content; boss-round filtering reads `isBoss`.
- `StageDefinition.boss = true` marks a source stage used independently as a boss stage. Validation checks an `isBoss` enemy in the active layout: fixed columns when present, otherwise `appearancePool`. Missing one reports `AW_STAGE_BOSS_MISSING`. Independent simulation also checks whether one was generated.
- `AdventureStepDefinition.boss = true` makes the last round of that adventure step a boss round. `LevelStageBuilder` resets each expanded round's stage flag from the step, so marking only the source stage does not produce a boss round. A boss step's source pool must contain a boss or validation reports `AW_ADVENTURE_BOSS_MISSING`.

Explicitly mark boss cards in `EnemyContent.CreateCard`; the base implementation does not do this:

```csharp
public override CardState CreateCard(string instanceId = null)
{
    CardState card = base.CreateCard(instanceId);
    card.enemyTier = 5;
    card.isBoss = true;
    card.guaranteedInStage = true;
    return card;
}
```

Add the card to the source stage's pool. Set the source stage flag when it must also work independently, and the step flag when the adventure should generate a boss round. Keep those flags consistent with the intended stage and music behavior. `guaranteedInStage` ensures the boss actually appears; passing pool validation alone does not guarantee a random draw.

The current adventure-step validator still checks the source `appearancePool` for a boss even when that source uses fixed columns. For a fixed boss adventure, put the real boss in the fixed layout and retain a boss template in the pool for that validator. The fixed runtime ignores the pool template. Test both registration and the actual expanded board.

### Generation profiles

- `StageGenerationProfiles.Layered`: introduces stronger enemies by step and round.
- `StageGenerationProfiles.Branching`: retains all pool exits; the selected exit's `exitBranchId` becomes an appearance tag for subsequent generation.
- `StageGenerationProfiles.Weighted`: uses content weights and appearance tags.

`Layered` and `LayeredBranching` fill remaining slots with ordinary enemies. After appearance filtering, every such step needs at least one positive-weight, non-guaranteed ordinary enemy candidate, or deck generation fails. For a camp, shop, or noncombat transition, use `Default` or `Branching` if appropriate; the pool still needs an exit and at least one eligible non-exit card.

### How long an exit branch tag lasts

Selecting any exit writes its `exitBranchId` to the current adventure state. An empty value clears the previous value. Entering a stage or an intermission does not expire it, but each later exit replaces it rather than accumulating history. The next stage filters using the latest selected exit.

In a linear adventure, step 1's branch affects step 2. After leaving step 2, step 3 sees step 2's exit tag. `Branching` retains all exit templates; exits themselves are not hidden by `RequiredAppearanceTags`. These fields alone do not carry an earlier route through an ordinary intermediate step.

For a reward immediately after a branch, give it matching `RequiredAppearanceTags`. To use earlier choices much later, design a supported mechanism to preserve and restore route history; one `exitBranchId` is not that history.

`AdventureDifficultyDefinition` supports initial attack/defense/HP enhancement, regional growth, gold and crystal multipliers, and a character list per difficulty. See the [adventure structure fragment](../../templates/en/07-three-region-adventure.cs.txt).

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(
    ModEntry.PackageId + ".enemy.moss_wolf");

return new StageDefinition
{
    id = Id,
    name = Name,
    subtitle = Subtitle,
    generatedCardCount = GameRules.CardsPerStage,
    appearancePool = new List<CardState>
    {
        wolf.CreateCard(Id + ".wolf"),
        ContentCards.Card(
            Id + ".exit", CardType.Exit, "Forest Exit", "Leave the forest.")
    },
    allowedCharacterIds = new List<string>
    {
        ModEntry.PackageId + ".character.lantern_ranger"
    }
};
```

### Victory conditions are checked at exits

`StageDefinition.victoryConditions` is a `List<string>` using limited expressions. With several conditions, any true condition permits passing. They are checked when the player clicks an exposed exit, rather than automatically on enemy death. A random pool still needs an exit.

To require at least one defeated enemy:

```csharp
public override StageDefinition CreateDefinition(GameContentRegistry registry)
{
    var stage = new StageDefinition
    {
        id = Id,
        name = Name,
        subtitle = Subtitle,
        generatedCardCount = GameRules.CardsPerStage,
        appearancePool = new List<CardState>
        {
            registry.Get<EnemyContent>(ModEntry.PackageId + ".enemy.moss_wolf")
                .CreateCard(Id + ".wolf"),
            ContentCards.Card(Id + ".exit", CardType.Exit, "Forest Exit", "Leave the forest.")
        }
    };
    stage.victoryConditions.Add("defeatedEnemies >= 1");
    return stage;
}
```

`defeatedEnemies` is the cumulative count for the entire run and does not distinguish enemy IDs. The core first blocks leaving while a living boss remains, then checks victory conditions. Living ordinary enemies do not independently block an exit. The declarative condition system has no specific-enemy defeat counter; a total defeat count cannot prove a particular target was killed. `EnemyTraitContent.OnKilled` also has no public API to end the stage.

### StageGraph routes and conditional edges

`StageDefinition.graphNodes` is a `List<StageGraphNodeDefinition>` with `nodeId`, `kind`, `contentId`, `required`, and `card`. `kind` uses `StageGraphNodeKind`: `Start`, `Encounter`, `Event`, `Camp`, `Exit`, `Victory`, or `Failure`. `graphEdges` is a `List<StageGraphEdgeDefinition>` with `fromNodeId`, `toNodeId`, `conditionExpression`, and `weight`. Use object initializers.

StageGraph traverses a directed route once when the stage loads; it is not an interactive map. Starting at the unique `Start`, it records each visited node in `stageGraphVisitedNodeIds`. A visited node's `card` is cloned, marked guaranteed, and added to `appearancePool`.

For direct C# `StageDefinition`, supply the content node's `card` snapshot yourself. `contentId` identifies the source; `kind` does not create a card for you. `required` is retained but currently ignored: visited cards are guaranteed even when it is false. For genuinely optional random cards, use non-guaranteed positive-weight entries in the random pool.

Each outgoing edge is evaluated against the current `GameState` on reaching its source. Supported syntax is `&&`, one optional leading `!` per term, `tag:<tag>`, `has:<id>`, `reach:<nodeId>`, and numeric comparisons `==`, `!=`, `>`, `>=`, `<`, `<=`. `||` and parentheses are unsupported.

Numeric keys are `hp`, `maxHp`, `attack`, `defense`, `wisdom`, `gold`, `dodge`, `turn`, `stageIndex`, `defeatedEnemies`, and `stagesCleared`; prefixes such as `player.hp` are also accepted. `tag:` checks appearance tags and character pool tags/ID. `has:` checks the current stage, character, equipped treasures, moves, starting move, and cards in columns. `reach:` checks nodes visited in this traversal. The current node is recorded before its outgoing edges are evaluated.

All matching edges participate in selection; one is drawn using positive finite `weight`. List order does not establish priority, and repeated loads need not take the same route. With no usable edge, `LoadStage` throws `InvalidOperationException` naming the stage and node; the exception can emerge during construction or character-selection reload.

Static validation attempts condition evaluation and checks node IDs, edge endpoints, connectivity, cycles, dead ends, and reachable Victory/Exit nodes. Condition evaluation short-circuits, so passing validation does not prove every clause was parsed; see the [condition reference](reference/conditions.md). A cycle reports `AW_STAGE_CYCLE`. It does not prove that every runtime state has a matching edge; a syntactically valid but always-false condition can pass. Provide successors for all states you allow.

A new game loads the stage before character selection, then again afterward. Initially the phase is `ChoosingCharacter` and `State.character` is null; `has:<characterId>` does not inspect `startingCharacterChoices`. Selection writes the character and `BaseStats`, including gold, before reloading; numeric conditions read that moment's `State.player`. Provide a preselection fallback such as `!has:<characterId>`.

Every load recreates `stageGraphVisitedNodeIds`, so traversal history does not persist between loads. `reach:<currentNode>` is true because the current node is recorded first.

`Victory` and `Exit` nodes set the graph result to `victory`; they do not finish the stage or replace a physical exit card. The player must click the exit, and at least one configured victory condition must be true. `Failure` sets the graph result to `failure`. On clicking an exit, that result and `failureConditions` are checked first; any failure removes the exit and loses the stage, before victory checks. Validation requires exactly one Start, structural reachability of all nodes, no cycles, outgoing edges on nonterminal nodes, and a reachable Victory or Exit. Test condition matching separately.

A minimal character-dependent route:

```csharp
string rangerId = ModEntry.PackageId + ".character.lantern_ranger";
EnemyContent wolf = registry.Get<EnemyContent>(
    ModEntry.PackageId + ".enemy.moss_wolf");

return new StageDefinition
{
    id = Id,
    name = Name,
    subtitle = Subtitle,
    generatedCardCount = GameRules.CardsPerStage,
    appearancePool = new List<CardState>
    {
        wolf.CreateCard(Id + ".pool_wolf"),
        ContentCards.Card(Id + ".exit", CardType.Exit, "Forest Exit", "Leave the forest.")
    },
    graphNodes = new List<StageGraphNodeDefinition>
    {
        new StageGraphNodeDefinition { nodeId = "start", kind = StageGraphNodeKind.Start },
        new StageGraphNodeDefinition
        {
            nodeId = "ranger", kind = StageGraphNodeKind.Encounter,
            contentId = wolf.Id, required = false,
            card = wolf.CreateCard(Id + ".node_wolf")
        },
        new StageGraphNodeDefinition { nodeId = "fallback", kind = StageGraphNodeKind.Failure },
        new StageGraphNodeDefinition { nodeId = "victory", kind = StageGraphNodeKind.Victory }
    },
    graphEdges = new List<StageGraphEdgeDefinition>
    {
        new StageGraphEdgeDefinition
        {
            fromNodeId = "start", toNodeId = "ranger",
            conditionExpression = "has:" + rangerId, weight = 1f
        },
        new StageGraphEdgeDefinition
        {
            fromNodeId = "start", toNodeId = "fallback",
            conditionExpression = "!has:" + rangerId, weight = 1f
        },
        new StageGraphEdgeDefinition
        {
            fromNodeId = "ranger", toNodeId = "victory",
            conditionExpression = "reach:ranger && has:" + rangerId, weight = 1f
        }
    }
};
```

The fallback allows the first, characterless preview load to traverse a route. `required = false` does not make the visited wolf optional. Removing the fallback can leave the constructor with no matching edge before character selection.

## 9. Items and encounters

`ItemContent` defaults: `CardType.Medicine` reads `Heal`; `CardType.Elixir` reads `Effect`; other usable items read `DodgeCharges`. For direct-damage items, override `CreateCard` and set `activationKind`, `targetKind`, and `effects` on the base card:

```csharp
using System.Collections.Generic;
using MiniAdventureWorld.Core;

public sealed class EmberVial : ItemContent
{
    public EmberVial() : base(ModEntry.PackageId + ".item.ember_vial") { }
    public override string Name => "Ember Vial";
    public override string Description => "Deal 5 damage to the selected enemy.";
    public override CardType CardType => CardType.Elixir;

    public override CardState CreateCard(string instanceId = null)
    {
        CardState card = base.CreateCard(instanceId);
        card.activationKind = CardActivationKind.Targeted;
        card.targetKind = CardTargetKind.Enemy;
        card.effects = new List<CardEffectData>
        {
            new CardEffectData { effectType = CardEffectType.Damage, value = 5 }
        };
        return card;
    }
}
```

A targeted item selects one currently exposed enemy. The core reads `CardEffectType.Damage` and uses shared enemy damage settlement. For area damage, retain `CardActivationKind.Direct` and use `CardEffectType.DamageAllEnemies`; ordinary direct-use items support it too. Both paths trigger `OnAfterDamaged` only on actual HP loss and do not trigger the basic-attack response phase's `OnRoundStart`. The targeted path handles damage and item-use notification without calling `ItemContent.Execute`; do not settle the same effect twice.

```csharp
public sealed class MoonDewPotion : ItemContent
{
    public MoonDewPotion()
        : base(ModEntry.PackageId + ".item.moon_dew_potion") { }
    public override string Name => "Moon Dew Potion";
    public override string Description => "Restore 6 HP.";
    public override CardType CardType => CardType.Medicine;
    public override int Heal => 6;
    public override int SellGold => 2;
}
```

Add an item to a stage with `registry.Get<ItemContent>(id).CreateCard(instanceId)`. Treasures enhance items through `OnBeforeItemEffect` or `OnItemUsed`; the item should not enumerate the player's treasures.

Encounters derive from `EventContent`. Default `Execute(CardExecutionContext)` calls `ResolveEncounter`, so ordinary core settlement needs no override. `CreateCard` copies `Action`, `RewardQuality`, `RewardCount`, `Effect`, and `Choices` to the card:

- `Action = PendingChoiceKind.None` (default): remove the event card, charge its `goldCost`, and apply `Effect`.
- `Action = PendingChoiceKind.Meditation`: draw stat rewards from `Choices`. A positive `RewardCount` chooses that many; otherwise use all Choices. `RewardQuality`, each `StatEffect`'s quality/weight, and required tags filter candidates. Selecting one charges the card's `goldCost` and applies that `StatEffect`. The card's `Effect` is not applied and these fields do not draw treasures.
- `TreasureUpgrade`, `TreasureReset`, or `TreasureFusion`: start the corresponding treasure-slot selection rather than granting stat choices.

For alternatives with separate stat costs and treasure rewards, override `CreateCard` and fill `CardState.richEventChoices`. A nonempty list takes precedence over basic `Action/Effect/Choices`. Default `Execute` still creates and resolves the choices; no custom UI is needed:

```csharp
using System.Collections.Generic;
using MiniAdventureWorld.Core;

public sealed class BriarShrineEvent : EventContent
{
    public BriarShrineEvent()
        : base(ModEntry.PackageId + ".event.briar_shrine") { }

    public override string Name => "Briar Shrine";
    public override string Description => "Pay a cost to receive a relic.";
    public override string ImageName => "";

    public override CardState CreateCard(string instanceId = null)
    {
        CardState card = base.CreateCard(instanceId);
        card.richEventChoices = new List<RichEventChoiceState>
        {
            new RichEventChoiceState
            {
                choiceId = Id + ".choice.attack",
                text = "Give up 2 attack to receive a Mossfire Relic.",
                cost = new StatEffect { attack = 2 },
                rewardContentId = ModEntry.PackageId + ".treasure.mossfire_relic",
                rewardContentCount = 1
            },
            new RichEventChoiceState
            {
                choiceId = Id + ".choice.hp",
                text = "Lose 3 HP to receive a Mossfire Relic.",
                cost = new StatEffect { hp = 3 },
                rewardContentId = ModEntry.PackageId + ".treasure.mossfire_relic",
                rewardContentCount = 1
            }
        };
        return card;
    }
}
```

`RichEventChoiceState.cost` can deduct HP, maximum HP, attack, defense, wisdom, dodge, or gold. Settlement checks affordability first, preserving at least 1 HP and maximum HP, then deducts costs, applies optional `reward` stats, and grants `rewardContentId`. A treasure reward must be registered; it is equipped in a free slot or placed in reserve. `rewardContentCount` sets quantity.

The basic Meditation path's card-level `goldCost` is shared by all options and charged on selection. `EventContent` has no corresponding property; set `card.goldCost` in an overridden `CreateCard`. Rich choices bypass this field and basic rewards. Use each branch's `cost.gold` for individual gold costs. Keep the two choice paths distinct.

For new card-face choices, use the complete C# [card-choice lesson](tutorials/card-choice.md). Keep the old `RichEventChoiceState` path only when maintaining existing events. Its `conditionExpression` uses the [limited condition grammar](reference/conditions.md). Conditions filter the opening snapshot and are checked again at confirmation; a changed condition returns `event_condition_changed`, and unaffordable costs return `event_cost_unavailable`. Both retain the choice without charging or rewarding.

For legacy C# rich branches, pair `rewardContentId` with a positive `rewardContentCount` and verify the referenced content type. Runtime caps repetitions at 100; missing or unsupported rewards may be silently skipped. Items apply their configured effects immediately, moves become learned moves, and treasures are equipped or placed in reserve.

`nextEventId` must resolve to registered `EventContent`: after settlement its card appears on top of the original column. `nextStageId` must name a stage in the current adventure's expanded stage list, not merely a registered source template. A C# adventure step expands to `<step.id>-round-<roundNumber>`, starting at 1. A successful transition waits for the intermission entry action. Choose one follow-up path and test it by clicking the actual cards.

Add event cards to stage pools through `CreateCard`. Override `Execute` only for custom execution, use public context, and keep game UI/scene objects out of settlement code.

## 10. Registration checklist

For a character, move, treasures, enemies, source stages, and adventure, check every class is registered, referenced types exist, pool tags match as intended, `EnemyTraitId` resolves, and stage cards are created from registered enemies. Boss steps need bosses in their source pools. Step and difficulty IDs must be unique, character restrictions must include the test character, descriptions must share execution formulas, and counters must have reset rules.

Use the [focused code snippets](../../templates/README.md) for individual parts. This repository does not include a complete adventure package.


## New card choices and specialized effects

The current addition uses CardChoiceRequest/CardChoiceOption with registered ICardChoiceResolver. Display cards are previews; any-size single choices use the formal paged overlay. Begin with the [task lesson](tutorials/card-choice.md), then [fields, rollback and saves](reference/card-choice.md). Legacy richEventChoices limits and reward handling do not carry over to the new path.
