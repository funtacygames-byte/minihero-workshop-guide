# Keep independent state for capped rules

[简体中文](../../zh-CN/tutorials/rules-and-state.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14


Goal: Practice Flask grants shield equal to 10% of the healing amount, at most three times per stage, resetting on a new stage with matching preview and execution. Prerequisites: [treasure lesson](treasure.md) and [event reference](../reference/events.md). [Fragment 13](../../../templates/en/13-stateful-relic.cs.txt) teaches state management; it is not a proposed new built-in treasure. Actual designs still require fingerprint comparison against the current treasure catalog.

## 1. Write a testable rule first

Trigger: positive settled healing. Input: `requested`. Reward: shield. State: per-instance count 0–3, reset by stage. Target: player. Limits: three triggers, no cost, one Legendary variant, level one. Shield classification and the life-build pool retain separate roles.

Add `source/PracticeCounterRelic.cs` and register it in Load. For deterministic acquisition, reuse [grant fragment 09](../../../templates/en/09-relic-grant.cs.txt), change rewardContentId to `.treasure.practice_counter`, and update encounter text. Do not rely on drawing a single Legendary variant from default chests. No other quality values were specified, so do not invent four more variants.

## 2. Where state belongs

`healingTriggers` is a public int on the concrete runtime treasure, retained by its serializable class. It must not be static, stored in UI or share a mutable List between treasures. `OnAfterHealing` checks healing and the cap before advancing the count and granting shield through Runtime. `OnSceneReset` clears it. Repeated OnTreasureStats recalculation must not advance counters.

Preview uses isolated state and runtime-content copies and should execute the same formula. An `if (IsPreview) return` must not remove the preview reward, and preview must not consume real triggers. Check cloning isolation for mutable reference fields; this fragment uses only an integer. Save restoration and runtime-instance copying are separate checks.

## 3. Test health states

| Condition | Settled healing | Expected count and shield |
| --- | ---: | --- |
| Sufficient missing HP, no modifiers | 10 | +1 trigger, +1 shield |
| Only 2 HP missing | 10 | Still +1 trigger, +1 shield |
| Full health | 10 | Still +1 trigger, +1 shield |
| Three triggers already used | 10 | No fourth shield reward |

This condition does not read `actual`. See shared Percent rounding in the event reference; base-stat conversion rounding does not apply to every shared percentage. Healing modifiers change requested before this rule reads it. Remove other shield sources before testing and record deltas rather than treating total shield as this treasure's reward.

## 4. Reset, restore and bilingual text

Save and restore after trigger three; a fourth still gives no shield. Enter the next stage and heal; the first trigger should work again. Two equipped copies keep independent counts. Repeated previews must not reduce real remaining triggers. Use “治疗量” / “healing amount”, preserving 10% and three triggers per stage without repeating overflow parentheticals.

For run-persistent growth, specify the saved object, settled resources, stage handoff and restore rules. Temporary bonuses reset by default. HP or gold already granted through shared Runtime does not have to be reversed on reset.

## 5. Adventure rules without treasure slots

Global adventure rules inherit `AdventureRuleContent` and implement Description, IconId and events in their own class. After Load registration, activate them through AdventureRuleIds or difficulty adventureRuleIds; they are not treasure rewards. Call base when overriding OnStageEntered to retain default status projection. Difficulty growth arrays inherit rules when null/empty; [0] explicitly disables that attribute's growth. Registration is not activation. Continue with [adventure modes](adventure-modes.md) for seeds and loops.
