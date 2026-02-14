import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 42.9,
	"longitude": 71.37,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "uv_index_max", "uv_index_clear_sky_max", "rain_sum", "precipitation_sum", "wind_speed_10m_max"],
	"hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "et0_fao_evapotranspiration", "soil_moisture_0_to_1cm", "temperature_80m", "uv_index", "uv_index_clear_sky", "is_day", "sunshine_duration", "wet_bulb_temperature_2m", "cape", "lifted_index", "convective_inhibition", "freezing_level_height", "total_column_integrated_water_vapour", "shortwave_radiation", "direct_radiation", "diffuse_radiation", "precipitation"],
	"current": ["temperature_2m", "relative_humidity_2m", "is_day", "precipitation", "weather_code", "wind_speed_10m", "rain"],
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process current data. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_is_day = current.Variables(2).Value()
current_precipitation = current.Variables(3).Value()
current_weather_code = current.Variables(4).Value()
current_wind_speed_10m = current.Variables(5).Value()
current_rain = current.Variables(6).Value()

print(f"\nCurrent time: {current.Time()}")
print(f"Current temperature_2m: {current_temperature_2m}")
print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
print(f"Current is_day: {current_is_day}")
print(f"Current precipitation: {current_precipitation}")
print(f"Current weather_code: {current_weather_code}")
print(f"Current wind_speed_10m: {current_wind_speed_10m}")
print(f"Current rain: {current_rain}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
hourly_et0_fao_evapotranspiration = hourly.Variables(3).ValuesAsNumpy()
hourly_soil_moisture_0_to_1cm = hourly.Variables(4).ValuesAsNumpy()
hourly_temperature_80m = hourly.Variables(5).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(6).ValuesAsNumpy()
hourly_uv_index_clear_sky = hourly.Variables(7).ValuesAsNumpy()
hourly_is_day = hourly.Variables(8).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(9).ValuesAsNumpy()
hourly_wet_bulb_temperature_2m = hourly.Variables(10).ValuesAsNumpy()
hourly_cape = hourly.Variables(11).ValuesAsNumpy()
hourly_lifted_index = hourly.Variables(12).ValuesAsNumpy()
hourly_convective_inhibition = hourly.Variables(13).ValuesAsNumpy()
hourly_freezing_level_height = hourly.Variables(14).ValuesAsNumpy()
hourly_total_column_integrated_water_vapour = hourly.Variables(15).ValuesAsNumpy()
hourly_shortwave_radiation = hourly.Variables(16).ValuesAsNumpy()
hourly_direct_radiation = hourly.Variables(17).ValuesAsNumpy()
hourly_diffuse_radiation = hourly.Variables(18).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(19).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
hourly_data["temperature_80m"] = hourly_temperature_80m
hourly_data["uv_index"] = hourly_uv_index
hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
hourly_data["is_day"] = hourly_is_day
hourly_data["sunshine_duration"] = hourly_sunshine_duration
hourly_data["wet_bulb_temperature_2m"] = hourly_wet_bulb_temperature_2m
hourly_data["cape"] = hourly_cape
hourly_data["lifted_index"] = hourly_lifted_index
hourly_data["convective_inhibition"] = hourly_convective_inhibition
hourly_data["freezing_level_height"] = hourly_freezing_level_height
hourly_data["total_column_integrated_water_vapour"] = hourly_total_column_integrated_water_vapour
hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
hourly_data["direct_radiation"] = hourly_direct_radiation
hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
hourly_data["precipitation"] = hourly_precipitation

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("\nHourly data\n", hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_uv_index_max = daily.Variables(5).ValuesAsNumpy()
daily_uv_index_clear_sky_max = daily.Variables(6).ValuesAsNumpy()
daily_rain_sum = daily.Variables(7).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(8).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(9).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["uv_index_max"] = daily_uv_index_max
daily_data["uv_index_clear_sky_max"] = daily_uv_index_clear_sky_max
daily_data["rain_sum"] = daily_rain_sum
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max

daily_dataframe = pd.DataFrame(data = daily_data)
print("\nDaily data\n", daily_dataframe)
