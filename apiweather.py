# -*- coding: utf-8 -*-

import requests
import pandas as pd
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo



def fetch_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    dt = data.get("dt")
    # Convert timestamp to UTC
    utc_time = datetime.fromtimestamp(dt, tz=timezone.utc)

    # Convert to Asia/Bangkok timezone
    bangkok_time = utc_time.astimezone(ZoneInfo("Asia/Bangkok"))

    weather_data = {
        "coord.lon": data["coord"].get("lon"),
        "coord.lat": data["coord"].get("lat"),
        "weather.id": data["weather"][0].get("id"),
        "weather.main": data["weather"][0].get("main"),
        "weather.description": data["weather"][0].get("description"),
        "weather.icon": data["weather"][0].get("icon"),
        "base": data.get("base"),
        "main.temp": data["main"].get("temp"),
        "main.feels_like": data["main"].get("feels_like"),
        "main.pressure": data["main"].get("pressure"),
        "main.humidity": data["main"].get("humidity"),
        "main.temp_min": data["main"].get("temp_min"),
        "main.temp_max": data["main"].get("temp_max"),
        "main.sea_level": data["main"].get("sea_level"),
        "main.grnd_level": data["main"].get("grnd_level"),
        "visibility": data.get("visibility"),
        "wind.speed": data["wind"].get("speed"),
        "wind.deg": data["wind"].get("deg"),
        "wind.gust": data["wind"].get("gust"),
        "clouds.all": data["clouds"].get("all"),
        "rain.1h": data.get("rain", {}).get("1h"),
        "snow.1h": data.get("snow", {}).get("1h"),
        "dt": bangkok_time,
        "acq_date" : bangkok_time.date(),
        "acq_time" : bangkok_time.strftime('%H:%M:%S'),
        "sys.type": data["sys"].get("type"),
        "sys.id": data["sys"].get("id"),
        "sys.country": data["sys"].get("country"),
        "sys.sunrise": data["sys"].get("sunrise"),
        "sys.sunset": data["sys"].get("sunset"),
        "timezone": data.get("timezone"),
        "id": data.get("id"),
        "name": data.get("name"),
        "cod": data.get("cod")
    }

    return weather_data

# Example usage
api_key = "c3c394ef76cc381e330ecdf90d766a10"  # Replace with your OpenWeatherMap API key
city = "Bangkok"  # Replace with the city of your choice

df = pd.DataFrame()
new_data = fetch_weather_data(city, api_key)
df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
print(df)
