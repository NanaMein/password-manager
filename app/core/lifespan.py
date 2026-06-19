from contextlib import asynccontextmanager
from fastapi import FastAPI
from cachetools import TTLCache
from datetime import timedelta


def time_to_live_cache(
        days: float| None = None,
        hours: float| None = None,
        minutes: float| None = None,
):
    _time = {}
    if days:
        _time["days"] = days
    if hours:
        _time["hours"] = hours
    if minutes:
        _time["minutes"] = minutes

    if not _time:

        raise TypeError("time_to_live_cache requires either days, hours, or minutes")

    _time_set = timedelta(**_time).total_seconds()

    return TTLCache(maxsize=1, ttl=_time_set)





@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.access_cache = time_to_live_cache(minutes=5)
    app.state.refresh_cache = time_to_live_cache(hours=2)
    try:
        yield
    finally:
        app.state.access_cache.clear()
        app.state.refresh_cache.clear()