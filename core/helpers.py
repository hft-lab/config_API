import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

def timestamp():
    return int(time.time() * 1000)

def datetime_utc_now():
    return datetime.utcnow()


def from_timestamp(timestamp, mls=True):
    if mls:
        return datetime.utcfromtimestamp(timestamp / 1000)

    return datetime.utcfromtimestamp(timestamp)

