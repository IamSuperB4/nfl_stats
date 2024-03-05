"""API Data"""
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(slots=True)
class Season():
    """Season information"""
    name: str
    year: int
    regular_season_week_count: int
    playoff_teams: int

@dataclass(slots=True)
class Team():
    """Team information for standings"""
    location: str
    name: str
    full_name: str
    division: str
    conference: str
    wins: int = field(default=0)
    losses: int = field(default=0)
    ties: int = field(default=0)
    win_percentage: float = field(default=0.0)
    point_differential: int = field(default=0)
    points_for: int = field(default=0)
    points_against: int = field(default=0)
    division_wins: int = field(default=0)
    division_losses: int = field(default=0)
    division_ties: int = field(default=0)
    conference_wins: int = field(default=0)
    conference_losses: int = field(default=0)
    conference_ties: int = field(default=0)
    offensive_rank: int = field(default=0)
    defensive_rank: int = field(default=0)
    playoff_rank: int = field(default=0)
    division_rank: int = field(default=0)
    playoff_clinch_type: str = field(default='')

@dataclass(slots=True)
class Game():
    """Game information"""
    id: int
    week: int
    week_name: str
    starttime: datetime
    away_team: str
    home_team: str
    away_score: int
    home_score: int
    overtime: bool

@dataclass(slots=True)
class TeamGame():
    """Team information"""
    week: int
    week_name: str
    opponent: str
    score: int
    opponent_score: int
    result: chr
    home_game: bool
    division_game: bool
    conference_game: bool
    playoff_game: bool
