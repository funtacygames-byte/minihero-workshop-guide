# 制作角色、特性和初始招式

[English](../../en/tutorials/character.md) · [目录](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14 · [验证范围](../reference/versions.md)

目标：在林径练习的选角页看到“提灯游侠”，基础生命 24、攻击 6、防御 1、智慧 2；开局只有“银辉箭”这一项初始招式。本课用三种内容组合角色，再把角色加入一个明确入口。

前置：[首个模组](first-mod.md)与[固定关卡](stage.md)。增加 `source/LanternRanger.cs`；三个素材必须由你提供，或先按下文做无自定义图片的规则检查。

安装修改后的构建前，按[首课](first-mod.md#4-修改一次并重新验证)递增 `package.json.version`；同一已安装版本不能对应不同内容。

## 1. 注册三个类

复制[角色、特性与初始招式片段](../../../templates/zh-CN/02-character-trait-and-move.cs.txt)，核对命名空间，在 `Load` 增加：

```csharp
registrar.AddContents(new LanternSight(), new SilverBolt(), new LanternRanger());
```

`LanternSight` 是独立角色特性；`SilverBolt` 是招式；`LanternRanger` 通过类型列表组合它们。引用类存在却未注册会加载失败。

片段声明了图标和头像路径。需要准备：`assets/icons/silver-bolt.png`（1:1）、`assets/icons/lantern-ranger.png`（284×512 或相同比例）、`assets/portraits/lantern-ranger-avatar.png`（1:1）。路径与规格见[资源课](assets-and-text.md)。

先检查规则时，可从 `SilverBolt` 和 `LanternRanger` 的类声明移除 `, IModPresentationContent`，并删除各自整个 `Presentation` 属性。这只移除自定义图片绑定，保留全部规则；不能保留指向不存在文件的绑定。完成后再加回自己的图片。

## 2. 将角色加入练习入口

在 `PracticeAdventure.Difficulties` 的 `availableHeroIds` 改为：

```csharp
availableHeroIds = new List<string>
{
    ModEntry.PackageId + ".character.lantern_ranger"
}
```

`availableHeroIds` 设置真正的选关名单。`PracticeStage.allowedCharacterIds` 可保留同一 ID 让元数据一致，但当前 C# 流程不靠该字段限制选人。这个关卡只有一个角色时，`maxHeroCount = 1` 即可。

若要加入正式大关卡，可使用 API 1.7.0 起的 `AddCharacterToLevel`，查[注册参考](../reference/entry.md)；不要把小关卡的牌池 ID 当成大关卡 ID。

## 3. 按动作验证

构建安装，完整重启。选择林径练习，在选角页检查名字和基础属性；进场后检查初始招式是银辉箭，次数为 2，将它指向暴露的守卫测试伤害和使用次数。

银辉箭单次伤害读取当前攻击的 2 倍，真实敌人伤害仍走统一结算。要测试“灯辉视野”额外攻击目标，需再摆第二名暴露敌人；单敌人牌场不能证明随机额外目标机制。

## 4. 核对当前开局限制

`StartingMoveTypes` 当前只把第一项加载为初始招式；后续项不会自动放入普通招式槽。`StartingTreasureTypes` 会登记、校验，但选角不发放。需要明确宝物奖励时使用[领取事件](treasure.md)。

片段包含 `CharacterTreasurePoolTags.HealingLifeBuild`，让首次创建的角色在尚未加入自有宝物时也有合法候选池。另一个 Tag `treasure_pool.your_package.lantern` 与[角色宝物片段](../../../templates/zh-CN/03-character-treasures.cs.txt)匹配，按任意交集进入候选。以后若移除生命构筑 Tag，先为剩余自定义 Tag 注册可入池宝物；空池会报告 `AW_CHARACTER_EMPTY_TREASURE_POOL`。改自定义 Tag 时两边一起改；权重用 `GetPoolWeight` 或角色 `SetWeight`。

## 验收与下一步

- 三个内容都注册，选择名单与 Stage 允许名单一致。
- 名字和属性出现；初始招式能命中并消耗次数。
- 双目标场景才验证额外目标；没有把未发放的开局声明称为可用功能。

继续[敌人与实例状态](enemy.md)。接口默认值与状态边界见[角色与敌人参考](../reference/actors.md)。


相关扩展：[自定义页面入口](custom-ui.md)。


## 让同一份源码随语言变化

本课片段已使用 ModText 读取角色、特性、招式和职业显示文字。将[中文示例键](../../../templates/zh-CN/localization.json)和[英文示例键](../../../templates/en/localization.json)的 entries 合并到你已有的两份目录，不覆盖生成条目。规则和 ID 保持同一份源码；切语言后新开测试局核对名称、说明和职业，详见[素材与文本课](assets-and-text.md)。
