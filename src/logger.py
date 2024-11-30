import logging
import logging.config
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s - %(message)s",
            "datefmt": "%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": (
                "[%(asctime)s] %(levelname)s "
                "(%(name)s %(module)s:%(lineno)d) - %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "WARNING",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": "INFO",
            "filename": LOG_FILE,
            "maxBytes": 1045576,
            "backupCount": 3,
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file", "console"],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
scheduler_logger = logging.getLogger('apscheduler')
scheduler_logger.setLevel(logging.WARNING)
httpx_logger = logging.getLogger('httpx')
httpx_logger.setLevel(logging.WARNING)
logger = logging.getLogger(__name__)