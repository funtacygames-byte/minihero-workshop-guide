# Let players choose between two supply cards

[简体中文](../../zh-CN/tutorials/card-choice.md) · [Index](../README.md)

Add **Camp Supplies** to Trail Lab. Opening it offers free healing for 5 HP or 1 defense for 2 gold. Make the two options first, then try them with and without enough gold.

**You need:** [Your first mod](first-mod.md) and [A fixed stage](stage.md). Copy [the supply source](../../../templates/en/10-card-choice.cs.txt) to a new `source/CampChoice.cs` using your project's namespace. Then edit your existing `ModEntry.cs` and `PracticeStage.cs`. You need no images or second entry class.

## 1. Place supplies above the guard

Save it as `source/CampChoice.cs`, using your namespace. Add this inside `Load` in your existing `ModEntry.cs`:

```csharp
registrar.AddContent(new CampChoice());
```

After `columns[0].cards.Add(guard);` in `PracticeStage.CreateDefinition`, add:

```csharp
columns[0].cards.Add(registry.Get<EventContent>(
    ModEntry.PackageId + ".event.camp_choice").CreateCard(Id + ".camp"));
```

If you placed Claim Relic earlier, temporarily remove its placement code but keep its registration. For this lesson, column one contains only exit, guard and supplies, with supplies exposed first. Retain the exit and complete column structure. Increment the package version, build and install, fully exit and restart, then start a new Trail Lab run.

## 2. Add option names and descriptions

Merge into the existing `localization/zh-Hans.json` and `localization/en.json`, preserving other keys:

These files contain displayed text only. Choice construction, costs and settlement stay in `CampChoice.cs`.

See the [actual bilingual card screenshots](../reference/visual-walkthrough.md#6-compare-a-real-c-card-choice) for the result.

```json
{
  "locale": "en",
  "entries": [
    {
      "key": "event.camp_choice.name",
      "value": "Camp Supplies"
    },
    {
      "key": "event.camp_choice.description",
      "value": "Choose healing or defensive supplies."
    },
    {
      "key": "choice.camp.heal.name",
      "value": "Moondew Kit"
    },
    {
      "key": "choice.camp.heal.description",
      "value": "Restore 5 HP."
    },
    {
      "key": "choice.camp.guard.name",
      "value": "Guard Supplies"
    },
    {
      "key": "choice.camp.guard.description",
      "value": "Pay 2 gold to gain 1 defense."
    }
  ]
}
```

Copy the six Chinese entries under `event.camp_choice.*` and `choice.camp.*` from the [Chinese sample catalog](../../../templates/zh-CN/localization.json), using [the merge steps](assets-and-text.md#merge-text-for-topic-fragments). Keep keys and 5/2/1 identical. Preview cards without built-in content translations use `ModText` when created. Open a fresh choice after changing language; do not assume arbitrary custom snapshot strings can be translated again automatically.

## 3. Try a choice, then try paying for defense

Start separate test runs and record HP, defense, gold and turn before and after. With less than 2 gold, the guard option is faded and unavailable; the free healing branch still completes the flow. With 2 gold, guard deducts exactly 2 and adds 1 defense. Healing uses the full healing pipeline; unchanged HP at full health does not mean healing never occurred. Then defeat the guard and click the exit.

Opening does not remove supplies, charge a cost or commit a turn. Confirmation rechecks source, condition and cost; the same choice cannot resolve twice. The initial request is mandatory by default, with no cancel button. The base explicitly uses the event name as its header.

For deterministic payment testing, you need not earn gold in another adventure. Before returning from `PracticeStage.CreateDefinition`, temporarily reorder column one and give the practice guard a 2-gold reward:

```csharp
guard.rewardGold = 2;
columns[0].cards.Clear();
columns[0].cards.Add(exit);
columns[0].cards.Add(registry.Get<EventContent>(
    ModEntry.PackageId + ".event.camp_choice").CreateCard(Id + ".camp"));
columns[0].cards.Add(guard);
```

This is a second test layout: guard, supplies, then exit. Increment version, build/install, fully restart and start a new run. After receiving the guard's 2 gold, record current gold and choose guard supplies to check an exact deduction of 2. Retain the original layout for insufficient-gold testing; do not change columns inside an already-open choice.

## 4. Make one observable change

Change healing `effect.hp` and the 5 in both descriptions to 8. Increment the version, rebuild and fully restart. Choose healing while injured and check the gain against healing modifiers. Changing only the display-card description has no mechanical effect.

For 7 cards, cancellation, a hidden header, chained choices or specialized effects, use the [complete card-choice reference](../reference/card-choice.md), including saves, rollback and diagnostics. Legacy `richEventChoices` is a separate event path with at most three branches; that limit does not apply to the new interface.

## 5. Add an optional follow-up choice

[Fragment 15](../../../templates/en/15-chained-choice.cs.txt) supplies the full `TwoStepSupplies` class. Copy it to `source/TwoStepSupplies.cs`, register it with `registrar.AddContent(new TwoStepSupplies());`, and replace the fixed column's `.event.camp_choice` reference with `.event.two_step_supplies`. Keep the guard and exit. Merge its six new keys plus the four reused `choice.camp.*` keys from the sample catalogs.

The first screen offers 3 gold, or 2 shield followed by an optional supply choice. The gold branch finishes immediately. The shield branch grants its reward and opens the next request through `context.OpenNext`. The original event is already consumed, so the second request sets no source and does not consume it again. Its `consumeTurn = false` still carries the first step's deferred turn; final confirmation or cancellation commits that turn once.

For the paid follow-up, use section 3's second layout: replace its event reference with .event.two_step_supplies, give the guard a 2-gold reward and defeat it before opening the cache. Use the original event-first layout to test insufficient gold, free healing and cancellation.

Increment version, build/install and fully restart. Choose Shield Kit: verify +2 shield and no turn yet, then save and restore the open second request. Guard supplies should cost 2 gold and add 1 defense, with one total turn. In another run, cancel the second screen: retain the 2 shield, spend no gold there and commit the earlier turn. Cancellation does not undo a successful first step. Finally test Loose Coins: +3 gold, no second screen and one turn. Use the [settlement reference](../reference/card-choice.md) for failure rollback.

## When changing choice behavior: three kinds of ID

`CampChoice.Id` identifies registered content and the saved resolver. `CardState.id` identifies a source or display-card instance. `CardChoiceOption.id` identifies a branch, such as `heal` or `guard`. These serve different purposes. Branches may share a card face, but option IDs must remain nonempty and unique.

The display card supplies its name, description and image only; choosing it does not run its original item, attack or purchase behavior. The base sets `resolverContentId = Id`, so the concrete class must call `context.ApplyEffect`. With a resolver, the host does not automatically apply `effect` again. Do not pay `cost`, remove the source or end the turn yourself; the core handles them.
