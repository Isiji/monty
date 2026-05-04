import typer

from sportslab.backtest.evaluate import evaluate_slate
from sportslab.backtest.settle import settle_and_score
from sportslab.db.base import Base
from sportslab.db.session import engine, get_session
from sportslab.grouping.create_groups import group_predictions
from sportslab.ingest.budget import calls_used_today
from sportslab.ingest.demo_seed import seed_demo_data
from sportslab.ingest.fetch_historical import fetch_historical_matches
from sportslab.ingest.fetch_upcoming import fetch_upcoming_matches
from sportslab.ingest.fetch_stats import ingest_fixture_stats
from sportslab.models.predict_football import predict_football
from sportslab.models.train_football import train_football_model

app = typer.Typer()

@app.command("init-db")
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    typer.echo("Database initialized")

@app.command("ingest-historical")
def ingest_historical(league: int = 39, season: int = 2024) -> None:
    with get_session() as session:
        count = fetch_historical_matches(session, league=league, season=season)
    typer.echo(f"Inserted {count} historical matches")

@app.command("api-budget")
def api_budget() -> None:
    with get_session() as session:
        used = calls_used_today(session, "api-football")
    typer.echo(f"api-football calls used today: {used}")

@app.command("seed-demo")
def seed_demo() -> None:
    with get_session() as session:
        seed_demo_data(session)
    typer.echo("Demo data seeded")

@app.command("fetch-upcoming")
def fetch_upcoming(league: int = 39, season: int = 2025, days_ahead: int = 7) -> None:
    with get_session() as session:
        count = fetch_upcoming_matches(session, league=league, season=season, days_ahead=days_ahead)
    typer.echo(f"Inserted {count} upcoming matches")

@app.command("ingest-stats")
def ingest_stats(limit: int = 20) -> None:
    with get_session() as session:
        count = ingest_fixture_stats(session, limit=limit)
    typer.echo(f"Inserted {count} team stat rows")

@app.command("train-football")
def train() -> None:
    with get_session() as session:
        train_football_model(session)
    typer.echo("Football model trained")

@app.command("predict-football")
def predict(slate: str = "demo", limit: int = 16) -> None:
    with get_session() as session:
        count = predict_football(session, slate=slate, limit=limit)
    typer.echo(f"Inserted {count} predictions")

@app.command("group-predictions")
def group(slate: str = "demo") -> None:
    with get_session() as session:
        averages = group_predictions(session, slate=slate)
    for group_name, avg in averages.items():
        typer.echo(f"{group_name}: {avg}")

@app.command("settle")
def settle(slate: str = "demo") -> None:
    with get_session() as session:
        run = settle_and_score(session, slate=slate)
    typer.echo(f"Backtest run {run.id} accuracy={run.overall_accuracy}")

@app.command("evaluate")
def evaluate(slate: str = "demo") -> None:
    with get_session() as session:
        rows = evaluate_slate(session, slate=slate)
    for row in rows:
        typer.echo(row)

if __name__ == "__main__":
    app()
