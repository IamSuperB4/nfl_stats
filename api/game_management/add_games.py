import pandas as pd


def read_games_from_excel(path: str) -> pd.DataFrame:
    games_df: pd.DataFrame = pd.read_csv(path)
    games_df = games_df[games_df['Week'].notna()]