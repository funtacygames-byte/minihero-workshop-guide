# 加入图片、音乐与双语文本

[English](../../en/tutorials/assets-and-text.md) · [目录](../README.md)

教程修订 2 · Mod API 1.8.0 · 2026-10-13 · [验证范围](../reference/versions.md)

目标：给一件已运行的宝物绑定自己的图标；中英文界面都显示名称与同一数值；普通场景播放指定探索曲。按这三个任务分步做，便于定位文件、文本或音频问题。

前置：[首个模组](first-mod.md)，音乐还需[固定关卡](stage.md)。准备自己的 1:1 PNG 和有使用权的 OGG/WAV；本仓库只有教学示意图，不附游戏美术和音频。

安装修改后的构建前，按[首课](first-mod.md#4-修改一次并重新验证)递增 `package.json.version`；同一已安装版本不能对应不同内容。

## 1. 给宝物绑定一张图

把图放到 `assets/icons/starter-relic.png`。在 `StarterRelic` 类声明加 `, IModPresentationContent`，类内加：

```csharp
public ModPresentation Presentation => ModAssets.Icon("assets/icons/starter-relic.png");
```

重新构建会验证图片并生成 `assets/asset-index.json`。不要手改索引，也不要把未裁切的 3×2 素材表当一张图标。构建安装后在图鉴看实际裁切、透明边缘和主体尺寸。

单张图与素材表的区别见[裁切示意](../reference/visual-walkthrough.md#5-只导出目标图标)。

![资源比例示意](../../../images/asset-dimensions.svg)

角色主图用 `Icon`，284×512（71:128）；头像 `Avatar`、敌人 `BattleArt` 与宝物图标用 1:1。角色 `Portrait` 是兼容回退，不能替代检查主槽位。所有路径相对于包根，详见[展示参考](../reference/presentation.md)。

## 2. 编辑两份文本，保留共同键

工程已生成 `localization/zh-Hans.json` 与 `localization/en.json`。在各自 `entries` 中编辑以下两项，不删除文件里其他生成条目：

| key | 中文 value | English value |
| --- | --- | --- |
| `content.starter_relic.name` | 旅者遗物 | Wayfarer's Relic |
| `content.starter_relic.description` | 进入场景时获得 {0} 点护盾。 | Gain {0} shield when entering a stage. |

`ModText.Get` 读取名称，`ModText.Format` 将 `BaseValue × level` 填入 `{0}`。不要翻译键名，或把 `{0}` 换成另一个编号。保留 JSON 的 `locale` 字段，并确认清单 `supportedLocales` 含 `zh-Hans` 和 `en`。

改文件后重新构建安装并重载；最终与 C# 改动一起完整重启。分别切换中英文，在图鉴查看一级与其他等级，数字意义相同。格式错误可能把原模板直接显示出来；按[排错](../troubleshooting.md)检查 JSON 和参数。

## 3. 增加关卡探索曲

放入 `music/trail-explore.ogg`，在 `Load` 注册主题：

```csharp
registrar.AddMusicTheme(new ModMusicTheme(
    ModEntry.PackageId + ".music.trail",
    new Dictionary<ModMusicCue, string>
    {
        [ModMusicCue.StageExplore] = "music/trail-explore.ogg"
    }));
```

在 `PracticeStage` 返回的 `StageDefinition` 填 `music = ModEntry.PackageId + ".music.trail"`。入口文件需 `using System.Collections.Generic;`。构建安装，进入普通练习场景听探索曲，并检查全局音乐音量。

Boss 主题可以再提供 `BossBattle`，缺失时回退同主题探索曲，再回退内置列表。`Victory` 当前没有接为 Mod 胜利页曲目。自定义页面的 `MainMenu` 是另一入口，不因 Stage 注册而替换全局主菜单，见[资源总览](../03-assets-and-presentation.md)。

## 验收与下一步

- 路径、索引与槽位对应；最终图片规格正确，主体不被裁掉。
- 两种语言键集与变量一致，切换后名称和数字正确。
- 曲目真实播放、循环/后续播放和音量正确；缺资源回退按预期。

下一步[打包、发布与更新](publish.md)。保持原 UI 字号和框尺寸，通过自然短译文适配版面；配置 API 的说明在[兼容页](../reference/compatibility.md)。
