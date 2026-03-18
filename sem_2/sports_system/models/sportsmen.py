from dataclasses import dataclass
from typing import Optional


@dataclass
class Sportsman:
    id: Optional[int]
    full_name: str
    squad_status: str
    position: str
    titles_count: int
    sport_type: str
    rank: str