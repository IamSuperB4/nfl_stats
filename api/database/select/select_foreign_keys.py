"""Handles getting Foreign keys""" 
from sqlalchemy import Connection, CursorResult, Select, select
from database.db_tables import season, division, team, game


async def get_season_id(db: Connection, year: int) -> int:
    """Returns the id of the season with the given year,
        or None if no season exists with the given year.

    Args:
        db (Connection): The database connection.
        year (int): The year of the season.

    Returns:
        int: The id of the season with the given year,
            or None if no season exists with the given year.
    """
    select_new_season_id: Select = (
        select(season.columns.Id).where(season.columns.Year == year).limit(1)
    )

    result: CursorResult = await db.execute(select_new_season_id)
    season_id: int = result.scalar()
    return season_id


async def get_division_ids(db: Connection, new_season_id: int) -> dict[str, int]:
    """Returns a dictionary of division names and their IDs for the given season.

    Args:
        db (Connection): The database connection.
        new_season_id (int): The ID of the season for which to retrieve the divisions.

    Returns:
        dict[str, int]: A dictionary of division names and their IDs for the given season.
    """
    select_division_ids: Select = select(
        division.columns.Name, division.columns.Id
    ).where(division.columns.SeasonId == new_season_id)

    result: CursorResult = await db.execute(select_division_ids)
    division_ids: dict[str, int] = {row[0]: row[1] for row in result}
    return division_ids


async def get_team_ids(db: Connection, new_season_id: int) -> dict[str, int]:
    """
    Returns a dictionary of team full names and their IDs for the given season and divisions.

    Args:
        db (Connection): The database connection.
        new_season_id (int): The ID of the season for which to retrieve the teams.

    Returns:
        dict[str, int]: A dictionary of team full names and their IDs for the given season and
            divisions.
    """
    select_team_id: Select = (
        select(team.columns.FullName, team.columns.Id)
        .join(division)
        .where(
            team.columns.DivisionId == division.columns.Id
            and division.columns.SeasonId == new_season_id
        )
    )

    result: CursorResult = await db.execute(select_team_id)
    team_ids: dict[str, int] = {row[0]: row[1] for row in result}
    return team_ids


async def get_game_ids(db: Connection, new_season_id: int) -> list[int]:
    """
    Returns a list of game IDs for the given season.

    Args:
        db (Connection): The database connection.
        new_season_id (int): The ID of the season for which to retrieve the game IDs.

    Returns:
        list[int]: A list of game IDs for the given season.

    """
    select_game_ids: Select = select(game.columns.Id).where(
        game.columns.SeasonId == new_season_id
    )

    result: CursorResult = await db.execute(select_game_ids)
    game_ids: list[int] = [row[0] for row in result]
    return game_ids