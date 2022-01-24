from datetime import datetime
import pandas as pd


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
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def convert_data_to_pandas(raw_data):
    """Converts API data from OpenWeatherMap to a pandas dataframe

    Parses the JSON data object and transforms it to a dataframe with a formatted
    date column

    Parameters
    ----------
    raw_data : JSON object

    Returns
    -------
    Pandas.dataframe
    Examples
    --------
    >>> convert_data_to_pandas(data)
    """
    if len(raw_data["list"]) > 1:
        data = pd.DataFrame.from_records(
            list(map(lambda x: x["components"], raw_data["list"]))
        )
        data["dt"] = list(
            map(lambda x: convert_unix_to_date(x["dt"]), raw_data["list"])
        )
    else:
        data = raw_data["coord"]
        data.update(raw_data["list"][0]["components"])
        data = pd.DataFrame.from_records([data])

    return data
