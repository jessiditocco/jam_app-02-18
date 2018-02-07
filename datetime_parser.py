from dateutil import parser
import pytz
from datetime import datetime


def parse_datetime(timezone, local_dt_str):
    """Takes a timezone and local datetime string and returns date and time"""

    # This takes our local dateime string and parses the string and returns a DT object without TZ
    dt_obj = parser.parse(local_dt_str)

    # This returns a timezone object
    tz = pytz.timezone(timezone)

    # Makes a new datetime object with timezone
    local_time = tz.localize(dt_obj)

    print local_time

parse_datetime(timezone = "America/Los_Angeles", local_dt_str = "2018-02-09T21:00:00")