import pytest
from providers.hotel_provider import get_hotel_provider, MockHotelProvider
from providers.flight_provider import get_flight_provider, MockFlightProvider
from providers.weather_provider import get_weather_provider
from providers.attraction_provider import get_attraction_provider

def test_hotel_provider():
    provider = get_hotel_provider()
    hotels = provider.search_hotels(destination="Bali", duration_days=5, travelers=2, budget=60000.0)
    assert len(hotels) >= 1
    assert "hotel_name" in hotels[0]
    assert "price_per_night" in hotels[0]
    assert "total_price" in hotels[0]
    assert hotels[0]["total_price"] > 0

def test_flight_provider():
    provider = get_flight_provider()
    res = provider.search_flights(source="Mumbai", destination="Bali", travelers=2, budget=60000.0)
    assert "options" in res
    assert len(res["options"]) >= 1
    assert res["recommended_flight"] is not None
    assert res["recommended_flight"]["total_price"] > 0

def test_weather_provider():
    provider = get_weather_provider()
    forecast = provider.get_forecast(destination="Bali", days=5)
    assert "forecast" in forecast
    assert len(forecast["forecast"]) == 5
    assert "temp_max" in forecast["forecast"][0]

def test_attraction_provider():
    provider = get_attraction_provider()
    attrs = provider.search_attractions(destination="Bali")
    assert len(attrs) >= 3
    assert "attraction_name" in attrs[0]
    assert "category" in attrs[0]
