"""Handles """

import pandas as pd
from sqlalchemy import Connection, CursorResult, Select, select
from data.data import Game, Season, Team
from database.db_tables import season, division, team, game, game_result
from database.database_helper import (
    DatabaseEnvVariables,
    async_create_sql_server_engine,
)


async def get_entire_season(season_year: int) -> tuple[Season, list[Team], list[Game]]:
    """
    Adds an entire NFL season to the database.

    Args:
        season_year (int): The season year for which the games are required.

    Returns:
        tuple[Season, list[Team], list[Game]]: A tuple containing season information,
            teams, and games.
    """
    engine = await async_create_sql_server_engine(
        DatabaseEnvVariables(server="Local_SQL_Server", database="NFL_Stats"), False
    )

    async with engine.begin() as db:
        season_info: Season = await get_season_info(db, season_year)
        teams: list[Team] = await get_teams_for_season(db, season_year)
        games: list[Game] = await get_games_for_season(db, season_year)

    await engine.dispose()

    return season_info, teams, games

async def get_season_info(db: Connection, season_year: int) -> Season:
    """
    This function retrieves the season information for a given season from the database.

    Args:
        db (Connection): The database connection.
        season_year (int): The season year for which the season information is required.

    Returns:
        Season: The season information for the given season.
    """
    season_select: Select = season.select().where(season.c.Year == season_year).limit(1)

    result: CursorResult = await db.execute(season_select)

    return Season(*result.one()[1:])


async def get_teams_for_season(db: Connection, season_year: int) -> list[Team]:
    """
    This function retrieves all the teams for a given season from the database.

    Args:
        db (Connection): The database connection.
        season_year (int): The season year.

    Returns:
        pd.DataFrame: A pandas dataframe containing the team information.
    """
    teams_select: Select = (
        select(
            team.columns.Location,
            team.columns.Name,
            team.columns.FullName,
            division.columns.Name.label('Division'),
            division.columns.Conference,
        )
        .join(division, onclause=division.columns.Id == team.columns.DivisionId)
        .join(season)
        .where(season.c.Year == season_year)
    )

    result: CursorResult = await db.execute(teams_select)

    # Fetch all rows from the cursor
    rows = result.fetchall()

    # Create a list of dataclasses
    return [Team(*row) for row in rows]


async def get_games_for_season(db: Connection, season_year: int) -> list[Game]:
    """
    This function retrieves all the games for a given season from the database.

    Args:
        db (Connection): The database connection.
        season_year (int): The season year for which the games are required.

    Returns:
        pd.DataFrame: A pandas dataframe containing the game details.
    """
    away_team = team.alias('away_team')
    home_team = team.alias('home_team')

    games_select: Select = (
        select(
            game.columns.Id,
            game.columns.Week,
            game.columns.WeekName,
            game.columns.StartTime,
            away_team.columns.FullName.label("AwayTeam"),
            home_team.columns.FullName.label("HomeTeam"),
            game_result.columns.AwayScore,
            game_result.columns.HomeScore,
            game_result.columns.Overtime,
        )
        .join(away_team, onclause=away_team.columns.Id == game.columns.AwayTeamId)
        .join(home_team, onclause=home_team.columns.Id == game.columns.HomeTeamId)
        .join(game_result)
        .join(season)
        .where(season.c.Year == season_year)
    )

    result: CursorResult = await db.execute(games_select)

    # Fetch all rows from the cursor
    rows = result.fetchall()

    # Create a list of dataclasses
    return [Game(*row) for row in rows]
