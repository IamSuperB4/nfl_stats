from dataclasses import dataclass
import datetime


@dataclass(slots=True, frozen=True)
class Game():
    week: int
    week_name: str
    game_time: datetime
    away_team: str
    home_team: str
    away_score: int
    home_score: int
    
@dataclass(slots=True, frozen=True)
class Division():
    name: int
    conference: int
    
@dataclass(slots=True, frozen=True)
class Team():
    location: str
    name: str
    full_name: str
    division: str