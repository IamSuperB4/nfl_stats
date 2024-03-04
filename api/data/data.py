"""API Data"""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Season():
    """Season information"""
    name: str
    year: int
    regular_season_week_count: int
    playoff_teams: int

@dataclass
class Team():
    """Team information for standings"""
    location: str
    name: str
    full_name: str
    division: str
    conference: str
    wins: int
    losses: int
    ties: int
    win_percentage: float
    point_differential: int
    points_for: int
    points_against: int
    division_record: str
    conference_record: str
    offensive_rank: int
    defensive_rank: int
    playoff_rank: int
    division_rank: int
    playoff_clinch_type: str

@dataclass
class Game():
    """Game information"""
    week: int
    week_name: str
    starttime: datetime
    away_team: str
    home_team: str
    away_team_score: int
    home_team_score: int
    overtime: bool
