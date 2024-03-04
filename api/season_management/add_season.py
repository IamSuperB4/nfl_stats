"""Add a season to the database."""
from datetime import datetime
import pandas as pd
from data.excel_conversion import Team, Division, Game, Season
from database.insert.db_insert import add_entire_season_to_database

async def add_completed_season_to_database_from_excel(
    file_path: str, year: int, playoff_teams: int, regular_season_week_count: int
) -> None:
    """This function adds a completed NFL season to the database.

    Args:
        file_path (str): The path to the Excel file.
        year (int): Season year.
        name (str): Season name (ie '2023-2024').
        playoff_teams (int): The number of playoff teams.
        regular_season_week_count (int): The number of weeks in the regular season.
    """
    # initiate constant variables based on the parameters passed in
    name = f'{year}-{year+1}'
    playoff_game_names = ['Wild Card', 'Divisional', 'Conference Championship', 'Super Bowl']
    excel_playoff_name_conversions = {
        'WildCard': regular_season_week_count + 1,
        'Division': regular_season_week_count + 2,
        'ConfChamp': regular_season_week_count + 3,
        'SuperBowl': regular_season_week_count + 4,
    }

    # create the games and teams dataframes from the Excel file
    games_df, teams_df = read_season_from_excel(file_path)

    # create Game objects from the games dataframe
    games_df['Game'] = games_df.apply(
        create_game,
        regular_season_week_count=regular_season_week_count,
        playoff_game_names=playoff_game_names,
        playoff_name_conversions=excel_playoff_name_conversions,
        axis=1)

    # create Team and Division objects from the teams dataframe
    teams_df = teams_df.apply(create_teams_and_divisions, axis=1)

    # create object lists from the games and teams dataframes
    games: list[Game] = games_df['Game'].to_list()
    teams: list[Team] = teams_df['Team'].to_list()
    divisions: list[Division] = teams_df['Division'].to_list()
    season: Season = Season(year=year,
        name=name,
        playoff_teams=playoff_teams,
        regular_season_week_count=regular_season_week_count
    )

    # add season to the database
    await add_entire_season_to_database(season, games, teams, divisions, True)

def read_season_from_excel(path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Reads the NFL season data from the given Excel file.

    Args:
        path (str): The path to the Excel file.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the games and teams dataframes.
    """
    games_df: pd.DataFrame = pd.read_excel(path, 'Games')

    # drop unnecessary columns
    games_df.drop(columns=['Day', 'Unnamed: 7', 'YdsW', 'TOW', 'YdsL', 'TOL'], axis=1, inplace=True)
    # rename unnamed columns
    games_df.rename(columns={'Unnamed: 5': 'At'}, inplace=True)
    # drop rows with no game data
    games_df = games_df[games_df['Week'].notna()]
    # replace convert 'At' column rows to strings, and replace nan values with empty strings
    games_df['At'] = games_df['At'].astype(str).str.replace('nan', '')

    teams_df: pd.DataFrame = pd.read_excel(path, 'Teams')

    return games_df, teams_df

def create_game(
    row: pd.Series,
    regular_season_week_count: int,
    playoff_game_names: list[str],
    playoff_name_conversions: dict[str, int]
) -> Game:
    """Creates a Game object from a pandas series representing a single NFL game.

    Parameters:
        row (pd.Series): A pandas series containing the game data.
        regular_season_week_count (int): The number of weeks in the regular season.
        playoff_game_names (list[str]): The names of the playoff games, in order.
        playoff_name_conversions (dict[str, int]): A dictionary mapping playoff game names
            to their index in the list of playoff games.

    Returns:
        Game: A Game object representing the given game data.
    """
    # convert the game start date and time to a datetime object
    date: datetime.date = row['Date'].date()
    time: datetime.time = datetime.strptime(row['Time'], "%I:%M%p").time()
    start_time = datetime.combine(date, time)

    # regular season games have a week number
    if isinstance(row['Week'], int):
        week: int = row['Week']
        week_name: str = f'Week {row['Week']}'
    # playoff games
    else:
        week: int = playoff_name_conversions[row['Week']]
        week_name: str = playoff_game_names[week - regular_season_week_count - 1]

    # '@' means the Loser/Tie team is the home team, and PtsW is the home team's score
    if row['At'] == '@':
        away_team = row['Winner/tie']
        home_team = row['Loser/tie']
        away_score = row['PtsW']
        home_score = row['PtsL']
    else:
        away_team = row['Loser/tie']
        home_team = row['Winner/tie']
        away_score = row['PtsL']
        home_score = row['PtsW']

    return Game(
        week=week,
        week_name=week_name,
        away_team=away_team,
        home_team=home_team,
        away_score=away_score,
        home_score=home_score,
        start_time=start_time,
        overtime=False
    )

def create_teams_and_divisions(row: pd.Series) -> pd.Series:
    """Creates a Team and Division object from a pandas series representing a NFL team.

    Parameters:
        row (pd.Series): A pandas series containing the team data.

    Returns:
        pd.Series: A pandas series containing the team and division data.
    """
    # team information
    location: str = row['Location']
    name: str = row['Name']
    full_name: str = f'{location} {name}'

    # division information
    division: str = row['Division']
    conference = division[:3]

    # create new columns with Team and Division objects
    row['Team'] = Team(location=location, name=name, full_name=full_name, division=division)
    row['Division'] = Division(name=division, conference=conference)

    return row
