import os, sys
from datetime import date
import logging

from main.config import LOG_PATH

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)

file_handler = logging.FileHandler(os.path.join(LOG_PATH, f"bigquery_bbc_{date.today().isoformat()}.log"))
file_handler.setFormatter(
    logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(process)d:%(thread)d:%(lineno)d:%(funcName)s:%(message)s")
)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
