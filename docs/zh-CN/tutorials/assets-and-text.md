# 换上自己的图片、音乐和文本

[English](../../en/tutorials/assets-and-text.md) · [目录](../README.md)

先给旅者遗物换一个图标，再改中英文名称，最后给林径练习配一首探索曲。三个任务可以分开做；你只有一张图时，可以只完成第一节。

**需要已有：**[首课](first-mod.md)的项目。音乐还需要[固定关卡](stage.md)。准备一张自己的正方形 PNG；做音乐部分时，再准备可以使用的 OGG 或 WAV 文件。

本页的 `assets`、`music`、`localization` 都在工坊“打开源码”进入的项目根目录里。没有对应文件夹时可以创建。改完后保存、递增 `package.json.version`、构建安装；包含 C# 变化时完整重启游戏。

## 1. 给旅者遗物换图标

把图片命名为 `starter-relic.png`，放到项目的 `assets/icons` 文件夹。最终路径应为 `assets/icons/starter-relic.png`，不要把图片只放在桌面上。

打开 `source/ModEntry.cs`，找到 `StarterRelic` 的类声明，在 `TreasureContent` 后面加上 `, IModPresentationContent`。然后在这个类内部、其他方法外面加入：

```csharp
public ModPresentation Presentation => ModAssets.Icon("assets/icons/starter-relic.png");
```

保存，递增版本并构建安装，完整重启。打开图鉴搜索旅者遗物，应该看到新图。主体被裁掉时，回绘图工具给原图留边距或裁成正方形，再重建。

![图片槽位和长宽比](../../../images/asset-dimensions.svg)

构建会生成 `assets/asset-index.json`，不用自己写索引。六格素材表也不能直接当单张图标，先按[裁切示意](../reference/visual-walkthrough.md#5-只导出目标图标)导出其中一张。

### 角色和敌人也想换图

角色课和敌人课默认不绑定自定义图片。准备好文件后，在对应类声明中加 `, IModPresentationContent`，再按下表给该类增加一个 `Presentation` 属性：

| 类 | 准备的文件 | 比例 |
| --- | --- | --- |
| `SilverBolt` | `assets/icons/silver-bolt.png` | 1:1 |
| `LanternRanger` | `assets/icons/lantern-ranger.png` 与 `assets/portraits/lantern-ranger-avatar.png` | 主图 71:128、带完整背景 PNG；头像 4:5（如 1024×1280）、完整背景 |
| `MossWolf` | `assets/portraits/moss-wolf.png` | 1:1 |

角色的 `Icon` 是带完整背景的高竖幅主图，选人页框为 284×512（71:128），源图可用 568×1024 等更高分辨率。`Avatar` 是另一张带背景的 4:5 肖像，战斗底栏用它显示，小头像取它的顶部正方形。两张都保持不透明，分别构图。按[完整素材规格](../03-assets-and-presentation.md)检查编码、最终宽高和背景；AI 请求见[双图提示词](../ai-authoring.md#为同一角色准备立绘和头像)。

`SilverBolt` 类里加入：

```csharp
public ModPresentation Presentation => ModAssets.Icon("assets/icons/silver-bolt.png");
```

`LanternRanger` 类里加入：

```csharp
public ModPresentation Presentation => ModAssets.Create(
    (ModPresentationSlot.Icon, "assets/icons/lantern-ranger.png"),
    (ModPresentationSlot.Portrait, "assets/icons/lantern-ranger.png"),
    (ModPresentationSlot.Avatar, "assets/portraits/lantern-ranger-avatar.png"));
```

`MossWolf` 类里加入：

```csharp
public ModPresentation Presentation => ModAssets.Enemy("assets/portraits/moss-wolf.png");
```

只给自己已准备好图片的类加绑定。构建提示资源不存在时，先检查路径和大小写。角色主图看 `Icon`，头像看 `Avatar`，不要拿同一张正方形头像直接塞进竖向主图。更多槽位见[展示参考](../reference/presentation.md)。

## 2. 改名字，保留代码用的键

打开项目的 `localization/zh-Hans.json` 和 `localization/en.json`。在各自的 `entries` 中找到：

| `key` 保持不变 | 中文 `value` | 英文 `value` |
| --- | --- | --- |
| `content.starter_relic.name` | 旅者遗物 | Wayfarer's Relic |
| `content.starter_relic.description` | 进入场景时获得 {0} 点护盾。 | Gain {0} shield when entering a stage. |

可以把名称改成自己喜欢的名字；两种语言都改各自的 `value`。不要改 `key`，代码靠它找文字。说明里的 `{0}` 也保留，它会被 `BaseValue × 等级` 替换，所以以后改数值不必再手改说明。

保留文件的 `locale` 和其他条目，确认 `package.json.supportedLocales` 含 `zh-Hans` 和 `en`。重新构建安装并重启，在游戏设置里分别切中英文，去图鉴搜索对应名字，检查一级说明的数字是否相同。

### 合并专题片段的文本

角色、敌人、奇遇等新内容的文本在[中文示例表](../../../templates/zh-CN/localization.json)和[英文示例表](../../../templates/en/localization.json)里。它们是可挑选的文本集合，不要整份覆盖自己的文件。

1. 在示例表按下表找到需要的键。
2. 将对应的 `{ "key": …, "value": … }` 对象复制进自己文件的 `entries` 数组，和原条目并排放。对象之间用逗号分隔，不增加另一层 `entries`。
3. 已有同名键时，直接修改原条目的 `value`，不要再添加一份。
4. 在另一种语言的文件中加入相同的键，使用对应译文。两边的数字和 `{0}` 等参数保持一致。
5. 构建安装。换语言后新开一局或重新打开一次抉择，检查文字。

| 正在做的内容 | 在示例表中搜索 |
| --- | --- |
| 林径练习 | `stage.practice.`、`adventure.practice.` |
| 领取遗物 | `event.relic_grant.` |
| 提灯游侠 | `character.lantern_ranger.`、`trait.lantern_sight.`、`move.silver_bolt.` |
| 苔背魔狼 | `enemy.moss_wolf.`、`enemy_trait.wounded_rage.` |
| 药剂和药瓶 | `item.moon_dew.`、`item.ember_vial.` |
| 营地补给 | `event.camp_choice.`、`choice.camp.` |
| 连续选择 | `event.two_step_supplies.`、`choice.supply.`，以及复用的 `choice.camp.` |
| 练习量瓶 | `treasure.practice_counter.` |
| 营地手册页面 | `ui.camp.` |
| 动态续接 | `adventure.continuation_lab.` |

仅增加 JSON 不会翻译仍写死在 C# 中的文字；教程片段已经使用 `ModText.Get` 或 `ModText.Format`。未加入译文时，游戏显示源码里的默认文字。旧牌面可能已经保存了文字，所以切语言后用新局、新抉择检查。

## 3. 给林径练习加探索音乐

把音频放到 `music/trail-explore.ogg`。若用 WAV，就使用真实的 `.wav` 文件，并把下方路径改为 `.wav`；只改扩展名不能转换音频。

在 `ModEntry.cs` 的原 `Load` 方法内部、已有注册旁边加入：

```csharp
registrar.AddMusicTheme(new ModMusicTheme(
    ModEntry.PackageId + ".music.trail",
    new Dictionary<ModMusicCue, string>
    {
        [ModMusicCue.StageExplore] = "music/trail-explore.ogg"
    }));
```

入口文件顶部保留 `using System.Collections.Generic;`。然后打开 `PracticeStage.cs`，在 `CreateDefinition` 返回的 `new StageDefinition { … }` 中加入 `music = ModEntry.PackageId + ".music.trail",`，与 `id`、`name` 等字段并排。

保存、递增版本、构建安装、完整重启。新开林径练习，进入普通场景后应听到自己的曲目。听不到时，先检查游戏设置的音乐音量，再查文件路径和主题 ID 是否一致。

做 Boss 场景时可以另设 `BossBattle`，缺失会先回退同主题探索曲，再用内置曲目。`Victory` 目前不能替换 Mod 胜利页音乐；开始页音乐也属于另一入口，见[音乐参考](../03-assets-and-presentation.md)。

接下来可以[准备发布](publish.md)。名称太长时，用自然短句重新表达并在游戏里检查；保留数值和规则，不通过改原版字号或文本框来挤进去。
