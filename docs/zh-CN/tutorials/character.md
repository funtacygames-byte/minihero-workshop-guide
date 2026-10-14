# 做一个有自己招式的角色

[English](../../en/tutorials/character.md) · [目录](../README.md)

这次把选角页的角色换成“提灯游侠”：基础生命 24、攻击 6、防御 1、智慧 2，带有“灯辉视野”特性和 2 次“银辉箭”。先让角色能选、招式能用，再给它加自己的图片。

**需要已有：**[首课](first-mod.md)和[固定关卡](stage.md)的项目。本课默认使用游戏后备图片，不需要事先准备素材。

**要编辑：**新建 `source/LanternRanger.cs`；修改 `source/ModEntry.cs` 和 `source/PracticeStage.cs`。保存后递增 `package.json.version`，构建安装并完整重启。

## 1. 注册三个类

把[角色、特性与初始招式源码](../../../templates/zh-CN/02-character-trait-and-move.cs.txt)完整复制到 `source/LanternRanger.cs`。在原 `ModEntry.cs` 的 `Load` 方法中增加：

```csharp
registrar.AddContents(new LanternSight(), new SilverBolt(), new LanternRanger());
```

源码里的 `LanternSight` 对应“灯辉视野”，`SilverBolt` 对应“银辉箭”，`LanternRanger` 才是角色。注册三者后，角色才能找到自己的特性和招式。

当前源码没有自定义图片绑定，复制后可以直接构建。做好角色后，再按[素材课](assets-and-text.md#角色和敌人也想换图)增加招式图标、角色主图和头像。先不要填尚不存在的图片路径。

## 2. 将角色加入练习入口

打开 `source/PracticeStage.cs`，找到 `PracticeAdventure` 的 `Difficulties` 属性。将其中原本只含符刃猎手的 `availableHeroIds` 列表替换为：

```csharp
availableHeroIds = new List<string>
{
    ModEntry.PackageId + ".character.lantern_ranger"
}
```

`availableHeroIds` 设置真正的选关名单。`PracticeStage.allowedCharacterIds` 可保留同一 ID 让元数据一致，但当前 C# 流程不靠该字段限制选人。这个关卡只有一个角色时，`maxHeroCount = 1` 即可。

若要加入正式大关卡，可使用 API 1.7.0 起的 `AddCharacterToLevel`，查[注册参考](../reference/entry.md)；不要把小关卡的牌池 ID 当成大关卡 ID。

## 3. 选择角色，试试招式

构建安装，完整重启。选择林径练习，在选角页检查名字和基础属性；进场后检查初始招式是银辉箭，次数为 2。按住初始招式“银辉箭”，拖到明牌守卫上松开，检查伤害，以及次数是否由 2 变为 1。

银辉箭单次伤害读取当前攻击的 2 倍，真实敌人伤害仍走统一结算。要测试“灯辉视野”额外攻击目标，在 `PracticeStage.CreateDefinition` 返回前加入下面这段代码，第二列也会露出一名守卫。然后用普通攻击打其中一名，观察两名敌人的伤害；银辉箭仍只打一个目标。

```csharp
CardState secondGuard = guard.Clone();
secondGuard.id = Id + ".guard.two";
columns[1].cards.Add(secondGuard);
```

## 4. 核对当前开局限制

`StartingMoveTypes` 当前只把第一项加载为初始招式；后续项不会自动放入普通招式槽。`StartingTreasureTypes` 会登记、校验，但选角不发放。需要明确宝物奖励时使用[领取事件](treasure.md)。

片段包含 `CharacterTreasurePoolTags.HealingLifeBuild`，让首次创建的角色在尚未加入自有宝物时也有合法候选池。另一个 Tag `treasure_pool.your_package.lantern` 与[角色宝物片段](../../../templates/zh-CN/03-character-treasures.cs.txt)匹配，按任意交集进入候选。以后若移除生命构筑 Tag，先为剩余自定义 Tag 注册可入池宝物；空池会报告 `AW_CHARACTER_EMPTY_TREASURE_POOL`。改自定义 Tag 时两边一起改；权重用 `GetPoolWeight` 或角色 `SetWeight`。

## 回游戏检查，然后继续

- 林径练习中可以选到提灯游侠，显示基础生命 24、攻击 6、防御 1、智慧 2。
- 银辉箭从 2 次变为 1 次，并命中选中的敌人。
- 摆两名敌人后，普通攻击能额外命中另一名；银辉箭仍为单目标。

继续[敌人与实例状态](enemy.md)。接口默认值与状态边界见[角色与敌人参考](../reference/actors.md)。

## 让同一份源码随语言变化

本课片段已使用 ModText 读取角色、特性、招式和职业显示文字。将[中文示例键](../../../templates/zh-CN/localization.json)和[英文示例键](../../../templates/en/localization.json)的 entries 合并到你已有的两份目录，不覆盖生成条目。规则和 ID 保持同一份源码；切语言后新开测试局核对名称、说明和职业，详见[素材与文本课](assets-and-text.md)。
