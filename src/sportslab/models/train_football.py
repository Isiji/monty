from pathlib import Path
import pickle

from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression

from sportslab.features.football_features import feature_columns, load_training_frame

MODEL_PATH = Path("artifacts/football_model.pkl")


def train_football_model(session) -> None:
    df = load_training_frame(session)
    x = df[feature_columns()]
    y = df["target"]

    base = LogisticRegression(max_iter=1000)
    model = CalibratedClassifierCV(base, cv=3, method="isotonic")
    model.fit(x, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_PATH.open("wb") as f:
        pickle.dump(model, f)
