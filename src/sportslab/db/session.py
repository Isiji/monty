from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sportslab.config import normalized_database_url, settings

engine = create_engine(normalized_database_url(settings.database_url), future=True)

def get_session() -> Session:
    return Session(engine)