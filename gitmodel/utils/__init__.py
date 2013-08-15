from dateutil.tz import tzlocal
from datetime import datetime
from time import time

try:
    import cjson as json
except ImportError:
    import json

import pygit2

from . import path

__all__ = ['json', 'make_signature', 'path']


def make_signature(name, email, timestamp=None, offset=None,
                   default_offset=None):
    """
    Creates a pygit2.Signature while making time and offset optional. By
    default, uses current time, and local offset as determined by
    ``dateutil.tz.tzlocal()``
    """
    if timestamp is None:
        timestamp = time()

    if offset is None and default_offset is None:
        # Get local offset
        dt = datetime.fromtimestamp(timestamp)
        aware = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                         dt.second, dt.microsecond, tzinfo=tzlocal())
        seconds = aware.utcoffset().days * 86400
        seconds += aware.utcoffset().seconds
        offset = seconds / 60
    elif offset is None:
        offset = default_offset

    return pygit2.Signature(name, email, timestamp, offset)
