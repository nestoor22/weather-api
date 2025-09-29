import logging
import logging.config
from logging import Logger

from json_log_formatter import JSONFormatter, VerboseJSONFormatter

from .config import settings
from .context_vars import TraceId


class _VerboseJSONFormatter(VerboseJSONFormatter):
    def json_record(self, message, extra, record):
        extra["trace_id"] = extra.get("trace_id") or TraceId.get(None)
        return super().json_record(message, extra, record)


class _JSONFormatter(JSONFormatter):
    def json_record(self, message, extra, record):
        extra["trace_id"] = extra.get("trace_id") or TraceId.get(None)
        return super().json_record(message, extra, record)


def configure_logger():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed_json": {
                    "()": "app.core.loggers._VerboseJSONFormatter"
                },
                "simple_json": {
                    "()": "app.core.loggers._JSONFormatter",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": (
                        "detailed_json" if settings.USE_JSON_LOGGING else None
                    ),
                    "level": logging.getLevelName(settings.LOG_LEVEL),
                },
                "console_simple": {
                    "class": "logging.StreamHandler",
                    "formatter": (
                        "simple_json" if settings.USE_JSON_LOGGING else None
                    ),
                    "level": logging.getLevelName(settings.LOG_LEVEL),
                },
            },
            "loggers": {
                "weather-api": {
                    "handlers": ["console"],
                    "propagate": False,
                    "level": logging.getLevelName(settings.LOG_LEVEL),
                },
                "uvicorn": {
                    "handlers": ["console_simple"],
                    "propagate": False,
                },
            },
            "root": {"handlers": ["console_simple"]},
        }
    )


logger: Logger = logging.getLogger("weather-api")
