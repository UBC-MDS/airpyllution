
from datetime import datetime

def date_conversion(utime):
    ts = int(utime)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
