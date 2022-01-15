# airpyllution
A package for visualizing or obtaining future, historic and current air pollution data using the [OpenWeather API](https://openweathermap.org).

## Summary
This package enables users to explore air pollution levels in locations around the world.
Using the [Air Pollution API](https://openweathermap.org/api/air-pollution), this package provides 3 functions that help to visualise present, future and historic air pollution data.  

The data returned from the API includes the polluting gases such as Carbon monoxide (CO), Nitrogen monoxide (NO), Nitrogen dioxide (NO2), Ozone (O3), Sulphur dioxide (SO2), Ammonia (NH3), and particulates (PM2.5 and PM10).

Using the OpenWeatherMap API requires sign up to gain access to an API key.   
For more information about API call limits and API care recommendations please visit the [OpenWeather how to start](https://openweathermap.org/appid) page.
## Functions
The functions are as follows:
- `get_air_pollution()`
- `get_pollution_history()`
- `get_pollution_forecast()`

### `get_air_pollution()`
Fetches the air pollution levels based on a location. Based on the values of the polluting gases, this package uses the [Air Quality Index](https://en.wikipedia.org/wiki/Air_quality_index#CAQI) to determine the level of pollution for the location and produces a coloured map of the area displaying the varying regions of air quality.

### `get_pollution_history()`
Requires a start and end date and fetches historic air pollution data for a specific location. The function returns a data frame with the values of the polluting gases over the specified date range.

### `get_pollution_forecast()`
Fetches air pollution data for the next 5 days for a specific location. The function returns a time series plot of the predicted pollution levels.


Although there is an abundance of python weather packages and APIs in the Python ecosystem (e.g. [python-weather](https://pypi.org/project/python-weather/), [weather-forecast](https://pypi.org/project/weather-forecast/)), this particular package looks at specifically air pollution data and uses the Air Pollution API from OpenWeather. This is a unique package with functionality that (we believe) has not been made before.

## Installation

```bash
$ pip install airpyllution
```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

Contributors 
- Christopher Alexander (@christopheralex)
- Daniel King (@danfke)
- Mel Liow (@mel-liow)

## License

`airpyllution` was created by Christopher Alexander, Daniel King, Mel Liow. It is licensed under the terms of the MIT license.

## Credits

`airpyllution` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
