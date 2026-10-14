# Limited conditions and position identities

[简体中文](../../zh-CN/reference/conditions.md) · [Index](../README.md)

Guide revision 5 · Mod API 1.8.0 · 2026-10-14


Conditions are not C#, JavaScript or arbitrary scripts. `DeclarativeConditionEvaluator.Evaluate(expression, state)` returns truth and fails on an unrecognized clause it actually evaluates. TryEvaluate reports evaluation success; out result carries truth. An empty expression passes.

Evaluation short-circuits: a false clause prevents later clauses from being parsed, so TryEvaluate is not a complete syntax validator. The current implementation also discards empty fragments from `&&` splitting. Do not use bare, leading or trailing conjunctions. Check each nonempty clause first, then test the complete condition against real state.

| Syntax | Meaning |
| --- | --- |
| `gold>=5` or `player.gold>=5` | Compare an attribute to a finite numeric constant |
| `hp>3 && gold>=2` | Every clause must pass |
| `!has:local.alice.lantern-trail.treasure.starter_relic` | Content is not held/present |
| `tag:treasure_pool.local.alice.lantern` | Active tags contain the case-sensitive tag |
| `reach:grove_gate` | A graph node ID has been visited |

Numeric keys are only hp, maxhp, attack, defense, wisdom, gold, dodge, turn, stageindex, defeatedenemies and stagescleared. The seven player resources support the player. prefix. Guessed fields such as shield or loopIndex are unsupported. Operators are >=, <=, ==, !=, > and <; the right side must be a finite constant, not another attribute or expression. OR `||`, parentheses, functions and arithmetic are unsupported. Implement complex rules in concrete C# content rather than constructing a plausible expression that always fails.

`tag:` reads appearanceTags, character pool tags and character ID, not treasure CategoryTags. `has:` checks current stage/character, equipped treasures, moves and cards throughout all columns, including covered cards. It is not restricted to exposed cards and does not check reserve treasures. `reach:` reads visited node IDs. Use exact stable IDs, not display names.

Check timing varies: new card choices check conditions and costs for display and confirmation. Legacy rich events filter branches by condition at opening, recheck condition and cost on confirmation, and do not automatically refilter the opened list. StageGraph checks edge conditions when selecting a path. Do not transfer timing assumptions between paths.

Columns are zero-based: the player's first column is 0. Fixed cards are stored bottom to top; the last is exposed. sourceCardId is an instance id; resolverContentId/rewardContentId are registered content IDs. Adventure-selection IDs, source Stage IDs, step IDs and expanded stage IDs differ too. Follow-up stage transitions require an expanded ID in the current campaign, not the registered source ID.

Debug with actual state and expected truth, starting with one clause such as `gold>=2` before combining. Keep a reachable fallback for paid or gated branches. Test exact affordability, one resource short, and an unaffordable branch after save restoration.
