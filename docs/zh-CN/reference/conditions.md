# 有限条件表达式与位置身份

[English](../../en/reference/conditions.md) · [Index](../README.md)

教程修订 6 · Mod API 1.10.0 · 2026-10-17


条件不是 C#、JavaScript 或任意脚本。`DeclarativeConditionEvaluator.Evaluate(expression, state)` 返回条件真假；遇到无法识别的已求值子句时返回 false。TryEvaluate 返回是否成功求值，out result 才是条件真假。空表达式通过。

求值会短路：前面的子句为 false 时，不继续解析后面的子句，因此 TryEvaluate 不是整条表达式的完整语法校验器。当前实现还会跳过 `&&` 分隔产生的空项；不要使用只有连接符、开头或结尾连接符的写法。作者应逐个验证非空子句，再测试完整条件在实际状态下的结果。

| 写法 | 意义 |
| --- | --- |
| `gold>=5` 或 `player.gold>=5` | 属性与有限数字常量比较 |
| `hp>3 && gold>=2` | 全部子句必须成立 |
| `!has:local.alice.lantern-trail.treasure.starter_relic` | 不持有／不出现该内容 |
| `tag:treasure_pool.local.alice.lantern` | 当前 active tags 包含区分大小写的标签 |
| `reach:grove_gate` | 已访问图节点 ID |

数值键仅 hp、maxhp、attack、defense、wisdom、gold、dodge、turn、stageindex、defeatedenemies、stagescleared；七种玩家资源支持 player. 前缀。不支持 shield、loopIndex 等猜测字段。运算符为 >=、<=、==、!=、>、<；右侧是有限数字常量，不能是另一个属性或算式。不支持 OR `||`、括号、函数或乘除。需要复杂规则时在具体 C# 内容内实现，别拼一个看似合理但永远 false 的表达式。

`tag:` 读取 appearanceTags、角色池 Tag 与角色 ID；不遍历宝物 CategoryTags。`has:` 检查当前场景／角色、装备宝物、招式和所有列内牌，包括覆盖的牌；不是“只查明牌”，也不意味着检查备用宝物。`reach:` 读取已访问节点列表。值按精确稳定 ID 使用，不用显示名称。

检查时机因入口不同：新卡牌选择在显示和确认检查条件及代价；旧富事件打开时按条件筛出分支，确认时重查条件与代价，打开后的列表不自动重筛；StageGraph 在选择路径时检查边条件。不要用某一路径的时机推断另一路径。

列下标从 0 开始，玩家“第一列”对应 0。固定列 cards 从底到顶，最后一张暴露。sourceCardId 是卡实例 id；resolverContentId/rewardContentId 是注册内容 id；冒险选择 ID、素材 Stage ID、步骤 ID、展开场景 ID 也不同。后续场景跳转需要当前冒险列表中的展开 ID，不是注册素材 ID。

调试条件时记录真实输入状态和预期真假，先用 `gold>=2` 等单句，再组合。为每个付费或受限分支保留可达后备路径，测试资源刚好够、差 1 和存档恢复后不够。
