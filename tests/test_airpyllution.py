from airpyllution import airpyllution
import pandas as pd
from pandas._testing import assert_frame_equal
from unittest.mock import patch
from constants import *
from airpyllution.utils import *


def mocked_requests_get_pollution_history(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    print(kwargs)
    if kwargs['url'] == 'http://api.openweathermap.org/data/2.5/air_pollution/history':

        if kwargs['params']['appid'] == 'invalid_api_key':
            return MockResponse(mock_api_invalid_key_error, 404)

        return MockResponse(mock_history_data, 200)

    elif kwargs['url'] == 'http://api.openweathermap.org/data/2.5/air_pollution/forecast':
        return MockResponse(mock_forecast_data, 200)
    
    return MockResponse({'cod': 401, 'message': 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.' }, 404)


@patch('requests.get', side_effect=mocked_requests_get_pollution_history)
def test_pollution_history(mock_api_call):
    """Test word counting from a file."""
    mock_params = {
        'lat': 49.28,
        'lon': 123.12,
        'start': 1606488670,
        'end': 1606747870,
        'appid': 'mock_api_key'
    }

    mock_incorrect_params = {
        'lat': 'latitude_val',
        'lon': 'longitude_val',
        'start': 1234.567,
        'end': 3.14159,
        'appid': 'invalid_api_key'
    }

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

    # Test for correct pandas output
    pollution_data_frame = airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid'])
    
    assert_frame_equal(pollution_data_frame, convert_data_to_pandas(mock_history_data))

