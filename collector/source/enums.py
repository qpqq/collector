from enum import StrEnum


# from cassiopeia
# https://github.com/meraki-analytics/cassiopeia

class Region(StrEnum):
    BR = 'BR'
    EUNE = 'EUNE'
    EUW = 'EUW'
    JP = 'JP'
    KR = 'KR'
    LAN = 'LAN'
    LAS = 'LAS'
    NA = 'NA'
    OCE = 'OCE'
    TR = 'TR'
    RU = 'RU'
    PH = 'PH'
    SG = 'SG'
    TH = 'TH'
    TW = 'TW'
    VN = 'VN'

    @property
    def platform(self) -> 'Platform':
        return getattr(Platform, self.name)

    def __repr__(self) -> str:
        return repr(self.value)


class Platform(StrEnum):
    BR1 = 'BR1'
    EUN1 = 'EUN1'
    EUW1 = 'EUW1'
    JP1 = 'JP1'
    KR = 'KR'
    LA1 = 'LA1'
    LA2 = 'LA2'
    NA1 = 'NA1'
    OC1 = 'OC1'
    TR1 = 'TR1'
    RU = 'RU'
    PH2 = 'PH2'
    SG2 = 'SG2'
    TH2 = 'TH2'
    TW2 = 'TW2'
    VN2 = 'VN2'

    def __repr__(self) -> str:
        return repr(self.value)


class GameMode(StrEnum):
    ARAM = 'ARAM'
    ASCENSION = 'ASCENSION'
    CLASSIC = 'CLASSIC'
    FIRSTBLOOD = 'FIRSTBLOOD'
    KINGPORO = 'KINGPORO'
    ODIN = 'ODIN'
    ONEFORALL = 'ONEFORALL'
    TUTORIAL = 'TUTORIAL'
    TUTORIAL_MODULE_1 = 'TUTORIAL_MODULE_1'
    TUTORIAL_MODULE_2 = 'TUTORIAL_MODULE_2'
    TUTORIAL_MODULE_3 = 'TUTORIAL_MODULE_3'
    SIEGE = 'SIEGE'
    ASSASSINATE = 'ASSASSINATE'
    DARKSTAR = 'DARKSTAR'
    ARSR = 'ARSR'
    URF = 'URF'
    DOOMBOTSTEEMO = 'DOOMBOTSTEEMO'
    STARGUARDIAN = 'STARGUARDIAN'
    PROJECT = 'PROJECT'
    OVERCHARGE = 'OVERCHARGE'
    SNOWURF = 'SNOWURF'
    PRACTICETOOL = 'PRACTICETOOL'
    NEXUSBLITZ = 'NEXUSBLITZ'
    ODYSSEY = 'ODYSSEY'
    ULTBOOK = 'ULTBOOK'
    CHERRY = 'CHERRY'
    WIPMODEWIP = 'WIPMODEWIP'


class GameType(StrEnum):
    CUSTOM_GAME = 'CUSTOM_GAME'
    TUTORIAL_GAME = 'TUTORIAL_GAME'
    MATCHED_GAME = 'MATCHED_GAME'


class Lane(StrEnum):
    TOP = 'TOP'
    JUNGLE = 'JUNGLE'
    MID = 'MID'
    MIDDLE = 'MIDDLE'
    BOTTOM = 'BOTTOM'
    UTILITY = 'UTILITY'
    INVALID_CAPS = 'INVALID'
    INVALID = 'Invalid'
    EMPTY = ''
    NONE = 'NONE'


class LaneDB(StrEnum):
    TOP_LANE = 'TOP_LANE'
    JUNGLE = 'JUNGLE'
    MID_LANE = 'MID_LANE'
    BOT_LANE = 'BOT_LANE'
    UTILITY = 'UTILITY'

    @staticmethod
    def from_lane(lane: Lane | None):
        match lane:
            case Lane.TOP:
                return LaneDB.TOP_LANE
            case Lane.JUNGLE:
                return LaneDB.JUNGLE
            case Lane.MID | Lane.MIDDLE:
                return LaneDB.MID_LANE
            case Lane.BOTTOM:
                return LaneDB.BOT_LANE
            case Lane.UTILITY:
                return LaneDB.UTILITY
            case _:
                return None


class Role(StrEnum):
    DUO = 'DUO'
    DUO_CARRY = 'DUO_CARRY'
    DUO_SUPPORT = 'DUO_SUPPORT'
    NONE = 'NONE'
    SOLO = 'SOLO'
    CARRY = 'CARRY'
    SUPPORT = 'SUPPORT'


class Tower(StrEnum):
    OUTER = 'OUTER_TURRET'
    INNER = 'INNER_TURRET'
    BASE = 'BASE_TURRET'
    NEXUS = 'NEXUS_TURRET'
    UNDEFINED = 'UNDEFINED_TURRET'
