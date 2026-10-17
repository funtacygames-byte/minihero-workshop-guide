# Source stages and selectable adventures

[简体中文](../../zh-CN/reference/stages.md) · [Index](../README.md)

Guide revision 6 · Mod API 1.10.0 · 2026-10-17

Baseline: 1.10.0. Start with [A fixed stage](../tutorials/stage.md), then use this field reference and the [API surface](api-surface.md).

## StageContent

```csharp
public abstract string Subtitle { get; }
public virtual bool IncludeInDefaultCampaign { get; }
public abstract StageDefinition CreateDefinition(GameContentRegistry registry);
```

`IncludeInDefaultCampaign` defaults to true; set it to false for a private practice source. `CreateDefinition` returns a board definition and resolves registered content through the registry. A stage alone does not create an adventure selection entry.

| StageDefinition field | Purpose/boundary |
| --- | --- |
| `id/name/subtitle` | Stable source ID and display text |
| `appearancePool` | Random candidates; random-layout validation checks this pool for an Exit |
| `fixedColumns` | Nonempty list fully replaces random layout; complete columns clone bottom-to-top |
| `columnCount/generatedCardCount` | Random-layout counts; fixed counts come from actual columns/cards |
| `allowedCharacterIds` | Stored and reference-validated metadata; current C# runtime does not enforce selection through this field |
| `music` | Registered music theme ID |
| `boss` | Stage boss flag used for music cue selection |
| `victoryConditions` | Conditions checked when an exit is used |
| `generationProfile` | Generation profile listed below |

Current C# validation checks the fixed cards for an exit when `fixedColumns` is nonempty; otherwise it checks the pool. A pool Exit template can be retained for earlier-version compatibility. Runtime does not insert that pool template into fixed columns. A partially fixed, partially randomly filled layout is not supported. Verify reachable exits and conditions through actual actions. Defeating ordinary enemies does not automatically win; living bosses prevent exit.

## AdventureContent and steps

Define `Description`, `PreviewImageId`, `SourceStageId`, `Steps`, and `Difficulties`; `Name/Id` come from the content base. `IncludeInSelection` defaults to true and `IntermissionInterval` to 2. Rule lists default to empty; Loop/Seed default to null.

`public virtual AdventureDefinition CreateDefinition()` copies steps, difficulties, and rules without storing a run's progress. The host merges adventures into level selection and expands steps into playable stages.

| AdventureStepDefinition | Default/meaning |
| --- | --- |
| `id` | Unique step ID; expanded stage is `<id>-round-<1-based round>` |
| `sourceStageId` | Registered source Stage ID |
| `columnCount` | `GameRules.ColumnCount` |
| `roundCount` | 6; explicitly use 1 or 2 for exercises |
| `cardsPerRound` | `GameRules.CardsPerStage`, for random layouts |
| `boss` | false; boss step marks its final round |
| `intermissionMode` | `Default`, combined with interval |
| `generationProfile` | Empty inherits the source profile |

`AdventureDifficultyDefinition` defaults to difficulty=1 and maxHeroCount=4, with empty character/rule lists. Attack, defense, HP, and reward enhancement default to 0; crystalRewardMultiplier defaults to 1. Growth and per-section arrays serve advanced designs; beginners need not fill every field.

Do not interchange IDs: Adventure identifies selection, Stage identifies source, and the step ID expands into actual stages. `nextStageId` must identify an actual stage in the current run; registered source content alone is insufficient.


All steps, including fixed layouts, must pass `columnCount` 1–5, `roundCount >= 1`, and `columnCount <= cardsPerRound <= 100`, or registration reports `AW_ADVENTURE_STEP_RANGE`. The practice fragment uses `cardsPerRound = GameRules.ColumnCount` (5) to pass this metadata check; its fixed board still contains only the two supplied cards. A boss step also requires an enemy with `isBoss` in the source `appearancePool` under the current adventure validator, even when the source uses fixed columns. Check that its actual fixed board also contains the intended boss.

With a nonempty availableHeroIds list, the host resolves those explicit IDs. An empty list uses the first clamp(maxHeroCount, 1, 4) entries of the character catalog; it does not mean every character. AddCharacterToLevel bindings can append characters afterward.

## Random generation and advanced topics

Public profiles are `StageGenerationProfiles.Default/Weighted/Layered/Branching/LayeredBranching`. They control draws and dealing without replacing exit/playability checks. Boss cards use `CardState.isBoss`; check source and step flags together. Guaranteed appearance also needs the actual generation constraints such as `guaranteedInStage`.

Loop `maximumLoops = 3` means three total loops; 0 means unlimited. Empty continuation results end an adventure. Daily seeds need an explicit UTC offset. C# StageGraph nodes need `card` snapshots, and graph Victory/Failure nodes do not replace physical exits. Code and conditions belong in the [advanced overview](../02-content-creation.md), not beginner prerequisites.
