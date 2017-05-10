
import datetime
import pytz

def tz2ntz(date_obj, tz, ntz):
    """
    :param date_obj: datetime object
    :param tz: old timezone
    :param ntz: new timezone
    """
    if isinstance(date_obj, datetime.date) and tz and ntz:
        date_obj = date_obj.replace(tzinfo=pytz.timezone(tz))
        return date_obj.astimezone(pytz.timezone(ntz))
    return False
