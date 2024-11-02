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

    # List[ParticipantDto]
    participants: List['Participant'] | None = Relationship(back_populates='match')
    # List[TeamDto]
    teams: List['Team'] | None = Relationship(back_populates='match')


class ChallengeParticipantLink(SQLModel, table=True):
    value: str | None = Field(None)

    challenge_id: int | None = Field(default=None, foreign_key='challenge.id', primary_key=True)
    challenge: Union['Challenge', None] = Relationship(back_populates='participant_links')
    participant_id: int | None = Field(default=None, foreign_key='participant.id', primary_key=True)
    participant: Union['Participant', None] = Relationship(back_populates='challenge_links')


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
    # missions: MissionsDto | None = Field(None)
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

    # PerkStatsDto
    defenseStat: int | None = Field(None, alias='defense')
    flexStat: int | None = Field(None, alias='flex')
    offenseStat: int | None = Field(None, alias='offense')

    match_id: int | None = Field(None, foreign_key='match.id')
    match: Match | None = Relationship(back_populates='participants')

    # dict[str, str]
    challenge_links: List[ChallengeParticipantLink] | None = Relationship(back_populates='participant')
    # MissionsDto
    missions: Union['Missions', None] = Relationship(back_populates='participant')
    # PerksDto
    perks: List['Perk'] | None = Relationship(back_populates='participant')


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


class Ban(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    championId: int | None = Field(None)
    pickTurn: int | None = Field(None)

    team_id: int | None = Field(None, foreign_key='team.id')
    team: Team | None = Relationship(back_populates='bans')


engine = create_engine(
    f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}',
    pool_recycle=3600
)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
