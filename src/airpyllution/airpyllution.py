import requests
import pandas as pd
from .utils import date_conversion

# import constants
OPEN_WEATHER_MAP_URL = 'http://api.openweathermap.org/data/2.5/air_pollution/history' 

def get_pollution_history(start_date, end_date, lat, lon, api_key):
    """Returns a dataframe of pollution history for a location between a specified date range
    
    Given a specified date range, the function makes an API request to the OpenWeather Air Pollution API and fetches
    historic pollution data for a given location.

    The function transforms the returned JSON object from the request into a Pandas dataframe.

    Note: Historical data is accessible from 27th November 2020

    Parameters
    ----------
    start_date : int
        start date of the time frame as a UNIX timestamp, e.g. 1606488670
    end_date : int
        end date of the time frame as a UNIX timetamp, e.g. 1606747870
    lat : float
        geographical latitude coordinate for the location
    lon : float
        geographical longitude coordinate for the location
    api_key: string
        OpenWeather API key
    Returns
    -------
    pandas.DataFrame
        a dataframe of the data returned from Air Pollution API - columns are as followed:
        ==========  ==============================================================
        date        int
        co          float: Carbon monoxide
        no          float: Nitrogen monoxide
        no2         float: Nitrogen dioxide
        o3          float: Ozone
        so2         float: Sulphur Dioxide
        pm2_5       float: Particulates 2.5
        pm10        float: Particulates 10
        nh3         float: Ammonia
        ==========  ==============================================================
    Examples
    --------
    >>> get_pollution_history(1606488670, 1606747870, 49.28, 123.12, "APIKEY_example")
    0 1606482000 270.367 5.867 43.184 4.783 14.544 13.448 15.524 0.289
    1 1606478400 280.38 8.605 42.155 2.459 14.901 15.103 17.249 0.162
    2 1606474800 293.732 13.523 41.47 1.173 15.14 17.727 19.929 0.072
    """ 

    # api_key = app.config["OPEN_WEATHER_MAP_API_KEY"]

    if not isinstance(lat, float):
        return "Latitude input should be a float"

    if not isinstance(lon, float):
        return "Longitude input should be a float"
    
    if not isinstance(start_date, int):
        return "start_date input should be an int"

    if not isinstance(end_date, int):
        return "end_date input should be an int"

    url = OPEN_WEATHER_MAP_URL
    method = 'GET'
    params = {
        'lat': lat,
        'lon': lon,
        'start': start_date,
        'end': end_date,
        'appid': api_key
    }

    
    response = requests.request(method=method, url=url, params=params)
    response_obj = dict(response.json())

    try: 
        data = pd.DataFrame.from_records(list(map(lambda x:x["components"],response_obj["list"])))
        data["dt"] = list(map(lambda x:date_conversion(x["dt"]),response_obj["list"]))

        return data

    except: 
        if 'cod' in response_obj:
            return response_obj['message']
        
        return "An error occurred requesting data from"
    


def get_air_pollution(lat, lon, api_key):
    """Returns a map depicting varying pollution levels for a specified location.
    
    The function makes an API request to the OpenWeather Air Pollution API and fetches
    pollution data for a given location.

    The function transforms the returned JSON object from the request into an altair chart.

    Parameters
    ----------
    lat : float
        geographical latitude coordinate for the location
    lon : float
        geographical longitude coordinate for the location
    api_key: string
        OpenWeather API key
    Returns
    -------
    altair.Chart

    Examples
    --------
    >>> get_air_pollution(49.2497, -123.1193, "APIKEY_example")
    """

def get_pollution_forecast(lat, lon, api_key):
    """Returns a time series plot showing predicted pollutant levels for the next 5 days.
    
    Performs an API request to OpenWeather Air Pollution API,
    retrieves weather forecast for the next 5 days, and
    creates a time series graph of the pollutants with their concentration levels.

    Parameters
    ----------
    lat : float
        geographical latitude coordinate for the location
    lon : float
        geographical longitude coordinate for the location
    api_key: string
        OpenWeather API key

    Returns
    -------
    altair.Chart
        altair chart object with the x axis as time/UNIX timestamp and 
        y axis as pollutant concentration.
        
    Examples
    --------
    >>> get_pollution_forecast(50, 50, "APIKEY_example")
    """