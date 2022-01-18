from airpyllution import airpyllution
import pandas as pd
from pandas._testing import assert_frame_equal
from unittest.mock import patch
from constants import *
from airpyllution.utils import *


def mocked_requests_get_pollution(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs['url'] == 'http://api.openweathermap.org/data/2.5/air_pollution/history':

        if kwargs['params']['appid'] == 'invalid_api_key':
            return MockResponse(mock_api_invalid_key_error, 404)

        return MockResponse(mock_history_data, 200)

    elif kwargs['url'] == 'http://api.openweathermap.org/data/2.5/air_pollution/forecast':

        if kwargs['params']['appid'] == 'invalid_api_key':
            return MockResponse(mock_api_invalid_key_error, 404)

        return MockResponse(mock_forecast_data, 200)
    
    return MockResponse({'cod': 401, 'message': 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.' }, 404)


@patch('requests.get', side_effect=mocked_requests_get_pollution)
def test_pollution_history(mock_api_call):
    """Test fetching pollution history from API"""

    # Invalid input type
    assert airpyllution.get_pollution_history(
        mock_incorrect_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid']) == "start_date input should be an int"

    # Invalid input type
    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_incorrect_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid']) == "end_date input should be an int"

    # Invalid input type
    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_incorrect_params['lat'], 
        mock_params['lon'], 
        mock_params['appid']) == "Latitude input should be a float"
    
    # Invalid input type
    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_incorrect_params['lon'], 
        mock_params['appid']) == "Longitude input should be a float"

    # Invalid API key
    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_incorrect_params['appid']) == 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'

    pollution_data_frame = airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid'])
    
    assert_frame_equal(pollution_data_frame, convert_data_to_pandas(mock_history_data))

@patch('requests.get', side_effect=mocked_requests_get_pollution)
def test_pollution_forecast(mock_api_call):
    """Tests pollution forecast function"""

    # Invalid input type
    assert airpyllution.get_pollution_forecast(
        mock_incorrect_params['lat'],
        mock_params['lon'],
        mock_params['appid']) == "Latitude input should be a float"

    assert airpyllution.get_pollution_forecast(
        mock_params['lat'],
        mock_incorrect_params['lon'],
        mock_params['appid']) == "Longitude input should be a float"

    assert airpyllution.get_pollution_forecast(
        mock_params['lat'],
        mock_params['lon'],
        0) == "API Key should be a string"
    
    # Invalid input values
    assert airpyllution.get_pollution_forecast(
        mock_incorrect_params['lat_oor'],
        mock_params['lon'],
        mock_params['appid']) == "Enter valid latitude values (Range should be -90<Latitude<90)"

    assert airpyllution.get_pollution_forecast(
        mock_params['lat'],
        mock_incorrect_params['lon_oor'],
        mock_params['appid']) == "Enter valid longitude values (Range should be -180<Longitude<180)"

    assert airpyllution.get_pollution_forecast(
        mock_params['lat'], 
        mock_params['lon'], 
        mock_incorrect_params['appid']) == 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'

    # Functionality check with mocked data
    forecast_chart = airpyllution.get_pollution_forecast(
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid'])
    
    assert forecast_chart.columns == 4 
    assert len(forecast_chart.data) > 2
    assert len(forecast_chart.data) == 16
    assert forecast_chart.title == "Pollutant concentration for the next 5 days"