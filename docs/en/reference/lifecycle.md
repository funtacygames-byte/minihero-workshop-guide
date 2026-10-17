# Definitions, runtime instances, and reset

[简体中文](../../zh-CN/reference/lifecycle.md) · [Index](../README.md)

Guide revision 7 · Mod API 1.11.0 · 2026-10-17

This page explains who owns state and when it is created, read, and cleared. Baseline: 1.11.0. See [Events](events.md) and [API declarations](api-surface.md) for member details.

![Content lifecycle](../../../images/content-lifecycle.svg)

## 1. Build and load definitions

Source compilation produces a DLL. The package loader checks the manifest, calls entry `Load`, collects definitions, and creates a registry. Constructors establish stable IDs. Loading definitions is not the start of a playable stage. The host configures text resolvers for the snapshot; mods should not replace them.

Characters combine registered traits and moves. Stages create scene definitions, and adventure steps expand into a stage list. A definition can serve multiple runs or enemy instances; it must not retain a run's player reference.

## 2. Run and instance ownership

| Data | Owner | Correct use |
| --- | --- | --- |
| Fixed treasure formula/quality configuration | Content definition | Repeatable reads, not stage progress |
| Treasure stacks, counters, pending enhancement | Concrete runtime treasure instance | Serializable fields, reset by default at new stages |
| Enemy counters and attack/defense deltas | `CardState` (`e.Owner`) | One card's state, not shared EnemyTraitContent fields |
| Granted HP, gold, and other resources | Current `GameState` | Shared Runtime/core settlement; not cleared like temporary treasure fields |
| Automatic requests and accumulated rewards | Current event | Host settles contributions; not a persistent cache |

A treasure definition creates separate `TreasureState.runtimeEffect` instances. Simple fields clone with them; mutable references need independent-copy checks so instances do not share one List. Do not retrieve UI or scene GameObjects to manufacture a missing runtime context.

## 3. Preview and execution

Preview uses isolated state and the same rules. `IsPreview` identifies the current window without permitting a separate numerical formula. Do not mutate static state, shared collections, or real instances during preview; hovering must not consume an enhancement.

Derived stats must be repeatably recalculated without accumulating drift. Base-stat conversion does not read other treasures' derived values, avoiding conversion cycles. Combine like percentages; see [Events](events.md) for rounding distinctions.

## 4. Stage boundaries and saves

Temporary treasure state resets at new stages by default. `OnSceneReset()` clears this class's counters, stacks, and pending effects; active-use rules restore the quality's `MaxUses`. Retain only necessary handoff state for explicitly permanent/run-long/next-stage exceptions. Granted resources and fixed configuration are not temporary counters.

The core clears leaving-stage temporary life-system state before intermission. Entry rewards settle on the next stage's entry. A treasure acquired after entry needs the next entry to test its effect; immediate shield gain on acquisition is not the test.

Save restoration preserves progress already recorded in current instances. Do not treat every load as a fresh stage. A new run creates new state. Enemy traits have no treasure-style reset callback: new cards start fresh, while clones and restored cards preserve their own fields.

## 5. Minimal author checks

Test two copies of a treasure, two copies of an enemy, repeated previews, caps, stage changes, new runs, and saved progress. State whether each datum should persist or clear. See the [treasure lesson](../tutorials/treasure.md) for deterministic grants and cross-stage checks, and the [testing overview](../04-testing-and-publishing.md) for the full list.
