"""Classes and functions to customize logs."""
import json
import logging
import sys
from pprint import pformat
from typing import TYPE_CHECKING, List, Any
from loguru import logger
from loguru._defaults import LOGURU_FORMAT  # noqa: WPS436
from boxv2.plugin import BasePlugin, BasePluginSettings
from copy import deepcopy

if TYPE_CHECKING:
    from loguru import Record  # noqa: WPS433  # pragma: no cover


class Settings(BasePluginSettings):
    SQL_DEBUG: bool = False


class LoguruPlugin(BasePlugin):
    """Loguru logger plugin."""

    settings_class = Settings
    max_payload_width = 88
    max_file_length = 40

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        self.configure_logger()

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""

    def configure_logger(self) -> None:
        """Add some loggers to loguru and config logging level."""
        # Handle default logs with loguru logger
        logging.getLogger().handlers = [InterceptHandler()]

        # enable pybotx logs to see payloads of messages
        logger.enable("botx")

        # configure sql logs of tortoise-orm
        logging.getLogger("db_client").setLevel(
            logging.DEBUG if self.settings.SQL_DEBUG else logging.INFO
        )

        # configure uvicorn logs
        for logger_name in ("uvicorn.asgi", "uvicorn.access"):
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]

        # configure format for all logs
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "format": self.format_record,
                    "level": logging.DEBUG if self.settings.DEBUG else logging.INFO,
                }
            ],
            patcher=copy_extra,
        )

    def format_record(self, record: dict) -> str:
        """
        Customize format for loguru loggers.

        Uses pformat for log any data like request or
        response body during debug. Works with logging if loguru handler it.

        Example:
        >>> payload = [
        >>>     {"users":[{"name": "Nick", "age": 87, "is_active": True},
        >>>     {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
        >>> logger.bind(payload=payload).debug("users payload")
        >>> [   {   'count': 2,
        >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
        >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
        """
        payload = record["extra"].get("payload")
        is_botx_client = record["extra"].get("botx_client", False)

        if payload is not None:
            if is_botx_client:
                self.format_botx_client_payload(payload)

            record["extra"]["payload"] = pformat(
                record["extra"]["payload"],
                indent=4,
                compact=True,
                width=self.max_payload_width,
            )
            return "{0}{1}{2}".format(
                LOGURU_FORMAT, "\n<level>{extra[payload]}</level>", "{exception}\n"
            )

        return "{0}{1}{2}".format(LOGURU_FORMAT, "", "{exception}\n")

    def format_botx_client_payload(self, payload: dict) -> None:
        """Format payload from BotX client requests if it's json."""
        content_type = payload.get("headers", {}).get("Content-Type")
        if content_type == "application/json":
            request_data = payload.get("request_data")
            if request_data is not None:
                payload["request_data"] = json.loads(request_data)
                fil = payload["request_data"].get("file", None)
                if fil:
                    fil["data"] = fil["data"][: self.max_file_length]


class InterceptHandler(logging.Handler):
    """
    Logging handler interceptor from loguru documentaion.

    For more info see https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging  # noqa: E501
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """Log the specified logging record by loguru logger."""
        try:
            # Get corresponding Loguru level if it exists
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and (frame.f_code.co_filename == logging.__file__):  # noqa: WPS609
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def copy_extra(record: "Record") -> None:
    record["extra"] = deepcopy(record["extra"])
