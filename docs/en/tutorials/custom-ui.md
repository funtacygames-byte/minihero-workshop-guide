# Build a custom start page and buttons

[简体中文](../../zh-CN/tutorials/custom-ui.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14


Goal: after enabling the mod and restarting, a Camp Guide appears. Check Page updates a line, Start Adventure invokes the host flow, and Original Menu returns to the original menu. Prerequisite: [first mod](first-mod.md). Add `source/CampPage.cs` from [fragment 11](../../../templates/en/11-custom-page.cs.txt). No image or scene Prefab is required.

## 1. Register a page, not content

Add to the existing `Load`:

```csharp
registrar.AddScreen(CampPage.Create());
```

The screen ID is the package ID plus `.screen.camp`. Element IDs such as `camp.title` are unique within this page and need no package prefix. Define the controller in the current Mod assembly. Load registers definitions; it does not search for GameObjects.

## 2. Three responsibilities

`ModUi.Column/Text/Button/HostButton` define the tree. `ModUiStyle` sets your page's size, spacing, Padding and colors. `ModScreenController` handles interaction. The example styles its new page without changing existing host text boxes or font sizes. Every element needs a nonempty ID; Text/Button needs a nonempty fallback. Custom buttons need ActionId; host buttons use existing commands.

Check Page invokes `OnAction("camp.check", context)` and `SetText`. Start Adventure invokes `ModStartScreenAction.StartNewGame`, rather than entering a specific Stage directly. Host commands retain host availability rules; ContinueGame is disabled without a save. `OnOpen` / `OnClose` manage page-local state, while `OnUpdate` receives unscaled delta time. Do not write files or alter combat every frame.

## 3. Text and language changes

Merge six keys: `ui.camp.title/ready/check/play/original/checked`, with 营地手册 / Camp Guide, 手册已就绪。 / Guide ready., 检查页面 / Check Page, 开始冒险 / Start Adventure, 原版菜单 / Original Menu, 按钮已响应。 / Button responded..

Tree TextKey values are resolved during shared language refresh. `SetText` supplies immediate text without changing TextKey. Reformat dynamic state with ModText in an appropriate page callback; do not call host-only ConfigureResolver. Reopen and click after switching language; check text, wrapping and response without resizing host UI for long translations.

## 4. Extend to two pages and images

Give the second page another package-owned ID and register it as `MainMenuPage` or `Overlay`. Navigate from the current controller with `context.OpenScreen(fullScreenId)`; it searches registered screens from this package only. There is no guarantee that every MainMenuPage receives an automatic menu entry, so start with explicit navigation from the replacement page. `context.CloseScreen()` closes a page; closing a replacement returns to the original menu.

`ModUi.Image` requires an existing package PNG/JPG/JPEG, not a public URL or local absolute path. Use `Scroll` for long text within your new page design, without changing original profession-name layouts. Register a `ModMusicTheme` and pass `musicThemeId` for page music; the host controls the MainMenu cue and global volume.

## 5. Acceptance and boundaries

Increment version, build, install, enable and fully restart. Check appearance, button response, original-menu fallback, starting a run, language readability and normal original menu after disabling the mod. This controller does not persist page state; controller fields are not automatically run-save data.

A package may register only one StartScreenReplacement. Several mods replacing the start page compete through priority selection; test with only this mod enabled first. See [page reference](../reference/custom-ui.md) for fields, tree limits and diagnostics. ModUi does not provide configuration writes, combat card choices or arbitrary Unity-component access.
