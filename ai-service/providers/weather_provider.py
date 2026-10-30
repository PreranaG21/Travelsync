import httpx
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from utils.geo import get_destination_coords

logger = logging.getLogger("travelsync.providers.weather")

WMO_WEATHER_CODES = {
    0: ("Clear sky", "Sunny", True),
    1: ("Mainly clear", "Mostly Sunny", True),
    2: ("Partly cloudy", "Partly Cloudy", True),
    3: ("Overcast", "Cloudy", True),
    45: ("Fog", "Foggy", True),
    48: ("Depositing rime fog", "Foggy", True),
    51: ("Light drizzle", "Light Drizzle", True),
    53: ("Moderate drizzle", "Drizzle", True),
    55: ("Dense drizzle", "Drizzle", False),
    61: ("Slight rain", "Light Rain", True),
    63: ("Moderate rain", "Rainy", False),
    65: ("Heavy rain", "Heavy Rain", False),
    80: ("Slight rain showers", "Showers", True),
    81: ("Moderate rain showers", "Rain Showers", False),
    82: ("Violent rain showers", "Heavy Rain", False),
    95: ("Thunderstorm", "Thunderstorm", False),
    96: ("Thunderstorm with slight hail", "Thunderstorm", False),
    99: ("Thunderstorm with heavy hail", "Severe Storm", False),
}

def parse_wmo_code(code: int) -> tuple:
    return WMO_WEATHER_CODES.get(code, ("Pleasant weather", "Partly Cloudy", True))

class WeatherProvider(ABC):
    @abstractmethod
    def get_forecast(self, destination: str, days: int = 5) -> Dict[str, Any]:
        pass

class OpenMeteoWeatherProvider(WeatherProvider):
    """Fetches real-time weather forecasts via Open-Meteo free API."""

    def get_forecast(self, destination: str, days: int = 5) -> Dict[str, Any]:
        lat, lon = get_destination_coords(destination)
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
        )

        try:
            with httpx.Client(timeout=4.0) as client:
                res = client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    daily = data.get("daily", {})
                    dates = daily.get("time", [])
                    max_temps = daily.get("temperature_2m_max", [])
                    min_temps = daily.get("temperature_2m_min", [])
                    precip_probs = daily.get("precipitation_probability_max", [])
                    weathercodes = daily.get("weathercode", [])

                    forecast_list: List[Dict[str, Any]] = []
                    for i in range(min(days, len(dates))):
                        code = weathercodes[i] if i < len(weathercodes) else 1
                        desc, short_cond, outdoor_ok = parse_wmo_code(code)
                        rain_prob = precip_probs[i] if (precip_probs and i < len(precip_probs)) else 15

                        forecast_list.append({
                            "day": i + 1,
                            "date": dates[i] if i < len(dates) else f"Day {i+1}",
                            "temp_max": round(max_temps[i], 1) if i < len(max_temps) else 29.0,
                            "temp_min": round(min_temps[i], 1) if i < len(min_temps) else 23.0,
                            "condition": short_cond,
                            "description": desc,
                            "rain_probability": rain_prob if rain_prob is not None else 15,
                            "is_outdoor_suitable": outdoor_ok and (rain_prob is None or rain_prob < 50)
                        })

                    avg_t = round(sum(f['temp_max'] for f in forecast_list) / max(1, len(forecast_list)))
                    has_rain = any(f['rain_probability'] > 40 for f in forecast_list)

                    return {
                        "destination": destination,
                        "latitude": lat,
                        "longitude": lon,
                        "source": "Open-Meteo API",
                        "forecast": forecast_list,
                        "summary": f"Average {avg_t}°C across {len(forecast_list)} days. {'Expect occasional rain showers.' if has_rain else 'Great sunny/clear conditions expected.'}"
                    }
        except Exception as e:
            logger.warning(f"Open-Meteo weather fetch failed: {e}. Generating fallback forecast.")

        fallback = []
        for day_num in range(1, days + 1):
            fallback.append({
                "day": day_num,
                "date": f"Day {day_num}",
                "temp_max": 29.5,
                "temp_min": 24.0,
                "condition": "Partly Cloudy",
                "description": "Pleasant tropical weather with gentle breeze",
                "rain_probability": 20,
                "is_outdoor_suitable": True
            })

        return {
            "destination": destination,
            "latitude": lat,
            "longitude": lon,
            "source": "Weather data temporarily unavailable (Estimated)",
            "forecast": fallback,
            "summary": "Pleasant tropical climate around 29°C, suitable for outdoor activities."
        }

def get_weather_provider() -> WeatherProvider:
    return OpenMeteoWeatherProvider()
