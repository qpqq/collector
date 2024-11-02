import sys
import traceback

from requests import ConnectionError
from riotwatcher import LolWatcher, ApiError
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select

from config import get_logger, NOT_FOUNDED_EXIT, NOT_FOUNDED_ERROR, NOT_FOUNDED_WARNING
from db import engine, Match, Participant, Challenge, ChallengeParticipantLink, Missions, Perk, Team, Ban
from handlers import PydanticDeserializer
from models import MatchDto, TimelineDto

logger = get_logger(__name__)


class Collector:
    def __init__(self, *, api_key: str, region: str):
        self.region = region
        self.api = LolWatcher(api_key, deserializer=PydanticDeserializer())

        self.index = -1
        self.last_founded = self.index

    def get(self, method, *args, retry: int = 0, error: Exception = None, **kwargs):
        if retry > 2:
            raise error

        try:
            result = method(*args, **kwargs)

            self.last_founded = self.index
            return result

        except ApiError as err:
            if err.response.status_code == 429:
                logger.warning(f'Flood penalty for {err.headers['Retry-After']}s')

            elif err.response.status_code == 404:
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
                raise

        except ConnectionError as err:
            logger.warning(f'ConnectionError occurred while {retry} retry')
            return self.get(method, *args, retry=retry + 1, error=err, **kwargs)

    def get_match_and_timeline(self):
        params = {
            'region': self.region,
            'match_id': f'RU_{self.index}'
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
    def _get_challenges(match: MatchDto, session: Session):
        challenges = set()
        for participant in match.info.participants:
            if participant.challenges is None:
                continue

            for challenge in participant.challenges:
                challenges.add(challenge)

        challenges_table: dict[str, Challenge] = {}
        for challenge in challenges:
            statement = insert(Challenge).values(name=challenge)
            # noinspection PyDeprecation
            session.execute(statement.on_conflict_do_nothing(index_elements=['name']))

            # noinspection PyTypeChecker,Pydantic
            challenges_table[challenge] = session.exec(
                select(Challenge).where(Challenge.name == challenge)).one()

        return challenges_table

    @staticmethod
    def _get_participants(match: MatchDto, challenges_table: dict[str, Challenge]):
        participants: list[Participant] = []
        for participant in match.info.participants:

            perks_db: list[Perk] = []
            for perk in participant.perks.styles:
                for selection in perk.selections:
                    perk_db = Perk.model_validate(selection.model_dump())
                    perk_db.description = perk.description
                    perk_db.style = perk.style

                    perks_db.append(perk_db)

            participant_db = Participant.model_validate(participant.model_dump())
            participant_db.defenseStat = participant.perks.statPerks.defense
            participant_db.flexStat = participant.perks.statPerks.flex
            participant_db.offenseStat = participant.perks.statPerks.offense
            participant_db.perks = perks_db

            if participant.missions is not None:
                participant_db.missions = Missions.model_validate(participant.missions.model_dump())

            if participant.challenges is not None:
                for challenge_name, challenge_value in participant.challenges.items():
                    ChallengeParticipantLink(
                        value=challenge_value,
                        challenge=challenges_table[challenge_name],
                        participant=participant_db
                    )

            participants.append(participant_db)

        return participants

    @staticmethod
    def _get_teams(match: MatchDto):
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

            teams.append(team_db)

        return teams

    def insert(self, match: MatchDto, timeline: TimelineDto):
        if match is None or timeline is None:
            return

        with Session(engine) as session:
            # noinspection PyTypeChecker,Pydantic
            if session.exec(select(Match).where(Match.matchId == match.metadata.matchId)).one_or_none() is not None:
                logger.warning(f'match with id = {self.index} and matchId = {match.metadata.matchId} already in db')
                return

            match_db = Match.model_validate(match.info.model_dump() | match.metadata.model_dump())
            match_db.participants = self._get_participants(match, self._get_challenges(match, session))
            match_db.teams = self._get_teams(match)

            session.add(match_db)
            session.commit()

        logger.info(f'match and timeline with id = {self.index} are inserted')

    def start(self, start: int):
        self.index = start
        self.last_founded = self.index - 1

        while True:
            try:
                match, timeline = self.get_match_and_timeline()
                self.insert(match, timeline)

            except Exception as err:
                logger.error(f'unexpected error {err}: {traceback.format_exc()}')

            self.index += 1
