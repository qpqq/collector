from datetime import datetime, UTC
from typing import List, Union

from pydantic import field_validator
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import SQLModel, Field, Column, Enum, Relationship, create_engine, Session, select

from config import get_logger
from enums import Region, GameMode, GameType, Lane, LaneDB, Role, Tower
from models import MatchDto

logger = get_logger(__name__)


def utcnow() -> datetime:
    return datetime.now(UTC)


class Match(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    inserted: datetime = Field(default_factory=utcnow)

    # MetadataDto
    dataVersion: str | None = None
    matchId: str | None = Field(None, unique=True)  # Unique constraint added

    # InfoDto
    endOfGameResult: str | None = None
    gameCreation: datetime | None = None
    gameDuration: int | None = None
    gameEndTimestamp: datetime | None = None
    gameId: int | None = None
    gameMode: GameMode | None = Field(None, sa_column=Column(Enum(GameMode)))
    gameName: str | None = None
    gameStartTimestamp: datetime | None = None
    gameType: GameType | None = Field(None, sa_column=Column(Enum(GameType)))
    gameVersion: str | None = None
    mapId: int | None = None
    platformId: Region | None = Field(None, sa_column=Column(Enum(Region)))
    queueId: int | None = None
    tournamentCode: str | None = None

    # InfoTimeLineDto
    frameInterval: int | None = None

    # List[ParticipantDto]
    participants: List['Participant'] | None = Relationship(back_populates='match')
    # List[TeamDto]
    teams: List['Team'] | None = Relationship(back_populates='match')
    # List[FramesTimeLineDto]
    frames: List['Frame'] | None = Relationship(back_populates='match')


class ChallengeParticipantLink(SQLModel, table=True):
    value: str | None = None

    challenge_id: int | None = Field(default=None, foreign_key='challenge.id', primary_key=True)
    challenge: 'Challenge' = Relationship(back_populates='participant_links')
    participant_id: int | None = Field(default=None, foreign_key='participant.id', primary_key=True)
    participant: 'Participant' = Relationship(back_populates='challenge_links')


class AssistingParticipantsLink(SQLModel, table=True):
    event_id: int | None = Field(default=None, foreign_key='event.id', primary_key=True)
    participant_id: int | None = Field(default=None, foreign_key='participant.id', primary_key=True)


class Participant(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    allInPings: int | None = None
    assistMePings: int | None = None
    assists: int | None = None
    baronKills: int | None = None
    bountyLevel: int | None = None
    champExperience: int | None = None
    champLevel: int | None = None
    championId: int | None = None
    championName: str | None = None
    commandPings: int | None = None
    championTransform: int | None = None
    consumablesPurchased: int | None = None
    damageDealtToBuildings: int | None = None
    damageDealtToObjectives: int | None = None
    damageDealtToTurrets: int | None = None
    damageSelfMitigated: int | None = None
    deaths: int | None = None
    detectorWardsPlaced: int | None = None
    doubleKills: int | None = None
    dragonKills: int | None = None
    eligibleForProgression: bool | None = None
    enemyMissingPings: int | None = None
    enemyVisionPings: int | None = None
    firstBloodAssist: bool | None = None
    firstBloodKill: bool | None = None
    firstTowerAssist: bool | None = None
    firstTowerKill: bool | None = None
    gameEndedInEarlySurrender: bool | None = None
    gameEndedInSurrender: bool | None = None
    holdPings: int | None = None
    getBackPings: int | None = None
    goldEarned: int | None = None
    goldSpent: int | None = None
    individualPosition: LaneDB | None = Field(None, sa_column=Column(Enum(LaneDB)))
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
    lane: LaneDB | None = Field(None, sa_column=Column(Enum(LaneDB)))
    largestCriticalStrike: int | None = None
    largestKillingSpree: int | None = None
    largestMultiKill: int | None = None
    longestTimeSpentLiving: int | None = None
    magicDamageDealt: int | None = None
    magicDamageDealtToChampions: int | None = None
    magicDamageTaken: int | None = None
    neutralMinionsKilled: int | None = None
    needVisionPings: int | None = None
    nexusKills: int | None = None
    nexusTakedowns: int | None = None
    nexusLost: int | None = None
    objectivesStolen: int | None = None
    objectivesStolenAssists: int | None = None
    onMyWayPings: int | None = None
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
    pushPings: int | None = None
    profileIcon: int | None = None
    puuid: str | None = None
    quadraKills: int | None = None
    riotIdGameName: str | None = None
    riotIdTagline: str | None = None
    role: Role | None = Field(None, sa_column=Column(Enum(Role)))
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
    teamId: int | None = Field(None, foreign_key='team.id')
    teamPosition: LaneDB | None = Field(None, sa_column=Column(Enum(LaneDB)))
    timeCCingOthers: int | None = None
    timePlayed: int | None = None
    totalAllyJungleMinionsKilled: int | None = None
    totalDamageDealt: int | None = None
    totalDamageDealtToChampions: int | None = None
    totalDamageShieldedOnTeammates: int | None = None
    totalDamageTaken: int | None = None
    totalEnemyJungleMinionsKilled: int | None = None
    totalHeal: int | None = None
    totalHealsOnTeammates: int | None = None
    totalMinionsKilled: int | None = None
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

    # extra
    basicPings: int | None = None
    dangerPings: int | None = None
    retreatPings: int | None = None
    baitPings: int | None = None
    riotIdName: str | None = None

    # PerkStatsDto
    defenseStat: int | None = Field(None, alias='defense')
    flexStat: int | None = Field(None, alias='flex')
    offenseStat: int | None = Field(None, alias='offense')

    @field_validator('individualPosition', 'lane', 'teamPosition', mode='before')
    def convert_values_to_str(cls, position: Lane | None) -> LaneDB | None:
        return LaneDB.from_lane(position)

    match_id: int | None = Field(None, foreign_key='match.id')
    match: Match = Relationship(back_populates='participants')
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

    participant_id: int | None = Field(None, foreign_key='participant.id')
    participant: Participant = Relationship(back_populates='missions')


class Perk(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    description: str | None = None
    style: int | None = None

    perk: int | None = None
    var1: int | None = None
    var2: int | None = None
    var3: int | None = None

    participant_id: int | None = Field(None, foreign_key='participant.id')
    participant: Participant = Relationship(back_populates='perks')


class Team(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    teamId: int | None = None
    win: bool | None = None

    # ObjectivesDto
    baronFirst: bool | None = None
    baronKills: int | None = None
    championFirst: bool | None = None
    championKills: int | None = None
    dragonFirst: bool | None = None
    dragonKills: int | None = None
    hordeFirst: bool | None = None
    hordeKills: int | None = None
    inhibitorFirst: bool | None = None
    inhibitorKills: int | None = None
    riftHeraldFirst: bool | None = None
    riftHeraldKills: int | None = None
    towerFirst: bool | None = None
    towerKills: int | None = None

    # List[BanDto]
    bans: List['Ban'] | None = Relationship(back_populates='team')

    match_id: int | None = Field(None, foreign_key='match.id')
    match: Match = Relationship(back_populates='teams')

    # List[ParticipantDto]
    participants: List[Participant] | None = Relationship(back_populates='team')


class Ban(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    championId: int | None = None
    pickTurn: int | None = None

    team_id: int | None = Field(None, foreign_key='team.id')
    team: Team = Relationship(back_populates='bans')


class Frame(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    timestamp: int | None = None

    match_id: int | None = Field(None, foreign_key='match.id')
    match: Match = Relationship(back_populates='frames')

    # List[EventsTimeLineDto]
    events: List['Event'] | None = Relationship(back_populates='frame')
    # List[ParticipantFramesDto]
    participant_frames: List['ParticipantFrame'] | None = Relationship(back_populates='frame')


class Event(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    timestamp: int | None = None
    type: str | None = None

    realTimestamp: datetime | None = None
    gameId: int | None = Field(None, foreign_key='match.id')
    winningTeamId: int | None = Field(None, foreign_key='team.id')  # original name winningTeam
    itemId: int | None = None
    participantId: int | None = Field(None, foreign_key='participant.id')
    levelUpType: str | None = None
    skillSlot: int | None = None
    level: int | None = None
    creatorId: int | None = Field(None, foreign_key='participant.id')
    wardType: str | None = None
    killerId: int | None = Field(None, foreign_key='participant.id')
    killStreakLength: int | None = None
    x: int | None = None
    y: int | None = None
    bounty: int | None = None
    shutdownBounty: int | None = None
    victimDamageDealt: List['VictimDamageDealt'] | None = Relationship(back_populates='event')
    victimDamageReceived: List['VictimDamageReceived'] | None = Relationship(back_populates='event')
    victimId: int | None = Field(None, foreign_key='participant.id')
    teamId: int | None = Field(None, foreign_key='team.id')
    buildingType: str | None = None
    towerType: Tower | None = Field(None, sa_column=Column(Enum(Tower)))
    laneType: str | None = None
    killType: str | None = None
    multiKillLength: int | None = None
    monsterType: str | None = None
    monsterSubType: str | None = None
    killerTeamId: int | None = Field(None, foreign_key='team.id')
    afterId: int | None = None
    beforeId: int | None = None
    goldGain: int | None = None
    actualStartTime: int | None = None
    name: str | None = None
    transformType: str | None = None

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
    frame: Frame = Relationship(back_populates='events')


class VictimDamageDealt(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    basic: bool | None = None
    magicDamage: int | None = None
    name: str | None = None
    participantId: int | None = Field(None, foreign_key='participant.id')
    physicalDamage: int | None = None
    spellName: str | None = None
    spellSlot: int | None = None
    trueDamage: int | None = None
    type: str | None = None

    event_id: int | None = Field(None, foreign_key='event.id')
    event: Event = Relationship(back_populates='victimDamageDealt')
    participant: Participant | None = Relationship()


class VictimDamageReceived(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    basic: bool | None = None
    magicDamage: int | None = None
    name: str | None = None
    participantId: int | None = Field(None, foreign_key='participant.id')
    physicalDamage: int | None = None
    spellName: str | None = None
    spellSlot: int | None = None
    trueDamage: int | None = None
    type: str | None = None

    event_id: int | None = Field(None, foreign_key='event.id')
    event: Event = Relationship(back_populates='victimDamageReceived')
    participant: Participant | None = Relationship()


class ParticipantFrame(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    # ParticipantFrameDto
    currentGold: int | None = None
    goldPerSecond: int | None = None
    jungleMinionsKilled: int | None = None
    level: int | None = None
    minionsKilled: int | None = None
    participantId: int | None = Field(None, foreign_key='participant.id')
    timeEnemySpentControlled: int | None = None
    totalGold: int | None = None
    xp: int | None = None

    # ChampionStatsDto
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

    # DamageStatsDto
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

    # PositionDto
    x: int | None = None
    y: int | None = None

    frame_id: int | None = Field(None, foreign_key='frame.id')
    frame: Frame = Relationship(back_populates='participant_frames')
    participant: Participant = Relationship(back_populates='participant_frames')


class DB:
    def __init__(self, postgres_user, postgres_password, postgres_host, postgres_database):
        self.engine = create_engine(
            f'postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_database}',
            pool_recycle=3600
        )

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def drop_tables(self):
        SQLModel.metadata.drop_all(self.engine)

    # noinspection PyPep8Naming
    def is_match_in_db(self, matchId: str) -> bool:
        with Session(self.engine) as session:
            # noinspection PyTypeChecker,Pydantic
            if session.exec(select(Match).where(Match.matchId == matchId)).one_or_none() is not None:
                return True

        return False

    def add_challenges(self, match: MatchDto) -> dict[str, Challenge]:
        challenges = set()
        for participant in match.info.participants:
            if participant.challenges is None:
                continue

            for challenge in participant.challenges:
                challenges.add(challenge)

        challenges_name_to_challenge = {}
        with Session(self.engine) as session:
            for challenge in challenges:
                statement = insert(Challenge).values(name=challenge)
                # noinspection PyDeprecation
                session.execute(statement.on_conflict_do_nothing(index_elements=['name']))

                # noinspection PyTypeChecker,Pydantic
                challenges_name_to_challenge[challenge] = session.exec(
                    select(Challenge).where(Challenge.name == challenge)
                ).one()

            session.commit()

        return challenges_name_to_challenge

    def add_match(self, match: Match):
        with Session(self.engine) as session:
            session.add(match)
            session.commit()
