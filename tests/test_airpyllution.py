from airpyllution import airpyllution
import pandas as pd

def test_pollution_history():
    """Test pollution history function"""
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
        'appid': 'fake'
    }

    assert airpyllution.get_pollution_history(
        mock_incorrect_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid']) == "start_date input should be an int"

    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_incorrect_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid']) == "end_date input should be an int"

    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_incorrect_params['lat'], 
        mock_params['lon'], 
        mock_params['appid']) == "Latitude input should be a float"
    
    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_incorrect_params['lon'], 
        mock_params['appid']) == "Longitude input should be a float"

    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_incorrect_params['appid']) == 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'

def test_pollution_forecast():
    """Tests pollution forecast function"""
    mock_params = {
        'lat': 49.28,
        'lon': 123.12,
        'appid': 'mock_api_key'
    }

    mock_incorrect_params = {
        'lat': 'latitude_val',
        'lon': 'longitude_val',
        'appid': 0,
        'appid_fake': "fake",
        'lat_oor': -100.0,
        'lon_oor': 181.0
    }

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
        mock_incorrect_params['appid']) == "API Key should be a string"
        
    assert airpyllution.get_pollution_forecast(
        mock_incorrect_params['lat_oor'],
        mock_params['lon'],
        mock_params['appid']) == "Enter valid latitude values (Range should be -90<Latitude<90)"

    assert airpyllution.get_pollution_forecast(
        mock_params['lat'],
        mock_incorrect_params['lon_oor'],
        mock_params['appid']) == "Enter valid latitude values (Range should be -180<Longitude<180))"

    # TODO: Checking if API key is false
    # assert airpyllution.get_pollution_history(
    #     mock_params['lat'],
    #     mock_params['lon'],
    #     mock_incorrect_params['appid_fake']) == 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'
