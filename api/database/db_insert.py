from api.data.excel_conversion import Team, Division, Game

def add_season(games: list[Game], teams: list[Team], divisions: list[Division], season: int, name: str, playoff_teams: int, regular_season_week_count: int):
    