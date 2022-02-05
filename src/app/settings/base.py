from pathlib import Path

from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    DEBUG: bool = False
    TESTING: bool = False
    LOG_LEVEL: str = "INFO"
    SHARED_DIR: str = "/code/shared"
    DIR_LOGS: Path = Path(SHARED_DIR, "/code/shared/logs")
