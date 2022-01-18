from airpyllution import airpyllution
import os
from dotenv import load_dotenv

load_dotenv()

def test_pollution_history():
    """Test word counting from a file."""
    mock_params = {
        'lat': 49.28,
        'lon': 123.12,
        'start': 1606488670,
        'end': 1606747870,
        'appid': 'mock_data'
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
        mock_incorrect_params['appid']) == "An error occurred requesting data from the api"

    assert airpyllution.get_pollution_history(
        mock_params['start'], 
        mock_params['end'], 
        mock_params['lat'], 
        mock_params['lon'], 
        mock_params['appid']) == "DATA HERE"