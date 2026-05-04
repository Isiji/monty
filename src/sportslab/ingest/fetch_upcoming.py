from datetime import date, timedelta

from sportslab.config import settings
from sportslab.db.models import Match
from sportslab.ingest.providers.api_football import ApiFootballClient


def fetch_upcoming_matches(session, league: int = 39, season: int = 2025, days_ahead: int = 7) -> int:
    if settings.sports_api_provider != "api-football":
        raise ValueError("Only api-football provider is currently supported")
    if not settings.sports_api_key:
        raise ValueError("SPORTSLAB_SPORTS_API_KEY is required")

    client = ApiFootballClient(api_key=settings.sports_api_key, base_url=settings.sports_api_base_url)
    fixtures = client.upcoming_fixtures(
        league=league,
        season=season,
        from_date=date.today(),
        to_date=date.today() + timedelta(days=days_ahead),
    )

    inserted = 0
    for fixture in fixtures:
        fixture_id = str(fixture["fixture"]["id"])
        exists = session.query(Match.id).filter_by(provider="api-football", provider_fixture_id=fixture_id).first()
        if exists:
            continue

        session.add(
            Match(
                sport="football",
                provider="api-football",
                provider_fixture_id=fixture_id,
                league=str(fixture["league"]["name"]),
                home_team=fixture["teams"]["home"]["name"],
                away_team=fixture["teams"]["away"]["name"],
                kickoff_date=date.fromisoformat(fixture["fixture"]["date"][:10]),
                home_goals=None,
                away_goals=None,
            )
        )
        inserted += 1
    session.commit()
    return inserted
