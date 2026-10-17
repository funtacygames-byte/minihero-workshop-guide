# Public API declaration index

[简体中文](../../zh-CN/reference/api-surface.md) · [Index](../README.md)

Guide revision 7 · API 1.11.0 · 2026-10-17

Selected public declarations extracted read-only from the authorized source, without implementations. This is not the entire SDK. Look up inherited members under their defining base and use the [rule references](../README.md#reference) for defaults and semantics. Maintainers can regenerate it with the [extractor](../../../tools/extract_api.py).

| Type | Type | Type |
| --- | --- | --- |
| [AdventureContent](#adventurecontent) | [AdventureContinuationContext](#adventurecontinuationcontext) | [AdventureDefinition](#adventuredefinition) |
| [AdventureDifficultyDefinition](#adventuredifficultydefinition) | [AdventureItemSegmentSettings](#adventureitemsegmentsettings) | [AdventureItemSegmentUnit](#adventureitemsegmentunit) |
| [AdventureLoopSettings](#adventureloopsettings) | [AdventureRuleContent](#adventurerulecontent) | [AdventureSeedMode](#adventureseedmode) |
| [AdventureSeedSettings](#adventureseedsettings) | [AdventureStepDefinition](#adventurestepdefinition) | [AfterHealingEvent](#afterhealingevent) |
| [AfterMoveResolvedEvent](#aftermoveresolvedevent) | [BeforeHealingEvent](#beforehealingevent) | [BeforeItemEffectEvent](#beforeitemeffectevent) |
| [BeforeMoveResolvedEvent](#beforemoveresolvedevent) | [BeforePlayerDamageEvent](#beforeplayerdamageevent) | [CardChoiceContext](#cardchoicecontext) |
| [CardChoiceEventContent](#cardchoiceeventcontent) | [CardChoiceOption](#cardchoiceoption) | [CardChoiceRequest](#cardchoicerequest) |
| [CardExecutionContext](#cardexecutioncontext) | [CharacterContent](#charactercontent) | [ColumnClearedEvent](#columnclearedevent) |
| [ContentCards](#contentcards) | [DeclarativeConditionEvaluator](#declarativeconditionevaluator) | [EnemyContent](#enemycontent) |
| [EnemyKilledEvent](#enemykilledevent) | [EnemyTraitContent](#enemytraitcontent) | [EnemyTraitDamageEvent](#enemytraitdamageevent) |
| [EnemyTraitEvent](#enemytraitevent) | [EventContent](#eventcontent) | [GameActionResult](#gameactionresult) |
| [GameContentModule](#gamecontentmodule) | [GameRuleEvent](#gameruleevent) | [IAdventureContinuationContent](#iadventurecontinuationcontent) |
| [ICardChoiceResolver](#icardchoiceresolver) | [IModLevelDifficultyRegistrar](#imodleveldifficultyregistrar) | [IModPresentationContent](#imodpresentationcontent) |
| [IModRegistrar](#imodregistrar) | [IModUiContext](#imoduicontext) | [IMultipleVariantEffect](#imultiplevarianteffect) |
| [ITreasureRuntime](#itreasureruntime) | [ItemContent](#itemcontent) | [ItemUsedEvent](#itemusedevent) |
| [MiniHeroMod](#miniheromod) | [MiniHeroModApi](#miniheromodapi) | [MiniHeroModAttribute](#miniheromodattribute) |
| [ModAssets](#modassets) | [ModConfig](#modconfig) | [ModConfigDefinition](#modconfigdefinition) |
| [ModConfigValueKind](#modconfigvaluekind) | [ModLevelDefinition](#modleveldefinition) | [ModLevelDifficultyDefinition](#modleveldifficultydefinition) |
| [ModLevelDifficultyExtensions](#modleveldifficultyextensions) | [ModLevelDifficultyValidation](#modleveldifficultyvalidation) | [ModMusicCue](#modmusiccue) |
| [ModMusicTheme](#modmusictheme) | [ModPersistentData](#modpersistentdata) | [ModPresentation](#modpresentation) |
| [ModPresentationSlot](#modpresentationslot) | [ModProgress](#modprogress) | [ModRegistrarExtensions](#modregistrarextensions) |
| [ModScreenController](#modscreencontroller) | [ModScreenDefinition](#modscreendefinition) | [ModScreenPlacement](#modscreenplacement) |
| [ModStartScreenAction](#modstartscreenaction) | [ModStartScreenButton](#modstartscreenbutton) | [ModStartScreenDefinition](#modstartscreendefinition) |
| [ModText](#modtext) | [ModUi](#modui) | [ModUiAlignment](#moduialignment) |
| [ModUiElement](#moduielement) | [ModUiElementKind](#moduielementkind) | [ModUiImageFit](#moduiimagefit) |
| [ModUiStyle](#moduistyle) | [ModUiThickness](#moduithickness) | [MoveCapacityEvent](#movecapacityevent) |
| [MoveContent](#movecontent) | [NormalAttackResolvedEvent](#normalattackresolvedevent) | [PlayerDamageTakenEvent](#playerdamagetakenevent) |
| [PlayerStatusProjectionEvent](#playerstatusprojectionevent) | [ProfessionContent](#professioncontent) | [ProfessionIds](#professionids) |
| [ProfessionUpgradeConfig](#professionupgradeconfig) | [ProfessionUpgradeCurrency](#professionupgradecurrency) | [ProfessionUpgradeEffectKind](#professionupgradeeffectkind) |
| [ProfessionUpgradeIds](#professionupgradeids) | [RichEventChoiceState](#richeventchoicestate) | [StageContent](#stagecontent) |
| [StageDefinition](#stagedefinition) | [StageEnteredEvent](#stageenteredevent) | [StageGenerationProfiles](#stagegenerationprofiles) |
| [StageGraphEdgeDefinition](#stagegraphedgedefinition) | [StageGraphNodeDefinition](#stagegraphnodedefinition) | [StageGraphNodeKind](#stagegraphnodekind) |
| [StatEffect](#stateffect) | [TraitContent](#traitcontent) | [TreasureContent](#treasurecontent) |
| [TreasurePoolDefinition](#treasurepooldefinition) | [TreasureStatsEvent](#treasurestatsevent) | [TurnEndedEvent](#turnendedevent) |

## AdventureContent

```csharp
public abstract class AdventureContent : GameContentModule
{
    protected AdventureContent();
    protected AdventureContent(string id) : base(id);
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

## AdventureContinuationContext

```csharp
public sealed class AdventureContinuationContext
{
    public GameState State { get; }
    public StageDefinition CompletedStage { get; }
    public IReadOnlyList<StageDefinition> CampaignStages { get; }
    public GameContentRegistry Registry { get; }
    public string Seed { get; }
    public int ContinuationIndex { get; }
}
```

## AdventureDefinition

```csharp
public sealed class AdventureDefinition
{
    public string id = string.Empty;
    public string name = string.Empty;
    public string description = string.Empty;
    public string previewImageId = string.Empty;
    public string sourceStageId = string.Empty;
    public int intermissionInterval = 2;
    public List<string> adventureRuleIds = new List<string>();
    public AdventureLoopSettings loop;
    public AdventureSeedSettings seedSettings;
    public List<AdventureStepDefinition> steps = new List<AdventureStepDefinition>();
    public List<AdventureDifficultyDefinition> difficulties = new List<AdventureDifficultyDefinition>();
    public AdventureDefinition Clone();
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
    public bool adventureItemPoolConfigured;
    public List<string> adventureItemPoolIds = new List<string>();
    public AdventureItemSegmentSettings adventureItemSegments;
    public AdventureDifficultyDefinition Clone();
}
```

## AdventureItemSegmentSettings

```csharp
public sealed class AdventureItemSegmentSettings
{
    public bool enabled;
    public AdventureItemSegmentUnit unit;
    public int segmentLength = 12;
    public int loopUnits;
    public AdventureItemSegmentSettings Clone();
}
```

## AdventureItemSegmentUnit

```csharp
public enum AdventureItemSegmentUnit
{
    [InspectorName("主线战斗场次")] CombatScene,
    [InspectorName("关卡步骤（首领组或区域）")] LevelStep,
}
```

## AdventureLoopSettings

```csharp
public sealed class AdventureLoopSettings
{
    public bool enabled;
    public int startStepIndex;
    public int maximumLoops;
    public int attackIncreasePerLoop;
    public int defenseIncreasePerLoop;
    public int healthIncreasePerLoop;
    public int rewardIncreasePerLoop;
    public AdventureLoopSettings Clone();
    public void Validate(int stepCount);
}
```

## AdventureRuleContent

```csharp
public abstract class AdventureRuleContent : GameContentModule
{
    public abstract string Description { get; }
    public abstract string IconId { get; }
    public virtual IReadOnlyList<int> RuleAttackGrowth { get; }
    public virtual IReadOnlyList<int> RuleDefenseGrowth { get; }
    public virtual IReadOnlyList<int> RuleHealthGrowth { get; }
    public virtual int ItemFrequencyBonusPercent { get; }
    public virtual int ChestQualitySteps { get; }
    public virtual bool BlocksFusion(TreasureRank rank);
    public virtual int StatusCount(GameState state);
    public virtual string StatusDescription(GameState state);
    public void PublishStatus(GameState state);
    public override void OnStageEntered(StageEnteredEvent e);
}
```

## AdventureSeedMode

```csharp
public enum AdventureSeedMode
{
    None,
    Fixed,
    Daily,
}
```

## AdventureSeedSettings

```csharp
public sealed class AdventureSeedSettings
{
    public AdventureSeedMode mode;
    public string seed = string.Empty;
    public int utcOffsetMinutes;
    public AdventureSeedSettings Clone();
    public void Validate();
    public string Resolve(string adventureId, int difficulty, string fallback, DateTimeOffset utcNow);
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

## BeforePlayerDamageEvent

```csharp
public sealed class BeforePlayerDamageEvent : GameRuleEvent
{
    public int baseDamage;
    public int bonusFlat;
    public int bonusPercent;
}
```

## CardChoiceContext

```csharp
public sealed class CardChoiceContext
{
    public GameEngine Engine { get; }
    public GameState State { get; }
    public ITreasureRuntime Runtime { get; }
    public CardChoiceRequest Request { get; }
    public CardChoiceOption Selected { get; }
    public void ApplyEffect(StatEffect effect, bool maxHpGainDoesNotHeal = false);
    public GameActionResult OpenNext(CardChoiceRequest request);
}
```

## CardChoiceEventContent

```csharp
public abstract class CardChoiceEventContent : EventContent, ICardChoiceResolver
{
    protected CardChoiceEventContent();
    protected CardChoiceEventContent(string id) : base(id);
    protected abstract IReadOnlyList<CardChoiceOption> CreateChoices(CardExecutionContext context);
    public abstract GameActionResult ResolveCardChoice(CardChoiceContext context);
    public override GameActionResult Execute(CardExecutionContext context);
}
```

## CardChoiceOption

```csharp
public sealed class CardChoiceOption
{
    public string id = string.Empty;
    public CardState card;
    public StatEffect effect;
    public StatEffect cost;
    public string conditionExpression = string.Empty;
    public bool enabled = true;
    public bool maxHpGainDoesNotHeal;
    public CardChoiceOption Clone();
}
```

## CardChoiceRequest

```csharp
public sealed class CardChoiceRequest
{
    public string title = string.Empty;
    public string titleLocalizationKey = string.Empty;
    public string titleContentId = string.Empty;
    public List<CardChoiceOption> options = new List<CardChoiceOption>();
    public string resolverContentId = string.Empty;
    public int sourceColumn = -1;
    public string sourceCardId = string.Empty;
    public bool consumeSource;
    public bool consumeTurn;
    public bool allowCancel;
    public bool commitTurnOnCancel;
    public CardChoiceRequest Clone();
}
```

## CardExecutionContext

```csharp
public sealed class CardExecutionContext
{
    public GameEngine Engine { get; }
    public CardState Card { get; }
    public int ColumnIndex { get; }
    public int TargetColumn { get; }
    public CardExecutionContext( GameEngine engine, CardState card, int columnIndex = -1, int targetColumn = -1);
}
```

## CharacterContent

```csharp
public abstract class CharacterContent : GameContentModule
{
    protected CharacterContent();
    protected CharacterContent(string id) : base(id);
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
    public virtual string ProfessionId { get; }
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

## DeclarativeConditionEvaluator

```csharp
public static class DeclarativeConditionEvaluator
{
    public static bool Evaluate(string expression, GameState state);
    public static bool TryEvaluate(string expression, GameState state, out bool result);
}
```

## EnemyContent

```csharp
public abstract class EnemyContent : GameContentModule
{
    protected EnemyContent();
    protected EnemyContent(string id) : base(id);
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
    protected EnemyTraitContent();
    protected EnemyTraitContent(string id) : base(id);
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
    protected EventContent();
    protected EventContent(string id) : base(id);
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

## GameActionResult

```csharp
public sealed class GameActionResult
{
    public bool ok;
    public string code;
    public string message;
    public object[] messageLocalizationArguments;
    public string messageLocalizationContentId;
    public string action;
    public int amount;
    public int slot = -1;
    public int columnIndex = -1;
    public int sourceColumn = -1;
    public int presentationCasterColumn = -1;
    public int targetColumn = -1;
    public int damageDealt;
    public int retaliationDamage;
    public int recoveredAfterHit;
    public int recoveredAfterKill;
    public int rewardGold;
    public int hpRecovered;
    public int playerHpBefore;
    public int playerHpAfter;
    public int enemyHpBefore;
    public int enemyHpAfter;
    public int enemyHpAfterAttack = -1;
    public bool dodged;
    public bool defeated;
    public CardState usedItem;
    public CardState enemy;
    public TreasureState treasure;
    public string presentationSourceContentId = string.Empty;
    public List<MoveHitResult> moveHits = new List<MoveHitResult>();
    public List<EnemyTraitPresentationRecord> enemyTraitPresentations = new List<EnemyTraitPresentationRecord>();
    public List<EnemyStatusPresentationRecord> enemyStatusPresentations = new List<EnemyStatusPresentationRecord>();
    public bool playHealingEffect;
    public bool playStrengtheningEffect;
    public bool playShieldGainedEffect;
    public bool playHealingSound;
    public bool playPlayerDamagedSound;
    public bool playBlockSound;
    public List<CardShuffleRecord> shuffledCards = new List<CardShuffleRecord>();
    public static GameActionResult Success(string code, string message = "");
    public static GameActionResult Failure(string code, string message, params object[] localizationArguments);
    public static GameActionResult FailureForContent(string code, string message, string contentId);
}
```

## GameContentModule

```csharp
public abstract class GameContentModule : IGameContent, IAppearanceContent
{
    protected GameContentModule();
    protected GameContentModule(string id);
    public virtual string Id { get; }
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

## IAdventureContinuationContent

```csharp
public interface IAdventureContinuationContent
{
    IReadOnlyList<StageDefinition> CreateNextStages(AdventureContinuationContext context);
}
```

## ICardChoiceResolver

```csharp
public interface ICardChoiceResolver : IGameContent
{
    GameActionResult ResolveCardChoice(CardChoiceContext context);
}
```

## IModLevelDifficultyRegistrar

```csharp
public interface IModLevelDifficultyRegistrar
{
    IReadOnlyList<ModLevelDefinition> GetLevels();
    void AddLevelDifficulty(ModLevelDifficultyDefinition definition);
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

## IModUiContext

```csharp
public interface IModUiContext
{
    string PackageId { get; }
    string ScreenId { get; }
    void OpenScreen(string screenId);
    void CloseScreen();
    void ExecuteHostAction(ModStartScreenAction action);
    void SetText(string elementId, string value);
    void SetVisible(string elementId, bool visible);
    void SetInteractable(string elementId, bool interactable);
    void SetImage(string elementId, string packageRelativeAsset);
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
    protected ItemContent();
    protected ItemContent(string id) : base(id);
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
    public const string Version = "1.11.0";
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

## ModConfigValueKind

```csharp
public enum ModConfigValueKind
{
    Toggle,
    Integer,
    Decimal,
    Choice,
    Text,
}
```

## ModLevelDefinition

```csharp
public sealed class ModLevelDefinition
{
    public string id = string.Empty;
    public string name = string.Empty;
    public List<AdventureDifficultyDefinition> difficulties = new List<AdventureDifficultyDefinition>();
    public ModLevelDefinition Clone();
}
```

## ModLevelDifficultyDefinition

```csharp
public sealed class ModLevelDifficultyDefinition
{
    public string id = string.Empty;
    public string packageId = string.Empty;
    public string levelId = string.Empty;
    public AdventureDifficultyDefinition difficulty;
}
```

## ModLevelDifficultyExtensions

```csharp
public static class ModLevelDifficultyExtensions
{
    public static IReadOnlyList<ModLevelDefinition> GetLevels(this IModRegistrar registrar);
    public static AdventureDifficultyDefinition GetLevelDifficulty(this IModRegistrar registrar, string levelId, int difficulty);
    public static AdventureDifficultyDefinition CopyLevelDifficulty(this IModRegistrar registrar, string sourceLevelId, int sourceDifficulty, int newDifficulty);
    public static void AddLevelDifficulty(this IModRegistrar registrar, string id, string levelId, AdventureDifficultyDefinition difficulty);
}
```

## ModLevelDifficultyValidation

```csharp
public static class ModLevelDifficultyValidation
{
    public static void Validate(AdventureDifficultyDefinition value);
}
```

## ModMusicCue

```csharp
public enum ModMusicCue
{
    MainMenu,
    StageExplore,
    BossBattle,
    Victory,
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

## ModPersistentData

```csharp
public sealed class ModPersistentData
{
    public string PackageId { get; }
    public string GetString(string key, string fallback = "");
    public int GetInt(string key, int fallback = 0);
    public bool GetBool(string key, bool fallback = false);
    public bool SetString(string key, string value);
    public bool SetInt(string key, int value);
    public bool SetBool(string key, bool value);
    public bool Remove(string key);
    public bool AddInt(string key, int amount);
    public bool TrySpend(string key, int amount);
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

## ModPresentationSlot

```csharp
public enum ModPresentationSlot
{
    Icon,
    Portrait,
    Avatar,
    BattleArt,
    IntentIcon,
    StageBackground,
    StageMapThumbnail,
    StageArrivalArt,
}
```

## ModProgress

```csharp
public static class ModProgress
{
    public static ModPersistentData ForPackage(string packageId);
    public static void ConfigureHost(Func<string, string, string> reader, Func<string, string, string, bool> writer);
    public static void ValidatePackageId(string id);
    public static void ValidateKey(string key);
}
```

## ModRegistrarExtensions

```csharp
public static class ModRegistrarExtensions
{
    public static void AddContents(this IModRegistrar registrar, params IGameContent[] contents);
}
```

## ModScreenController

```csharp
public abstract class ModScreenController
{
    public virtual void OnOpen(IModUiContext context);
    public virtual void OnClose(IModUiContext context);
    public virtual void OnAction(string actionId, IModUiContext context);
    public virtual void OnUpdate(float unscaledDeltaTime, IModUiContext context);
}
```

## ModScreenDefinition

```csharp
public sealed class ModScreenDefinition
{
    public ModScreenDefinition(string id, ModScreenPlacement placement, ModUiElement root, ModScreenController controller = null, int priority = 0, bool closeOnEscape = true, string musicThemeId = "");
    public string Id { get; }
    public ModScreenPlacement Placement { get; }
    public ModUiElement Root { get; }
    public ModScreenController Controller { get; }
    public int Priority { get; }
    public bool CloseOnEscape { get; }
    public string MusicThemeId { get; }
}
```

## ModScreenPlacement

```csharp
public enum ModScreenPlacement
{
    StartScreenReplacement,
    MainMenuPage,
    Overlay,
}
```

## ModStartScreenAction

```csharp
public enum ModStartScreenAction
{
    StartNewGame,
    ContinueGame,
    OpenSettings,
    OpenAbout,
    ShowOriginalMenu,
    QuitGame,
}
```

## ModStartScreenButton

```csharp
public sealed class ModStartScreenButton
{
    public ModStartScreenButton(string id, string labelKey, string labelFallback, ModStartScreenAction action);
    public string Id { get; }
    public string LabelKey { get; }
    public string LabelFallback { get; }
    public ModStartScreenAction Action { get; }
}
```

## ModStartScreenDefinition

```csharp
public sealed class ModStartScreenDefinition
{
    public ModStartScreenDefinition( string id, string titleKey, string titleFallback, string subtitleKey, string subtitleFallback, IReadOnlyList<ModStartScreenButton> buttons, string footerKey = "", string footerFallback = "", string backgroundColor = "#102A2A", string panelColor = "#F0D7A5F2", string accentColor = "#D79A45", string textColor = "#2E190F");
    public string Id { get; }
    public string TitleKey { get; }
    public string TitleFallback { get; }
    public string SubtitleKey { get; }
    public string SubtitleFallback { get; }
    public IReadOnlyList<ModStartScreenButton> Buttons { get; }
    public string FooterKey { get; }
    public string FooterFallback { get; }
    public string BackgroundColor { get; }
    public string PanelColor { get; }
    public string AccentColor { get; }
    public string TextColor { get; }
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

## ModUi

```csharp
public static class ModUi
{
    public static ModUiElement Column(string id, params ModUiElement[] children);
    public static ModUiElement Row(string id, params ModUiElement[] children);
    public static ModUiElement Panel(string id, params ModUiElement[] children);
    public static ModUiElement Scroll(string id, params ModUiElement[] children);
    public static ModUiElement Text(string id, string key, string fallback);
    public static ModUiElement Image(string id, string packageRelativeAsset);
    public static ModUiElement Button(string id, string key, string fallback, string actionId);
    public static ModUiElement HostButton(string id, string key, string fallback, ModStartScreenAction action);
    public static ModUiElement Spacer(string id, float size);
}
```

## ModUiAlignment

```csharp
public enum ModUiAlignment
{
    Start,
    Center,
    End,
    Stretch,
}
```

## ModUiElement

```csharp
public sealed class ModUiElement
{
    public ModUiElement(string id, ModUiElementKind kind, IReadOnlyList<ModUiElement> children = null);
    public string Id { get; }
    public ModUiElementKind Kind { get; }
    public IReadOnlyList<ModUiElement> Children { get; }
    public ModUiStyle Style { get; set; }
    public string TextKey { get; set; }
    public string TextFallback { get; set; }
    public string ImageAsset { get; set; }
    public string ActionId { get; set; }
    public bool UsesHostAction { get; set; }
    public ModStartScreenAction HostAction { get; set; }
    public bool Visible { get; set; }
    public bool Interactable { get; set; }
}
```

## ModUiElementKind

```csharp
public enum ModUiElementKind
{
    Column,
    Row,
    Panel,
    Text,
    Image,
    Button,
    Spacer,
    Scroll,
}
```

## ModUiImageFit

```csharp
public enum ModUiImageFit
{
    Stretch,
    Contain,
    Cover,
}
```

## ModUiStyle

```csharp
public sealed class ModUiStyle
{
    public float Width { get; set; }
    public float Height { get; set; }
    public float MinWidth { get; set; }
    public float MinHeight { get; set; }
    public float FlexibleWidth { get; set; }
    public float FlexibleHeight { get; set; }
    public float Gap { get; set; }
    public ModUiThickness Padding { get; set; }
    public ModUiAlignment HorizontalAlignment { get; set; }
    public ModUiAlignment VerticalAlignment { get; set; }
    public string BackgroundColor { get; set; }
    public string TextColor { get; set; }
    public float FontSize { get; set; }
    public bool Bold { get; set; }
    public bool RaycastTarget { get; set; }
    public ModUiImageFit ImageFit { get; set; }
}
```

## ModUiThickness

```csharp
public readonly struct ModUiThickness
{
    public ModUiThickness(int all) : this(all, all, all, all);
    public ModUiThickness(int horizontal, int vertical) : this(horizontal, horizontal, vertical, vertical);
    public ModUiThickness(int left, int right, int top, int bottom);
    public int Left { get; }
    public int Right { get; }
    public int Top { get; }
    public int Bottom { get; }
}
```

## MoveCapacityEvent

```csharp
public sealed class MoveCapacityEvent : GameRuleEvent
{
    public MoveState move;
    public int baseMaxUses;
    public int bonusMaxUses;
}
```

## MoveContent

```csharp
public abstract class MoveContent : GameContentModule, IUseCardContent
{
    protected MoveContent();
    protected MoveContent(string id) : base(id);
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

## NormalAttackResolvedEvent

```csharp
public sealed class NormalAttackResolvedEvent : GameRuleEvent
{
    public bool tookDamage;
    public int damageDealt;
    public int restoreMoveUses;
    public IReadOnlyList<MoveHitResult> hits = Array.Empty<MoveHitResult>();
    public long healingPercentDamage;
    public string healingSourceContentId = string.Empty;
    public MoveHitResult healingSourceHit;
    public void RegisterHealingPresentation(string sourceContentId, MoveHitResult hit);
}
```

## PlayerDamageTakenEvent

```csharp
public sealed class PlayerDamageTakenEvent : GameRuleEvent
{
    public int damage;
    public int absorbed;
    public int hpDamage;
    public int TotalDamageTaken { get; }
    public string enemyAttackerId = string.Empty;
    public int enemyAttackerColumnIndex = -1;
    public int requestedReflectionDamage { get; private set; }
    public void ReflectDamageToAttacker(int amount);
}
```

## PlayerStatusProjectionEvent

```csharp
public sealed class PlayerStatusProjectionEvent : GameRuleEvent
{
    public PlayerAttackEmpoweredStatus attackDamage { get; private set; }
    public PlayerMultiAttackStatus multiAttack { get; private set; }
    public PlayerLifestealStatus lifesteal { get; private set; }
}
```

## ProfessionContent

```csharp
public abstract class ProfessionContent : GameContentModule
{
    public abstract string PackageId { get; }
    public abstract IReadOnlyList<ProfessionUpgradeConfig> Upgrades { get; }
    public virtual ProfessionUpgradeCurrency UpgradeCurrency { get; }
    public virtual string CurrencyKey { get; }
    public virtual string CurrencyName { get; }
    public virtual string CurrencyIconId { get; }
    public void ValidateRegistration(string packageId);
    public int UpgradeLevel(GameState state, string upgradeId);
    public virtual string UpgradeDescription(string upgradeId, int level);
}
```

## ProfessionIds

```csharp
public static class ProfessionIds
{
    public const string Assassin = "profession.assassin";
    public const string Warrior = "profession.warrior";
    public const string Ranger = "profession.ranger";
    public const string Mage = "profession.mage";
    public const string MartialArtist = "profession.martial_artist";
    public static string FromCharacterId(string characterId);
    public static string DisplayName(string professionId);
}
```

## ProfessionUpgradeConfig

```csharp
public sealed class ProfessionUpgradeConfig
{
    public string id = string.Empty;
    public string name = string.Empty;
    public string description = string.Empty;
    public string iconId = string.Empty;
    public string builtInUpgradeId = string.Empty;
    public ProfessionUpgradeEffectKind effectKind = ProfessionUpgradeEffectKind.Custom;
    public int valuePerLevel;
    public int[] costs = Array.Empty<int>();
    public static ProfessionUpgradeConfig FromBuiltIn(string id, string builtInUpgradeId);
    public static IReadOnlyList<ProfessionUpgradeConfig> CopyBuiltInProfession(string sourceProfessionId, string professionId);
    public ProfessionUpgradeConfig Clone();
}
```

## ProfessionUpgradeCurrency

```csharp
public enum ProfessionUpgradeCurrency
{
    ModCurrency,
    GameCrystals,
}
```

## ProfessionUpgradeEffectKind

```csharp
public enum ProfessionUpgradeEffectKind
{
    StartingWisdom,
    StartingGold,
    StartingMaxHp,
    StartingAttack,
    StartingDefense,
    StartingRandomTreasure,
    IntermissionHealing,
    BossShield,
    BossDodge,
    BossDefeatHealingPercent,
    PotionEffectPercent,
    Custom,
}
```

## ProfessionUpgradeIds

```csharp
public static class ProfessionUpgradeIds
{
    public const string AssassinWisdom = "profession.assassin.wisdom";
    public const string AssassinStartingGold = "profession.assassin.starting_gold";
    public const string AssassinMaxHp = "profession.assassin.max_hp";
    public const string AssassinAttack = "profession.assassin.attack";
    public const string AssassinStartingTreasure = "profession.assassin.starting_treasure";
    public const string WarriorMaxHp = "profession.warrior.max_hp";
    public const string WarriorStartingGold = "profession.warrior.starting_gold";
    public const string WarriorDefense = "profession.warrior.defense";
    public const string WarriorIntermissionHealing = "profession.warrior.intermission_healing";
    public const string WarriorBossShield = "profession.warrior.boss_shield";
    public const string RangerAttack = "profession.ranger.attack";
    public const string RangerStartingGold = "profession.ranger.starting_gold";
    public const string RangerMaxHp = "profession.ranger.max_hp";
    public const string RangerBossDodge = "profession.ranger.boss_dodge";
    public const string RangerStartingTreasure = "profession.ranger.starting_treasure";
    public const string MageWisdom = "profession.mage.wisdom";
    public const string MageMaxHp = "profession.mage.max_hp";
    public const string MageStartingGold = "profession.mage.starting_gold";
    public const string MageBossDefeatHealingPercent = "profession.mage.boss_defeat_healing_percent";
    public const string MagePotionEffectPercent = "profession.mage.potion_effect_percent";
    public const string MartialArtistMaxHp = "profession.martial_artist.max_hp";
    public const string MartialArtistStartingGold = "profession.martial_artist.starting_gold";
    public const string MartialArtistStartingTreasure = "profession.martial_artist.starting_treasure";
    public const string MartialArtistIntermissionHealing = "profession.martial_artist.intermission_healing";
    public const string MartialArtistBossShield = "profession.martial_artist.boss_shield";
}
```

## RichEventChoiceState

```csharp
public sealed class RichEventChoiceState
{
    public string choiceId = string.Empty;
    public string text = string.Empty;
    public string conditionExpression = string.Empty;
    public StatEffect cost;
    public StatEffect reward;
    public string rewardContentId = string.Empty;
    public int rewardContentCount;
    public string nextStageId = string.Empty;
    public string nextEventId = string.Empty;
    public RichEventChoiceState Clone();
}
```

## StageContent

```csharp
public abstract class StageContent : GameContentModule
{
    protected StageContent();
    protected StageContent(string id) : base(id);
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

## StageGenerationProfiles

```csharp
public static class StageGenerationProfiles
{
    public const string Default = "workshop.default";
    public const string Weighted = "workshop.weighted.v1";
    public const string Layered = "workshop.layered.v1";
    public const string Branching = "workshop.branching.v1";
    public const string LayeredBranching = "workshop.layered-branching.v1";
}
```

## StageGraphEdgeDefinition

```csharp
public sealed class StageGraphEdgeDefinition
{
    public string fromNodeId = string.Empty;
    public string toNodeId = string.Empty;
    public string conditionExpression = string.Empty;
    public float weight = 1f;
    public StageGraphEdgeDefinition Clone();
}
```

## StageGraphNodeDefinition

```csharp
public sealed class StageGraphNodeDefinition
{
    public string nodeId = string.Empty;
    public StageGraphNodeKind kind;
    public string contentId = string.Empty;
    public bool required;
    public CardState card;
    public StageGraphNodeDefinition Clone();
}
```

## StageGraphNodeKind

```csharp
public enum StageGraphNodeKind
{
    Start,
    Encounter,
    Event,
    Camp,
    Exit,
    Victory,
    Failure,
}
```

## StatEffect

```csharp
public sealed class StatEffect
{
    public string blessingType = string.Empty;
    public TreasureRank appearanceQuality = TreasureRank.Common;
    public float appearanceWeight = 1f;
    public List<string> requiredAppearanceTags = new List<string>();
    public int hp;
    public int maxHp;
    public int attack;
    public int defense;
    public int wisdom;
    public int dodgeCharges;
    public int gold;
    public StatEffect Clone();
}
```

## TraitContent

```csharp
public abstract class TraitContent : GameContentModule
{
    protected TraitContent();
    protected TraitContent(string id) : base(id);
    public abstract string Description { get; }
}
```

## TreasureContent

```csharp
public abstract class TreasureContent : GameContentModule
{
    protected TreasureContent();
    protected TreasureContent(string id) : base(id);
    protected TreasureContent(string displayName, TreasureRank maximumRank);
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
    protected virtual void SynchronizeRuntimeConfiguration();
    protected void SynchronizeLinearQualityValues(TreasureRank minimumRank, int firstValue);
    public abstract string Describe(int level);
    public virtual GameActionResult Execute(TreasureState treasure, TreasureActivationContext context);
    public TreasureDefinition CreateDefinition();
    public virtual TreasureState CreateState(int level = 1);
    public virtual TreasureContent CloneRuntime();
    protected virtual string DescribeVariant(int value, int level);
    public virtual IEnumerable<TreasureState> GetStateVariants();
    protected TreasureState CreateVariant(TreasureRank rank, int level = 1);
    protected static string ChanceText(int value);
    protected static string ChancePrefix(int value);
    protected static void CountFrequency( ref int accumulatedTriggers, ref int sceneRewards, int threshold, int sceneCap, Action reward);
    protected static void CountAmount( ref int accumulatedAmount, ref int sceneRewards, int amount, int threshold, int sceneCap, Action reward);
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

## TurnEndedEvent

```csharp
public sealed class TurnEndedEvent : GameRuleEvent
{
    public int turn;
}
```
