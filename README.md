# Sports Research Lab

Python-first machine learning research platform for sports predictions, confidence-ranked grouping, and backtesting.

## Setup

1. Create `.env` from `.env.example` and fill your credentials.
2. Install dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Sprint 2 commands

```bash
sportslab init-db
sportslab api-budget
sportslab ingest-historical --league 39 --season 2024
sportslab fetch-upcoming --league 39 --season 2025 --days-ahead 7
sportslab ingest-stats --limit 20
sportslab train-football
sportslab predict-football --limit 16
sportslab group-predictions --slate demo
sportslab settle --slate demo
sportslab evaluate --slate demo
```

## Migrations

```bash
alembic upgrade head
```


## Backtesting data source
Historical fixtures and statistics are ingested from API-Football endpoints (`/fixtures`, `/fixtures/statistics`).
