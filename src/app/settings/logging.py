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
        "uvicorn.access": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": Path(settings.DIR_LOGS / "access.log").as_posix(),
            "maxBytes": 1024**3 * 10,
            "backupCount": 10,
        },
        "uvicorn.error": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": Path(settings.DIR_LOGS / "error.log").as_posix(),
            "maxBytes": 1024**3 * 10,
            "backupCount": 10,
        },
        "elasticapm": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": Path(settings.DIR_LOGS / "elasticapm.log").as_posix(),
            "maxBytes": 1024**3 * 10,
            "backupCount": 10,
        },
        "progress": {
            "level": settings.LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": Path(settings.DIR_LOGS / "progress.log").as_posix(),
            "maxBytes": 1024**3 * 10,
            "backupCount": 10,
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
        "uvicorn.access": {
            "handlers": ["console", "uvicorn.access"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "uvicorn.error"],
            "level": "ERROR",
            "propagate": False,
        },
        "elasticapm": {
            "handlers": ["console", "elasticapm"],
            "level": "WARNING",
            "propagate": False,
        },
        "app.services.progress": {
            "handlers": ["console", "progress"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "app.etl": {
            "handlers": ["console", "etl"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}
