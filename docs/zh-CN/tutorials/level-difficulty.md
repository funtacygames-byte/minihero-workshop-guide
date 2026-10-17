# 给现有关卡新增一档难度

[English](../../en/tutorials/level-difficulty.md) · [目录](../README.md)

这次不新建地图，把暮光彼岸的一档难度复制到苍莽幽径，修改敌人强化和水晶倍率，再作为新档位加入选关。

需要已完成[首课](first-mod.md)，并使用支持 **Mod API 1.10.0** 的游戏生成开发引用。旧版游戏缺少接口时，先更新游戏并重新生成引用；仅把清单版本改大不会增加接口。先按正常流程解锁目标地图。

## 1. 添加一个注册辅助类

把[难度复制片段](../../../templates/zh-CN/16-level-difficulty.cs.txt)保存为 `source/ExtraDifficulty.cs`，命名空间与原入口一致。在原 `ModEntry.Load` 中增加：

```csharp
ExtraDifficulty.Register(registrar);
```

保留已有注册，不再添加另一个入口。把 `package.json.modApiVersion` 设为 `1.10.0`，同时递增包的 `version`。

片段先用 `GetLevels()` 查看当前已加载的大关卡及完整难度配置，再从目标的最高编号加 1。默认目标有六档，所以新档是 VII；其他 Mod 已追加档位时，以实际最高编号为准。

## 2. 复制后改哪些字段？

示例的 `CopyLevelDifficulty("challenge_starlit_expedition", 3, next)` 读取暮光彼岸 III 的独立副本，再设置新编号。它把敌人额外攻击改成 8、额外生命改成 20、水晶倍率改成 1.8；其他复制来的配置保留。

| 方法 | 作用 |
| --- | --- |
| `GetLevels()` | 查看大关卡 ID、名称与难度列表 |
| `GetLevelDifficulty(levelId, difficulty)` | 读取指定难度的独立副本 |
| `CopyLevelDifficulty(sourceLevelId, sourceDifficulty, newDifficulty)` | 读取副本并设置新编号 |
| `AddLevelDifficulty(id, targetLevelId, definition)` | 将修改后的副本追加到目标地图 |

来源和目标可以相同，也可以是其他已加载的 Mod 地图。引用其他 Mod 时声明依赖并让它先加载；本包可先注册自己的冒险，再向它追加档位。也能继续读取本次 `Load` 中刚注册的档位。

复制包含角色与人数、规则 ID、额外攻防生命、奖励、各区域成长数组、道具白名单和分段设置。列表、数组和分段配置相互独立，注册时还会再次复制。修改新档位不会改动来源。地图本身的布局、牌池和基础成长仍由目标决定，相同参数放到不同地图，最终敌人属性可能不同。

只借用数值时，按设计明确改写或清空 `adventureRuleIds`、角色名单和道具限制。区域成长数组为 `null` 或空数组时继承规则，`new[] { 0 }` 明确关闭该项成长。启用分段道具池时保留六个互不重复的普通冒险道具 ID。

## 3. 在游戏里检查

合并[示例文本表](../../../templates/zh-CN/localization.json)与[英文表](../../../templates/en/localization.json)中的 `difficulty.starlight.description`，按[文本合并步骤](assets-and-text.md#合并专题片段的文本)处理。构建安装，完整退出并重启。

在苍莽幽径找到新档位，检查新说明和原有档位；进入战斗确认敌人强化，保存继续后编号仍正确。逐档解锁的地图要求先通关前一编号，因此编号应连续；本来全档开放的地图保留原规则。测试模式可进入所有档位，但不会留下 Mod 选关通关进度。

Mod 通关的选关记录独立保存，用于启用 Mod 时的解锁和通关标记；新增难度按声明稳定 ID 记录。停用后隐藏这些 Mod 记录与追加档位，官方通关、角色进度、成就和水晶不因 Mod 对局增加。示例的 1.8 是难度配置里的倍率，不代表 Mod 对局会发放官方水晶。

缺失模板或目标、重复编号、缺失引用及无效数值会导致加载诊断。声明 ID 必须属于自己的包且唯一；不要用区域、小关卡或牌池 ID 代替大关卡 ID。遇到错误先看第一条诊断，改源码后重建并重启。
