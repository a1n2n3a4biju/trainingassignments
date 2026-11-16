
import httpx
from langchain_core.tools import tool


@tool
def weather_forecast_tool(
    destination: str,
    start_date: str,
    end_date: str
):
    """Retrieve actual weather forecast for a destination and travel dates."""

    location = get_coordinates(destination)

    if location is None:
        return {
            "error": "Destination not found"
        }

    weather = get_weather(
        location["latitude"],
        location["longitude"],
        start_date,
        end_date
    )

    if weather is None:
        return {
            "error": "Weather forecast unavailable"
        }

    return {
        "location": location,
        "forecast": weather
    }

# STEP 1: Convert city name into latitude and longitude

def get_coordinates(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = httpx.get(url, params=params, timeout=15)

    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    location = data["results"][0]

    return {
        "city": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    }


# STEP 2: Fetch weather forecast

def get_weather(latitude, longitude, start_date, end_date):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weather_code"
        ],
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto"
    }

    response = httpx.get(url, params=params, timeout=20)

    response.raise_for_status()

    data = response.json()

    if "daily" not in data:
        return None

    daily = data["daily"]

    if not daily.get("time"):
        return None

    weather_records = []

    for i in range(len(daily["time"])):

        weather_records.append({
            "date": daily["time"][i],
            "max_temperature": daily["temperature_2m_max"][i],
            "min_temperature": daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
            "weather_code": daily["weather_code"][i]
        })

    return weather_records


# STEP 3: Test the weather functions

if __name__ == "__main__":

    city = "Jaipur"

    print("Getting location details...")

    location = get_coordinates(city)

    if location:

        print("Location found!")
        print(location)

        print("\nFetching weather forecast...")

        weather = get_weather(
            location["latitude"],
            location["longitude"],
            "2026-11-20",
            "2026-11-23"
        )

        if weather:

            print("\nWeather Forecast:")

            for day in weather:
                print(day)

        else:
            print("Weather forecast is unavailable.")

    else:
        print("City not found!")
