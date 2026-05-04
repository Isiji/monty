from datetime import date

from sportslab.config import settings
from sportslab.db.models import Match
from sportslab.ingest.budget import calls_used_today, record_call
from sportslab.ingest.providers.api_football import ApiFootballClient


def fetch_historical_matches(session, league: int, season: int) -> int:
    if not settings.sports_api_key:
        raise ValueError("SPORTSLAB_SPORTS_API_KEY is required")

    used = calls_used_today(session, "api-football")
    if used >= settings.sports_api_daily_limit:
        raise RuntimeError("Daily API call budget exhausted")

    client = ApiFootballClient(api_key=settings.sports_api_key, base_url=settings.sports_api_base_url)
    fixtures = client.fixtures_by_season(league=league, season=season)
    record_call(session, "api-football", "/fixtures")

    inserted = 0
    for fixture in fixtures:
        fixture_id = str(fixture["fixture"]["id"])
        existing = session.query(Match.id).filter_by(provider="api-football", provider_fixture_id=fixture_id).first()
        if existing:
            continue
        goals = fixture.get("goals") or {}
        session.add(
            Match(
                sport="football",
                provider="api-football",
                provider_fixture_id=fixture_id,
                season=season,
                league=str(fixture["league"]["name"]),
                home_team=fixture["teams"]["home"]["name"],
                away_team=fixture["teams"]["away"]["name"],
                kickoff_date=date.fromisoformat(fixture["fixture"]["date"][:10]),
                home_goals=goals.get("home"),
                away_goals=goals.get("away"),
            )
        )
        inserted += 1
    session.commit()
    return inserted
