# Common loguru logger config for project
import json

import requests
from loguru import logger

import logging  # noqa


logger.add("../out.log", backtrace=True, diagnose=True, rotation="1 week")  # Caution, may leak sensitive data in prod


ERRBOT_WEBSERVER_URL = "http://localhost:3141/send_message"
ERRBOT_PROJECT_CHANNEL_ID = "#general"


def _send_to_errbot(msg: str) -> None:
    with requests.Session() as s:
        s.post(ERRBOT_WEBSERVER_URL, data={"payload": json.dumps({"to": ERRBOT_PROJECT_CHANNEL_ID, "text": msg})})


# logger.add(_send_to_errbot, level="WARNING")  # noqa


# can't run PropagateHandler and InterceptHandler together?
class InterceptHandler(logging.Handler):
    def emit(self, record):  # type: ignore
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0)
