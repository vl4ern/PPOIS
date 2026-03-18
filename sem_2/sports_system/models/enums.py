from enum import Enum

class SquadStatus(Enum):
    MAIN = "основной"
    RESERVE = "запасной"
    UNKNOWN = "N/A"

class SportRank(Enum):
    YOUTH_FIRST = "1-й юношеский"
    SECOND = "2-й разряд"
    THIRD = "3-й разряд"
    CMS = "КМС"
    MASTER = "Мастер спорта"