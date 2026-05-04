from sqlalchemy import func, select

from sportslab.db.models import BacktestRun, Match, Prediction


def settle_and_score(session, slate: str) -> BacktestRun:
    preds = list(session.scalars(select(Prediction).where(Prediction.slate == slate)))
    if not preds:
        raise ValueError("No predictions for slate")

    correct = 0
    settled = 0
    for p in preds:
        match = session.get(Match, p.match_id)
        if match is None or match.home_goals is None or match.away_goals is None:
            continue
        settled += 1
        home_win = match.home_goals > match.away_goals
        if (p.predicted_label == "HOME_WIN" and home_win) or (
            p.predicted_label == "NOT_HOME_WIN" and not home_win
        ):
            correct += 1

    accuracy = (correct / settled) if settled else 0.0
    run = BacktestRun(slate=slate, overall_accuracy=round(accuracy, 4))
    session.add(run)
    session.commit()
    return run
