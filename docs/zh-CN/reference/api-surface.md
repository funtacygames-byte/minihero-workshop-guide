# 公开 API 声明索引

[English](../../en/reference/api-surface.md) · [目录](../README.md)

教程修订 2 · API 1.8.0 · 2026-10-13

从当前授权工程只读提取的选定公开声明，不包含方法实现；它不是完整 SDK 文档。继承成员在定义它的基类下查询。默认值与调用语义须同时查对应[规则参考](../README.md#reference)。维护者可使用[提取工具](../../../tools/extract_api.py)重新生成。

| Type | Type | Type |
| --- | --- | --- |
| [AdventureContent](#adventurecontent) | [AdventureDifficultyDefinition](#adventuredifficultydefinition) | [AdventureStepDefinition](#adventurestepdefinition) |
| [AfterHealingEvent](#afterhealingevent) | [AfterMoveResolvedEvent](#aftermoveresolvedevent) | [BeforeHealingEvent](#beforehealingevent) |
| [BeforeItemEffectEvent](#beforeitemeffectevent) | [BeforeMoveResolvedEvent](#beforemoveresolvedevent) | [CharacterContent](#charactercontent) |
| [ColumnClearedEvent](#columnclearedevent) | [ContentCards](#contentcards) | [EnemyContent](#enemycontent) |
| [EnemyKilledEvent](#enemykilledevent) | [EnemyTraitContent](#enemytraitcontent) | [EnemyTraitDamageEvent](#enemytraitdamageevent) |
| [EnemyTraitEvent](#enemytraitevent) | [EventContent](#eventcontent) | [GameContentModule](#gamecontentmodule) |
| [GameRuleEvent](#gameruleevent) | [IModPresentationContent](#imodpresentationcontent) | [IModRegistrar](#imodregistrar) |
| [IMultipleVariantEffect](#imultiplevarianteffect) | [ITreasureRuntime](#itreasureruntime) | [ItemContent](#itemcontent) |
| [ItemUsedEvent](#itemusedevent) | [MiniHeroMod](#miniheromod) | [MiniHeroModApi](#miniheromodapi) |
| [MiniHeroModAttribute](#miniheromodattribute) | [ModAssets](#modassets) | [ModConfig](#modconfig) |
| [ModConfigDefinition](#modconfigdefinition) | [ModMusicTheme](#modmusictheme) | [ModPresentation](#modpresentation) |
| [ModRegistrarExtensions](#modregistrarextensions) | [ModText](#modtext) | [MoveContent](#movecontent) |
| [StageContent](#stagecontent) | [StageDefinition](#stagedefinition) | [StageEnteredEvent](#stageenteredevent) |
| [TraitContent](#traitcontent) | [TreasureContent](#treasurecontent) | [TreasurePoolDefinition](#treasurepooldefinition) |
| [TreasureStatsEvent](#treasurestatsevent) |  |  |

## AdventureContent

```csharp
public abstract class AdventureContent : GameContentModule
{
    public abstract string Description { get; }
    public abstract string PreviewImageId { get; }
    public abstract string SourceStageId { get; }
    public virtual bool IncludeInSelection { get; }
    public virtual int IntermissionInterval { get; }
    public virtual IReadOnlyList<string> AdventureRuleIds { get; }
    public virtual AdventureLoopSettings LoopSettings { get; }
    public virtual AdventureSeedSettings SeedSettings { get; }
    public abstract IReadOnlyList<AdventureStepDefinition> Steps { get; }
    public abstract IReadOnlyList<AdventureDifficultyDefinition> Difficulties { get; }
    public virtual AdventureDefinition CreateDefinition();
}
```

## AdventureDifficultyDefinition

```csharp
public sealed class AdventureDifficultyDefinition
{
    public int difficulty = 1;
    public string description = string.Empty;
    public int maxHeroCount = 4;
    public List<string> availableHeroIds = new List<string>();
    public List<string> adventureRuleIds = new List<string>();
    public int attackEnhance;
    public int defenseEnhance;
    public int healthEnhance;
    public int rewardEnhance;
    public float crystalRewardMultiplier = 1f;
    public float attackGrowthPerMajorStage;
    public float defenseGrowthPerMajorStage;
    public float healthGrowthPerMajorStage;
    public int[] ruleAttackBySection;
    public int[] ruleDefenseBySection;
    public int[] ruleHealthBySection;
    public AdventureDifficultyDefinition Clone();
}
```

## AdventureStepDefinition

```csharp
public sealed class AdventureStepDefinition
{
    public string id = string.Empty;
    public string displayName = string.Empty;
    public string description = string.Empty;
    public string sourceStageId = string.Empty;
    public int columnCount = GameRules.ColumnCount;
    public int roundCount = 6;
    public int cardsPerRound = GameRules.CardsPerStage;
    public bool boss;
    public IntermissionMode intermissionMode = IntermissionMode.Default;
    public string generationProfile = string.Empty;
    public AdventureStepDefinition Clone();
}
```

## AfterHealingEvent

```csharp
public sealed class AfterHealingEvent : GameRuleEvent
{
    public int requested;
    public int actual;
    public int overflow;
    public bool potion;
}
```

## AfterMoveResolvedEvent

```csharp
public sealed class AfterMoveResolvedEvent : GameRuleEvent
{
    public MoveState move;
    public bool automatic;
    public IReadOnlyList<MoveHitResult> hits = Array.Empty<MoveHitResult>();
    public int targetCount;
    public int damagedTargetCount;
    public int totalDamage;
    public int defeatedEnemies;
    public int shield;
}
```

## BeforeHealingEvent

```csharp
public sealed class BeforeHealingEvent : GameRuleEvent
{
    public int baseAmount;
    public bool potion;
    public int bonusFlat;
    public int bonusPercent;
}
```

## BeforeItemEffectEvent

```csharp
public sealed class BeforeItemEffectEvent : GameRuleEvent
{
    public CardState item;
    public int bonusPercent;
    public int extraUseCount;
}
```

## BeforeMoveResolvedEvent

```csharp
public sealed class BeforeMoveResolvedEvent : GameRuleEvent
{
    public MoveState move;
    public bool automatic;
    public int targetCount = 1;
    public int damagePercent;
    public int damageFlat;
    public bool preferHighestHp;
    public int additionalTriggerCount;
}
```

## CharacterContent

```csharp
public abstract class CharacterContent : GameContentModule
{
    public abstract string Role { get; }
    public abstract string School { get; }
    public virtual string Description { get; }
    public abstract PlayerState BaseStats { get; }
    public virtual bool IncludeInDefaultRoster { get; }
    public virtual IReadOnlyList<Type> TraitTypes { get; }
    public virtual IReadOnlyList<Type> StartingTreasureTypes { get; }
    public virtual IReadOnlyList<Type> StartingMoveTypes { get; }
    public virtual IReadOnlyList<string> TreasurePoolTags { get; }
    public virtual TreasurePoolDefinition TreasurePool { get; }
    public virtual CharacterDefinition CreateDefinition(GameContentRegistry registry);
}
```

## ColumnClearedEvent

```csharp
public sealed class ColumnClearedEvent : GameRuleEvent
{
    public int columnIndex;
    public int automaticInitialMoveTriggers;
}
```

## ContentCards

```csharp
public static class ContentCards
{
    public static CardState Card(string id, CardType type, string name, string description);
    public static CardState Enemy( string id, string name, string description, int attack, int defense, int hp, int reward, string icon, int tier, bool boss = false, int weight = 10, string enemyTraitId = "");
    public static CardState Medicine(string id, string name, string description, int heal, int sellGold);
    public static CardState Elixir(string id, string name, string description, StatEffect effect, int sellGold);
    public static CardState Technique(string id, string name, string description, int dodge, int sellGold);
    public static CardState Move<TMove>(GameContentRegistry registry, string id) where TMove : MoveContent;
    public static CardState Chest(string id, TreasureRank rewardQuality = TreasureRank.Common);
    public static CardState Meditation( string id, TreasureRank rewardQuality = TreasureRank.Common, int rewardCount = 3);
    public static CardState Encounter( string id, string name, string description, PendingChoiceKind action, StatEffect effect = null, TreasureRank rewardQuality = TreasureRank.Common, int rewardCount = 0);
    public static CardState Treasure<TTreasure>(GameContentRegistry registry, string id) where TTreasure : TreasureContent;
}
```

## EnemyContent

```csharp
public abstract class EnemyContent : GameContentModule
{
    public abstract string Description { get; }
    public abstract int Attack { get; }
    public abstract int Defense { get; }
    public abstract int MaxHp { get; }
    public abstract int RewardGold { get; }
    public virtual string Icon { get; }
    public virtual string EnemyTraitId { get; }
    public virtual CardState CreateCard(string instanceId = null);
}
```

## EnemyKilledEvent

```csharp
public sealed class EnemyKilledEvent : GameRuleEvent
{
    public CardState enemy;
    public int columnIndex = -1;
    public bool allEnemiesDefeated;
    public int restoreMoveUses;
    public int automaticInitialMoveTriggers;
    public int adjacentDamage;
    public string adjacentDamageSourceId = string.Empty;
    public int randomDefenseReduction;
    public int randomDefenseReductionTurns;
    public string randomDefenseReductionSourceId = string.Empty;
}
```

## EnemyTraitContent

```csharp
public abstract class EnemyTraitContent : GameContentModule
{
    public abstract string Description { get; }
    public virtual string Icon { get; }
    public virtual int Countdown { get; }
    public virtual int GetCountdown(CardState owner);
    public virtual bool CountdownAfterOthers { get; }
    public virtual string GetRuntimeName(CardState owner);
    public virtual string GetRuntimeDescription(CardState owner);
    public virtual string GetRuntimeStatusDescriptionLocalizationKey(CardState owner);
    public virtual void OnStaticStats(EnemyTraitEvent gameEvent);
    public virtual void OnPlayerAttack(EnemyTraitPlayerAttackEvent gameEvent);
    public virtual void OnBeforeDamaged(EnemyTraitDamageEvent gameEvent);
    public virtual void OnAfterDamaged(EnemyTraitEvent gameEvent);
    public virtual void OnRoundStart(EnemyTraitEvent gameEvent);
    public virtual void OnRoundEnd(EnemyTraitEvent gameEvent);
    public virtual void OnDeath(EnemyTraitEvent gameEvent);
    public virtual void OnEnemyDied(EnemyTraitObservedDeathEvent gameEvent);
    public virtual void OnCountdown(EnemyTraitEvent gameEvent);
    public virtual bool GrantsKillCredit(CardState owner);
    public virtual string GetRuntimeStatus(CardState owner);
    public virtual bool IsRuntimeStatusVisible(CardState owner);
    public virtual bool TryGetRuntimeStatusCount(CardState owner, out int count);
}
```

## EnemyTraitDamageEvent

```csharp
public sealed class EnemyTraitDamageEvent : EnemyTraitEvent
{
    public int IncomingDamage { get; }
    public int FinalDamage { get; private set; }
    public bool Prevented { get; private set; }
    public void AddDamage(int amount);
    public void ReduceDamage(int amount);
    public void PreventDamage();
}
```

## EnemyTraitEvent

```csharp
public class EnemyTraitEvent
{
    public GameState State { get; }
    public CardState Owner { get; }
    public int ColumnIndex { get; }
    public EnemyTraitRuntime Runtime { get; }
    public int DamageDealt { get; }
}
```

## EventContent

```csharp
public abstract class EventContent : GameContentModule
{
    public abstract string Description { get; }
    public abstract string ImageName { get; }
    public virtual PendingChoiceKind Action { get; }
    public virtual TreasureRank RewardQuality { get; }
    public virtual int RewardCount { get; }
    public virtual StatEffect Effect { get; }
    public virtual IReadOnlyList<StatEffect> Choices { get; }
    public virtual CardState CreateCard(string instanceId = null);
    public virtual GameActionResult Execute(CardExecutionContext context);
}
```

## GameContentModule

```csharp
public abstract class GameContentModule : IGameContent, IAppearanceContent
{
    public string Id { get; }
    public abstract string Name { get; }
    public virtual int Order { get; }
    public virtual ContentCombatVfxProfile CombatVfxProfile { get; }
    public virtual TreasureRank AppearanceQuality { get; }
    public virtual IReadOnlyList<string> RequiredAppearanceTags { get; }
    public virtual bool CanAppear(AppearanceContext context);
    public virtual float GetWeight(AppearanceContext context);
    public virtual void OnBeforeAttack(BeforeAttackEvent gameEvent);
    public virtual void OnPlayerStatusProjection(PlayerStatusProjectionEvent gameEvent);
    public virtual void OnStageEntered(StageEnteredEvent gameEvent);
    public virtual void OnStageLeaving(StageLeavingEvent gameEvent);
    public virtual void OnRecycleValue(RecycleValueEvent gameEvent);
    public virtual void OnMoveUsed(MoveUsedEvent gameEvent);
    public virtual void OnMoveStarted(MoveStartedEvent gameEvent);
    public virtual void OnMoveCapacity(MoveCapacityEvent gameEvent);
    public virtual void OnBeforeMoveResolved(BeforeMoveResolvedEvent gameEvent);
    public virtual void OnAfterMoveResolved(AfterMoveResolvedEvent gameEvent);
    public virtual void OnTreasureStats(TreasureStatsEvent gameEvent);
    public virtual void OnBeforeHealing(BeforeHealingEvent gameEvent);
    public virtual void OnBeforePlayerDamage(BeforePlayerDamageEvent gameEvent);
    public virtual void OnPlayerDamageResolved(PlayerDamageResolvedEvent gameEvent);
    public virtual void OnPlayerDamageTaken(PlayerDamageTakenEvent gameEvent);
    public virtual void OnBeforeReflectionDamage(BeforeReflectionDamageEvent gameEvent);
    public virtual void OnAfterReflectionDamage(AfterReflectionDamageEvent gameEvent);
    public virtual void OnAfterHealing(AfterHealingEvent gameEvent);
    public virtual void OnDamageDealt(DamageDealtEvent gameEvent);
    public virtual void OnBeforeEnemyDamage(BeforeEnemyDamageEvent gameEvent);
    public virtual void OnEnemyIntent(EnemyIntentEvent gameEvent);
    public virtual void OnDodgeGained(DodgeGainedEvent gameEvent);
    public virtual void OnDodgeTriggered(DodgeTriggeredEvent gameEvent);
    public virtual void OnBeforeEnemyMarked(BeforeEnemyMarkedEvent gameEvent);
    public virtual void OnEnemyMarked(EnemyMarkedEvent gameEvent);
    public virtual void OnBeforeItemEffect(BeforeItemEffectEvent gameEvent);
    public virtual void OnBeforeShieldGained(BeforeShieldGainedEvent gameEvent);
    public virtual void OnAfterShieldGained(AfterShieldGainedEvent gameEvent);
    public virtual void OnTurnStarted(TurnStartedEvent gameEvent);
    public virtual void OnTurnEnded(TurnEndedEvent gameEvent);
    public virtual void OnPlayerHpDamaged(PlayerHpDamagedEvent gameEvent);
    public virtual void OnEnemyKilled(EnemyKilledEvent gameEvent);
    public virtual void OnEnemyDied(EnemyDiedEvent gameEvent);
    public virtual void OnItemUsed(ItemUsedEvent gameEvent);
    public virtual void OnTreasureUsed(TreasureUsedEvent gameEvent);
    public virtual void OnNormalAttackResolved(NormalAttackResolvedEvent gameEvent);
    public virtual void OnBeforeNormalAttackTargets(BeforeNormalAttackTargetsEvent gameEvent);
    public virtual void OnNormalAttackStarted(NormalAttackStartedEvent gameEvent);
    public virtual void OnSceneReset();
    public virtual void OnColumnCleared(ColumnClearedEvent gameEvent);
}
```

## GameRuleEvent

```csharp
public abstract class GameRuleEvent
{
    public GameState State { get; }
    public IGameContent Source { get; }
    public int SourceLevel { get; }
    public bool IsPreview { get; }
    public TreasureState TreasureState { get; }
    public MoveState MoveState { get; }
    public CardState EnemyState { get; }
    public ITreasureRuntime Runtime { get; }
    public int Percent(int amount, int percent);
}
```

## IModPresentationContent

```csharp
public interface IModPresentationContent
{
    ModPresentation Presentation { get; }
}
```

## IModRegistrar

```csharp
public interface IModRegistrar
{
    string PackageId { get; }
    string PackageRoot { get; }
    void AddContent(IGameContent content);
    void AddCharacterToLevel(string levelId, string characterId, int difficulty = 0);
    void AddMusicTheme(ModMusicTheme theme);
    void AddConfig(ModConfigDefinition definition);
    void AddStartScreen(ModStartScreenDefinition definition);
    void AddScreen(ModScreenDefinition definition);
}
```

## IMultipleVariantEffect

```csharp
public interface IMultipleVariantEffect
{
    IEnumerable<TreasureContent> GetVariants();
}
```

## ITreasureRuntime

```csharp
public interface ITreasureRuntime
{
    int EmptyColumnCount { get; }
    int Percent(int amount, int percent);
    bool RollPercent(int percent);
    int Heal(int amount, bool potion = false);
    int DamagePlayer(int amount);
    int AddShield(int amount);
    int GainDodge(int amount);
    void AddPermanentAttack(int amount);
    void AddPermanentDefense(int amount);
    void AddPermanentMaxHp(int amount);
    void AddPermanentWisdom(int amount);
    void DamageRandomEnemy(int amount, string sourceContentId = "");
    void DamageRandomEnemies(int count, int amount, string sourceContentId = "");
    void DamageLowestEnemy(int amount);
    void DamageHighestEnemy(int amount, string sourceContentId = "");
    void DamageAllEnemies(int amount, string sourceContentId = "");
    void ReduceHighestEnemyAttack(int amount);
    void ReduceRandomEnemyAttack(int amount, int durationTurns, string sourceContentId = "");
    void ReduceRandomEnemyDefense(int amount);
    void ReduceRandomEnemyDefenses(int count, int amount);
    void IncreaseRandomEnemyDamageTaken(int amount, int durationTurns, string sourceContentId = "");
    void PlayEnemyWeakening(CardState enemy, string sourceContentId = "");
    void MarkRandomEnemies(int count, string sourceContentId = "");
    void MarkEnemy(CardState enemy, string sourceContentId = "");
    void MarkRandomEnemyExcept(CardState excludedEnemy, string sourceContentId = "");
    void SpawnRecoveryPotion(int preferredColumnIndex = -1);
}
```

## ItemContent

```csharp
public abstract class ItemContent : GameContentModule, IUseCardContent
{
    public abstract string Description { get; }
    public abstract CardType CardType { get; }
    public virtual int Heal { get; }
    public virtual int DodgeCharges { get; }
    public virtual int SellGold { get; }
    public virtual StatEffect Effect { get; }
    public virtual string Icon { get; }
    public virtual CardState CreateCard(string instanceId = null);
    public virtual CardUseResult Execute(CardState card, CardUseContext context);
}
```

## ItemUsedEvent

```csharp
public sealed class ItemUsedEvent : GameRuleEvent
{
    public CardState item;
    public bool potion;
    public int restoreMoveUses;
}
```

## MiniHeroMod

```csharp
public abstract class MiniHeroMod
{
    public abstract void Load(IModRegistrar registrar);
}
```

## MiniHeroModApi

```csharp
public static class MiniHeroModApi
{
    public const string Version = "1.8.0";
    public const string MinimumCompatibleVersion = "1.0.0";
}
```

## MiniHeroModAttribute

```csharp
public sealed class MiniHeroModAttribute : Attribute
{
    public MiniHeroModAttribute(string packageId);
    public string PackageId { get; }
}
```

## ModAssets

```csharp
public static class ModAssets
{
    public static ModPresentation Icon(string path);
    public static ModPresentation Character(string portrait, string avatar = "");
    public static ModPresentation Enemy(string battleArt, string icon = "", string intentIcon = "");
    public static ModPresentation Stage(string background, string mapThumbnail = "", string arrivalArt = "");
    public static ModPresentation Create(params (ModPresentationSlot slot, string path)[] assets);
}
```

## ModConfig

```csharp
public static class ModConfig
{
    public static string Get(string packageId, string id, string fallback = "");
    public static bool GetBool(string packageId, string id, bool fallback = false);
    public static int GetInt(string packageId, string id, int fallback = 0, int minimum = int.MinValue, int maximum = int.MaxValue);
    public static double GetDecimal(string packageId, string id, double fallback = 0d, double minimum = double.MinValue, double maximum = double.MaxValue);
    public static string GetChoice(string packageId, string id, string fallback, IReadOnlyList<string> choices);
    public static void ConfigureResolver(Func<string, string, string, string> value);
}
```

## ModConfigDefinition

```csharp
public sealed class ModConfigDefinition
{
    public ModConfigDefinition(string id, string displayName, ModConfigValueKind kind, string defaultValue, string category = "常规", string description = "", double minimum = 0d, double maximum = 0d, bool requiresReload = false, IReadOnlyList<string> choices = null) : this(id, displayName, kind, defaultValue, category, description, minimum, maximum, requiresReload, choices, null);
    public ModConfigDefinition(string id, string displayName, ModConfigValueKind kind, string defaultValue, string category, string description, double minimum, double maximum, bool requiresReload, IReadOnlyList<string> choices, IReadOnlyList<string> choiceDisplayNames);
    public string Id { get; }
    public string DisplayName { get; }
    public ModConfigValueKind Kind { get; }
    public string DefaultValue { get; }
    public string Category { get; }
    public string Description { get; }
    public double Minimum { get; }
    public double Maximum { get; }
    public bool RequiresReload { get; }
    public IReadOnlyList<string> Choices { get; }
    public IReadOnlyList<string> ChoiceDisplayNames { get; }
    public string GetChoiceDisplayName(string value);
}
```

## ModMusicTheme

```csharp
public sealed class ModMusicTheme
{
    public ModMusicTheme(string id, IReadOnlyDictionary<ModMusicCue, string> tracks);
    public string Id { get; }
    public IReadOnlyDictionary<ModMusicCue, string> Tracks { get; }
}
```

## ModPresentation

```csharp
public sealed class ModPresentation
{
    public ModPresentation(IReadOnlyDictionary<ModPresentationSlot, string> assets);
    public IReadOnlyDictionary<ModPresentationSlot, string> Assets { get; }
    public string GetAssetPath(ModPresentationSlot slot);
}
```

## ModRegistrarExtensions

```csharp
public static class ModRegistrarExtensions
{
    public static void AddContents(this IModRegistrar registrar, params IGameContent[] contents);
}
```

## ModText

```csharp
public static class ModText
{
    public static string Get(string packageId, string key, string fallback = "");
    public static string Format(string packageId, string key, string fallback, params object[] arguments);
    public static void ConfigureResolver(Func<string, string, string, string> value);
}
```

## MoveContent

```csharp
public abstract class MoveContent : GameContentModule, IUseCardContent
{
    public abstract string Description { get; }
    public virtual MoveTargetKind TargetKind { get; }
    public virtual MoveActivationKind ActivationKind { get; }
    public virtual int MaxUses { get; }
    public virtual int AttackMultiplier { get; }
    public virtual int Heal { get; }
    public virtual int DodgeCharges { get; }
    public virtual int SellGold { get; }
    public virtual string Icon { get; }
    public virtual string AnimationSlot { get; }
    public virtual string AudioSlot { get; }
    public virtual string VfxSlot { get; }
    public virtual string CameraSlot { get; }
    public virtual CardState CreateCard(string instanceId = null);
    public virtual MoveState CreateState();
    public override void OnMoveUsed(MoveUsedEvent gameEvent);
    public virtual CardUseResult Execute(CardState card, CardUseContext context);
}
```

## StageContent

```csharp
public abstract class StageContent : GameContentModule
{
    public abstract string Subtitle { get; }
    public virtual bool IncludeInDefaultCampaign { get; }
    public abstract StageDefinition CreateDefinition(GameContentRegistry registry);
}
```

## StageDefinition

```csharp
public sealed class StageDefinition
{
    public string id = string.Empty;
    public string name = string.Empty;
    public string subtitle = string.Empty;
    public string adventureId = string.Empty;
    public string mapId = string.Empty;
    public int mapIndex;
    public int levelIndex;
    public int smallStageIndex;
    public int roundIndex;
    public bool boss;
    public bool isTutorial;
    public bool countsAsClearedStage = true;
    public bool nextRoundIsBoss;
    public int intermissionInterval = 2;
    public IntermissionMode intermissionMode = IntermissionMode.Default;
    public int columnCount = GameRules.ColumnCount;
    public int difficulty = 1;
    public string difficultyDescription = string.Empty;
    public List<string> adventureRuleIds = new List<string>();
    public bool adventureItemPoolConfigured;
    public List<string> adventureItemPoolIds = new List<string>();
    public AdventureItemSegmentPlan adventureItemSegmentPlan;
    public bool adventureItemSegmentsConfigured;
    public int adventureItemSegmentIndex;
    public float crystalRewardMultiplier = 1f;
    public List<CardState> appearancePool = new List<CardState>();
    public int generatedCardCount;
    public string generationProfile = string.Empty;
    public List<CardState> cards = new List<CardState>();
    public List<CardColumnState> fixedColumns = new List<CardColumnState>();
    public string background = string.Empty;
    public string music = string.Empty;
    public StarlitFinalChallengeSettings starlitFinalSettings;
    public string configuredRunSeed = string.Empty;
    public AdventureLoopSettings adventureLoop;
    public int adventureLoopStartStageIndex;
    public int adventureLoopTemplateStageCount;
    public int adventureContinuationIndex;
    public bool adventureHasFinalSettings;
    public bool finalSettingsPresenceRecorded;
    public List<string> allowedCharacterIds = new List<string>();
    public List<StageGraphNodeDefinition> graphNodes = new List<StageGraphNodeDefinition>();
    public List<StageGraphEdgeDefinition> graphEdges = new List<StageGraphEdgeDefinition>();
    public List<string> victoryConditions = new List<string>();
    public List<string> failureConditions = new List<string>();
    public StageDefinition Clone();
}
```

## StageEnteredEvent

```csharp
public sealed class StageEnteredEvent : GameRuleEvent
{
    public int stageIndex;
    public string stageId = string.Empty;
    public int healing;
    public int dodgeCharges;
    public int gold;
    public int automaticInitialMoveTriggers;
}
```

## TraitContent

```csharp
public abstract class TraitContent : GameContentModule
{
    public abstract string Description { get; }
}
```

## TreasureContent

```csharp
public abstract class TreasureContent : GameContentModule
{
    public TreasureRank Quality { get; }
    public int EffectValue { get; }
    public override string Name { get; }
    public virtual TreasureRank Rank { get; }
    public override TreasureRank AppearanceQuality { get; }
    public virtual int BaseValue { get; }
    public virtual int SellGold { get; }
    public virtual int MaxLevel { get; }
    public virtual string Icon { get; }
    public virtual bool Exclusive { get; }
    public virtual bool IncludeInDefaultChestPool { get; }
    public virtual IReadOnlyList<string> PoolTags { get; }
    public virtual IReadOnlyList<string> CategoryTags { get; }
    public virtual IReadOnlyList<string> FunctionTags { get; }
    public virtual float GetPoolWeight(string poolTag);
    public virtual TreasureActivationKind ActivationKind { get; }
    public virtual int MaxUses { get; }
    public abstract string Describe(int level);
    public virtual GameActionResult Execute(TreasureState treasure, TreasureActivationContext context);
    public TreasureDefinition CreateDefinition();
    public virtual TreasureState CreateState(int level = 1);
    public TreasureContent CloneRuntime();
    public virtual IEnumerable<TreasureState> GetStateVariants();
}
```

## TreasurePoolDefinition

```csharp
public sealed class TreasurePoolDefinition
{
    public List<string> includeTags = new List<string>();
    public List<string> includeTreasureIds = new List<string>();
    public List<string> excludeTreasureIds = new List<string>();
    public List<TreasurePoolWeightOverride> weightOverrides = new List<TreasurePoolWeightOverride>();
    public static TreasurePoolDefinition Create();
    public static TreasurePoolDefinition FromBuiltInCharacter(string characterId);
    public TreasurePoolDefinition IncludeTag(string tag);
    public TreasurePoolDefinition IncludeTags(IEnumerable<string> tags);
    public TreasurePoolDefinition Include(params string[] treasureIds);
    public TreasurePoolDefinition IncludeFeature(params string[] treasureIds);
    public TreasurePoolDefinition Exclude(params string[] treasureIds);
    public TreasurePoolDefinition SetWeight(string treasureId, float weight);
    public bool Includes(TreasureContent treasure);
    public float ResolvePoolWeight(TreasureContent treasure);
    public bool TryGetWeightOverride(string treasureId, out float weight);
    public TreasurePoolDefinition Clone();
}
```

## TreasureStatsEvent

```csharp
public sealed class TreasureStatsEvent : GameRuleEvent
{
    public int baseAttack;
    public int baseDefense;
    public int baseMaxHp;
    public int baseWisdom;
    public int attackFlat;
    public int defenseFlat;
    public int maxHpFlat;
    public int wisdomFlat;
    public int attackPercent;
    public int defensePercent;
    public int maxHpPercent;
}
```
