from typing import List

from pydantic import BaseModel, Field, field_validator


# Match models

class ObjectiveDto(BaseModel):
    first: bool | None = Field(None)
    kills: int | None = Field(None)


class ObjectivesDto(BaseModel):
    baron: ObjectiveDto | None = Field(None)
    champion: ObjectiveDto | None = Field(None)
    dragon: ObjectiveDto | None = Field(None)
    horde: ObjectiveDto | None = Field(None)
    inhibitor: ObjectiveDto | None = Field(None)
    riftHerald: ObjectiveDto | None = Field(None)
    tower: ObjectiveDto | None = Field(None)


class BanDto(BaseModel):
    championId: int | None = Field(None)
    pickTurn: int | None = Field(None)


class TeamDto(BaseModel):
    bans: List[BanDto] | None = Field(None)
    objectives: ObjectivesDto | None = Field(None)
    teamId: int | None = Field(None)
    win: bool | None = Field(None)


class PerkStyleSelectionDto(BaseModel):
    perk: int | None = Field(None)
    var1: int | None = Field(None)
    var2: int | None = Field(None)
    var3: int | None = Field(None)


class PerkStyleDto(BaseModel):
    description: str | None = Field(None)
    selections: List[PerkStyleSelectionDto] | None = Field(None)
    style: int | None = Field(None)


class PerkStatsDto(BaseModel):
    defense: int | None = Field(None)
    flex: int | None = Field(None)
    offense: int | None = Field(None)


class PerksDto(BaseModel):
    statPerks: PerkStatsDto | None = Field(None)
    styles: List[PerkStyleDto] | None = Field(None)


class MissionsDto(BaseModel):
    playerScore0: int | None = Field(None)
    playerScore1: int | None = Field(None)
    playerScore2: int | None = Field(None)
    playerScore3: int | None = Field(None)
    playerScore4: int | None = Field(None)
    playerScore5: int | None = Field(None)
    playerScore6: int | None = Field(None)
    playerScore7: int | None = Field(None)
    playerScore8: int | None = Field(None)
    playerScore9: int | None = Field(None)
    playerScore10: int | None = Field(None)
    playerScore11: int | None = Field(None)


class ParticipantDto(BaseModel):
    allInPings: int | None = Field(None, description='Yellow crossed swords')
    assistMePings: int | None = Field(None, description='Green flag')
    assists: int | None = Field(None)
    baronKills: int | None = Field(None)
    bountyLevel: int | None = Field(None)
    champExperience: int | None = Field(None)
    champLevel: int | None = Field(None)
    championId: int | None = Field(None,
                                   description='Prior to patch 11.4, on Feb 18th, 2021, this field returned invalid championIds. We recommend determining the champion based on the championName field for matches played prior to patch 11.4.')
    championName: str | None = Field(None)
    commandPings: int | None = Field(None, description='Blue generic ping (ALT+click)')
    championTransform: int | None = Field(None,
                                          description='This field is currently only utilized for Kayn\'s transformations. (Legal values: 0 - None, 1 - Slayer, 2 - Assassin)')
    consumablesPurchased: int | None = Field(None)
    challenges: dict[str, str] | None = Field(None)  # ChallengesDto
    damageDealtToBuildings: int | None = Field(None)
    damageDealtToObjectives: int | None = Field(None)
    damageDealtToTurrets: int | None = Field(None)
    damageSelfMitigated: int | None = Field(None)
    deaths: int | None = Field(None)
    detectorWardsPlaced: int | None = Field(None)
    doubleKills: int | None = Field(None)
    dragonKills: int | None = Field(None)
    eligibleForProgression: bool | None = Field(None)
    enemyMissingPings: int | None = Field(None, description='Yellow questionmark')
    enemyVisionPings: int | None = Field(None, description='Red eyeball')
    firstBloodAssist: bool | None = Field(None)
    firstBloodKill: bool | None = Field(None)
    firstTowerAssist: bool | None = Field(None)
    firstTowerKill: bool | None = Field(None)
    gameEndedInEarlySurrender: bool | None = Field(None,
                                                   description='This is an offshoot of the OneStone challenge. The code checks if a spell with the same instance ID does the final point of damage to at least 2 Champions. It doesn\'t matter if they\'re enemies, but you cannot hurt your friends.')
    gameEndedInSurrender: bool | None = Field(None)
    holdPings: int | None = Field(None)
    getBackPings: int | None = Field(None, description='Yellow circle with horizontal line')
    goldEarned: int | None = Field(None)
    goldSpent: int | None = Field(None)
    individualPosition: str | None = Field(None,
                                           description='Both individualPosition and teamPosition are computed by the game server and are different versions of the most likely position played by a player. The individualPosition is the best guess for which position the player actually played in isolation of anything else. The teamPosition is the best guess for which position the player actually played if we add the constraint that each team must have one top player, one jungle, one middle, etc. Generally the recommendation is to use the teamPosition field over the individualPosition field.')
    inhibitorKills: int | None = Field(None)
    inhibitorTakedowns: int | None = Field(None)
    inhibitorsLost: int | None = Field(None)
    item0: int | None = Field(None)
    item1: int | None = Field(None)
    item2: int | None = Field(None)
    item3: int | None = Field(None)
    item4: int | None = Field(None)
    item5: int | None = Field(None)
    item6: int | None = Field(None)
    itemsPurchased: int | None = Field(None)
    killingSprees: int | None = Field(None)
    kills: int | None = Field(None)
    lane: str | None = Field(None)
    largestCriticalStrike: int | None = Field(None)
    largestKillingSpree: int | None = Field(None)
    largestMultiKill: int | None = Field(None)
    longestTimeSpentLiving: int | None = Field(None)
    magicDamageDealt: int | None = Field(None)
    magicDamageDealtToChampions: int | None = Field(None)
    magicDamageTaken: int | None = Field(None)
    missions: MissionsDto | None = Field(None)
    neutralMinionsKilled: int | None = Field(None,
                                             description='neutralMinionsKilled = mNeutralMinionsKilled, which is incremented on kills of kPet and kJungleMonster')
    needVisionPings: int | None = Field(None, description='Green ward')
    nexusKills: int | None = Field(None)
    nexusTakedowns: int | None = Field(None)
    nexusLost: int | None = Field(None)
    objectivesStolen: int | None = Field(None)
    objectivesStolenAssists: int | None = Field(None)
    onMyWayPings: int | None = Field(None, description='Blue arrow pointing at ground')
    participantId: int | None = Field(None)
    playerScore0: int | None = Field(None)
    playerScore1: int | None = Field(None)
    playerScore2: int | None = Field(None)
    playerScore3: int | None = Field(None)
    playerScore4: int | None = Field(None)
    playerScore5: int | None = Field(None)
    playerScore6: int | None = Field(None)
    playerScore7: int | None = Field(None)
    playerScore8: int | None = Field(None)
    playerScore9: int | None = Field(None)
    playerScore10: int | None = Field(None)
    playerScore11: int | None = Field(None)
    pentaKills: int | None = Field(None)
    perks: PerksDto | None = Field(None)
    physicalDamageDealt: int | None = Field(None)
    physicalDamageDealtToChampions: int | None = Field(None)
    physicalDamageTaken: int | None = Field(None)
    placement: int | None = Field(None)
    playerAugment1: int | None = Field(None)
    playerAugment2: int | None = Field(None)
    playerAugment3: int | None = Field(None)
    playerAugment4: int | None = Field(None)
    playerSubteamId: int | None = Field(None)
    pushPings: int | None = Field(None, description='Green minion')
    profileIcon: int | None = Field(None)
    puuid: str | None = Field(None)
    quadraKills: int | None = Field(None)
    riotIdGameName: str | None = Field(None)
    riotIdTagline: str | None = Field(None)
    role: str | None = Field(None)
    sightWardsBoughtInGame: int | None = Field(None)
    spell1Casts: int | None = Field(None)
    spell2Casts: int | None = Field(None)
    spell3Casts: int | None = Field(None)
    spell4Casts: int | None = Field(None)
    subteamPlacement: int | None = Field(None)
    summoner1Casts: int | None = Field(None)
    summoner1Id: int | None = Field(None)
    summoner2Casts: int | None = Field(None)
    summoner2Id: int | None = Field(None)
    summonerId: str | None = Field(None)
    summonerLevel: int | None = Field(None)
    summonerName: str | None = Field(None)
    teamEarlySurrendered: bool | None = Field(None)
    teamId: int | None = Field(None)
    teamPosition: str | None = Field(None,
                                     description='Both individualPosition and teamPosition are computed by the game server and are different versions of the most likely position played by a player. The individualPosition is the best guess for which position the player actually played in isolation of anything else. The teamPosition is the best guess for which position the player actually played if we add the constraint that each team must have one top player, one jungle, one middle, etc. Generally the recommendation is to use the teamPosition field over the individualPosition field.')
    timeCCingOthers: int | None = Field(None)
    timePlayed: int | None = Field(None)
    totalAllyJungleMinionsKilled: int | None = Field(None)
    totalDamageDealt: int | None = Field(None)
    totalDamageDealtToChampions: int | None = Field(None)
    totalDamageShieldedOnTeammates: int | None = Field(None)
    totalDamageTaken: int | None = Field(None)
    totalEnemyJungleMinionsKilled: int | None = Field(None)
    totalHeal: int | None = Field(None,
                                  description='Whenever positive health is applied (which translates to all heals in the game but not things like regeneration), totalHeal is incremented by the amount of health received. This includes healing enemies, jungle monsters, yourself, etc')
    totalHealsOnTeammates: int | None = Field(None,
                                              description='Whenever positive health is applied (which translates to all heals in the game but not things like regeneration), totalHealsOnTeammates is incremented by the amount of health received.  This is post modified, so if you heal someone missing 5 health for 100 you will get +5 totalHealsOnTeammates')
    totalMinionsKilled: int | None = Field(None,
                                           description='totalMillionsKilled = mMinionsKilled, which is only incremented on kills of kTeamMinion, kMeleeLaneMinion, kSuperLaneMinion, kRangedLaneMinion and kSiegeLaneMinion')
    totalTimeCCDealt: int | None = Field(None)
    totalTimeSpentDead: int | None = Field(None)
    totalUnitsHealed: int | None = Field(None)
    tripleKills: int | None = Field(None)
    trueDamageDealt: int | None = Field(None)
    trueDamageDealtToChampions: int | None = Field(None)
    trueDamageTaken: int | None = Field(None)
    turretKills: int | None = Field(None)
    turretTakedowns: int | None = Field(None)
    turretsLost: int | None = Field(None)
    unrealKills: int | None = Field(None)
    visionScore: int | None = Field(None)
    visionClearedPings: int | None = Field(None)
    visionWardsBoughtInGame: int | None = Field(None)
    wardsKilled: int | None = Field(None)
    wardsPlaced: int | None = Field(None)
    win: bool | None = Field(None)

    # noinspection PyNestedDecorators
    @field_validator('challenges', mode='before')
    def convert_values_to_str(cls, obj: dict | None) -> dict[str, str] | None:
        if obj is None:
            return None

        return {key: repr(val) for key, val in obj.items()}


class InfoDto(BaseModel):
    endOfGameResult: str | None = Field(None, description='Refer to indicate if the game ended in termination.')
    gameCreation: int | None = Field(None,
                                     description='Unix timestamp for when the game is created on the game server (i.e., the loading screen).')
    gameDuration: int | None = Field(None,
                                     description='Prior to patch 11.20, this field returns the game length in milliseconds calculated from gameEndTimestamp - gameStartTimestamp. Post patch 11.20, this field returns the max timePlayed of any participant in the game in seconds, which makes the behavior of this field consistent with that of match-v4. The best way to handling the change in this field is to treat the value as milliseconds if the gameEndTimestamp field isn\'t in the response and to treat the value as seconds if gameEndTimestamp is in the response.')
    gameEndTimestamp: int | None = Field(None,
                                         description='Unix timestamp for when match ends on the game server. This timestamp can occasionally be significantly longer than when the match "ends". The most reliable way of determining the timestamp for the end of the match would be to add the max time played of any participant to the gameStartTimestamp. This field was added to match-v5 in patch 11.20 on Oct 5th, 2021.')
    gameId: int | None = Field(None)
    gameMode: str | None = Field(None, description='Refer to the Game Constants documentation.')
    gameName: str | None = Field(None)
    gameStartTimestamp: int | None = Field(None, description='Unix timestamp for when match starts on the game server.')
    gameType: str | None = Field(None)
    gameVersion: str | None = Field(None,
                                    description='The first two parts can be used to determine the patch a game was played on.')
    mapId: int | None = Field(None, description='Refer to the Game Constants documentation.')
    participants: List[ParticipantDto] | None = Field(None)
    platformId: str | None = Field(None, description='Platform where the match was played.')
    queueId: int | None = Field(None, description='Refer to the Game Constants documentation.')
    teams: List[TeamDto] | None = Field(None)
    tournamentCode: str | None = Field(None,
                                       description='Tournament code used to generate the match. This field was added to match-v5 in patch 11.13 on June 23rd, 2021.')


class MetadataDto(BaseModel):
    dataVersion: str | None = Field(None, description='Match data version.')
    matchId: str | None = Field(None, description='Match id.')
    participants: List[str] | None = Field(None, description='A list of participant PUUIDs.')


class MatchDto(BaseModel):
    metadata: MetadataDto | None = Field(None, description='Match metadata.')
    info: InfoDto | None = Field(None, description='Match info.')


# Timeline models

class PositionDto(BaseModel):
    x: int | None = Field(None)
    y: int | None = Field(None)


class DamageStatsDto(BaseModel):
    magicDamageDone: int | None = Field(None)
    magicDamageDoneToChampions: int | None = Field(None)
    magicDamageTaken: int | None = Field(None)
    physicalDamageDone: int | None = Field(None)
    physicalDamageDoneToChampions: int | None = Field(None)
    physicalDamageTaken: int | None = Field(None)
    totalDamageDone: int | None = Field(None)
    totalDamageDoneToChampions: int | None = Field(None)
    totalDamageTaken: int | None = Field(None)
    trueDamageDone: int | None = Field(None)
    trueDamageDoneToChampions: int | None = Field(None)
    trueDamageTaken: int | None = Field(None)


class ChampionStatsDto(BaseModel):
    abilityHaste: int | None = Field(None)
    abilityPower: int | None = Field(None)
    armor: int | None = Field(None)
    armorPen: int | None = Field(None)
    armorPenPercent: int | None = Field(None)
    attackDamage: int | None = Field(None)
    attackSpeed: int | None = Field(None)
    bonusArmorPenPercent: int | None = Field(None)
    bonusMagicPenPercent: int | None = Field(None)
    ccReduction: int | None = Field(None)
    cooldownReduction: int | None = Field(None)
    health: int | None = Field(None)
    healthMax: int | None = Field(None)
    healthRegen: int | None = Field(None)
    lifesteal: int | None = Field(None)
    magicPen: int | None = Field(None)
    magicPenPercent: int | None = Field(None)
    magicResist: int | None = Field(None)
    movementSpeed: int | None = Field(None)
    omnivamp: int | None = Field(None)
    physicalVamp: int | None = Field(None)
    power: int | None = Field(None)
    powerMax: int | None = Field(None)
    powerRegen: int | None = Field(None)
    spellVamp: int | None = Field(None)


class ParticipantFrameDto(BaseModel):
    championStats: ChampionStatsDto | None = Field(None)
    currentGold: int | None = Field(None)
    damageStats: DamageStatsDto | None = Field(None)
    goldPerSecond: int | None = Field(None)
    jungleMinionsKilled: int | None = Field(None)
    level: int | None = Field(None)
    minionsKilled: int | None = Field(None)
    participantId: int | None = Field(None)
    position: PositionDto | None = Field(None)
    timeEnemySpentControlled: int | None = Field(None)
    totalGold: int | None = Field(None)
    xp: int | None = Field(None)


class ParticipantFramesDto(BaseModel):
    ParticipantFrameDto1: ParticipantFrameDto | None = Field(None, alias='1',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto2: ParticipantFrameDto | None = Field(None, alias='2',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto3: ParticipantFrameDto | None = Field(None, alias='3',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto4: ParticipantFrameDto | None = Field(None, alias='4',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto5: ParticipantFrameDto | None = Field(None, alias='5',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto6: ParticipantFrameDto | None = Field(None, alias='6',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto7: ParticipantFrameDto | None = Field(None, alias='7',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto8: ParticipantFrameDto | None = Field(None, alias='8',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto9: ParticipantFrameDto | None = Field(None, alias='9',
                                                             description='Key value mapping for each participant')
    ParticipantFrameDto10: ParticipantFrameDto | None = Field(None, alias='10',
                                                              description='Key value mapping for each participant')


class EventsTimeLineDto(BaseModel):
    timestamp: int | None = Field(None)
    realTimestamp: int | None = Field(None)
    type: str | None = Field(None)


class FramesTimeLineDto(BaseModel):
    events: List[EventsTimeLineDto] | None = Field(None)
    participantFrames: ParticipantFramesDto | None = Field(None)
    timestamp: int | None = Field(None)


class ParticipantTimeLineDto(BaseModel):
    participantId: int | None = Field(None)
    puuid: str | None = Field(None)


class InfoTimeLineDto(BaseModel):
    endOfGameResult: str | None = Field(None, description='Refer to indicate if the game ended in termination.')
    frameInterval: int | None = Field(None)
    gameId: int | None = Field(None)
    participants: List[ParticipantTimeLineDto] | None = Field(None)
    frames: List[FramesTimeLineDto] | None = Field(None)


class MetadataTimeLineDto(BaseModel):
    dataVersion: str | None = Field(None, description='Match data version.')
    matchId: str | None = Field(None, description='Match id.')
    participants: List[str] | None = Field(None, description='A list of participant PUUIDs.')


class TimelineDto(BaseModel):
    metadata: MetadataTimeLineDto | None = Field(None, description='Match metadata.')
    info: InfoTimeLineDto | None = Field(None, description='Match info.')
