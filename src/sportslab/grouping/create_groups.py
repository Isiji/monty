from statistics import mean

from sqlalchemy import delete, select

from sportslab.db.models import Prediction, PredictionGroupItem


def _group_sizes(total: int) -> list[int]:
    if total < 12:
        raise ValueError("Need at least 12 predictions to create 4 groups of 3-4.")
    sizes = [3, 3, 3, 3]
    remainder = min(total, 16) - 12
    for i in range(remainder):
        sizes[i] += 1
    return sizes


def group_predictions(session, slate: str) -> dict[str, float]:
    preds = list(
        session.scalars(
            select(Prediction)
            .where(Prediction.slate == slate)
            .order_by(Prediction.confidence.desc(), Prediction.id.asc())
        )
    )

    sizes = _group_sizes(len(preds))
    session.execute(delete(PredictionGroupItem).where(PredictionGroupItem.slate == slate))

    idx = 0
    averages: dict[str, float] = {}
    for gnum, size in enumerate(sizes, start=1):
        group_name = f"Group {gnum}"
        chunk = preds[idx : idx + size]
        idx += size
        for p in chunk:
            session.add(PredictionGroupItem(slate=slate, group_name=group_name, prediction_id=p.id))
        averages[group_name] = round(mean(p.confidence for p in chunk), 4)

    session.commit()
    return averages
