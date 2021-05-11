from datetime import timedelta
from datetime import datetime, tzinfo, timedelta

from utils.formatting import format_label


class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"

    def utcoffset(self, dt):
        return timedelta(0)


def iso_now():
    return datetime.utcnow().replace(tzinfo=simple_utc()).isoformat()
