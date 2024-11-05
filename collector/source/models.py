from typing import List

from pydantic import BaseModel, Field, field_validator, ConfigDict

from enums import GameMode, GameType, Lane, Role, Tower, Region


# Match models

class ObjectiveDto(BaseModel):
    first: bool | None = None
    kills: int | None = None

    model_config = ConfigDict(extra='forbid')


class ObjectivesDto(BaseModel):
    baron: ObjectiveDto | None = None
    champion: ObjectiveDto | None = None
    dragon: ObjectiveDto | None = None
    horde: ObjectiveDto | None = None
    inhibitor: ObjectiveDto | None = None
    riftHerald: ObjectiveDto | None = None
    tower: ObjectiveDto | None = None

    model_config = ConfigDict(extra='forbid')


class BanDto(BaseModel):
    championId: int | None = None
    pickTurn: int | None = None

    model_config = ConfigDict(extra='forbid')


class TeamDto(BaseModel):
    bans: List[BanDto] | None = None
    objectives: ObjectivesDto | None = None
    teamId: int | None = None
    win: bool | None = None

    model_config = ConfigDict(extra='forbid')


class PerkStyleSelectionDto(BaseModel):
    perk: int | None = None
    var1: int | None = None
    var2: int | None = None
    var3: int | None = None

    model_config = ConfigDict(extra='forbid')


class PerkStyleDto(BaseModel):
    description: str | None = None
    selections: List[PerkStyleSelectionDto] | None = None
    style: int | None = None

    model_config = ConfigDict(extra='forbid')


class PerkStatsDto(BaseModel):
    defense: int | None = None
    flex: int | None = None
    offense: int | None = None

    model_config = ConfigDict(extra='forbid')


class PerksDto(BaseModel):
    statPerks: PerkStatsDto | None = None
    styles: List[PerkStyleDto] | None = None

    model_config = ConfigDict(extra='forbid')


class MissionsDto(BaseModel):
    playerScore0: int | None = None
    playerScore1: int | None = None
    playerScore2: int | None = None
    playerScore3: int | None = None
    playerScore4: int | None = None
    playerScore5: int | None = None
    playerScore6: int | None = None
    playerScore7: int | None = None
    playerScore8: int | None = None
    playerScore9: int | None = None
    playerScore10: int | None = None
    playerScore11: int | None = None

    model_config = ConfigDict(extra='forbid')


class ParticipantDto(BaseModel):
    allInPings: int | None = Field(None, description='Yellow crossed swords')
    assistMePings: int | None = Field(None, description='Green flag')
    assists: int | None = None
    baronKills: int | None = None
    bountyLevel: int | None = None
    champExperience: int | None = None
    champLevel: int | None = None
    championId: int | None = Field(None,
                                   description='Prior to patch 11.4, on Feb 18th, 2021, this field returned invalid championIds. We recommend determining the champion based on the championName field for matches played prior to patch 11.4.')
    championName: str | None = None
    commandPings: int | None = Field(None, description='Blue generic ping (ALT+click)')
    championTransform: int | None = Field(None,
                                          description='This field is currently only utilized for Kayn\'s transformations. (Legal values: 0 - None, 1 - Slayer, 2 - Assassin)')
    consumablesPurchased: int | None = None
    challenges: dict[str, str] | None = None  # ChallengesDto
    damageDealtToBuildings: int | None = None
    damageDealtToObjectives: int | None = None
    damageDealtToTurrets: int | None = None
    damageSelfMitigated: int | None = None
    deaths: int | None = None
    detectorWardsPlaced: int | None = None
    doubleKills: int | None = None
    dragonKills: int | None = None
    eligibleForProgression: bool | None = None
    enemyMissingPings: int | None = Field(None, description='Yellow questionmark')
    enemyVisionPings: int | None = Field(None, description='Red eyeball')
    firstBloodAssist: bool | None = None
    firstBloodKill: bool | None = None
    firstTowerAssist: bool | None = None
    firstTowerKill: bool | None = None
    gameEndedInEarlySurrender: bool | None = Field(None,
                                                   description='This is an offshoot of the OneStone challenge. The code checks if a spell with the same instance ID does the final point of damage to at least 2 Champions. It doesn\'t matter if they\'re enemies, but you cannot hurt your friends.')
    gameEndedInSurrender: bool | None = None
    holdPings: int | None = None
    getBackPings: int | None = Field(None, description='Yellow circle with horizontal line')
    goldEarned: int | None = None
    goldSpent: int | None = None
    individualPosition: Lane | None = Field(None,
                                            description='Both individualPosition and teamPosition are computed by the game server and are different versions of the most likely position played by a player. The individualPosition is the best guess for which position the player actually played in isolation of anything else. The teamPosition is the best guess for which position the player actually played if we add the constraint that each team must have one top player, one jungle, one middle, etc. Generally the recommendation is to use the teamPosition field over the individualPosition field.')
    inhibitorKills: int | None = None
    inhibitorTakedowns: int | None = None
    inhibitorsLost: int | None = None
    item0: int | None = None
    item1: int | None = None
    item2: int | None = None
    item3: int | None = None
    item4: int | None = None
    item5: int | None = None
    item6: int | None = None
    itemsPurchased: int | None = None
    killingSprees: int | None = None
    kills: int | None = None
    lane: Lane | None = None
    largestCriticalStrike: int | None = None
    largestKillingSpree: int | None = None
    largestMultiKill: int | None = None
    longestTimeSpentLiving: int | None = None
    magicDamageDealt: int | None = None
    magicDamageDealtToChampions: int | None = None
    magicDamageTaken: int | None = None
    missions: MissionsDto | None = None
    neutralMinionsKilled: int | None = Field(None,
                                             description='neutralMinionsKilled = mNeutralMinionsKilled, which is incremented on kills of kPet and kJungleMonster')
    needVisionPings: int | None = Field(None, description='Green ward')
    nexusKills: int | None = None
    nexusTakedowns: int | None = None
    nexusLost: int | None = None
    objectivesStolen: int | None = None
    objectivesStolenAssists: int | None = None
    onMyWayPings: int | None = Field(None, description='Blue arrow pointing at ground')
    participantId: int | None = None
    playerScore0: int | None = None
    playerScore1: int | None = None
    playerScore2: int | None = None
    playerScore3: int | None = None
    playerScore4: int | None = None
    playerScore5: int | None = None
    playerScore6: int | None = None
    playerScore7: int | None = None
    playerScore8: int | None = None
    playerScore9: int | None = None
    playerScore10: int | None = None
    playerScore11: int | None = None
    pentaKills: int | None = None
    perks: PerksDto | None = None
    physicalDamageDealt: int | None = None
    physicalDamageDealtToChampions: int | None = None
    physicalDamageTaken: int | None = None
    placement: int | None = None
    playerAugment1: int | None = None
    playerAugment2: int | None = None
    playerAugment3: int | None = None
    playerAugment4: int | None = None
    playerAugment5: int | None = None
    playerAugment6: int | None = None
    playerSubteamId: int | None = None
    pushPings: int | None = Field(None, description='Green minion')
    profileIcon: int | None = None
    puuid: str | None = None
    quadraKills: int | None = None
    riotIdGameName: str | None = None
    riotIdTagline: str | None = None
    role: Role | None = None
    sightWardsBoughtInGame: int | None = None
    spell1Casts: int | None = None
    spell2Casts: int | None = None
    spell3Casts: int | None = None
    spell4Casts: int | None = None
    subteamPlacement: int | None = None
    summoner1Casts: int | None = None
    summoner1Id: int | None = None
    summoner2Casts: int | None = None
    summoner2Id: int | None = None
    summonerId: str | None = None
    summonerLevel: int | None = None
    summonerName: str | None = None
    teamEarlySurrendered: bool | None = None
    teamId: int | None = None
    teamPosition: Lane | None = Field(None,
                                      description='Both individualPosition and teamPosition are computed by the game server and are different versions of the most likely position played by a player. The individualPosition is the best guess for which position the player actually played in isolation of anything else. The teamPosition is the best guess for which position the player actually played if we add the constraint that each team must have one top player, one jungle, one middle, etc. Generally the recommendation is to use the teamPosition field over the individualPosition field.')
    timeCCingOthers: int | None = None
    timePlayed: int | None = None
    totalAllyJungleMinionsKilled: int | None = None
    totalDamageDealt: int | None = None
    totalDamageDealtToChampions: int | None = None
    totalDamageShieldedOnTeammates: int | None = None
    totalDamageTaken: int | None = None
    totalEnemyJungleMinionsKilled: int | None = None
    totalHeal: int | None = Field(None,
                                  description='Whenever positive health is applied (which translates to all heals in the game but not things like regeneration), totalHeal is incremented by the amount of health received. This includes healing enemies, jungle monsters, yourself, etc')
    totalHealsOnTeammates: int | None = Field(None,
                                              description='Whenever positive health is applied (which translates to all heals in the game but not things like regeneration), totalHealsOnTeammates is incremented by the amount of health received.  This is post modified, so if you heal someone missing 5 health for 100 you will get +5 totalHealsOnTeammates')
    totalMinionsKilled: int | None = Field(None,
                                           description='totalMillionsKilled = mMinionsKilled, which is only incremented on kills of kTeamMinion, kMeleeLaneMinion, kSuperLaneMinion, kRangedLaneMinion and kSiegeLaneMinion')
    totalTimeCCDealt: int | None = None
    totalTimeSpentDead: int | None = None
    totalUnitsHealed: int | None = None
    tripleKills: int | None = None
    trueDamageDealt: int | None = None
    trueDamageDealtToChampions: int | None = None
    trueDamageTaken: int | None = None
    turretKills: int | None = None
    turretTakedowns: int | None = None
    turretsLost: int | None = None
    unrealKills: int | None = None
    visionScore: int | None = None
    visionClearedPings: int | None = None
    visionWardsBoughtInGame: int | None = None
    wardsKilled: int | None = None
    wardsPlaced: int | None = None
    win: bool | None = None

    # noinspection PyNestedDecorators
    @field_validator('challenges', mode='before')
    def convert_values_to_str(cls, obj: dict | None) -> dict[str, str] | None:
        if obj is None:
            return None

        return {key: repr(val) for key, val in obj.items()}

    basicPings: int | None = None
    dangerPings: int | None = None
    retreatPings: int | None = None
    baitPings: int | None = None
    riotIdName: str | None = None
    model_config = ConfigDict(extra='forbid')


class InfoDto(BaseModel):
    endOfGameResult: str | None = Field(None, description='Refer to indicate if the game ended in termination.')
    gameCreation: int | None = Field(None,
                                     description='Unix timestamp for when the game is created on the game server (i.e., the loading screen).')
    gameDuration: int | None = Field(None,
                                     description='Prior to patch 11.20, this field returns the game length in milliseconds calculated from gameEndTimestamp - gameStartTimestamp. Post patch 11.20, this field returns the max timePlayed of any participant in the game in seconds, which makes the behavior of this field consistent with that of match-v4. The best way to handling the change in this field is to treat the value as milliseconds if the gameEndTimestamp field isn\'t in the response and to treat the value as seconds if gameEndTimestamp is in the response.')
    gameEndTimestamp: int | None = Field(None,
                                         description='Unix timestamp for when match ends on the game server. This timestamp can occasionally be significantly longer than when the match "ends". The most reliable way of determining the timestamp for the end of the match would be to add the max time played of any participant to the gameStartTimestamp. This field was added to match-v5 in patch 11.20 on Oct 5th, 2021.')
    gameId: int | None = None
    gameMode: GameMode | None = Field(None, description='Refer to the Game Constants documentation.')
    gameName: str | None = None
    gameStartTimestamp: int | None = Field(None, description='Unix timestamp for when match starts on the game server.')
    gameType: GameType | None = None
    gameVersion: str | None = Field(None,
                                    description='The first two parts can be used to determine the patch a game was played on.')
    mapId: int | None = Field(None, description='Refer to the Game Constants documentation.')
    participants: List[ParticipantDto] | None = None
    platformId: Region | None = Field(None, description='Platform where the match was played.')
    queueId: int | None = Field(None, description='Refer to the Game Constants documentation.')
    teams: List[TeamDto] | None = None
    tournamentCode: str | None = Field(None,
                                       description='Tournament code used to generate the match. This field was added to match-v5 in patch 11.13 on June 23rd, 2021.')

    model_config = ConfigDict(extra='forbid')


class MetadataDto(BaseModel):
    dataVersion: str | None = Field(None, description='Match data version.')
    matchId: str | None = Field(None, description='Match id.')
    participants: List[str] | None = Field(None, description='A list of participant PUUIDs.')

    model_config = ConfigDict(extra='forbid')


class MatchDto(BaseModel):
    metadata: MetadataDto | None = Field(None, description='Match metadata.')
    info: InfoDto | None = Field(None, description='Match info.')

    model_config = ConfigDict(extra='forbid')


# Timeline models

class PositionDto(BaseModel):
    x: int | None = None
    y: int | None = None

    model_config = ConfigDict(extra='forbid')


class DamageStatsDto(BaseModel):
    magicDamageDone: int | None = None
    magicDamageDoneToChampions: int | None = None
    magicDamageTaken: int | None = None
    physicalDamageDone: int | None = None
    physicalDamageDoneToChampions: int | None = None
    physicalDamageTaken: int | None = None
    totalDamageDone: int | None = None
    totalDamageDoneToChampions: int | None = None
    totalDamageTaken: int | None = None
    trueDamageDone: int | None = None
    trueDamageDoneToChampions: int | None = None
    trueDamageTaken: int | None = None

    model_config = ConfigDict(extra='forbid')


class ChampionStatsDto(BaseModel):
    abilityHaste: int | None = None
    abilityPower: int | None = None
    armor: int | None = None
    armorPen: int | None = None
    armorPenPercent: int | None = None
    attackDamage: int | None = None
    attackSpeed: int | None = None
    bonusArmorPenPercent: int | None = None
    bonusMagicPenPercent: int | None = None
    ccReduction: int | None = None
    cooldownReduction: int | None = None
    health: int | None = None
    healthMax: int | None = None
    healthRegen: int | None = None
    lifesteal: int | None = None
    magicPen: int | None = None
    magicPenPercent: int | None = None
    magicResist: int | None = None
    movementSpeed: int | None = None
    omnivamp: int | None = None
    physicalVamp: int | None = None
    power: int | None = None
    powerMax: int | None = None
    powerRegen: int | None = None
    spellVamp: int | None = None

    model_config = ConfigDict(extra='forbid')


class ParticipantFrameDto(BaseModel):
    championStats: ChampionStatsDto | None = None
    currentGold: int | None = None
    damageStats: DamageStatsDto | None = None
    goldPerSecond: int | None = None
    jungleMinionsKilled: int | None = None
    level: int | None = None
    minionsKilled: int | None = None
    participantId: int | None = None
    position: PositionDto | None = None
    timeEnemySpentControlled: int | None = None
    totalGold: int | None = None
    xp: int | None = None

    model_config = ConfigDict(extra='forbid')


class VictimDamageDealt(BaseModel):
    basic: bool | None = None
    magicDamage: int | None = None
    name: str | None = None
    participantId: int | None = None
    physicalDamage: int | None = None
    spellName: str | None = None
    spellSlot: int | None = None
    trueDamage: int | None = None
    type: str | None = None

    model_config = ConfigDict(extra='forbid')


class VictimDamageReceived(BaseModel):
    basic: bool | None = None
    magicDamage: int | None = None
    name: str | None = None
    participantId: int | None = None
    physicalDamage: int | None = None
    spellName: str | None = None
    spellSlot: int | None = None
    trueDamage: int | None = None
    type: str | None = None

    model_config = ConfigDict(extra='forbid')


class EventsTimeLineDto(BaseModel):
    timestamp: int | None = None
    type: str | None = None

    realTimestamp: int | None = None  # PAUSE_END, GAME_END
    gameId: int | None = None  # GAME_END
    winningTeam: int | None = None  # GAME_END
    itemId: int | None = None  # ITEM_PURCHASED, ITEM_DESTROYED
    participantId: int | None = None  # ITEM_PURCHASED, ITEM_DESTROYED
    levelUpType: str | None = None  # SKILL_LEVEL_UP
    skillSlot: int | None = None  # SKILL_LEVEL_UP
    level: int | None = None  # LEVEL_UP
    creatorId: int | None = None  # WARD_PLACED
    wardType: str | None = None  # WARD_PLACED
    killerId: int | None = None  # CHAMPION_KILL, BUILDING_KILL, CHAMPION_SPECIAL_KILL, ELITE_MONSTER_KILL
    killStreakLength: int | None = None  # CHAMPION_KILL
    position: PositionDto | None = None  # CHAMPION_KILL, TURRET_PLATE_DESTROYED, BUILDING_KILL
    bounty: int | None = None  # CHAMPION_KILL, BUILDING_KILL, ELITE_MONSTER_KILL
    shutdownBounty: int | None = None  # CHAMPION_KILL
    victimDamageDealt: List[VictimDamageDealt] | None = None  # CHAMPION_KILL
    victimDamageReceived: List[VictimDamageReceived] | None = None  # CHAMPION_KILL
    victimId: int | None = None  # CHAMPION_KILL
    assistingParticipantIds: List[int] | None = None  # CHAMPION_KILL, BUILDING_KILL, ELITE_MONSTER_KILL
    teamId: int | None = None  # BUILDING_KILL, TURRET_PLATE_DESTROYED, ELITE_MONSTER_KILL
    buildingType: str | None = None  # BUILDING_KILL
    towerType: Tower | None = None  # BUILDING_KILL
    laneType: str | None = None  # TURRET_PLATE_DESTROYED, BUILDING_KILL
    killType: str | None = None  # CHAMPION_SPECIAL_KILL
    multiKillLength: int | None = None  # CHAMPION_SPECIAL_KILL
    monsterType: str | None = None  # ELITE_MONSTER_KILL
    monsterSubType: str | None = None  # ELITE_MONSTER_KILL
    killerTeamId: int | None = None  # ELITE_MONSTER_KILL
    afterId: int | None = None  # ITEM_UNDO
    beforeId: int | None = None  # ITEM_UNDO
    goldGain: int | None = None  # ITEM_UNDO
    actualStartTime: int | None = None  # OBJECTIVE_BOUNTY_PRESTART
    name: str | None = None  # DRAGON_SOUL_GIVEN
    transformType: str | None = None  # CHAMPION_TRANSFORM

    model_config = ConfigDict(extra='forbid')


class FramesTimeLineDto(BaseModel):
    events: List[EventsTimeLineDto] | None = None
    participantFrames: dict[str, ParticipantFrameDto] | None = None
    timestamp: int | None = None

    model_config = ConfigDict(extra='forbid')


class ParticipantTimeLineDto(BaseModel):
    participantId: int | None = None
    puuid: str | None = None

    model_config = ConfigDict(extra='forbid')


class InfoTimeLineDto(BaseModel):
    endOfGameResult: str | None = Field(None, description='Refer to indicate if the game ended in termination.')
    frameInterval: int | None = None
    gameId: int | None = None
    participants: List[ParticipantTimeLineDto] | None = None
    frames: List[FramesTimeLineDto] | None = None

    model_config = ConfigDict(extra='forbid')


class MetadataTimeLineDto(BaseModel):
    dataVersion: str | None = Field(None, description='Match data version.')
    matchId: str | None = Field(None, description='Match id.')
    participants: List[str] | None = Field(None, description='A list of participant PUUIDs.')

    model_config = ConfigDict(extra='forbid')


class TimelineDto(BaseModel):
    metadata: MetadataTimeLineDto | None = Field(None, description='Match metadata.')
    info: InfoTimeLineDto | None = Field(None, description='Match info.')

    model_config = ConfigDict(extra='forbid')
