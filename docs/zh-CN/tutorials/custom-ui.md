# 做一个有按钮的开始页面

[English](../../en/tutorials/custom-ui.md) · [目录](../README.md)

把开始页换成“营地手册”：点击“检查页面”改变一行文字，点击“开始冒险”进入正常开局流程，也能点“原版菜单”返回。先把这三个按钮做通，再扩展页面。

**需要已有：**[首课](first-mod.md)。将[营地页面源码](../../../templates/zh-CN/11-custom-page.cs.txt)复制到新文件 `source/CampPage.cs`，命名空间与入口一致；修改原 `source/ModEntry.cs`。不用准备图片，也不需要 Unity 场景或 Prefab。

## 1. 注册页面而不是注册内容

在已有 `Load` 中添加：

```csharp
registrar.AddScreen(CampPage.Create());
```

页面 ID 是包 ID＋`.screen.camp`；树中的 `camp.title` 等元素 ID 只在当前页面唯一，不需要每项加包前缀。页面控制器必须定义在当前 Mod 程序集。入口只注册页面与定义，不在 Load 时找 GameObject。

## 2. 回游戏试试三个按钮

1. 保存源码、递增版本、构建安装并启用，完整退出重启。开始页应显示“营地手册”和三个按钮。
2. 点击“检查页面”，状态文字应从“手册已就绪。”变为“按钮已响应。”。
3. 点击“原版菜单”，应回到熟悉的主菜单。
4. 重新启动游戏，再点营地手册的“开始冒险”，应进入正常的开局流程。
5. 最后从原菜单进入工坊停用这份模组，重启后应恢复原版开始页。

这份示例没有保存页面状态；重新打开时回到初始文字是正常的。要检查英文，可以先返回原菜单，在设置里换语言，再重启查看页面。

每包只能注册一个 StartScreenReplacement。其他模组也替换开始页时存在优先级选择，测试时先单独启用。更多字段、树容量和诊断见[页面参考](../reference/custom-ui.md)。ModUi 没有配置写入、战斗卡选择或任意 Unity 组件操作入口。

## 3. 文本和语言切换

按[文本合并步骤](assets-and-text.md#合并专题片段的文本)添加以下六项。规则和按钮响应在 C#，这里的键负责查显示文字。

| 键 | 中文 | English |
| --- | --- | --- |
| `ui.camp.title` | 营地手册 | Camp Guide |
| `ui.camp.ready` | 手册已就绪。 | Guide ready. |
| `ui.camp.check` | 检查页面 | Check Page |
| `ui.camp.play` | 开始冒险 | Start Adventure |
| `ui.camp.original` | 原版菜单 | Original Menu |
| `ui.camp.checked` | 按钮已响应。 | Button responded. |

控件树中的 TextKey 随统一语言刷新解析；`SetText` 是即时文字，不会自动更改 TextKey。若需要维持动态状态，在合适的页面回调重新用 ModText 格式化；不要调用宿主专用 ConfigureResolver。切语言后重新打开并点击，核对文本、换行和按钮响应；不为长译文修改宿主 UI。

## 4. 扩展为两页与图片区

第二页使用不同的包内页面 ID，并注册为 `MainMenuPage` 或 `Overlay`。从当前控制器用 `context.OpenScreen(fullScreenId)` 打开；它只查本包注册页面。当前没有保证所有 MainMenuPage 自动出现在菜单上的入口，因此先用开始页按钮显式导航。关闭用 `context.CloseScreen()`；关闭替换开始页会返回原版菜单。

`ModUi.Image` 要绑定已存在的包内 PNG/JPG/JPEG；不能填公网 URL 或本机绝对路径。`Scroll` 可容纳长说明；只在新页面设计中使用，不给原版职业名控件擅自改布局。页面音乐注册 `ModMusicTheme` 后传 `musicThemeId`，由宿主 MainMenu cue 和全局音量控制。

## 5. 三层分工

`ModUi.Column/Text/Button/HostButton` 定义控件树；`ModUiStyle` 是你自己页面的宽高、间距、Padding 和颜色；`ModScreenController` 处理交互。示例只设置新页面样式，不修改宿主已有文本框或字号。元素必须有非空 ID，Text/Button 必须有非空 fallback；自定义按钮要有 ActionId，宿主按钮使用现成命令。

“检查页面”走 `OnAction("camp.check", context)` 再 `SetText`；“开始冒险”走 `ModStartScreenAction.StartNewGame`，不是直接进入某个 Stage。宿主命令仍按宿主可用性执行，ContinueGame 无存档时禁用。`OnOpen`／`OnClose` 管理页面局部状态，`OnUpdate` 接受不受时间缩放影响的 delta，不应每帧写文件或改战斗。
