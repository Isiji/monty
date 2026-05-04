from pathlib import Path
import pickle

from sportslab.db.models import Prediction
from sportslab.features.football_features import feature_columns, load_upcoming_frame

MODEL_PATH = Path("artifacts/football_model.pkl")


def predict_football(session, slate: str, limit: int = 16) -> int:
    with MODEL_PATH.open("rb") as f:
        model = pickle.load(f)

    df = load_upcoming_frame(session, limit=limit)
    if df.empty:
        return 0

    probs = model.predict_proba(df[feature_columns()])

    inserted = 0
    for i, row in df.iterrows():
        p_home = float(probs[i][1])
        label = "HOME_WIN" if p_home >= 0.5 else "NOT_HOME_WIN"
        conf = p_home if p_home >= 0.5 else 1 - p_home
        session.add(
            Prediction(
                slate=slate,
                match_id=int(row["match_id"]),
                predicted_label=label,
                confidence=round(conf, 4),
            )
        )
        inserted += 1

    session.commit()
    return inserted
