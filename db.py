from datetime import datetime
from typing import List, Union

from sqlmodel import SQLModel, Field, create_engine, Relationship

from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB


class Match(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    # MetadataDto
    dataVersion: str | None = Field(None, description='Match data version.')
    matchId: str | None = Field(None, description='Match id.', unique=True)  # Unique constraint added

    # InfoDto
    endOfGameResult: str | None = Field(None, description='Refer to indicate if the game ended in termination.')
    gameCreation: datetime | None = Field(None,
                                          description='Unix timestamp for when the game is created on the game server (i.e., the loading screen).')
    gameDuration: int | None = Field(None,
                                     description='Prior to patch 11.20, this field returns the game length in milliseconds calculated from gameEndTimestamp - gameStartTimestamp. Post patch 11.20, this field returns the max timePlayed of any participant in the game in seconds, which makes the behavior of this field consistent with that of match-v4. The best way to handling the change in this field is to treat the value as milliseconds if the gameEndTimestamp field isn\'t in the response and to treat the value as seconds if gameEndTimestamp is in the response.')
    gameEndTimestamp: datetime | None = Field(None,
                                              description='Unix timestamp for when match ends on the game server. This timestamp can occasionally be significantly longer than when the match "ends". The most reliable way of determining the timestamp for the end of the match would be to add the max time played of any participant to the gameStartTimestamp. This field was added to match-v5 in patch 11.20 on Oct 5th, 2021.')
    gameId: int | None = Field(None)
    gameMode: str | None = Field(None, description='Refer to the Game Constants documentation.')
    gameName: str | None = Field(None)
    gameStartTimestamp: datetime | None = Field(None,
                                                description='Unix timestamp for when match starts on the game server.')
    gameType: str | None = Field(None)
    gameVersion: str | None = Field(None,
                                    description='The first two parts can be used to determine the patch a game was played on.')
    mapId: int | None = Field(None, description='Refer to the Game Constants documentation.')
    platformId: str | None = Field(None, description='Platform where the match was played.')
    queueId: int | None = Field(None, description='Refer to the Game Constants documentation.')
    tournamentCode: str | None = Field(None,
                                       description='Tournament code used to generate the match. This field was added to match-v5 in patch 11.13 on June 23rd, 2021.')

    # InfoTimeLineDto
    frameInterval: int | None = Field(None)

    # List[ParticipantDto]
    participants: List['Participant'] | None = Relationship(back_populates='match')
    # List[TeamDto]
    teams: List['Team'] | None = Relationship(back_populates='match')
    # List[FramesTimeLineDto]
    frames: List['Frame'] | None = Relationship(back_populates='match')


class ChallengeParticipantLink(SQLModel, table=True):
    value: str | None = Field(None)

    challenge_id: int | None = Field(default=None, foreign_key='challenge.id', primary_key=True)
    challenge: Union['Challenge', None] = Relationship(back_populates='participant_links')
    participant_id: int | None = Field(default=None, foreign_key='participant.id', primary_key=True)
    participant: Union['Participant', None] = Relationship(back_populates='challenge_links')


class AssistingParticipantsLink(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key='event.id', primary_key=True)
    participant_id: int | None = Field(default=None, foreign_key='participant.id', primary_key=True)


class Participant(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

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
    physicalDamageDealt: int | None = Field(None)
    physicalDamageDealtToChampions: int | None = Field(None)
    physicalDamageTaken: int | None = Field(None)
    placement: int | None = Field(None)
    playerAugment1: int | None = Field(None)
    playerAugment2: int | None = Field(None)
    playerAugment3: int | None = Field(None)
    playerAugment4: int | None = Field(None)
    playerAugment5: int | None = Field(None)
    playerAugment6: int | None = Field(None)
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
    teamId: int | None = Field(None, foreign_key='team.id')
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

    # extra
    basicPings: int | None = Field(None)
    dangerPings: int | None = Field(None)
    retreatPings: int | None = Field(None)
    baitPings: int | None = Field(None)
    riotIdName: str | None = Field(None)

    # PerkStatsDto
    defenseStat: int | None = Field(None, alias='defense')
    flexStat: int | None = Field(None, alias='flex')
    offenseStat: int | None = Field(None, alias='offense')

    match_id: int | None = Field(None, foreign_key='match.id')
    match: Match | None = Relationship(back_populates='participants')
    team: Union['Team', None] = Relationship(back_populates='participants')

    # dict[str, str]
    challenge_links: List[ChallengeParticipantLink] | None = Relationship(back_populates='participant')
    # MissionsDto
    missions: Union['Missions', None] = Relationship(back_populates='participant')
    # PerksDto
    perks: List['Perk'] | None = Relationship(back_populates='participant')
    # List[ParticipantFramesDto]
    participant_frames: List['ParticipantFrame'] | None = Relationship(back_populates='participant')


class Challenge(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    name: str | None = Field(None, unique=True)

    participant_links: List[ChallengeParticipantLink] | None = Relationship(back_populates='challenge')


class Missions(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

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

    participant_id: int | None = Field(None, foreign_key='participant.id')
    participant: Participant | None = Relationship(back_populates='missions')


class Perk(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    description: str | None = Field(None)
    style: int | None = Field(None)

    perk: int | None = Field(None)
    var1: int | None = Field(None)
    var2: int | None = Field(None)
    var3: int | None = Field(None)

    participant_id: int | None = Field(None, foreign_key='participant.id')
    participant: Participant | None = Relationship(back_populates='perks')


class Team(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    teamId: int | None = Field(None)
    win: bool | None = Field(None)

    # ObjectivesDto
    baronFirst: bool | None = Field(None)
    baronKills: int | None = Field(None)
    championFirst: bool | None = Field(None)
    championKills: int | None = Field(None)
    dragonFirst: bool | None = Field(None)
    dragonKills: int | None = Field(None)
    hordeFirst: bool | None = Field(None)
    hordeKills: int | None = Field(None)
    inhibitorFirst: bool | None = Field(None)
    inhibitorKills: int | None = Field(None)
    riftHeraldFirst: bool | None = Field(None)
    riftHeraldKills: int | None = Field(None)
    towerFirst: bool | None = Field(None)
    towerKills: int | None = Field(None)

    # List[BanDto]
    bans: List['Ban'] | None = Relationship(back_populates='team')

    match_id: int | None = Field(None, foreign_key='match.id')
    match: Match | None = Relationship(back_populates='teams')

    # List[ParticipantDto]
    participants: List[Participant] | None = Relationship(back_populates='team')


class Ban(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    championId: int | None = Field(None)
    pickTurn: int | None = Field(None)

    team_id: int | None = Field(None, foreign_key='team.id')
    team: Team | None = Relationship(back_populates='bans')


class Frame(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    timestamp: int | None = Field(None)

    match_id: int | None = Field(None, foreign_key='match.id')
    match: Match | None = Relationship(back_populates='frames')

    # List[EventsTimeLineDto]
    events: List['Event'] | None = Relationship(back_populates='frame')
    # List[ParticipantFramesDto]
    participant_frames: List['ParticipantFrame'] | None = Relationship(back_populates='frame')


class Event(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    timestamp: int | None = Field(None)
    type: str | None = Field(None)

    realTimestamp: datetime | None = Field(None)
    gameId: int | None = Field(None, foreign_key='match.id')
    winningTeamId: int | None = Field(None, foreign_key='team.id')  # original name winningTeam
    itemId: int | None = Field(None)
    participantId: int | None = Field(None, foreign_key='participant.id')
    levelUpType: str | None = Field(None)
    skillSlot: int | None = Field(None)
    level: int | None = Field(None)
    creatorId: int | None = Field(None, foreign_key='participant.id')
    wardType: str | None = Field(None)
    killerId: int | None = Field(None, foreign_key='participant.id')
    killStreakLength: int | None = Field(None)
    x: int | None = Field(None)
    y: int | None = Field(None)
    bounty: int | None = Field(None)
    shutdownBounty: int | None = Field(None)
    victimDamageDealt: List['VictimDamageDealt'] | None = Relationship(back_populates='event')
    victimDamageReceived: List['VictimDamageReceived'] | None = Relationship(back_populates='event')
    victimId: int | None = Field(None, foreign_key='participant.id')
    teamId: int | None = Field(None, foreign_key='team.id')
    buildingType: str | None = Field(None)
    towerType: str | None = Field(None)
    laneType: str | None = Field(None)
    killType: str | None = Field(None)
    multiKillLength: int | None = Field(None)
    monsterType: str | None = Field(None)
    monsterSubType: str | None = Field(None)
    killerTeamId: int | None = Field(None, foreign_key='team.id')
    afterId: int | None = Field(None)
    beforeId: int | None = Field(None)
    goldGain: int | None = Field(None)
    actualStartTime: int | None = Field(None)
    name: str | None = Field(None)
    transformType: str | None = Field(None)

    game: Match | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.gameId]'})
    winningTeam: Team | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.winningTeamId]'})
    participant: Participant | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.participantId]'})
    creator: Participant | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.creatorId]'})
    killer: Participant | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.killerId]'})
    victim: Participant | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.victimId]'})
    team: Team | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.teamId]'})
    killerTeam: Team | None = Relationship(sa_relationship_kwargs={'foreign_keys': '[Event.killerTeamId]'})

    assistingParticipants: List[Participant] | None = Relationship(link_model=AssistingParticipantsLink)

    frame_id: int | None = Field(None, foreign_key='frame.id')
    frame: Frame | None = Relationship(back_populates='events')


class VictimDamageDealt(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    basic: bool | None = Field(None)
    magicDamage: int | None = Field(None)
    name: str | None = Field(None)
    participantId: int | None = Field(None, foreign_key='participant.id')
    physicalDamage: int | None = Field(None)
    spellName: str | None = Field(None)
    spellSlot: int | None = Field(None)
    trueDamage: int | None = Field(None)
    type: str | None = Field(None)

    event_id: int | None = Field(None, foreign_key='event.id')
    event: Event | None = Relationship(back_populates='victimDamageDealt')
    participant: Participant | None = Relationship()


class VictimDamageReceived(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    basic: bool | None = Field(None)
    magicDamage: int | None = Field(None)
    name: str | None = Field(None)
    participantId: int | None = Field(None, foreign_key='participant.id')
    physicalDamage: int | None = Field(None)
    spellName: str | None = Field(None)
    spellSlot: int | None = Field(None)
    trueDamage: int | None = Field(None)
    type: str | None = Field(None)

    event_id: int | None = Field(None, foreign_key='event.id')
    event: Event | None = Relationship(back_populates='victimDamageReceived')
    participant: Participant | None = Relationship()


class ParticipantFrame(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    # ParticipantFrameDto
    currentGold: int | None = Field(None)
    goldPerSecond: int | None = Field(None)
    jungleMinionsKilled: int | None = Field(None)
    level: int | None = Field(None)
    minionsKilled: int | None = Field(None)
    participantId: int | None = Field(None, foreign_key='participant.id')
    timeEnemySpentControlled: int | None = Field(None)
    totalGold: int | None = Field(None)
    xp: int | None = Field(None)

    # ChampionStatsDto
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

    # DamageStatsDto
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

    # PositionDto
    x: int | None = Field(None)
    y: int | None = Field(None)

    frame_id: int | None = Field(None, foreign_key='frame.id')
    frame: Frame | None = Relationship(back_populates='participant_frames')
    participant: Participant | None = Relationship(back_populates='participant_frames')


engine = create_engine(
    f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}',
    pool_recycle=3600
)


def drop_create_all():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    drop_create_all()
