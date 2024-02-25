"""NFL_Stats database ORM Classes"""
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, MetaData, String, Table

meta = MetaData()

user = Table(
    'User', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('Username', String, nullable=False),
    Column('FirstName', String, nullable=False),
    Column('LastName', String, nullable=False),
    Column('Money', Integer, nullable=False)
)

season = Table(
    'Season', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('Name', String, nullable=False),
    Column('Year', Integer, nullable=False),
    Column('RegularSeasonWeekCount', Integer, nullable=False),
    Column('PlayoffTeams', Integer, nullable=False)
)

division = Table(
    'Division', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('Name', String, nullable=False),
    Column('Conference', String, nullable=True),
    Column('SeasonId', Integer, ForeignKey('Season.Id'), nullable=False)
)

team = Table(
    'Team', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('Location', String, nullable=False),
    Column('Name', String, nullable=False),
    Column('FullName', String, nullable=False),
    Column('DivisionId', Integer, ForeignKey('Division.Id'), nullable=False)
)

game = Table(
    'Game', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('SeasonId', Integer, ForeignKey('Season.Id'), nullable=False),
    Column('Week', Integer, nullable=False),
    Column('WeekName', String, nullable=False),
    Column('StartTime', DateTime, nullable=True),
    Column('AwayTeamId', Integer, ForeignKey('Team.Id'), nullable=False),
    Column('HomeTeamId', Integer, ForeignKey('Team.Id'), nullable=False),
)

game_result = Table(
    'GameResult', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('GameId', Integer, ForeignKey('Game.Id'), nullable=False),
    Column('AwayScore', Integer, nullable=False),
    Column('HomeScore', Integer, nullable=False),
    Column('Overtime', Boolean, nullable=False),
)

game_line = Table(
    'GameLine', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('GameId', Integer, ForeignKey('Game.Id'), nullable=False),
    Column('LineType', String, nullable=False),
    Column('Line', Float, nullable=True),
    Column('Odds', Integer, nullable=True),
    Column('Winner',Integer, nullable=True)
)

bets = Table(
    'Bet', meta,
    Column('Id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('UserId', Integer, ForeignKey('User.Id'), nullable=False),
    Column('GameLineId', Integer, ForeignKey('GameLine.Id'), nullable=True),
    Column('Type', String, nullable=False),
    Column('Selection', Boolean, nullable=False),
    Column('Amount', Integer, nullable=False),
)