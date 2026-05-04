from datetime import date, datetime, time

from sqlalchemy import func, select

from sportslab.db.models import ApiCallLog


def calls_used_today(session, provider: str) -> int:
    start = datetime.combine(date.today(), time.min)
    end = datetime.combine(date.today(), time.max)
    stmt = select(func.count(ApiCallLog.id)).where(
        ApiCallLog.provider == provider,
        ApiCallLog.called_at >= start,
        ApiCallLog.called_at <= end,
    )
    return int(session.scalar(stmt) or 0)


def record_call(session, provider: str, endpoint: str) -> None:
    session.add(ApiCallLog(provider=provider, endpoint=endpoint))
    session.commit()
