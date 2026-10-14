# 操作配图与文件定位

[English](../../en/reference/visual-walkthrough.md) · [目录](../README.md)

教程修订 2 · Mod API 1.8.0 · 2026-10-14

截图来自正式工程的实际英文界面。创建和构建使用隔离的教程测试工作区及真实服务，未改动按钮、布局或文字；不包含用户现有项目。截图用于定位操作，不替代独立游戏完整重启验收。Alice 是教学用名字，作者栏填写自己的名字即可。

## 1. 进入工坊

![英文冒险工坊首页](../../../images/ui-workshop-overview-en.png)

主菜单左下角交叉工具按钮打开工坊。中间 **Develop Mods → Open** 进入开发；上方 **Manage Mods** 管理安装与启用。首课不用导入官方冒险样例。

## 2. 创建与打开源码

![填写首课包 ID 和显示名的新建窗口](../../../images/ui-new-project-en.png)

**Stable Package ID** 填 `local.alice.lantern-trail`，**Display Name** 是显示名。点击 **Create Project**；成功提示给出你本机的项目位置。已有同名 ID 时换一个，并核对生成的命名空间与清单入口。

![源项目关键文件示意](../../../images/source-layout.svg)

这是按实际生成目录绘制的关键文件示意，不是文件管理器截图或完整文件列表。项目行的蓝色源码文件夹图标打开 `Sources/<packageId>`；锤子向下箭头图标构建并安装；最右的包图标打开发布准备。编辑 `source/ModEntry.cs`，保留生成的 csproj，不在 Builds 或 Installed 修改源码。

## 3. 确认构建结果

![首课项目 v0.1.1 构建安装成功](../../../images/ui-build-success-en.png)

图中已按[首课](../tutorials/first-mod.md)改为 4 并将版本升到 `0.1.1`。底部 **Installation successful** 表示安装成功；行内 **Ready to build** 只是源项目构建入口状态，不是 SDK 检测，也不表示玩法验收完成。完整退出并重启后，再去图鉴核对一级说明。

![图鉴中旅者遗物的普通品质与 4 点护盾说明](../../../images/ui-codex-result-en.png)

主菜单打开 **Codex → Treasures**，角色筛选选 **All Characters**，搜索 `Wayfarer's Relic`，再点击结果。截图按实际加载结果选择普通品质；默认可能显示最高可用品质，各品质在本课共用一级数值 4。品质箭头不用于升级。此课未绑定自定义美术，图标只帮助识别结果，不是要求你另行提供的素材。

## 4. 找到错误报告

![失败报告目录与首条错误读法](../../../images/diagnostic-route.svg)

失败时游戏尝试自动打开报告文件夹。若打开失败，从工坊根目录按自己的包 ID、实际时间戳找到 `install-failure.txt`。图中 CS1002 仅演示文件、行列与错误的读法；以自己报告的第一条错误为准。参阅[排错](../troubleshooting.md)，分享前移除私人绝对路径。

## 5. 只导出目标图标

![素材表与单张图标的导出区别](../../../images/icon-crop-check.svg)

六格素材表不是一张宝物图标。在绘图工具中单独导出目标图，留出合理边距。这里是中性示意，不是游戏渲染；绑定后仍须在实际图鉴和牌场检查主体、透明边缘及比例，见[素材课](../tutorials/assets-and-text.md)。
