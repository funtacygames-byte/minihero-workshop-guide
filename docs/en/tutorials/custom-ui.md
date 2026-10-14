# Create a start page with working buttons

[简体中文](../../zh-CN/tutorials/custom-ui.md) · [Index](../README.md)

Replace the start page with a **Camp Guide**. **Check Page** changes a line of text, **Start Adventure** starts the normal new-game flow, and **Original Menu** takes you back. Get these three buttons working before expanding the page.

**You need:** [Your first mod](first-mod.md). Copy [the camp-page source](../../../templates/en/11-custom-page.cs.txt) to a new `source/CampPage.cs`, matching your entry's namespace, and edit your existing `source/ModEntry.cs`. No images, Unity scenes or Prefabs are required.

## 1. Register a page, not content

Add to the existing `Load`:

```csharp
registrar.AddScreen(CampPage.Create());
```

The screen ID is the package ID plus `.screen.camp`. Element IDs such as `camp.title` are unique within this page and need no package prefix. Define the controller in the current Mod assembly. Load registers definitions; it does not search for GameObjects.

## 2. Try all three buttons in the game

1. Save, increment the version, build and install, enable the mod and fully restart. The start page should show **Camp Guide** and three buttons.
2. Choose **Check Page**. The status should change from **Guide ready.** to **Button responded.**
3. Choose **Original Menu** to return to the familiar main menu.
4. Restart again and choose **Start Adventure** on the Camp Guide. It should enter the normal new-game flow.
5. Finally, open Workshop from the original menu, disable this mod and restart. The original start page should return.

This example does not save page state; returning to the initial status when it reopens is normal. To check Chinese, return to the original menu, change language in settings, then restart and inspect the page.

A package may register only one StartScreenReplacement. Several mods replacing the start page compete through priority selection; test with only this mod enabled first. See [page reference](../reference/custom-ui.md) for fields, tree limits and diagnostics. ModUi does not provide configuration writes, combat card choices or arbitrary Unity-component access.

## 3. Text and language changes

Use [the text-merging steps](assets-and-text.md#merge-text-for-topic-fragments) to add these six entries. C# defines the behavior; these keys look up displayed text.

| Key | Chinese | English |
| --- | --- | --- |
| `ui.camp.title` | 营地手册 | Camp Guide |
| `ui.camp.ready` | 手册已就绪。 | Guide ready. |
| `ui.camp.check` | 检查页面 | Check Page |
| `ui.camp.play` | 开始冒险 | Start Adventure |
| `ui.camp.original` | 原版菜单 | Original Menu |
| `ui.camp.checked` | 按钮已响应。 | Button responded. |

Tree TextKey values are resolved during shared language refresh. `SetText` supplies immediate text without changing TextKey. Reformat dynamic state with ModText in an appropriate page callback; do not call host-only ConfigureResolver. Reopen and click after switching language; check text, wrapping and response without resizing host UI for long translations.

## 4. Extend to two pages and images

Give the second page another package-owned ID and register it as `MainMenuPage` or `Overlay`. Navigate from the current controller with `context.OpenScreen(fullScreenId)`; it searches registered screens from this package only. There is no guarantee that every MainMenuPage receives an automatic menu entry, so start with explicit navigation from the replacement page. `context.CloseScreen()` closes a page; closing a replacement returns to the original menu.

`ModUi.Image` requires an existing package PNG/JPG/JPEG, not a public URL or local absolute path. Use `Scroll` for long text within your new page design, without changing original profession-name layouts. Register a `ModMusicTheme` and pass `musicThemeId` for page music; the host controls the MainMenu cue and global volume.

## 5. Three responsibilities

`ModUi.Column/Text/Button/HostButton` define the tree. `ModUiStyle` sets your page's size, spacing, Padding and colors. `ModScreenController` handles interaction. The example styles its new page without changing existing host text boxes or font sizes. Every element needs a nonempty ID; Text/Button needs a nonempty fallback. Custom buttons need ActionId; host buttons use existing commands.

Check Page invokes `OnAction("camp.check", context)` and `SetText`. Start Adventure invokes `ModStartScreenAction.StartNewGame`, rather than entering a specific Stage directly. Host commands retain host availability rules; ContinueGame is disabled without a save. `OnOpen` / `OnClose` manage page-local state, while `OnUpdate` receives unscaled delta time. Do not write files or alter combat every frame.
