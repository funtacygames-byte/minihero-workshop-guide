# 给角色接入水晶职业强化

[English](../../en/tutorials/profession.md) · [目录](../README.md)

把提灯游侠的职业改为**符文师**，复制魔法师的五项强化。玩家在现有职业强化页使用与内置职业相同的水晶购买，符文师的强化等级独立保存。

先完成[角色教程](character.md)，并使用生成 SDK 包含 **API 1.11.0** 的游戏版本。缺少 `ProfessionUpgradeCurrency` 或 `CopyBuiltInProfession` 时，更新游戏并重新生成开发引用。把网页上的声明复制进工程不能补上接口实现。

## 添加职业并绑定角色

把[职业源码](../../../templates/zh-CN/18-crystal-profession.cs.txt)复制到 `source/RunesmithProfession.cs`，命名空间改为现有入口的命名空间。在现有 `ModEntry.Load` 内注册：

```csharp
registrar.AddContent(new RunesmithProfession());
```

保留提灯游侠、特性和招式的原注册。在 `source/LanternRanger.cs` 的 `LanternRanger` 类中增加以下职业属性，并替换已有的 `Role` 属性：

```csharp
public override string ProfessionId => ModEntry.PackageId + ".profession.runesmith";
public override string Role => ModText.Get(ModEntry.PackageId, "profession.runesmith.name", "符文师");
```

从[英文](../../../templates/en/localization.json)和[中文](../../../templates/zh-CN/localization.json)文本表示例合并 `profession.runesmith.name`，值分别为 `Runesmith` 和 `符文师`。把 `package.json.modApiVersion` 改为 `"1.11.0"`，递增包版本，构建安装后完全退出并重启游戏。

`GameCrystals` 选择本体水晶余额和水晶图标。默认的 `ModCurrency` 则消费本包 `CurrencyKey` 对应的独立资源，默认键为 `training_points`；`CurrencyName` 和 `CurrencyIconId` 表示这份资源的名称和图标。选择独立资源前先给玩家获取途径，见[独立永久进度](#独立永久进度)。

## 买一级并检查结果

选择试验小径和提灯游侠，打开角色原有的职业强化页。页面应显示符文师、五个强化节点和本体水晶余额。开局金币节点在 0 级时花费 **50 水晶**。购买后余额减少 50，节点变为 1 级；新开一局获得 **2 枚额外金币**，内置魔法师的等级保持原值。

水晶不足时再尝试购买，余额和等级都应保持原值；满级后不能继续购买。完全重启游戏检查等级保存。停用并重新启用同一包会保留等级；修改职业或节点 ID 会创建不同节点。

每局开始时锁定强化快照。之后购买的强化在新局或重新开始时生效；继续旧存档恢复旧强化快照。永久扣除的水晶不会随战局回档。

水晶购买由游戏的强化按钮完成。Mod 回调不能通过 `ModProgress` 发放或扣除本体水晶；普通工坊对局奖励仍与官方水晶奖励、成就分开。

## 复制整套职业或组合单个节点

若要直接使用魔法师及其已有共享等级，可把角色的 `ProfessionId` 设为 `ProfessionIds.Mage`，`Role` 同样使用魔法师译名。需要独立等级时再注册自己的职业。

片段使用 `CopyBuiltInProfession(ProfessionIds.Mage, Id)`，把 `Mage` 改成 `Warrior`、`Ranger` 或 `Assassin`，即可复制对应职业的整套强化。效果、价格和等级上限一并复制，新 ID 归到你的职业下，等级与原职业独立。

若要自行组合节点，用以下内容替换 `Upgrades` 属性：

```csharp
public override IReadOnlyList<ProfessionUpgradeConfig> Upgrades => new[]
{
    ProfessionUpgradeConfig.FromBuiltIn(Id + ".wisdom", ProfessionUpgradeIds.MageWisdom),
    ProfessionUpgradeConfig.FromBuiltIn(Id + ".boss_shield", ProfessionUpgradeIds.WarriorBossShield)
};
```

返回的配置可修改 `costs`、`valuePerLevel`、`name`、`description` 和 `iconId`。`costs` 逐级列出正数价格，数组长度就是上限；每节点最多 100 级，每职业最多 32 个节点。ID 须属于当前职业的命名空间，同一种标准 `effectKind` 在职业内只能出现一次。复制的名称和当前等级说明会沿用游戏翻译，直到你替换对应字段。自定义说明支持 `{level}` 和 `{value}`，后者为等级乘以 `valuePerLevel`。

新机制使用 `ProfessionUpgradeEffectKind.Custom`，在职业自己的通用规则事件中实现，通过 `UpgradeLevel(e.State, upgradeId)` 读取等级。专属规则放在职业类中，不向游戏引擎添加职业专属分支。

## 独立永久进度

经验、解锁或独立训练资源见[职业与永久进度教程](profession-progress.md)，其中包含 `ModProgress`、成功回调写入、预览只读、数据上限和奖励去重。永久进度不会随战局回档。

发布前确定货币模式，切换模式不会转移余额或已购等级。
