from etl.settings.base import CommonSettings


class DevSettings(CommonSettings):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
