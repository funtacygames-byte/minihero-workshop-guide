# 04 Testing and publishing

[简体中文](../zh-CN/04-testing-and-publishing.md) · [Guide index](README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14

Start with [Your first mod](tutorials/first-mod.md). This page is a manual; use the [task index](README.md) for guided steps.

Compilation is the start of verification. Also check registration, bindings, values, state resets, assets, installation, and behavior in a clean environment.

Fixed `CardColumnState.cards` are stored **bottom to top**, with the last item exposed. Put an exit before its guard in the list to place it beneath the guard. Test actual card clicks as well as registration and list sizes.

The source folder's ID must match `package.json.packageId`. Empty IDs, invalid JSON, and mismatches are diagnosed before preparation or compilation. A failed build/install should leave the installed version intact. Preserve your Sources, repair the manifest according to the diagnostic, and retry.

## Contents

1. Basic checks for every content type
2. Treasure tests
3. Character, enemy, and stage tests
4. Artwork and music tests
5. Troubleshooting order
6. Common errors
7. API version and compatibility
8. Permissions, trust, and signatures
9. Packaging checklist
10. Publishing and updating in the game
11. Browsing and configuration

## 1. Basic checks for every content type

- IDs are unique and start with the package ID and a dot.
- Classes are `public` with public parameterless constructors.
- All content is registered in `Load`.
- Numbers, caps, and duration match real execution.
- Missing localization has readable fallback text.
- Artwork, music, and code paths match exactly, including case.
- Verify a C# change at least once after fully restarting.

## 2. Treasure tests

For every treasure, cover:

- Level 1 and maximum level, and every quality actually provided.
- Full/low HP, zero/high shield.
- No enemies, one enemy, and several enemies.
- First trigger, reaching a threshold, and crossing several thresholds at once.
- Per-stage trigger cap and counter resets.
- Permanent stats retained across stage changes.
- Preview versus real execution.
- Stacking with another percentage modifier of the same kind.

Compare trigger, input, main benefit, state structure, target range, and costs/limits with existing treasures. If all six closely match, change the decision value or explicitly identify the old treasure being replaced.

### Column clearing and automatic moves

Check `OnColumnCleared` fires only when the final card in the column is removed. Defeating an enemy with cards beneath it is insufficient. Clearing several columns dispatches for each newly empty column, and a refilled column can trigger again later.

`automaticInitialMoveTriggers` counts requests, not successes. Automatic calls have no selected target column: `MoveTargetKind.Enemy` cannot choose an enemy by itself. Use `RandomEnemy` for automatic exposed-enemy targeting and test both available and absent targets.

Count successes with `OnAfterMoveResolved` and `automatic == true`; test early termination without a legal target. Grant post-move shield through `e.shield += amount`, without also calling `Runtime.AddShield`. There is currently no identifier connecting a particular clear request to its move result.

## 3. Character, enemy, and stage tests

### Characters

Check base stats, displayed/working traits, and the single starting move loaded into `State.initialMove`. Check the expected intersection between character tags and treasure `PoolTags`. Character selection currently grants no `StartingTreasureTypes` and does not put the second starting-move entry into an ordinary move slot.

### Enemies and composite traits

Check values, registered `EnemyTraitId`, and the timing of damage, round, death, and countdown callbacks. Counters must be isolated per enemy instance.

For a composite trait, override several callbacks in one trait class. Count damage only after HP loss and keep stacks independent. `OnRoundStart` is the enemy response phase after a basic attack; defeated or no-longer-exposed enemies are skipped. Test defense growth and restoration from a snapshot.

### Direct damage and multiple hits

A targeted item's `CardEffectType.Damage` hits only its selected enemy. A direct-use item's `DamageAllEnemies` hits current exposed enemies individually. For both, check `OnAfterDamaged` only on HP removal, overkill not overcounted, column changes on death, and absence of the basic-attack-only `OnRoundStart`. `MultiHit` dispatches damage callbacks per damaging hit, while `MoveUsed` remains once per move.

### Encounters and rich choices

Test `Action=None` direct effects, `Action=Meditation` stat filtering/count/selection, and nonempty `richEventChoices` taking precedence. Cover payable and unpayable stat/gold costs, post-cost rewards, free and reserve treasure slots, and separation between branches. An unaffordable choice must not charge partially or grant a reward. Rich choices should not accidentally apply basic `Effect`, `Choices`, or card-level `goldCost`.

For legacy C# rich events, check conditions again at confirmation, keep failures free of partial costs/rewards, and verify registered reward types and counts. Test follow-up event placement and use actual expanded stage IDs for stage transitions. New card-face choices use the [C# choice checklist](tutorials/card-choice.md).

### Stage layout and victory

Check registration, membership in the intended adventure, random-pool counts, fixed-card order, and a clickable exit. With `fixedColumns`, only those columns should appear: empty columns stay empty, random candidates are not mixed in, and total card count equals the fixed cards. Current C# validation checks exits in fixed columns for fixed layouts and in `appearancePool` for random layouts. If retaining a pool Exit template for earlier-version compatibility, verify it does not appear in the fixed board.

Test clicking an exit before and after `victoryConditions` becomes true. The condition is checked on the click, not automatically on a kill. `defeatedEnemies >= 1` counts run-wide defeats, not a specific enemy. Living ordinary enemies do not block exits by themselves; a living boss does. Include the test character in the difficulty roster and create enemy cards from registered content.

### StageGraph

Both preselection and postselection loads need a usable route. For `has:` character routing, test the fallback and recalculation after selection. Before selection, `State.character` is null and `has:` ignores the candidate list. Selection writes the character and `BaseStats` before reload; numeric conditions read that player's current stats.

Every load rebuilds `stageGraphVisitedNodeIds` and records the current node before outgoing conditions. The selected route does not inherit preview visits, while `reach:<currentNode>` is true. Test `reach:`, `tag:`, and numeric comparisons. Multiple matching edges must use positive weights rather than list priority; use several seeds to check selection.

A syntactically valid, always-false edge can pass static registration but fail `LoadStage` with `InvalidOperationException` naming a node with no usable successor. Graph cycles should report `AW_STAGE_CYCLE`. A C# node needs its `card` snapshot; a visited card is guaranteed even with `required=false`. Use the random pool for optional cards.

Traverse Victory and Failure, then click the physical exit. Failure loses on exit settlement; Victory still requires an exit and any configured victory condition. C# stages supply `node.card` explicitly; `contentId` alone does not create the snapshot.

### Bosses

Set `CardState.isBoss` on the boss card and `AdventureStepDefinition.boss` on the adventure step. A source stage used independently as a boss stage also needs `StageDefinition.boss`. Check load diagnostics, the expanded final round's flag, and guaranteed boss generation through `guaranteedInStage`.

## 4. Artwork and music tests

Check icons, main character art, avatars, enemy art, backgrounds, map thumbnails, and arrival art. Inspect transparency, safe margins, scaling, and cropping at different resolutions.

Use 284×512 (71:128) for main character `Icon`, square `Avatar/BattleArt`, and preferably the same tall size for a fallback `Portrait`. Treasure and move icons are square. Never bind a raw 3×2 sheet directly. Rebuild after slicing so `assets/asset-index.json` records the final files.

Check `StageExplore` on ordinary stages and `BossBattle` on boss stages. Missing boss music first falls back to same-theme exploration; missing/failed exploration falls back to the built-in in-game playlist. An ordinary stage with a boss-only theme also uses that playlist. Verify global and relative mod volume, playback after a track finishes, and that disabling a mod or changing stages does not retain the wrong theme.

## 5. Troubleshooting order

1. Run `dotnet --version` in a terminal; keep the generated csproj and game references, then build. A row marked **Ready to build** does not replace the SDK check.
2. For compilation, find the first `.cs(line,column)` error; later errors may follow from it.
3. For installation, inspect hash diagnostics rather than editing Builds.
4. For installed but absent content, check package ID, entry type, `codeEntryPoint`, enabled state, and reload.
5. For broken bindings, check referenced types/IDs were registered. A missing/wrong character reference may mean the class is not public, its ID is outside the package namespace, or `Load` omitted `registrar.AddContent(new YourCharacter())`.
6. For an inactive rule, check callback choice, field semantics, and `SourceLevel`.
7. For artwork, check standard folders, relative paths, casing, slots, and index.
8. For music, check theme registration, stage `music`, OGG/WAV files, and boss flags.
9. For an already loaded DLL, fully exit and restart before judging the change.

## 6. Common errors

- `MH_MODSOURCE_DOTNET`: dotnet cannot start; install or repair the SDK.
- `MH_MODSOURCE_BUILD`: compilation error; fix the reported file and line.
- `MH_MOD_API_INCOMPATIBLE`: the mod requires an API beyond the game's supported range.
- `MH_MOD_MUSIC_ID`: duplicate theme ID or ID outside the package namespace.
- `MH_MOD_MUSIC_ASSET`: missing audio or unsupported format.
- `MH_MOD_PRESENTATION_ASSET`: artwork path, index, or slot mismatch.
- `AW_BUILD_HASH_MISSING`: not a built output or missing hash manifest.
- `AW_BUILD_HASH_MISMATCH`: files changed after building.
- Content ID outside the package: missing `packageId + "."` prefix.
- Treasure never drawn: check the tag intersection, then `TreasurePool.Exclude` or an intended `Include`.
- Missing character move/trait: unregistered type or wrong reference.
- No enemies in a stage: retrieve registered enemies and call `CreateCard`.

## 7. API version and compatibility

The current API is **1.8.0**, with minimum compatible version **1.0.0**. Older mods using older capabilities can continue to load. For `AddCharacterToLevel`, declare at least 1.7.0:

```json
{ "modApiVersion": "1.7.0" }
```

For 1.8 features such as adventure rules, looping, seed settings, or dynamic continuation, declare `modApiVersion: "1.8.0"`. Declaring a higher version than the game supports is rejected because methods may be unavailable. The assembly's major version stays stable to reduce disruption from additive API changes.

## 8. Permissions, trust, and signatures

C# mods must declare `code.execute`. Their DLLs have the game process's local permissions; enable code only from sources you trust.

Hashes detect changes and do not certify authorship. The author field is not platform-verified, and certificate signing is not currently provided. Trust binds to the exact package ID, version, and hash; changing files requires confirmation again.

## 9. Packaging checklist

- Increase the `package.json` version; do not publish different contents under one version.
- Include the manifest, your DLL, and the localization/artwork/music actually used.
- Exclude development references, `source/bin`, `source/obj`, caches, and game API/Core DLLs.
- Test from a clean installation rather than only existing caches.
- Confirm build and installed-copy hashes match.
- List dependency versions, default configuration, changes requiring restart, and known limits.
- Remove absolute local paths, personal account folders, temporary files, and private data.
- Preserve the relationship between source version and published package for reproduction.

## 10. Publishing and updating in the game

1. Select your source project in **Develop Mods**. Use **Open source** to edit version, cover, and preview paths in `package.json`. The shipped guide is read-only; your Sources is editable.
2. Open release preparation and enter title, description, comma-separated tags, and version notes. Visibility defaults to private.
3. Save a draft to retain incomplete metadata in workshop-root `State/Publication/<packageId>.json`.
4. Validation/upload checks required metadata, compiles C#, validates the package, image paths, and hashes, then exports to `Exports/<packageId>/<version>-<uniqueId>/`. This publishing flow does not install or execute that DLL. After validation, Steam creates an item or updates the locally bound item.
5. The new Steam item ID is saved immediately in the publication state file. If uploading fails, retry the same item; keep its state file. Increase the package version before updating. Exported `content/` is the uploaded payload; `publication.json` records export metadata. `coverAsset` supplies the main cover, and `previewAssets` supplies extra images. Updates reuse the item and replace its extra previews with the current list.
6. Visibility defaults to private. The upload area links to the Steam Workshop agreement. If Steam requires acceptance after the first publication, the item stays hidden until accepted.

The manifest's `coverAsset` must be a package-local relative image path. Optional `previewAssets` lists extra detail images. The game passes these to Steam, but its current local validator accepts only correctly encoded PNG, JPG, or JPEG, excluding GIF. Neither side may exceed 4096 pixels, and every file must be strictly smaller than **1,048,576 bytes** (1 MiB, shown as “1 MB” in the UI). Use 16:9 for landscape previews, such as 1280×720 or 1672×941, then compress the file. A separate square adventure cover is suitable; character art and avatars serve their own UI slots.

Check actual byte sizes for every cover and preview. A high-resolution in-game background may be too large for a preview: export a genuinely compressed JPG and use that path in `previewAssets`, rather than merely changing the extension. Rebuild afterward.

The game's Steam upload requires a successfully initialized client, App ID `5302070`, and the corresponding Workshop access and backend configuration. Current code connects subscription scanning, download requests, and importing downloaded packages. Downloaded code packages still require trust and enabling in management. Test uploads, subscriptions, updates, and downloads separately in a real Steam client. Local building and validation can be completed without Steam access, but do not establish that online flows work.

## 11. Browsing and configuration

Browsing combines duplicate sources and historical versions by package ID and prefers the latest available package. Filters cover not installed, updates, and repair; sorting includes name, modification time, and size. After installation, go to management; code mods still need trust confirmation and enabling.

There is no player-facing mod configuration page. `AddConfig` and `ModConfig` retain underlying compatibility interfaces. Author and test against source defaults. Do not promise workshop menus for toggles, choices, numbers, or text. To change a C# default, rebuild, install, and fully restart to verify it.
