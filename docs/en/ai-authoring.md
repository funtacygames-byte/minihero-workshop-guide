# AI authoring tasks and delivery contract

[简体中文](../zh-CN/ai-authoring.md) · [Index](README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14


Give AI this page, the [feature map](feature-map.md), the task lesson, its references and focused fragments together. Offline readers start at root `llms.txt`. Machine indexes are [capabilities.json](../capabilities.json) and selected [api-surface.json](../api-surface.json). The guide does not replace game-generated references.

## 1. Route the task before assuming host capabilities

| Goal | Read first | Required delivery |
| --- | --- | --- |
| New treasure/change numbers | [Treasure](tutorials/treasure.md), [state](tutorials/rules-and-state.md) | Fingerprint, quality values, description formula, pool, reset, specified acquisition |
| New card-face choice | [Choice](tutorials/card-choice.md), [fields](reference/card-choice.md) | Concrete class, option IDs, faces, effects, costs, resolver, stage placement |
| Item/encounter reward | [Items/events](tutorials/items-and-events.md) | Direct or targeted path, reward type, registration/appearance, turn |
| New page/start menu | [Pages](tutorials/custom-ui.md) | Tree, controller, AddScreen, actions, fallback, bilingual text |
| New character/move | [Character](tutorials/character.md) | Referenced classes, selection entry, pool, first initial move, target checks |
| Random challenge/endless mode | [Modes](tutorials/adventure-modes.md) | Seed, date offset, total loops including first, unique continuation IDs, termination |
| Configuration change | [Configuration](tutorials/configuration.md) | No player page; definition default, getter fallback, one formula |

Reading declarations without semantics can misuse requested, source IDs or consumeTurn. Report a missing interface rather than inventing fields, menus, hot unloading or ModUi.SetConfig. Before using choices, confirm the actual Core reference contains those types; an API string of 1.8.0 does not prove an older installation includes recent additions.

## 2. Record six inputs before editing

Package ID and generated namespace; actual reference version and target types; existing files and full entry point; intended player actions; six-part mechanical fingerprint; assets and verification environment. Read package.json and the generated csproj first. Preserve codeEntryPoint and a single ModEntry. Mark missing evidence unassessed rather than reporting a failed scan as zero issues.

MiniHero is Western fantasy/fairy-tale adventure; Yaoguang is the explicitly authorized ancient Chinese heroine exception. Latest user instructions, applicable AGENTS and current code outrank historical designs. Old Wuxia identifiers do not define genre, and translation does not authorize stable-ID/key migration.

## 3. Deliver files and an observable result

Gameplay rules go in C# content classes under source/*.cs. Do not replace them with declarative gameplay JSON or contentIndex recipes. The package manifest is generated metadata, and localization JSON contains only displayed text. Generated projects target netstandard2.1 and C# 9, referencing game-generated API/Core. Runtime packages need package.json, mod/<AssemblyName>.dll, localization/zh-Hans.json and en.json, plus assets actually used. Full codeEntryPoint must match namespace plus class. Content IDs start with package ID plus a dot. Declare code.execute; code runs with user permissions, not in a sandbox.

List changed/new files, Load registration, the pool/stage referencing the content, added locale keys, player entry and expected result. Explain where fragment dependencies such as registry/context/nextRequest come from. A class with omitted abstract members or undefined types is not complete. Do not publish game-reference DLLs, bin/obj, .tmode-sdk, private paths or saves. See [project manual](01-project-and-build.md) for source and release output.

## 4. Preserve these rules

- CategoryTags, PoolTags and RequiredAppearanceTags have separate purposes. Candidate pools match any intersection; weight uses GetPoolWeight.
- Five/four/three/two quality values begin at Common/Uncommon/Rare/Epic and end at Legendary. Explicitly define a single Legendary variant rather than inheriting the default five.
- Healing-linked rules use settled AfterHealingEvent.requested. actual is for resources/presentation; explicit overflow rules use overflow. Natural descriptions say “治疗量” / healing amount.
- A new stage resets temporary treasure counters, stacks, pending effects and quotas, and restores active uses. Preserve handoff data only for explicit cross-stage exceptions.
- Base-stat conversions round down; shared percentages add before settlement. Preview follows the same rules without consuming real state.
- Specialized behavior belongs in concrete content, using common core settlement. Display cards do not execute original behavior; resolvers save stable IDs and must not end turns themselves.
- English uses attack by default and basic attack when distinction is needed; preserve technical NormalAttack identifiers. Shorten translations naturally without changing host UI.

## 5. Copyable task prompt

```text
Use guide revision 4 and the current generated MiniHero references.
Author the gameplay rules in C# content classes.
Task: add a two-card choice to my existing fixed test stage.
Keep the existing package ID, namespace, entry point and unrelated content.
Branch heal: restore 5 HP, free. Branch guard: pay 2 gold, gain 1 defense.
Use CardChoiceEventContent; do not execute display-card behavior.
Deliver the complete concrete class, Load registration, stage placement,
Chinese/English localization keys, dependencies and expected checks.
State which compilation, gameplay, saves, UI and Steam checks actually ran.
Do not invent host APIs. Report missing references or unsupported behavior.
```

For complex effects, specify trigger, input, reward, state, target and cost before generation. Referencing another game's documentation does not mean copying its APIs or images.

## 6. Evidence before delivery

Use the [debugging lesson](tutorials/debugging.md) to record compilation, loading, deterministic gameplay, boundaries, preview, reset, restore, bilingual UI and publication. Verify new DLLs after a full restart; same-process reload is insufficient. State unexecuted checks; existing tests and link checks are not current runtime evidence. Unity verification uses only the already-open formal Editor, without copies, a second Editor or Temp/PlayerBuildProject.
