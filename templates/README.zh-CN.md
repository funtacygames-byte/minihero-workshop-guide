# 把示例代码放进自己的项目

[English](README.md) · [教程目录](../docs/zh-CN/README.md)

这些 `.cs.txt` 文件是可阅读的 C# 源码。先按[首课](../docs/zh-CN/tutorials/first-mod.md)创建自己的项目，再挑需要的文件复制。只下载本仓库，还不能把它当模组安装。

## 复制前先看这四点

1. 通过游戏的“打开源码”进入自己的项目。新源码都放进其中的 `source` 文件夹，并保存成 **`.cs`**，去掉链接文件末尾的 `.txt`。
2. **只有 01 替换 `ModEntry.cs`。**其他文件加入原项目，不增加第二个 `ModEntry`。新文件的 `namespace` 与现有入口一致。
3. 示例默认包 ID 为 `local.alice.lantern-trail`，命名空间为 `LocalAliceLanternTrailMod`。使用其他包 ID 时，先按首课适配 01；其他片段继续引用 `ModEntry.PackageId`。
4. 类写好后，还要在 `Load` 注册，并放进关卡或角色池。页面用 `AddScreen`、音乐用主题注册，具体位置见对应教程。

## 先完成这三个文件

| 源码 | 保存到自己的项目 | 跟着哪篇做 |
| --- | --- | --- |
| [01 入门宝物和入口](zh-CN/01-entry-and-config.cs.txt) | **替换** `source/ModEntry.cs` | [首课](../docs/zh-CN/tutorials/first-mod.md) |
| [08 固定关卡和冒险入口](zh-CN/08-fixed-stage-lab.cs.txt) | 新建 `source/PracticeStage.cs` | [第一个关卡](../docs/zh-CN/tutorials/stage.md) |
| [09 领取遗物奇遇](zh-CN/09-relic-grant.cs.txt) | 新建 `source/RelicGrant.cs` | [获得并使用宝物](../docs/zh-CN/tutorials/treasure.md) |

这条路线不用外部图片或音乐。01 文件名中的 `config` 保留旧链接含义；当前首课直接使用源码默认数值。

## 再按兴趣选择

| 源码 | 建议文件名 | 需要留意 |
| --- | --- | --- |
| [02 角色、特性、招式](zh-CN/02-character-trait-and-move.cs.txt) | `source/LanternRanger.cs` | 默认后备图片；按[角色课](../docs/zh-CN/tutorials/character.md)加入选关名单 |
| [03 角色专属宝物](zh-CN/03-character-treasures.cs.txt) | `source/CharacterTreasures.cs` | 与 02 的自定义池 Tag 一致；罗盘需要自己的图标 |
| [04 敌人和特性](zh-CN/04-enemies-and-traits.cs.txt) | `source/MossWolf.cs` | 默认后备图片；按[敌人课](../docs/zh-CN/tutorials/enemy.md)替换守卫 |
| [05 随机关卡绑定](zh-CN/05-stage-bindings.cs.txt) | `source/LanternTrail.cs` | 先有 02 的角色、04 的敌人及三张场景图，另需冒险入口 |
| [06 音乐主题](zh-CN/06-stage-music.cs.txt) | `source/MusicIds.cs` | 自备 OGG/WAV，注册主题后在关卡引用；看[音乐课](../docs/zh-CN/tutorials/assets-and-text.md) |
| [07 三地区结构](zh-CN/07-three-region-adventure.cs.txt) | `source/MyAdventure.cs` | 先实现并注册它引用的三个 Stage；看[多场景课](../docs/zh-CN/tutorials/adventure.md) |
| [10 双卡选择](zh-CN/10-card-choice.cs.txt) | `source/CampChoice.cs` | 在 08 放卡；看[补给选择课](../docs/zh-CN/tutorials/card-choice.md) |
| [11 页面和按钮](zh-CN/11-custom-page.cs.txt) | `source/CampPage.cs` | 用 `AddScreen(CampPage.Create())`；看[页面课](../docs/zh-CN/tutorials/custom-ui.md) |
| [12 两种道具](zh-CN/12-items.cs.txt) | `source/PracticeItems.cs` | 注册后放入牌列；看[道具课](../docs/zh-CN/tutorials/items-and-events.md) |
| [13 三次上限量瓶](zh-CN/13-stateful-relic.cs.txt) | `source/PracticeCounterRelic.cs` | 用 09 确定领取，摆四瓶药剂检查；看[状态课](../docs/zh-CN/tutorials/rules-and-state.md) |
| [14 有限动态续接](zh-CN/14-dynamic-continuation.cs.txt) | `source/ContinuingPracticeAdventure.cs` | 需要 08 的 `PracticeStage`；替换冒险注册，共三场景 |
| [15 连续选择](zh-CN/15-chained-choice.cs.txt) | `source/TwoStepSupplies.cs` | 将 08 的事件改为此类；按[连续选择步骤](../docs/zh-CN/tutorials/card-choice.md)测试确认和取消 |
| [16 难度复制](zh-CN/16-level-difficulty.cs.txt) | `source/ExtraDifficulty.cs` | 在原 Load 调用 `ExtraDifficulty.Register(registrar)`；[难度课](../docs/zh-CN/tutorials/level-difficulty.md) |
| [17 职业与进度](zh-CN/17-profession-progress.cs.txt) | `source/LanternTraining.cs` | 注册职业并修改 02 的 ProfessionId/Role；[职业课](../docs/zh-CN/tutorials/profession-progress.md) |

不要一次复制全部文件。特别是 07 不包含它所引用的三个地区关卡，不能单独运行。需要图片的片段应先放好文件；角色和敌人课则可以先无自定义图片完成。

## 文本从哪里取？

[中文文本表](zh-CN/localization.json)和[英文文本表](en/localization.json)列出示例名称与说明。只合并本课需要的 `entries`，保留自己的包名、其他键和 `locale`。逐课键前缀与具体合并操作见[素材与文本课](../docs/zh-CN/tutorials/assets-and-text.md#合并专题片段的文本)。

保存后递增 `package.json.version`，回游戏“构建并安装”，完整退出重启，再照专题里的步骤检查。
