from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import requests


@dataclass
class ApiFootballClient:
    api_key: str
    base_url: str = "https://v3.football.api-sports.io"

    def _get(self, path: str, params: dict) -> dict:
        response = requests.get(
            f"{self.base_url}{path}",
            params=params,
            headers={"x-apisports-key": self.api_key},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def upcoming_fixtures(self, league: int, season: int, from_date: date, to_date: date) -> list[dict]:
        payload = self._get(
            "/fixtures",
            {
                "league": league,
                "season": season,
                "from": from_date.isoformat(),
                "to": to_date.isoformat(),
            },
        )
        return payload.get("response", [])

    def fixtures_by_season(self, league: int, season: int) -> list[dict]:
        payload = self._get("/fixtures", {"league": league, "season": season})
        return payload.get("response", [])

    def fixture_statistics(self, fixture_id: int) -> list[dict]:
        payload = self._get("/fixtures/statistics", {"fixture": fixture_id})
        return payload.get("response", [])
