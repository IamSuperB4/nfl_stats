"""Handles adding data to individual tables"""
from sqlalchemy import Connection, Insert, insert
from data.excel_conversion import Season, Team, Division, Game
from database.db_tables import season, division, team, game, game_result


async def add_season(db: Connection, season_info: Season) -> None:
    """Adds a new season to the database.

    Args:
        db (Connection): The database connection.
        season_info (Season): A Season object containing information about the season to add.
    """
    season_insert: Insert = insert(season).values(
        Name=season_info.name,
        Year=season_info.year,
        PlayoffTeams=season_info.playoff_teams,
        RegularSeasonWeekCount=season_info.regular_season_week_count,
    )

    await db.execute(season_insert)


async def add_divisions(
    db: Connection, divisions: list[Division], new_season_id: int
) -> None:
    """Adds a list of divisions to the database.

    Args:
        db (Connection): The database connection.
        divisions (list[Division]): The list of divisions to add.
        new_season_id (int): The id of the season to which the divisions belong.
    """
    division_values = [
        {
            "Name": div.name,
            "Conference": div.conference,
            "SeasonId": new_season_id,
        }
        for div in divisions
    ]

    division_insert: Insert = division.insert().values(division_values)

    await db.execute(division_insert)


async def add_teams(
    db: Connection, teams: list[Team], division_ids: dict[str, int]
) -> None:
    """Adds a list of teams to the database.

    Args:
        db (Connection): The database connection.
        teams (list[Team]): The list of teams to add.
        division_ids (dict[str, int]): A dictionary of division names and their IDs.
    """
    team_values = [
        {
            "Location": t.location,
            "Name": t.name,
            "FullName": t.full_name,
            "DivisionId": division_ids[t.division],
        }
        for t in teams
    ]

    team_insert: Insert = team.insert().values(team_values)

    await db.execute(team_insert)


async def add_games(
    db: Connection, games: list[Game], team_ids: dict[str, int], season_id: int
) -> None:
    """Adds a list of games to the database.

    Args:
        db (Connection): The database connection.
        games (list[Game]): The list of games to add.
        team_ids (dict[str, int]): A dictionary of team full names and their IDs.
        season_id (int): The ID of the season to which the games belong.

    Returns:
        None
    """
    game_values = [
        {
            "SeasonId": season_id,
            "HomeTeamId": team_ids[g.home_team],
            "AwayTeamId": team_ids[g.away_team],
            "StartTime": g.start_time,
            "Week": g.week,
            "WeekName": g.week_name,
        }
        for g in games
    ]

    game_insert: Insert = game.insert().values(game_values)

    await db.execute(game_insert)


async def add_game_results(
    db: Connection, games: list[Game], game_ids: list[int]
) -> None:
    """Adds the results of a list of games to the database.

    Args:
        db (Connection): The database connection.
        games (list[Game]): A list of games with their results.
        game_ids (list[int]): A list of game IDs.
    """
    game_result_values = [
        {
            "GameId": game_ids[i],
            "AwayScore": g.away_score,
            "HomeScore": g.home_score,
            "Overtime": g.overtime,
        }
        for i, g in enumerate(games)
    ]

    game_result_insert: Insert = game_result.insert().values(game_result_values)

    await db.execute(game_result_insert)