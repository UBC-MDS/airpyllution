# AirPyllution
A package for visualizing future, historic and current air pollution data using the [OpenWeather API](https://openweathermap.org).

## Summary
This package enables users to explore air pollution levels in locations around the world.
Using the [Air Pollution API](https://openweathermap.org/api/air-pollution), this package provides 3 functions that help to visualise present, future and historic air pollution data.  
The data returned from the API includes the polluting gases such as Carbon monoxide (CO), Nitrogen monoxide (NO), Nitrogen dioxide (NO2), Ozone (O3), Sulphur dioxide (SO2), Ammonia (NH3), and particulates (PM2.5 and PM10).

Using the OpenWeatherMap API requires sign up to gain access to an API key. The API key should be stored in the `config.py` file. (TO ADD)
For more information about API call limits and API care recommendations please visit the OpenWeather [How to start](https://openweathermap.org/appid) page.
## Functions
The functions are as follows:
- `getAirPollution()`
- `getPollutionHistory()`
- `getPollutionForecast()`

### `getAirPollution()`
Fetches the air pollution levels based on a location (string). Based on the values of the polluting gases, this package uses the [Air Quality Index](https://en.wikipedia.org/wiki/Air_quality_index#CAQI) to determine the level of pollution for the location and produces a coloured map of the area displaying the varying regions of air quality.

### `getPollutionHistory()`
Requires a start and end date and fetches historic air pollution data for a specific location. The function returns a data frame with the values of the polluting gases over the specified date range.

### `getPollutionForecast()`
Fetches air pollution data for the next 5 days for a specific location. The function returns a time series plot of the predicted pollution levels.


a paragraph describing where your packages fit into the Python ecosystem (are there any other Python packages that have the same/similar functionality? Provide links to any that do. If none exist, then clearly state this as well).



## Installation

```bash
$ pip install AirPyllution
```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`AirPyllution` was created by Christopher Alexander, Daniel King, Mel Liow. It is licensed under the terms of the MIT license.

## Credits

`AirPyllution` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
