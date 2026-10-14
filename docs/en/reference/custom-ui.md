# UI tree and host boundaries

[简体中文](../../zh-CN/reference/custom-ui.md) · [Index](../README.md)

Guide revision 5 · Mod API 1.8.0 · 2026-10-14


Follow the [custom-page lesson](../tutorials/custom-ui.md), then inspect [ModUi](api-surface.md#modui) and [IModUiContext](api-surface.md#imoduicontext). These interfaces describe page data that the host renders as Unity UI; they do not grant scene-editing access.

| Type / field | Constraint |
| --- | --- |
| `ModScreenDefinition.Id` | Unique within the package namespace |
| `Placement` | StartScreenReplacement, MainMenuPage, Overlay; an enum value does not guarantee an automatic entry everywhere |
| `Root` | Non-null tree; all element IDs unique within the page |
| `Controller` | Optional; if supplied, belongs to this Mod assembly |
| `Priority` | Used when choosing a replacement start page; replacements are not all displayed together |
| `CloseOnEscape` | True by default; still provide an original-menu fallback |
| `MusicThemeId` | Optional; package-owned ID referencing a registered theme |
| `ModUiElement` | TextKey/TextFallback, ImageAsset, ActionId, Visible, Interactable, Style |
| `ModUiStyle` | Width/Height/MinWidth/MinHeight default to -1, Gap to 8, FontSize to 28; negative dimensions use host automatic layout |

Kinds are limited to Column, Row, Panel, Text, Image, Button, Spacer and Scroll. Only the four containers accept children. Text/Image/Button/Spacer cannot contain controls. Style values must be finite: width, height and minimum sizes at most 4096; FlexibleWidth/Height nonnegative; Gap 0–256; FontSize 1–256; each Padding side 0–1024. Colors use `#RRGGBB` or `#RRGGBBAA`; optional colors may be empty. Root depth is 0; maximum depth is 16 and a page may contain at most 256 nodes. A page is not an unbounded data table.

`IModUiContext` provides page text, visibility, interaction and image updates; same-package navigation; closing; and host actions. It has no configuration-write or combat-state access. An incorrect element ID may produce no visible update; use observable text changes to diagnose it.

Host actions are StartNewGame, ContinueGame, OpenSettings, OpenAbout, ShowOriginalMenu and QuitGame only. Custom button ActionId goes to the controller; HostButton goes to the host. An ActionId is not an invented host command.

| Diagnostic | Check |
| --- | --- |
| `MH_MOD_SCREEN_ID` | Package prefix and duplicate page ID |
| `MH_MOD_SCREEN_CONTROLLER_ASSEMBLY` | Controller's declaring assembly |
| `MH_MOD_SCREEN_MUSIC_ID` | Package-owned theme ID |
| `MH_MOD_SCREEN_REPLACEMENT_DUPLICATE` | One replacement per package |
| `MH_MOD_SCREEN_SCHEMA` | Tree, fallback text, action, image file or Style |

Sources: current `MiniHeroModApi.cs`, `CodeModAssemblyLoader.cs`, `ModScreenHost.cs` and `MainMenuController.cs`. Compilation proves declaration availability only; verify language refresh, navigation, Escape, screen ratios and music in-game.
