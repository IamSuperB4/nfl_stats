"""Handle databse insertions"""

from data.excel_conversion import Season, Team, Division, Game
from database.database_helper import (
    DatabaseEnvVariables,
    async_create_sql_server_engine,
)
from database.insert.individual_inserts import (
    add_season,
    add_divisions,
    add_teams,
    add_games,
    add_game_results,
)
from database.select.select_foreign_keys import (
    get_season_id,
    get_division_ids,
    get_team_ids,
    get_game_ids,
)


async def add_entire_season_to_database(
    season_info: Season,
    divisions: list[Division],
    teams: list[Team],
    games: list[Game],
    completed_season: bool,
) -> None:
    """Adds an entire NFL season to the database.

    Args:
        games (list[Game]): A list of games for the season.
        teams (list[Team]): A list of teams in the season.
        divisions (list[Division]): A list of divisions in the season.
        season_info (Season): A Season object containing information about the season.
    """
    engine = await async_create_sql_server_engine(
        DatabaseEnvVariables(server="Local_SQL_Server", database="NFL_Stats"), True
    )

    async with engine.begin() as db:
        await add_season(db, season_info)
        season_id = await get_season_id(db, season_info.year)

        await add_divisions(db, divisions, season_id)
        division_ids = await get_division_ids(db, season_id)

        await add_teams(db, teams, division_ids)
        team_ids = await get_team_ids(db, season_id)

        await add_games(db, games, team_ids, season_id)

        if completed_season:
            game_ids = await get_game_ids(db, season_id)
            await add_game_results(db, games, game_ids)

        db.commit()
