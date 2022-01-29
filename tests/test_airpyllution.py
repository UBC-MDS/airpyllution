from airpyllution import airpyllution
from pandas._testing import assert_frame_equal
from unittest.mock import patch
from constants import (
    mock_api_invalid_key_error,
    mock_error_params,
    mock_forecast_data,
    mock_history_data,
    mock_incorrect_params,
    mock_params,
    mock_pollution_data,
    mock_invalid_message,
)
from airpyllution.utils import convert_data_to_pandas
import altair as alt
from math import floor


def mocked_requests_get_pollution(*args, **kwargs):
    """
    Function for mocking a Response object.
    This intercepts any API calls when called within the test suite and returns
    an instance of a MockResponse object. This should be used with
    the @patch decorator.
    """

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (
        kwargs["url"]
        == "http://api.openweathermap.org/data/2.5/air_pollution/history"
    ):

        if kwargs["params"]["appid"] == "invalid_api_key":
            return MockResponse(mock_api_invalid_key_error, 404)

        if kwargs["params"]["appid"] == "api_error":
            return "ERROR"

        return MockResponse(mock_history_data, 200)

    elif (
        kwargs["url"] == "http://api.openweathermap.org/data/2.5/air_pollution"
    ):

        if kwargs["params"]["appid"] == "invalid_api_key":
            return MockResponse(mock_api_invalid_key_error, 404)

        if kwargs["params"]["appid"] == "api_error":
            return "ERROR"

        return MockResponse(mock_pollution_data, 200)

    elif (
        kwargs["url"]
        == "http://api.openweathermap.org/data/2.5/air_pollution/forecast"
    ):

        if kwargs["params"]["appid"] == "invalid_api_key":
            return MockResponse(mock_api_invalid_key_error, 404)

        if kwargs["params"]["appid"] == "api_error":
            return "ERROR"
        return MockResponse(mock_forecast_data, 200)

    return MockResponse({"cod": 401, "message": mock_invalid_message,}, 404,)


@patch("requests.get", side_effect=mocked_requests_get_pollution)
def test_pollution_history(mock_api_call):
    """Test fetching pollution history from API"""

    # Invalid input type
    assert (
        airpyllution.get_pollution_history(
            mock_incorrect_params["start"],
            mock_params["end"],
            mock_params["lat"],
            mock_params["lon"],
            mock_params["appid"],
        )
        == "start_date input should be an int"
    )

    # Invalid input type
    assert (
        airpyllution.get_pollution_history(
            mock_params["start"],
            mock_incorrect_params["end"],
            mock_params["lat"],
            mock_params["lon"],
            mock_params["appid"],
        )
        == "end_date input should be an int"
    )

    # Invalid input type
    assert (
        airpyllution.get_pollution_history(
            mock_params["start"],
            mock_params["end"],
            mock_incorrect_params["lat"],
            mock_params["lon"],
            mock_params["appid"],
        )
        == "Latitude input should be a float"
    )

    # Invalid input type
    assert (
        airpyllution.get_pollution_history(
            mock_params["start"],
            mock_params["end"],
            mock_params["lat"],
            mock_incorrect_params["lon"],
            mock_params["appid"],
        )
        == "Longitude input should be a float"
    )

    # API error
    assert (
        airpyllution.get_pollution_history(
            mock_params["start"],
            mock_params["end"],
            mock_params["lat"],
            mock_params["lon"],
            mock_error_params["appid"],
        )
        == "An error occurred requesting data from the API"
    )

    # Invalid API key, tests nested try-except
    assert (
        airpyllution.get_pollution_history(
            mock_params["start"],
            mock_params["end"],
            mock_params["lat"],
            mock_params["lon"],
            mock_incorrect_params["appid"],
        )
        == mock_invalid_message
    )

    pollution_data_frame = airpyllution.get_pollution_history(
        mock_params["start"],
        mock_params["end"],
        mock_params["lat"],
        mock_params["lon"],
        mock_params["appid"],
    )

    assert_frame_equal(
        pollution_data_frame, convert_data_to_pandas(mock_history_data)
    )


@patch("requests.get", side_effect=mocked_requests_get_pollution)
def test_air_pollution(mock_api_call):
    """Tests get air pollution function"""

    # Invalid input type
    assert (
        airpyllution.get_air_pollution(
            mock_incorrect_params["lat"],
            mock_params["lon"],
            mock_params["appid"],
        )
        == "Latitude input should be a float or an integer"
    )

    assert (
        airpyllution.get_air_pollution(
            mock_params["lat"],
            mock_incorrect_params["lon"],
            mock_params["appid"],
        )
        == "Longitude input should be a float or an integer"
    )

    assert (
        airpyllution.get_air_pollution(
            mock_params["lat"], mock_params["lon"], 0
        )
        == "API Key should be a string"
    )

    # Invalid input values
    assert (
        airpyllution.get_air_pollution(
            mock_incorrect_params["lat_oor"],
            mock_params["lon"],
            mock_params["appid"],
        )
        == "Enter valid latitude values (Range should be -90<Latitude<90)"
    )

    assert (
        airpyllution.get_air_pollution(
            mock_params["lat"],
            mock_incorrect_params["lon_oor"],
            mock_params["appid"],
        )
        == "Enter valid longitude values (Range should be -180<Longitude<180)"
    )

    # API error
    assert (
        airpyllution.get_air_pollution(
            mock_params["lat"], mock_params["lon"], mock_error_params["appid"],
        )
        == "An error occurred requesting data from the API"
    )

    assert (
        airpyllution.get_air_pollution(
            mock_params["lat"],
            mock_params["lon"],
            mock_incorrect_params["appid"],
        )
        == mock_invalid_message
    )

    assert (
        airpyllution.get_air_pollution(
            mock_params["lat"], mock_params["lon"], mock_params["appid"], 0
        )
        == "Figure title should be a string"
    )

    # Functionality check with mocked data
    fig = airpyllution.get_air_pollution(
        mock_params["lat"], mock_params["lon"], mock_params["appid"], "test"
    )
    # Check that the plot is a geographic scatter plot
    assert fig["data"][0]["type"] == "scattergeo"
    # Check that there are 8 pollutants
    assert len(fig["data"]) == 8
    # Check that the plot title matches fig_title
    assert fig["layout"]["title"]["text"] == "test"
    # Check that the legend title is correct
    assert fig["layout"]["legend"]["title"]["text"] == "Pollutant"
    # Check that the latitude value is correct on the plot
    assert floor(fig["data"][0]["lat"][0]) == floor(mock_params["lat"])
    # Check that the longitude value is correct on the plot
    assert floor(fig["data"][0]["lon"][0]) == floor(mock_params["lon"])


@patch("requests.get", side_effect=mocked_requests_get_pollution)
def test_pollution_forecast(mock_api_call):
    """Tests pollution forecast function"""

    # Invalid input type
    assert (
        airpyllution.get_pollution_forecast(
            mock_incorrect_params["lat"],
            mock_params["lon"],
            mock_params["appid"],
        )
        == "Latitude input should be a float"
    )

    assert (
        airpyllution.get_pollution_forecast(
            mock_params["lat"],
            mock_incorrect_params["lon"],
            mock_params["appid"],
        )
        == "Longitude input should be a float"
    )

    assert (
        airpyllution.get_pollution_forecast(
            mock_params["lat"], mock_params["lon"], 0
        )
        == "API Key should be a string"
    )

    # Invalid input values
    assert (
        airpyllution.get_pollution_forecast(
            mock_incorrect_params["lat_oor"],
            mock_params["lon"],
            mock_params["appid"],
        )
        == "Enter valid latitude values (Range should be -90<Latitude<90)"
    )

    assert (
        airpyllution.get_pollution_forecast(
            mock_params["lat"],
            mock_incorrect_params["lon_oor"],
            mock_params["appid"],
        )
        == "Enter valid longitude values (Range should be -180<Longitude<180)"
    )

    assert (
        airpyllution.get_pollution_forecast(
            mock_params["lat"], mock_params["lon"], mock_error_params["appid"],
        )
        == "An error occurred requesting data from the API"
    )

    assert (
        airpyllution.get_pollution_forecast(
            mock_params["lat"],
            mock_params["lon"],
            mock_incorrect_params["appid"],
        )
        == mock_invalid_message
    )

    # Functionality check with mocked data
    forecast_chart = airpyllution.get_pollution_forecast(
        mock_params["lat"], mock_params["lon"], mock_params["appid"]
    )

    assert forecast_chart.columns == 3
    assert len(forecast_chart.data) > 2
    assert len(forecast_chart.data) == 16
    assert (
        forecast_chart.title == "Pollutant concentration for the next 5 days"
    )
    chart_dict = forecast_chart.to_dict()
    assert chart_dict["facet"] == alt.Facet("Pollutants:N").to_dict()
