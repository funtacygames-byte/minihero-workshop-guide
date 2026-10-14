# Troubleshoot by symptom

[简体中文](../zh-CN/troubleshooting.md) · [Index](README.md)

Guide revision 2 · API 1.8.0 · 2026-10-14

Find the failing phase before editing its files. Keep Sources; do not patch Builds or Installed. Baseline: API 1.8.0, guide revision 2.

## Get the actual error

Run `dotnet --version` in a terminal, then build from the development page. **Ready to build** means the source project meets the build-entry conditions; it is not an SDK detection result. The current UI has no separate SDK/API status panel. Current build/install failures automatically open a diagnostic folder containing `install-failure.txt`. If opening fails, the same report remains under workshop root `InstallFailures/<packageId>/<timestamp>/`.

The report records operation, package ID, source/build locations, stable error codes, field paths, and content IDs. Find the first C# `.cs(line,column): error CS...`, fix it, then build again. Later errors can be consequences. Package details in management also show loading diagnostics. Replace personal paths with `<project>` before sharing.

The final “build failed” line alone cannot identify an environment, syntax, manifest, or asset problem.

`AW_INSTALL_FAILED` with “same version, different content”: increment `version` in the Sources manifest, rebuild, and install. Keep the package ID stable. A full restart cannot resolve a rejected installation.

## Source will not compile

| Observation/code | Next action | Expected result |
| --- | --- | --- |
| `MH_MODSOURCE_DOTNET` | Run `dotnet --version` in a terminal; install SDK and reopen development | The command prints a version and rebuilding starts compilation |
| `MH_MODSOURCE_SDK` | Use a Windows Mono game build supporting C# mods and regenerate development references | Current API/Core can be used for compilation |
| `MH_MODSOURCE_BUILD` / CS error | Fix first file/line; check imports, braces, and abstract properties | Your DLL is produced |
| Directory ID differs from manifest | Match directory, packageId, and attribute; preserve released IDs | `MH_MODSOURCE_ID_MISMATCH` resolved |
| Editor shows errors, game builds | Keep generated csproj; refresh references and check editor file locks | Same references in both environments |

## Source compiles but loading fails

1. Confirm the correct package is enabled and installation succeeded; fully exit and restart.
2. `MH_MOD_ENTRYPOINT_MISSING`: match `codeEntryPoint` to the public full entry type, including namespace. See [Entry](reference/entry.md).
3. `MH_MOD_PACKAGE_ID_MISMATCH`: manifest packageId and `[MiniHeroMod(...)]` must agree exactly.
4. `MH_MOD_ASSEMBLY_MISSING`: point `codeAssembly` to actual output; source alone is not an installable package.
5. `MH_MOD_API_INCOMPATIBLE` / `MH_MOD_DEPENDENCY_LOAD`: rebuild against current game references and inspect unsupported APIs/dependencies. Do not place game API/Core DLLs in mod/.
6. `MH_MOD_LOAD_FAILED`: read the full exception and registration. Check public classes, parameterless constructors, unique IDs, registered references, and valid assets.

After loading, search the first lesson's treasure in the codex with all characters selected. Random chest draws are not a loading check.

## Content exists but effects fail or treasure is absent from draws

Check timing first. A stage-entry treasure acquired after entry needs the next stage. Do description and execution share a formula? Is SourceLevel mistaken for quality? Do healing rules read settled `requested`? Is move shield both accumulated and immediately granted? Use [Event contracts](reference/events.md).

For draw eligibility, inspect final character TreasurePool, any intersection of PoolTags, Include/Exclude overrides, quality, and appearance conditions. CategoryTags does not control eligibility, and eligibility does not guarantee a draw. The [specific reward encounter](tutorials/treasure.md) separates rule failures from randomness.

## Changes still show old behavior

Edit Sources, save all files, rebuild and install, confirm no failure diagnostic, fully exit every game process, restart, and begin a new run. A prior save's generated cards and runtime instances may retain data; structural changes need a new-run check. Same-process reload is not a C# hot unload.

## Character or art is incomplete

Missing character/trait/move reference: check public classes, package-prefixed IDs, and Load registration. Defining a class is insufficient. StartingTreasureTypes does not grant rewards; later StartingMoveTypes entries are not equipped. See [Limits](reference/compatibility.md).

`AW_CHARACTER_EMPTY_TREASURE_POOL`: the final character pool needs eligible registered treasures. The character lesson includes a life-build tag for its starting pool; using only a custom tag requires registering treasures with that tag before loading.

`MH_MOD_PRESENTATION_ASSET`: check existence, package-relative paths, case, standard directories, index, and slots. Main character art uses Icon; Portrait is a compatibility fallback. Do not substitute a square avatar for 71:128 main art. Correct dimensions still require in-game crop checks.

## Stage has no entry, guard, or usable exit

Registering a Stage alone does not create an Adventure entry. Check adventure registration, IncludeInSelection, difficulties, and character lists. Fixed cards are stored bottom-to-top; the last is exposed. Add exit before guard. Fixed columns do not receive random filler cards.

`AW_ADVENTURE_STEP_RANGE`: columns must be 1–5, rounds at least 1, and cardsPerRound between column count and 100. Fixed layouts still pass through step-field validation, while actual cards come from fixedColumns. This lesson uses a nominal 5 and actual 2.

`AW_STAGE_EXIT_MISSING`: current C# registration checks fixed-column exits for fixed layouts and pool exits for random layouts. Keep a pool Exit template for older-version compatibility if needed and verify it is absent from the fixed board. Unmet conditions and living bosses can also block exit. A graph Victory node does not replace an exit card.

## Asset, installation, or release failure

| Diagnostic | Action |
| --- | --- |
| `MH_MOD_MUSIC_ID` / `MH_MOD_MUSIC_ASSET` | Check theme ID/registration and OGG/WAV relative paths |
| `MH_MOD_STAGE_MUSIC_MISSING` | Match Stage.music to a registered theme or clear unused binding |
| Raw `{0}` appears | Check key, argument count, and string.Format syntax |
| `AW_BUILD_HASH_MISSING/MISMATCH` | Rebuild from Sources; do not modify built files |
| Invalid publishing preview | Supply the final valid file indicated by preparation diagnostics |
| Steam item submitted but hidden | Check agreement and actual visibility; local export is not online proof |

## Minimal reproduction for maintainers

Include game/API/guide versions, package ID, exact lesson/step, expected and observed behavior, first stable code, and necessary source. State names, levels, uses, and targets precisely. Remove private information. Reduce complex mods to a reproducible subset; do not upload game DLLs, entire saves, or credentials. Record entry, loading, gameplay, and online delivery separately; see [Versions and validation](reference/versions.md).
