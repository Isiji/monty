from sportslab.config import settings
from sportslab.db.models import Match, TeamMatchStat
from sportslab.ingest.budget import calls_used_today, record_call
from sportslab.ingest.providers.api_football import ApiFootballClient


def _stat_value(stats: list[dict], stat_type: str, default: int | float = 0):
    for item in stats:
        if item.get("type") == stat_type:
            value = item.get("value")
            if isinstance(default, float):
                if isinstance(value, str) and value.endswith("%"):
                    return float(value.rstrip("%"))
                return float(value or 0)
            return int(value or 0)
    return default


def ingest_fixture_stats(session, limit: int = 20) -> int:
    if not settings.sports_api_key:
        raise ValueError("SPORTSLAB_SPORTS_API_KEY is required")

    used = calls_used_today(session, "api-football")
    budget_left = settings.sports_api_daily_limit - used
    if budget_left <= 0:
        raise RuntimeError("Daily API call budget exhausted")

    client = ApiFootballClient(api_key=settings.sports_api_key, base_url=settings.sports_api_base_url)
    matches = (
        session.query(Match)
        .filter(Match.provider == "api-football", Match.home_goals.isnot(None), Match.away_goals.isnot(None))
        .limit(min(limit, budget_left))
        .all()
    )

    inserted = 0
    for match in matches:
        existing = session.query(TeamMatchStat.id).filter_by(match_id=match.id).first()
        if existing or not match.provider_fixture_id:
            continue
        stats_rows = client.fixture_statistics(int(match.provider_fixture_id))
        record_call(session, "api-football", "/fixtures/statistics")

        for row in stats_rows:
            team_name = row.get("team", {}).get("name")
            stats = row.get("statistics", [])
            is_home = 1 if team_name == match.home_team else 0
            goals = match.home_goals if is_home else match.away_goals
            session.add(
                TeamMatchStat(
                    match_id=match.id,
                    team=team_name,
                    is_home=is_home,
                    goals=int(goals or 0),
                    corners=_stat_value(stats, "Corner Kicks", 0),
                    shots_on_target=_stat_value(stats, "Shots on Goal", 0),
                    possession=_stat_value(stats, "Ball Possession", 0.0),
                    fouls=_stat_value(stats, "Fouls", 0),
                    cards=_stat_value(stats, "Yellow Cards", 0) + _stat_value(stats, "Red Cards", 0),
                    keeper_saves=_stat_value(stats, "Goalkeeper Saves", 0),
                )
            )
            inserted += 1
    session.commit()
    return inserted
