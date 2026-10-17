# 给角色加职业强化和永久训练点

[English](../../en/tutorials/profession-progress.md) · [目录](../README.md)

让提灯游侠每击败一名敌人获得 1 训练点，再到现有角色强化页购买“体魄”：每级开局最大生命增加 2 点，共两级，价格依次为 2、3 训练点。

需要完成[角色课](character.md)，并使用支持 **Mod API 1.9.0** 或更高版本的游戏重新生成开发引用。保留角色的现有特性、招式和出场名单。

## 1. 注册职业并关联角色

把[职业片段](../../../templates/zh-CN/17-profession-progress.cs.txt)保存为 `source/LanternTraining.cs`，命名空间与入口一致。在原 `ModEntry.Load` 的角色注册行之前增加：

```csharp
registrar.AddContent(new LanternTraining());
```

在已有的 `LanternRanger` 类中添加 `ProfessionId`，并把原来的 `Role` 属性替换为下面这一项，不保留两个 `Role`：

```csharp
public override string ProfessionId => ModEntry.PackageId + ".profession.trailwarden";
public override string Role => ModText.Get(ModEntry.PackageId, "profession.trailwarden.name", "林地守卫");
```

把清单的 `modApiVersion` 设为 `1.9.0`；还使用难度复制接口时用 `1.10.0`。合并两种语言示例表中的 `profession.trailwarden.` 条目，按[文本合并步骤](assets-and-text.md#合并专题片段的文本)操作。递增包版本，构建安装并完整重启。

## 2. 获得资源并购买一级

用提灯游侠进入有守卫的练习关卡，击败敌人后回到角色强化页。训练点应增加；攒够 2 点后购买一级体魄，资源扣除 2，等级变为 1。重新开局时，基础最大生命 24 加上强化 2，得到 26。再攒 3 点购买二级，新开局最大生命为 28，此后不能再升级。

职业的 `Upgrades` 返回强化定义。`costs` 每项是升到下一级的价格，数组长度就是等级上限；不推算额外档位。每个职业 1–32 项，每项 1–100 级，价格为正数。强化 ID 以职业 ID 加点开头。示例用 `StartingMaxHp`，由共同规则结算；自定义规则使用 `Custom`，效果写在职业自己的事件回调中，通过 `UpgradeLevel(e.State, upgradeId)` 读取本局锁定等级。

升级费用来自该职业的 `CurrencyKey`，默认 `training_points`；扣费与升一级在宿主一次保存，本课消费本包训练点；API 1.11 另支持[本体水晶强化](profession.md)。职业及强化定义保持无状态。职业名称和强化标题用自然短译文，沿用现有字号和文本框。

## 3. 自己的永久标记

其他章节解锁或资源也能放在本包的永久标量数据中：

```csharp
var progress = ModProgress.ForPackage(ModEntry.PackageId);
int defeated = progress.GetInt("enemies_defeated", 0);
bool accepted = progress.AddInt("enemies_defeated", 1);
```

把写入放在成功的正式游戏动作或页面 `OnOpen/OnAction` 回调里。查询内容、战斗预览、状态投影、页面 `OnUpdate/OnClose` 和存档恢复不能提交永久写入；写方法会返回 `false`。失败动作和异常回调丢弃本次变更，后台线程不能提交。

数据由宿主按包 ID 保存，模组不获得磁盘路径或文件写权限。键用 ASCII 英文语义标识，可含数字、点、短横线和下划线；`__` 开头由宿主保留。每个字符串最多 16 KiB，每包最多 512 项、值合计 256 KiB。可用 `GetString/GetInt/GetBool`、`SetString/SetInt/SetBool`、`AddInt/Remove/TrySpend`；写方法的返回值表示是否接受这次修改。

强化在开局锁定快照。局外购买不改变进行中的对局；继续旧存档恢复旧等级，新开局读取新等级。永久资源不会随回档倒退；若某奖励不能反复刷取，作者需记录稳定章节或奖励 ID。停用、重新安装同一包 ID 不会删除这些数据；更换包 ID 会使用另一份进度。

检查重启后资源和等级仍保留，再用旧存档、新开局各试一次。接口声明见[API 索引](../reference/api-surface.md#professioncontent)。

[使用本体水晶并复制内置职业强化](profession.md)。
