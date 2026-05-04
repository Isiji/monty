from datetime import date, timedelta
import random

from sqlalchemy import delete

from sportslab.config import settings
from sportslab.db.models import Match, TeamMatchStat

TEAMS = [
    "Arsenal",
    "Liverpool",
    "Chelsea",
    "Newcastle",
    "Brighton",
    "Tottenham",
    "Aston Villa",
    "West Ham",
]


def seed_demo_data(session, historical_matches: int = 120, upcoming_matches: int = 20) -> None:
    random.seed(settings.random_seed)

    session.execute(delete(TeamMatchStat))
    session.execute(delete(Match))

    start = date.today() - timedelta(days=historical_matches)
    for idx in range(historical_matches + upcoming_matches):
        home, away = random.sample(TEAMS, 2)
        kickoff = start + timedelta(days=idx)
        played = idx < historical_matches

        home_goals = random.randint(0, 4) if played else None
        away_goals = random.randint(0, 4) if played else None

        match = Match(
            provider="internal",
            provider_fixture_id=f"demo-{idx}",
            league="Premier League",
            home_team=home,
            away_team=away,
            kickoff_date=kickoff,
            home_goals=home_goals,
            away_goals=away_goals,
        )
        session.add(match)
        session.flush()

        for team, is_home, goals in [(home, 1, home_goals), (away, 0, away_goals)]:
            g = goals if goals is not None else random.randint(0, 3)
            session.add(
                TeamMatchStat(
                    match_id=match.id,
                    team=team,
                    is_home=is_home,
                    goals=g,
                    corners=random.randint(1, 10),
                    shots_on_target=max(1, g + random.randint(1, 6)),
                    possession=random.uniform(35, 65),
                    fouls=random.randint(6, 18),
                    cards=random.randint(0, 5),
                    keeper_saves=random.randint(0, 8),
                )
            )

    session.commit()
