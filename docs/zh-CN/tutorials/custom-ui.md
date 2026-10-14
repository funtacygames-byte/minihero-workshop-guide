# 制作自定义开始页与按钮

[English](../../en/tutorials/custom-ui.md) · [Index](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14


目标：启用模组并重启后出现营地手册页，“检查页面”更新一行文字，“开始冒险”进入宿主流程，“原版菜单”能返回原菜单。前置：[首课](first-mod.md)，新增 `source/CampPage.cs`，用[片段 11](../../../templates/zh-CN/11-custom-page.cs.txt)。没有图片或场景 Prefab 依赖。

## 1. 注册页面而不是注册内容

在已有 `Load` 中添加：

```csharp
registrar.AddScreen(CampPage.Create());
```

页面 ID 是包 ID＋`.screen.camp`；树中的 `camp.title` 等元素 ID 只在当前页面唯一，不需要每项加包前缀。页面控制器必须定义在当前 Mod 程序集。入口只注册页面与定义，不在 Load 时找 GameObject。

## 2. 三层分工

`ModUi.Column/Text/Button/HostButton` 定义控件树；`ModUiStyle` 是你自己页面的宽高、间距、Padding 和颜色；`ModScreenController` 处理交互。示例只设置新页面样式，不修改宿主已有文本框或字号。元素必须有非空 ID，Text/Button 必须有非空 fallback；自定义按钮要有 ActionId，宿主按钮使用现成命令。

“检查页面”走 `OnAction("camp.check", context)` 再 `SetText`；“开始冒险”走 `ModStartScreenAction.StartNewGame`，不是直接进入某个 Stage。宿主命令仍按宿主可用性执行，ContinueGame 无存档时禁用。`OnOpen`／`OnClose` 管理页面局部状态，`OnUpdate` 接受不受时间缩放影响的 delta，不应每帧写文件或改战斗。

## 3. 文本和语言切换

合并 `ui.camp.title/ready/check/play/original/checked` 六个键：营地手册／Camp Guide、手册已就绪。／Guide ready.、检查页面／Check Page、开始冒险／Start Adventure、原版菜单／Original Menu、按钮已响应。／Button responded.。

控件树中的 TextKey 随统一语言刷新解析；`SetText` 是即时文字，不会自动更改 TextKey。若需要维持动态状态，在合适的页面回调重新用 ModText 格式化；不要调用宿主专用 ConfigureResolver。切语言后重新打开并点击，核对文本、换行和按钮响应；不为长译文修改宿主 UI。

## 4. 扩展为两页与图片区

第二页使用不同的包内页面 ID，并注册为 `MainMenuPage` 或 `Overlay`。从当前控制器用 `context.OpenScreen(fullScreenId)` 打开；它只查本包注册页面。当前没有保证所有 MainMenuPage 自动出现在菜单上的入口，因此先用开始页按钮显式导航。关闭用 `context.CloseScreen()`；关闭替换开始页会返回原版菜单。

`ModUi.Image` 要绑定已存在的包内 PNG/JPG/JPEG；不能填公网 URL 或本机绝对路径。`Scroll` 可容纳长说明；只在新页面设计中使用，不给原版职业名控件擅自改布局。页面音乐注册 `ModMusicTheme` 后传 `musicThemeId`，由宿主 MainMenu cue 和全局音量控制。

## 5. 验收与边界

递增版本、构建安装、启用、完整重启。验证页出现、检查按钮响应、原菜单可回退、开始新局可用、切语言可读、停用模组后原菜单正常。此例控制器不持久化页面状态；若需要保存不能假定 controller 字段是局内存档。

每包只能注册一个 StartScreenReplacement。其他模组也替换开始页时存在优先级选择，测试时先单独启用。更多字段、树容量和诊断见[页面参考](../reference/custom-ui.md)。ModUi 没有配置写入、战斗卡选择或任意 Unity 组件操作入口。
