"""Objects convert from Excel into class structures for NFL_Stats database ORM."""
from dataclasses import dataclass
import datetime

@dataclass(slots=True, frozen=True)
class Season:
    """Season class for NFL_Stats database ORM"""
    year: int
    name: str
    playoff_teams: int
    regular_season_week_count: int

@dataclass(slots=True, frozen=True)
class Game:
    """Game class for NFL_Stats database ORM"""
    week: int
    week_name: str
    start_time: datetime
    away_team: str
    home_team: str
    away_score: int
    home_score: int
    overtime: bool


@dataclass(slots=True, frozen=True)
class Division:
    """Division class for NFL_Stats database ORM"""
    name: int
    conference: str


@dataclass(slots=True, frozen=True)
class Team:
    """Team class for NFL_Stats database ORM"""
    location: str
    name: str
    full_name: str
    division: str
