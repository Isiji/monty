from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sportslab.config import settings


engine = create_engine(settings.database_url, future=True)


def get_session() -> Session:
    return Session(engine)
