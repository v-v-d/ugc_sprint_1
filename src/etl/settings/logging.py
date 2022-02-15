from pathlib import Path

from app.settings import settings

LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(funcName)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
        },
        "etl": {
            "level": settings.LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": Path(settings.DIR_LOGS / "etl.log").as_posix(),
            "maxBytes": 1024**3 * 10,
            "backupCount": 10,
        },
    },
    "loggers": {
        "app.etl": {
            "handlers": ["console", "etl"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}
