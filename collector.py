import sys
import traceback
from enum import StrEnum

from requests import ConnectionError
from riotwatcher import LolWatcher, ApiError
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select

from config import get_logger, NOT_FOUNDED_EXIT, NOT_FOUNDED_ERROR, NOT_FOUNDED_WARNING
from db import (
    engine,
    Match,
    Participant,
    Challenge,
    ChallengeParticipantLink,
    Missions,
    Perk,
    Team,
    Ban,
    ParticipantFrame,
    Frame,
    Event,
    VictimDamageDealt,
    VictimDamageReceived
)
from handlers import PydanticDeserializer
from models import MatchDto, TimelineDto, FramesTimeLineDto, ParticipantDto

logger = get_logger(__name__)


class Region(StrEnum):
    brazil = 'BR'
    europe_north_east = 'EUNE'
    europe_west = 'EUW'
    japan = 'JP'
    korea = 'KR'
    latin_america_north = 'LAN'
    latin_america_south = 'LAS'
    north_america = 'NA'
    oceania = 'OCE'
    turkey = 'TR'
    russia = 'RU'
    philippines = 'PH'
    singapore = 'SG'
    thailand = 'TH'
    taiwan = 'TW'
    vietnam = 'VN'

    @property
    def platform(self) -> 'Platform':
        return getattr(Platform, self.name)

    def __repr__(self) -> str:
        return repr(self.value)


class Platform(StrEnum):
    brazil = 'BR1'
    europe_north_east = 'EUN1'
    europe_west = 'EUW1'
    japan = 'JP1'
    korea = 'KR'
    latin_america_north = 'LA1'
    latin_america_south = 'LA2'
    north_america = 'NA1'
    oceania = 'OC1'
    turkey = 'TR1'
    russia = 'RU'
    philippines = 'PH2'
    singapore = 'SG2'
    thailand = 'TH2'
    taiwan = 'TW2'
    vietnam = 'VN2'

    def __repr__(self) -> str:
        return repr(self.value)


class Collector:
    def __init__(self, *, api_key: str, region: Region):
        self.region = region
        self.api = LolWatcher(api_key, deserializer=PydanticDeserializer())

        self.index = -1
        self.last_founded = self.index

    # noinspection PyPep8Naming
    @property
    def matchId(self) -> str:
        return f'{self.region}_{self.index}'

    def get(self, method, *args, retry: int = 0, error: Exception = None, **kwargs) -> MatchDto | TimelineDto | None:
        if retry > 2:
            logger.error('All retries are exceeded')
            raise error

        try:
            result = method(*args, **kwargs)

            self.last_founded = self.index
            return result

        except ApiError as err:
            if err.response.status_code == 404:
                logger.info(
                    f'{method.__qualname__}('
                    f'{', '.join([repr(arg) for arg in args])}'
                    f'{', ' if args and kwargs else ''}'
                    f'{', '.join([f'{repr(key)}={repr(val)}' for key, val in kwargs.items()])}'
                    f') doesn\'t found entity'
                )

                if self.index - self.last_founded > NOT_FOUNDED_EXIT:
                    logger.critical(
                        f'NOT_FOUNDED_EXIT reached: last_founded = {self.last_founded}, index = {self.index}'
                    )
                    sys.exit()

                elif self.index - self.last_founded > NOT_FOUNDED_ERROR:
                    logger.error(
                        f'NOT_FOUNDED_ERROR reached: last_founded = {self.last_founded}, index = {self.index}'
                    )

                elif self.index - self.last_founded > NOT_FOUNDED_WARNING:
                    logger.warning(
                        f'NOT_FOUNDED_WARNING reached: last_founded = {self.last_founded}, index = {self.index}'
                    )

            else:
                logger.warning(f'HTTPError occurred while {retry} retry')
                return self.get(method, *args, retry=retry + 1, error=err, **kwargs)

        except ConnectionError as err:
            logger.warning(f'ConnectionError occurred while {retry} retry')
            return self.get(method, *args, retry=retry + 1, error=err, **kwargs)

    def get_match_and_timeline(self) -> tuple[None, None] | tuple[MatchDto, None] | tuple[MatchDto, TimelineDto]:
        params = {
            'region': self.region.platform,
            'match_id': self.matchId
        }

        match: MatchDto = self.get(self.api.match.by_id, **params)
        if not match:
            return None, None

        timeline: TimelineDto = self.get(self.api.match.timeline_by_match, **params)
        if not timeline:
            logger.error(f'timeline is None but match isn\'t with id = f{self.index}')
            return match, None

        logger.info(f'match and timeline with id = {self.index} are retrieved')
        return match, timeline

    @staticmethod
    def _get_challenges(match: MatchDto, session: Session) -> dict[str, Challenge]:
        challenges = set()
        for participant in match.info.participants:
            if participant.challenges is None:
                continue

            for challenge in participant.challenges:
                challenges.add(challenge)

        challenges_name_to_challenge = {}
        for challenge in challenges:
            statement = insert(Challenge).values(name=challenge)
            # noinspection PyDeprecation
            session.execute(statement.on_conflict_do_nothing(index_elements=['name']))

            # noinspection PyTypeChecker,Pydantic
            challenges_name_to_challenge[challenge] = session.exec(
                select(Challenge).where(Challenge.name == challenge)
            ).one()

        return challenges_name_to_challenge

    @staticmethod
    def _get_perks(participant: ParticipantDto) -> list[Perk]:
        perks_db = []
        for perk in participant.perks.styles:
            for selection in perk.selections:
                perk_db = Perk.model_validate(selection.model_dump())
                perk_db.description = perk.description
                perk_db.style = perk.style

                perks_db.append(perk_db)

        return perks_db

    def _get_participants(
            self, match: MatchDto, challenges_table: dict[str, Challenge], session: Session
    ) -> list[Participant]:
        participants: list[Participant] = []
        for participant in match.info.participants:

            participant_db = Participant.model_validate(participant.model_dump())
            participant_db.defenseStat = participant.perks.statPerks.defense
            participant_db.flexStat = participant.perks.statPerks.flex
            participant_db.offenseStat = participant.perks.statPerks.offense

            participant_db.perks = self._get_perks(participant)

            if participant.missions is not None:
                participant_db.missions = Missions.model_validate(participant.missions.model_dump())

            if participant.challenges is not None:
                for challenge_name, challenge_value in participant.challenges.items():
                    session.add(ChallengeParticipantLink(
                        value=challenge_value,
                        challenge=challenges_table[challenge_name],
                        participant=participant_db
                    ))

            participants.append(participant_db)

        return participants

    @staticmethod
    def _get_teams(match: MatchDto, participants: list[Participant]) -> list[Team]:
        teams: list[Team] = []
        for team in match.info.teams:
            team_db = Team.model_validate(team.model_dump())

            team_db.baronFirst = team.objectives.baron.first
            team_db.baronKills = team.objectives.baron.kills
            team_db.championFirst = team.objectives.champion.first
            team_db.championKills = team.objectives.champion.kills
            team_db.dragonFirst = team.objectives.dragon.first
            team_db.dragonKills = team.objectives.dragon.kills
            if team.objectives.horde is not None:
                team_db.hordeFirst = team.objectives.horde.first
                team_db.hordeKills = team.objectives.horde.kills
            team_db.inhibitorFirst = team.objectives.inhibitor.first
            team_db.inhibitorKills = team.objectives.inhibitor.kills
            team_db.riftHeraldFirst = team.objectives.riftHerald.first
            team_db.riftHeraldKills = team.objectives.riftHerald.kills
            team_db.towerFirst = team.objectives.tower.first
            team_db.towerKills = team.objectives.tower.kills

            team_db.bans = [Ban.model_validate(ban.model_dump()) for ban in team.bans]
            team_db.participants = [participant for participant in participants if participant.teamId == team.teamId]

            teams.append(team_db)

        return teams

    @staticmethod
    def _get_victim_damages_dealt(
            event: Event, participant_id_to_participant: dict[int, Participant]
    ) -> list[VictimDamageDealt]:
        victim_damages_dealt_db = []
        for victim_damage_dealt in event.victimDamageDealt:
            victim_damage_dealt_db = VictimDamageDealt.model_validate(
                victim_damage_dealt.model_dump()
            )
            victim_damage_dealt_db.participant = participant_id_to_participant[
                victim_damage_dealt.participantId
            ] if victim_damage_dealt.participantId != 0 else None

            victim_damages_dealt_db.append(victim_damage_dealt_db)

        return victim_damages_dealt_db

    @staticmethod
    def _get_victim_damages_received(
            event: Event, participant_id_to_participant: dict[int, Participant]
    ) -> list[VictimDamageReceived]:
        victim_damages_received_db = []
        for victim_damage_received in event.victimDamageReceived:
            victim_damage_received_db = VictimDamageReceived.model_validate(
                victim_damage_received.model_dump()
            )

            victim_damage_received_db.participant = participant_id_to_participant[
                victim_damage_received.participantId
            ] if victim_damage_received.participantId != 0 else None

            victim_damages_received_db.append(victim_damage_received_db)

        return victim_damages_received_db

    def _get_events(
            self,
            match: Match,
            frame: FramesTimeLineDto,
            participant_id_to_participant: dict[int, Participant],
            team_id_to_team: dict[int, Team]
    ) -> list[Event]:
        events_db = []
        for event in frame.events:
            event_db = Event.model_validate(event.model_dump())

            if event.victimDamageDealt:
                event_db.victimDamageDealt = self._get_victim_damages_dealt(event, participant_id_to_participant)

            if event.victimDamageReceived:
                event_db.victimDamageReceived = self._get_victim_damages_received(event, participant_id_to_participant)

            if event.position:
                event_db.x = event.position.x
                event_db.y = event.position.y

            event_db.game = match
            event_db.winningTeam = team_id_to_team.get(event.winningTeam)
            event_db.participant = participant_id_to_participant.get(event.participantId)
            event_db.creator = participant_id_to_participant.get(event.creatorId)
            event_db.killer = participant_id_to_participant.get(event.killerId)
            event_db.victim = participant_id_to_participant.get(event.victimId)
            event_db.team = team_id_to_team.get(event.teamId)
            event_db.killerTeam = team_id_to_team.get(event.killerTeamId)

            if event.assistingParticipantIds:
                event_db.assistingParticipants = [
                    participant_id_to_participant[participant_id]
                    for participant_id
                    in set(event.assistingParticipantIds)
                ]

            events_db.append(event_db)

        return events_db

    @staticmethod
    def _get_participant_frames(
            frame: FramesTimeLineDto, participant_id_to_participant: dict[int, Participant]
    ) -> list[ParticipantFrame]:
        participant_frames_db = []
        for participant_id, participant_frames in frame.participantFrames.items():
            participant_frame_db = ParticipantFrame.model_validate(
                participant_frames.model_dump() |
                participant_frames.championStats.model_dump() |
                participant_frames.damageStats.model_dump() |
                participant_frames.position.model_dump()
            )

            participant_frame_db.participant = participant_id_to_participant[participant_frames.participantId]
            participant_frames_db.append(participant_frame_db)

        return participant_frames_db

    def _get_frames(
            self, timeline: TimelineDto, match: Match, participants: list[Participant], teams: list[Team]
    ) -> list[Frame]:
        participant_id_to_participant = {participant.participantId: participant for participant in participants}
        team_id_to_team = {team.teamId: team for team in teams}

        frames_db = []
        for frame in timeline.info.frames:
            frame_db = Frame(timestamp=frame.timestamp)

            frame_db.events = self._get_events(match, frame, participant_id_to_participant, team_id_to_team)
            frame_db.participant_frames = self._get_participant_frames(frame, participant_id_to_participant)

            frames_db.append(frame_db)

        return frames_db

    # noinspection PyPep8Naming
    def is_match_in_db(self) -> bool:
        with Session(engine) as session:
            # noinspection PyTypeChecker,Pydantic
            if session.exec(select(Match).where(Match.matchId == self.matchId)).one_or_none() is not None:
                logger.warning(f'match with id = {self.index} and matchId = {self.matchId} already in db')
                return True

        return False

    def insert(self, match: MatchDto, timeline: TimelineDto):
        if match is None or timeline is None:
            return

        with Session(engine) as session:
            match_db = Match.model_validate(match.info.model_dump() | match.metadata.model_dump())

            challenges = self._get_challenges(match, session)
            participants = self._get_participants(match, challenges, session)
            teams = self._get_teams(match, participants)
            frames = self._get_frames(timeline, match_db, participants, teams)

            match_db.frameInterval = timeline.info.frameInterval
            match_db.participants = participants
            match_db.teams = teams
            match_db.frames = frames

            session.add(match_db)
            session.commit()

        logger.info(f'match and timeline with id = {self.index} are inserted')

    def start(self, start_id: int):
        self.index = start_id
        self.last_founded = self.index - 1

        while True:
            try:
                if not self.is_match_in_db():
                    match, timeline = self.get_match_and_timeline()
                    self.insert(match, timeline)

            except Exception as err:
                logger.error(f'unexpected error {err}: {traceback.format_exc()}')

            # break
            self.index += 1
