import requests
from airpyllution.utils import convert_data_to_pandas
import plotly.express as px
import altair as alt
import pandas as pd

alt.renderers.enable("mimetype")

# import constants
OPEN_WEATHER_MAP_URL = "http://api.openweathermap.org/data/2.5/air_pollution"


def get_pollution_history(start_date, end_date, lat, lon, api_key):
    """Returns a dataframe of pollution history for a location between
    a specified date range

    Given a specified date range, the function makes an API request to
    the OpenWeather Air Pollution API and fetches historic pollution data
    for a given location.

    The function transforms the returned JSON object from the request into
    a Pandas dataframe.

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
        a dataframe of the data returned from the API.
        Columns are as followed:
        ==========  =================================================
        date        int
        co          float: Carbon monoxide
        no          float: Nitrogen monoxide
        no2         float: Nitrogen dioxide
        o3          float: Ozone
        so2         float: Sulphur Dioxide
        pm2_5       float: Particulates 2.5
        pm10        float: Particulates 10
        nh3         float: Ammonia
        ==========  ==================================================
    Examples
    --------
    >>> get_pollution_history(1606488670, 1606747870, 49.28, 123.12,
    "APIKEY_example")
    0 1606482000 270.367 5.867 43.184 4.783 14.544 13.448 15.524 0.289
    1 1606478400 280.38 8.605 42.155 2.459 14.901 15.103 17.249 0.162
    2 1606474800 293.732 13.523 41.47 1.173 15.14 17.727 19.929 0.072
    """

    # api_key = app.config["OPEN_WEATHER_MAP_API_KEY"]

    if not isinstance(lat, (float, int)):
        return "Latitude input should be a float"

    if not isinstance(lon, (float, int)):
        return "Longitude input should be a float"

    if not isinstance(start_date, int):
        return "start_date input should be an int"

    if not isinstance(end_date, int):
        return "end_date input should be an int"

    url = OPEN_WEATHER_MAP_URL + "/history"
    params = {
        "lat": lat,
        "lon": lon,
        "start": start_date,
        "end": end_date,
        "appid": api_key,
    }

    try:
        response = requests.get(url=url, params=params)
        response_obj = response.json()

        try:
            data = convert_data_to_pandas(response_obj)
            return data
        except Exception:
            if "cod" in response_obj:
                return response_obj["message"]
    except Exception:
        return "An error occurred requesting data from the API"


def get_air_pollution(lat, lon, api_key, fig_title=""):
    """Returns a map depicting varying pollution levels for a specified location.

    The function makes an API request to the OpenWeather Air Pollution
    API and fetches pollution data for a given location.

    The function transforms the returned JSON object from the request
    into a plotly plot.

    Parameters
    ----------
    lat : float
        geographical latitude coordinate for the location
    lon : float
        geographical longitude coordinate for the location
    api_key: string
        OpenWeather API key
    fig_title: string
        title of returned figure
    Returns
    -------
    plotly.graph_objs._figure.Figure

    Examples
    --------
    >>> get_air_pollution(49.2497, -123.1193, "APIKEY_example")
    """
    if not isinstance(lat, (float, int)):
        return "Latitude input should be a float or an integer"

    if not isinstance(lon, (float, int)):
        return "Longitude input should be a float or an integer"

    if not isinstance(api_key, str):
        return "API Key should be a string"

    if lat < -90.0 or lat > 90.0:
        return "Enter valid latitude values (Range should be -90<Latitude<90)"

    if lon < -180.0 or lon > 180.0:
        return (
            "Enter valid longitude values (Range should be -180<Longitude<180)"
        )

    if not isinstance(fig_title, str):
        return "Figure title should be a string"

    url = OPEN_WEATHER_MAP_URL
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
    }

    try:
        response = requests.get(url=url, params=params)
        response_obj = response.json()
        try:
            data = convert_data_to_pandas(response_obj)
        except Exception:
            if "cod" in response_obj:
                return response_obj["message"]
    except Exception:
        return "An error occurred requesting data from the API"

    data = data.melt(
        id_vars=["lon", "lat"],
        value_vars=["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"],
    )

    data = data.replace(
        {
            "co": "CO",
            "no": "NO",
            "no2": "NO2",
            "o3": "O3",
            "so2": "SO2",
            "pm2_5": "PM2.5",
            "pm10": "PM10",
            "nh3": "NH3",
        }
    )

    fig = px.scatter_geo(
        data,
        lon="lon",
        lat="lat",
        color="variable",
        size="value",
        projection="natural earth",
        labels={
            "lon": "Longitude",
            "lat": "Latitude",
            "variable": "Pollutant",
            "value": "Conc. (µg/m^3)",
        },
        title=fig_title,
    )

    fig.update_layout(
        legend={"yanchor": "middle", "y": 0.72, "xanchor": "right", "x": 1.2},
        title={"y": 0.85, "x": 0.47, "xanchor": "center", "yanchor": "top"},
    )

    return fig


def get_pollution_forecast(lat, lon, api_key):
    """Returns a time series plot showing predicted pollutant levels
    for the next 5 days.

    Performs an API request to OpenWeather Air Pollution API,
    retrieves weather forecast for the next 5 days, and creates a time series
    graph of the pollutants with their concentration levels.

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
    if not isinstance(lat, (float, int)):
        return "Latitude input should be a float"

    if not isinstance(lon, (float, int)):
        return "Longitude input should be a float"

    if not isinstance(api_key, str):
        return "API Key should be a string"

    if lat < -90.0 or lat > 90.0:
        return "Enter valid latitude values (Range should be -90<Latitude<90)"

    if lon < -180.0 or lon > 180.0:
        return (
            "Enter valid longitude values (Range should be -180<Longitude<180)"
        )

    url = OPEN_WEATHER_MAP_URL + "/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key}

    try:
        response = requests.get(url=url, params=params)
        response_obj = response.json()
        try:
            data = convert_data_to_pandas(response_obj)
        except Exception:
            if "cod" in response_obj:
                return response_obj["message"]
    except Exception:
        return "An error occurred requesting data from the API"

    if len(data) >= 1:
        try:
            data = data.melt(
                id_vars=["dt"],
                value_vars=[
                    "co",
                    "no",
                    "no2",
                    "o3",
                    "so2",
                    "pm2_5",
                    "pm10",
                    "nh3",
                ],
                var_name="Pollutants",
                value_name="Concentration",
            )
            data["dt"] = pd.to_datetime(data["dt"])
            chart = (
                alt.Chart(data)
                .mark_line()
                .encode(
                    x=alt.X("dt", title="date"),
                    y=alt.Y("Concentration", title="Concentration"),
                    color=alt.Color("Pollutants"),
                )
                .properties(width=100, height=100)
                .facet(facet="Pollutants:N", columns=3)
                .resolve_axis(x="independent", y="independent")
                .resolve_scale(x="independent", y="independent")
                .properties(
                    title="Pollutant concentration for the next 5 days",
                )
                .configure_title(fontSize=24, anchor="middle")
            )
        except Exception:
            return "An error occured in plotting"
        return chart
    else:
        return "Insufficient data to forecast/plot."
