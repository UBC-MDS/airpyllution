from airpyllution import airpyllution
import os
from dotenv import load_dotenv

load_dotenv()

def test_pollution_history():
    """Test word counting from a file."""
    params = {
        'lat': 'lakjs',
        'lon': 123.12,
        'start': 1606488670,
        'end': 1606747870,
        'appid': 'hi'
    }
    # print(os.getenv('OPEN_WEATHER_MAP_API_KEY'))

    actual = airpyllution.get_pollution_history(params['lat'], params['lon'], params['start'], params['end'], params['appid'])
    expected = "Latitude input should be a float"
    assert actual == expected, "pollution history incorrectly returns string"