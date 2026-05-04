import pandas as pd
from sqlalchemy import text


def load_training_frame(session) -> pd.DataFrame:
    query = text(
        """
        SELECT m.id as match_id, m.home_goals, m.away_goals,
               hs.shots_on_target as home_sot, hs.corners as home_corners, hs.possession as home_poss,
               hs.fouls as home_fouls, hs.cards as home_cards,
               as1.shots_on_target as away_sot, as1.corners as away_corners, as1.possession as away_poss,
               as1.fouls as away_fouls, as1.cards as away_cards
        FROM matches m
        JOIN team_match_stats hs ON hs.match_id = m.id AND hs.is_home = 1
        JOIN team_match_stats as1 ON as1.match_id = m.id AND as1.is_home = 0
        WHERE m.home_goals IS NOT NULL AND m.away_goals IS NOT NULL
        ORDER BY m.kickoff_date
        """
    )
    df = pd.read_sql(query, session.bind)
    df["target"] = (df["home_goals"] > df["away_goals"]).astype(int)
    return df


def load_upcoming_frame(session, limit: int = 16) -> pd.DataFrame:
    query = text(
        """
        SELECT m.id as match_id,
               hs.shots_on_target as home_sot, hs.corners as home_corners, hs.possession as home_poss,
               hs.fouls as home_fouls, hs.cards as home_cards,
               as1.shots_on_target as away_sot, as1.corners as away_corners, as1.possession as away_poss,
               as1.fouls as away_fouls, as1.cards as away_cards
        FROM matches m
        JOIN team_match_stats hs ON hs.match_id = m.id AND hs.is_home = 1
        JOIN team_match_stats as1 ON as1.match_id = m.id AND as1.is_home = 0
        WHERE m.home_goals IS NULL AND m.away_goals IS NULL
        ORDER BY m.kickoff_date
        LIMIT :limit
        """
    )
    return pd.read_sql(query, session.bind, params={"limit": limit})


def feature_columns() -> list[str]:
    return [
        "home_sot", "home_corners", "home_poss", "home_fouls", "home_cards",
        "away_sot", "away_corners", "away_poss", "away_fouls", "away_cards",
    ]
