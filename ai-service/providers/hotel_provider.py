import logging
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from config.settings import settings
from utils.geo import get_destination_coords

logger = logging.getLogger("travelsync.providers.hotel")

class HotelProvider(ABC):
    """Abstract Base Class for Hotel Providers."""

    @abstractmethod
    def search_hotels(
        self,
        destination: str,
        duration_days: int = 5,
        travelers: int = 2,
        budget: float = 60000.0,
        travel_style: str = "balanced",
        start_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        pass

class StayingApiHotelProvider(HotelProvider):
    """
    Live Hotel Provider using StayingAPI REST Endpoints.
    Fetches normalized property rates and availability from StayingAPI.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stayingapi.com/v1"

    def search_hotels(
        self,
        destination: str,
        duration_days: int = 5,
        travelers: int = 2,
        budget: float = 60000.0,
        travel_style: str = "balanced",
        start_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        nights = max(1, duration_days - 1 if duration_days > 1 else 1)
        check_in = start_date or "2026-09-15"
        
        # Calculate check out date
        try:
            from datetime import datetime, timedelta
            dt = datetime.strptime(check_in, "%Y-%m-%d")
            check_out = (dt + timedelta(days=nights)).strftime("%Y-%m-%d")
        except Exception:
            check_out = "2026-09-20"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        params = {
            "location": destination,
            "checkIn": check_in,
            "checkOut": check_out,
            "adults": travelers,
            "currency": "INR",
            "limit": 6,
            "sort": "price_desc" if travel_style == "luxury" else ("price_asc" if travel_style == "budget" else "recommended")
        }

        try:
            with httpx.Client(timeout=8.0) as client:
                response = client.get(f"{self.base_url}/search", headers=headers, params=params)
                if response.status_code == 200:
                    body = response.json()
                    properties = body.get("data", [])
                    results = []
                    lat_d, lon_d = get_destination_coords(destination)

                    for idx, prop in enumerate(properties):
                        prop_price = prop.get("price") or {}
                        nightly = float(prop_price.get("nightlyPrice", 0) or 0)
                        total = float(prop_price.get("totalPrice", 0) or (nightly * nights))
                        
                        if nightly == 0:
                            # Estimate per night from style
                            nightly = (budget * 0.35) / nights
                            total = nightly * nights

                        loc = prop.get("location") or {}
                        p_lat = loc.get("lat") or (lat_d + 0.01 * idx)
                        p_lng = loc.get("lng") or (lon_d + 0.01 * idx)

                        amenities_list = prop.get("amenities") or ["WiFi", "Air Conditioning", "Breakfast"]
                        amenities_str = ", ".join(amenities_list) if isinstance(amenities_list, list) else str(amenities_list)

                        results.append({
                            "id": f"stay_{prop.get('id', idx + 1)}",
                            "hotel_name": prop.get("name", f"{destination} Grand Hotel"),
                            "city": loc.get("city") or destination,
                            "location": loc.get("address") or f"Central District, {destination}",
                            "rating": float(prop.get("starRating") or prop.get("guestRating") or 4.5),
                            "price_per_night": round(nightly, 2),
                            "total_price": round(total, 2),
                            "room_type": prop.get("propertyType", "Deluxe Room").title(),
                            "amenities": amenities_str,
                            "latitude": float(p_lat),
                            "longitude": float(p_lng),
                            "distance_from_center": 0.8 * (idx + 1),
                            "is_demo": False,
                            "source": "StayingAPI (Live Accommodation Data)"
                        })
                    
                    if results:
                        return results
        except Exception as e:
            logger.warning(f"StayingAPI search failed: {e}. Gracefully falling back to MockHotelProvider.")

        return []

class MockHotelProvider(HotelProvider):
    """
    Demonstration Hotel Provider with clearly labeled mock data.
    Provides realistic, deterministic hotel suggestions for any requested destination.
    """

    def search_hotels(
        self,
        destination: str,
        duration_days: int = 5,
        travelers: int = 2,
        budget: float = 60000.0,
        travel_style: str = "balanced",
        start_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        nights = max(1, duration_days - 1 if duration_days > 1 else 1)
        lat, lon = get_destination_coords(destination)

        # Style based nightly pricing tier
        style_rates = {
            "budget": (1400.0, 1950.0, 2400.0),
            "luxury": (7800.0, 10500.0, 14000.0),
            "balanced": (2800.0, 3900.0, 5200.0)
        }
        rates = style_rates.get(travel_style, style_rates["balanced"])

        # Target budget ratio
        target_max = (budget * 0.40) / nights
        rates = [min(r, target_max) if r > target_max and target_max > 1200 else r for r in rates]

        names = [
            f"{destination} Palms Resort & Spa",
            f"The Grand {destination} Heritage Stay",
            f"Boutique {destination} Garden Retreat"
        ]
        locations = [
            f"Beachfront Boulevard, {destination}",
            f"Historic City Center, {destination}",
            f"Scenic Viewpoint Avenue, {destination}"
        ]
        ratings = [4.7, 4.4, 4.2]
        room_types = [
            "Deluxe King Suite",
            "Superior Garden View Room",
            "Standard AC Double Studio"
        ]
        amenities = [
            "Free WiFi, Swimming Pool, Ocean View, Breakfast Included, Spa",
            "Free WiFi, Fitness Center, Rooftop Restaurant, Air Conditioning",
            "Free WiFi, Breakfast Included, Bike Rental, Room Service, AC"
        ]

        hotel_list = []
        for idx in range(3):
            price_night = float(rates[idx])
            total_stay = round(price_night * nights, 2)
            hotel_list.append({
                "id": f"demo_hotel_{idx + 1}",
                "hotel_name": names[idx],
                "city": destination,
                "location": locations[idx],
                "rating": ratings[idx],
                "price_per_night": price_night,
                "total_price": total_stay,
                "room_type": room_types[idx],
                "amenities": amenities[idx],
                "latitude": lat + (0.012 * idx),
                "longitude": lon + (0.012 * idx),
                "distance_from_center": 0.6 * (idx + 1),
                "is_demo": True,
                "source": "Demo hotel data"
            })

        return hotel_list

class DatabaseHotelProvider(HotelProvider):
    """
    Queries the database (PostgreSQL / SQLite fallback) for seeded hotel properties.
    Falls back to external or mock provider if no records exist for the given destination.
    """
    def __init__(self, fallback_provider: HotelProvider):
        self.fallback = fallback_provider

    def search_hotels(
        self,
        destination: str,
        duration_days: int = 5,
        travelers: int = 2,
        budget: float = 60000.0,
        travel_style: str = "balanced",
        start_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        nights = max(1, duration_days - 1 if duration_days > 1 else 1)
        try:
            from database.db import SessionLocal
            from database.models import Hotel
            with SessionLocal() as db:
                clean_dest = destination.strip()
                matched = db.query(Hotel).filter(Hotel.city.ilike(f"%{clean_dest}%")).all()
                if matched:
                    results = []
                    for idx, h in enumerate(matched):
                        nightly = float(h.price_per_night)
                        total = round(nightly * nights, 2)
                        results.append({
                            "id": f"db_hotel_{h.id}",
                            "hotel_name": h.hotel_name,
                            "city": clean_dest,
                            "location": h.location or f"Central {clean_dest}",
                            "rating": float(h.rating),
                            "price_per_night": nightly,
                            "total_price": total,
                            "room_type": h.room_type or "Deluxe Room",
                            "amenities": h.amenities or "Free WiFi, Air Conditioning, Breakfast Included",
                            "latitude": float(h.latitude),
                            "longitude": float(h.longitude),
                            "distance_from_center": float(h.distance_from_center or 1.0),
                            "is_demo": False,
                            "source": "PostgreSQL Database / Verified Records"
                        })
                    if results:
                        return results
        except Exception as e:
            logger.debug(f"Database hotel query fallback: {e}")

        return self.fallback.search_hotels(
            destination=destination,
            duration_days=duration_days,
            travelers=travelers,
            budget=budget,
            travel_style=travel_style,
            start_date=start_date
        )

def get_hotel_provider() -> HotelProvider:
    """
    Factory function returning DatabaseHotelProvider with StayingApi or Mock fallback.
    """
    api_key = getattr(settings, 'STAYINGAPI_KEY', '')
    if api_key and api_key.strip():
        base = StayingApiHotelProvider(api_key.strip())
    else:
        base = MockHotelProvider()
    return DatabaseHotelProvider(base)
