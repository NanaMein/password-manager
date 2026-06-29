from contextlib import asynccontextmanager
from fastapi import FastAPI
from cachetools import TTLCache
from datetime import timedelta
from pydantic import BaseModel, Field
from app.core.config import get_settings_instance
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path



class StartupStatus(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Manila")))
    working_directory: str = "pending"
    vault_directory: str = "pending"

    initial_user_status: str = "pending"



class StartupStateManagement:
    def __init__(self, startup_status: StartupStatus):
        self._startup_status = startup_status
        self.settings = get_settings_instance()

    @property
    def generate_updated_status(self):
        self.working_directory_status_update()
        self.vault_directory_status_update()
        self.user_status_update()
        return self._startup_status

    @staticmethod
    def _create_new_directory(file: Path):
        if not file.is_dir():
            file.mkdir(parents=True, exist_ok=True)
            test_file = file / ".write_test"
            test_file.touch()
            test_file.unlink()
            return True
        return False

    def working_directory_status_update(self):
        is_created = self._create_new_directory(file=self.settings.working_dir)
        if is_created:
            self._startup_status.working_directory = "NEW"

        else:
            self._startup_status.working_directory = "OLD"

        return self

    def vault_directory_status_update(self):
        secret_vault_path = self.settings.secret_vault_storage

        if secret_vault_path.is_dir():
            if any(secret_vault_path.iterdir()):
                _status = "OLD"
            else:
                _status = "EMPTY"
        else:
            is_created = self._create_new_directory(file=secret_vault_path)
            _status = "NEW" if is_created else "FAILED"

        self._startup_status.vault_directory = _status
        return self

    def user_status_update(self):
        if self._startup_status.working_directory == "OLD" and self._startup_status.vault_directory == "OLD":
            self._startup_status.initial_user_status = "EXISTING_USER"

        elif self._startup_status.working_directory == "NEW" and self._startup_status.vault_directory == "OLD":
            self._startup_status.initial_user_status = "EXISTING_USER"

        else:
            self._startup_status.initial_user_status = "NEW_USER"
        return self


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


    startup_status = StartupStatus()
    updated_status = StartupStateManagement(startup_status)
    app.state.startup_status = updated_status.generate_updated_status


    try:
        yield
    finally:
        app.state.access_cache.clear()
        app.state.refresh_cache.clear()