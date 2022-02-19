import logging
import os.path
from datetime import datetime
from pathlib import Path


Path("mpdblogs").mkdir(exist_ok=True)

logger = logging.Logger("mpdb", "DEBUG")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("mpdblogs/" + datetime.now().strftime("%d-%m-%y_%H-%M-%S") + ".txt")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(fmt=f"{os.path.basename(__file__)} :: %(levelname)s :: %(message)s"))
logger.addHandler(fh)


def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def warn(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


def critical(msg):
    logger.critical(msg)
