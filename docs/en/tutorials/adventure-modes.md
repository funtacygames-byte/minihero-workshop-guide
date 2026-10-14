# Add seeds and loops to your adventure

[简体中文](../../zh-CN/tutorials/adventure-modes.md) · [Index](../README.md)

Want friends to play the same random challenge, or enemies to grow stronger with each pass? Start by giving your adventure a fixed seed, then try daily seeds and a three-pass loop. Dynamic continuation is covered later and is optional.

**You need:** [Connected stages](adventure.md). The first three examples edit only `PracticeAdventure` in `source/PracticeStage.cs`. Place each property inside the class, outside other methods. Keep only one property with each name; do not paste both `SeedSettings` examples at once.

After each change, save, increment the package version, build and install, fully restart and start a new run. Keep a copy of the working source to compare against.

## 1. Fixed challenge

Add inside PracticeAdventure:

```csharp
public override AdventureSeedSettings SeedSettings => new AdventureSeedSettings
{
    mode = AdventureSeedMode.Fixed, seed = "lantern-practice-v1"
};
```

The fixed string becomes the run seed. Use the same content version, difficulty and action sequence to reproduce a run. Fixed columns are already deterministic; a random pool makes seed differences more visible. Seeds do not guarantee identical output across game/API or content versions, and provide no leaderboard, anti-cheat or daily-reward system.

## 2. When does the daily seed change?

Replace the property above with:

```csharp
public override AdventureSeedSettings SeedSettings => new AdventureSeedSettings
{
    mode = AdventureSeedMode.Daily, seed = "lantern-daily-v1", utcOffsetMinutes = 480
};
```

480 is the minute offset for UTC+8. The daily string combines prefix, adventure ID, difficulty and the offset date as yyyy-MM-dd. The valid offset is -840 to 840; Fixed/Daily prefixes cannot be empty. New runs use the new date; a run's seed is saved, so restoring across midnight does not reroll it.

Check same-day new runs, different difficulties, midnight boundaries and old-run restoration. Record UTC test time and offset. This is a client-side date rule, without an automatic server reward or leaderboard system.

## 3. Three passes through the adventure

Add one LoopSettings override:

```csharp
public override AdventureLoopSettings LoopSettings => new AdventureLoopSettings
{
    enabled = true, startStepIndex = 0, maximumLoops = 3,
    attackIncreasePerLoop = 1, defenseIncreasePerLoop = 0,
    healthIncreasePerLoop = 2, rewardIncreasePerLoop = 0
};
```

startStepIndex is a zero-based Steps index, not the expanded stageIndex. maximumLoops includes the first pass: 1 adds none, 3 means three total, and 0 is unlimited. Enable explicitly; increments and limit are nonnegative. Each later pass clones first-pass templates rather than repeatedly increasing the preceding pass: an hp=8 guard has 8/10/12 across three passes, and attack gains +0/+1/+2 relative to its original value.

Only the exit of the last expanded stage prepares the next batch; normal preparation and stage resets still apply. Temporary treasure stacks do not persist merely because the same adventure loops. A finite limit must end in victory, and restarting must remove stages appended in the previous run.

## 4. Dynamic continuation

A concrete AdventureContent may implement `IAdventureContinuationContent.CreateNextStages`. The context's State, CompletedStage and CampaignStages are independent copies. Read Seed, ContinuationIndex and State.selectedBranchId for decisions; changing those copies does not grant real rewards. Create registered content with Registry without mutating shared definitions.

An empty list ends normally; each batch may contain at most 4096 stages. Returned IDs must be nonempty and unique against all previous stages. Retain legal columns, exits and bosses. The first ContinuationIndex is 1. If both a provider and LoopSettings exist, the provider takes precedence; automatic looping is not applied in addition.

For complex continuation, plan output IDs, source stages, termination, branches and random strategy before writing the method. Invalid output fails exit continuation, so do not charge external costs first. Generated stages enter the saved campaign list; restoration must retain them rather than relying on local controller fields.

### Run a complete bounded continuation

Copy [fragment 14](../../../templates/en/14-dynamic-continuation.cs.txt) to `source/ContinuingPracticeAdventure.cs`. Keep `PracticeStage` from fragment 08; replace the existing `new PracticeAdventure()` registration with `new ContinuingPracticeAdventure()`. Do not register both just to test the same board.

The first stage uses its own step ID. Each exit asks the provider for another stage; indices 1 and 2 return `.continuation.1` and `.continuation.2`, then index 3 returns an empty array. The result is three stages total. It creates a fresh definition from the registered source, preserves its complete fixed columns and exit, and assigns a unique expanded ID. Growth is not added automatically: this example uses the same guard stats in every stage.

Merge the three `adventure.continuation_lab.*` entries from the sample catalogs. Increment package version, build/install and fully restart. Select Trail Relay, defeat the guard and use the exit three times, completing preparation between stages. The third exit should finish with victory. Save after the first continuation is appended and restore; confirm the same generated stage ID remains and no duplicate is appended. Restart a new run to confirm old generated stages do not remain.

## 5. Test one change at a time

Check one fixed-seed run first, then daily date calculation, three loops without a provider, and finally a provider with branches. Record expanded IDs, seed, stage/loop indices, enemy values, exit result and the next stage after restoration. Increment version and fully restart after code changes. For route conditions, see [condition reference](../reference/conditions.md) and the [advanced manual](../02-content-creation.md).
