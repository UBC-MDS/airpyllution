
from datetime import datetime

def convert_unix_to_date(utime):
    """Returns formatted date time string
    
    Given a UNIX timestamp, this function reformats the timestamp to a string

    Parameters
    ----------
    utime : int
        UNIX timestamp, e.g. 1606488670
    Returns
    -------
    datetime 
    Examples
    --------
    >>> date_conversion(1606488670)
    2020-11-27 17:00:00
    """ 
    ts = int(utime)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
