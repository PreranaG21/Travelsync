import logging
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from config.settings import settings

logger = logging.getLogger("travelsync.providers.flight")

AIRLINE_FLEET = {
    "Bali": [
        {"name": "VietJet Air", "code": "VJ", "base_price": 9500, "duration": "8h 15m", "stops": 1},
        {"name": "Singapore Airlines", "code": "SQ", "base_price": 14200, "duration": "7h 40m", "stops": 1},
        {"name": "Garuda Indonesia", "code": "GA", "base_price": 16800, "duration": "6h 50m", "stops": 0},
        {"name": "Batik Air", "code": "OD", "base_price": 10800, "duration": "8h 45m", "stops": 1},
    ],
    "Goa": [
        {"name": "IndiGo", "code": "6E", "base_price": 3200, "duration": "1h 20m", "stops": 0},
        {"name": "Air India Express", "code": "IX", "base_price": 3500, "duration": "1h 15m", "stops": 0},
        {"name": "Akasa Air", "code": "QP", "base_price": 2900, "duration": "1h 25m", "stops": 0},
    ],
    "Mumbai": [
        {"name": "IndiGo", "code": "6E", "base_price": 3800, "duration": "2h 10m", "stops": 0},
        {"name": "Air India", "code": "AI", "base_price": 4600, "duration": "2h 05m", "stops": 0},
        {"name": "Vistara", "code": "UK", "base_price": 5200, "duration": "2h 00m", "stops": 0},
    ],
    "Delhi": [
        {"name": "IndiGo", "code": "6E", "base_price": 3900, "duration": "2h 15m", "stops": 0},
        {"name": "Air India", "code": "AI", "base_price": 4800, "duration": "2h 10m", "stops": 0},
        {"name": "SpiceJet", "code": "SG", "base_price": 3400, "duration": "2h 20m", "stops": 0},
    ],
    "Jaipur": [
        {"name": "IndiGo", "code": "6E", "base_price": 3100, "duration": "1h 45m", "stops": 0},
        {"name": "Alliance Air", "code": "9I", "base_price": 2800, "duration": "1h 50m", "stops": 0},
    ],
    "Bangkok": [
        {"name": "Thai AirAsia", "code": "FD", "base_price": 8200, "duration": "4h 25m", "stops": 0},
        {"name": "Thai Airways", "code": "TG", "base_price": 13500, "duration": "4h 15m", "stops": 0},
        {"name": "IndiGo", "code": "6E", "base_price": 7900, "duration": "4h 30m", "stops": 0},
    ],
    "Singapore": [
        {"name": "Scoot", "code": "TR", "base_price": 8600, "duration": "5h 30m", "stops": 0},
        {"name": "Singapore Airlines", "code": "SQ", "base_price": 17800, "duration": "5h 15m", "stops": 0},
        {"name": "Air India", "code": "AI", "base_price": 11200, "duration": "5h 45m", "stops": 0},
    ],
    "Dubai": [
        {"name": "FlyDubai", "code": "FZ", "base_price": 9400, "duration": "3h 45m", "stops": 0},
        {"name": "Emirates", "code": "EK", "base_price": 16500, "duration": "3h 30m", "stops": 0},
        {"name": "Air India Express", "code": "IX", "base_price": 8500, "duration": "3h 55m", "stops": 0},
    ],
    "Paris": [
        {"name": "Air France", "code": "AF", "base_price": 24500, "duration": "9h 30m", "stops": 0},
        {"name": "Lufthansa", "code": "LH", "base_price": 21500, "duration": "11h 15m", "stops": 1},
        {"name": "Emirates", "code": "EK", "base_price": 23000, "duration": "11h 45m", "stops": 1},
    ],
    "London": [
        {"name": "British Airways", "code": "BA", "base_price": 25500, "duration": "9h 45m", "stops": 0},
        {"name": "Virgin Atlantic", "code": "VS", "base_price": 26000, "duration": "9h 50m", "stops": 0},
        {"name": "Air India", "code": "AI", "base_price": 22000, "duration": "10h 10m", "stops": 0},
    ],
    "Tokyo": [
        {"name": "All Nippon Airways", "code": "NH", "base_price": 28000, "duration": "8h 40m", "stops": 0},
        {"name": "Japan Airlines", "code": "JL", "base_price": 29500, "duration": "8h 35m", "stops": 0},
        {"name": "Singapore Airlines", "code": "SQ", "base_price": 23500, "duration": "11h 20m", "stops": 1},
    ],
    "Rome": [
        {"name": "ITA Airways", "code": "AZ", "base_price": 22500, "duration": "9h 15m", "stops": 0},
        {"name": "Qatar Airways", "code": "QR", "base_price": 21000, "duration": "10h 50m", "stops": 1},
    ],
    "New York": [
        {"name": "Air India", "code": "AI", "base_price": 38000, "duration": "15h 30m", "stops": 0},
        {"name": "United Airlines", "code": "UA", "base_price": 42000, "duration": "16h 00m", "stops": 0},
        {"name": "Emirates", "code": "EK", "base_price": 36000, "duration": "18h 30m", "stops": 1},
    ],
    "Indonesia": [
        {"name": "Garuda Indonesia", "code": "GA", "base_price": 16800, "duration": "6h 50m", "stops": 0},
        {"name": "VietJet Air", "code": "VJ", "base_price": 9500, "duration": "8h 15m", "stops": 1},
        {"name": "Singapore Airlines", "code": "SQ", "base_price": 14200, "duration": "7h 40m", "stops": 1},
        {"name": "Batik Air", "code": "OD", "base_price": 10800, "duration": "8h 45m", "stops": 1},
    ],
    "Japan": [
        {"name": "All Nippon Airways", "code": "NH", "base_price": 28000, "duration": "8h 40m", "stops": 0},
        {"name": "Japan Airlines", "code": "JL", "base_price": 29500, "duration": "8h 35m", "stops": 0},
        {"name": "Singapore Airlines", "code": "SQ", "base_price": 23500, "duration": "11h 20m", "stops": 1},
    ]
}

class FlightProvider(ABC):
    """Abstract base class for Flight Providers."""

    @abstractmethod
    def search_flights(
        self,
        source: str,
        destination: str,
        travelers: int = 1,
        budget: float = 60000.0,
        departure_date: Optional[str] = None
    ) -> Dict[str, Any]:
        pass

class AmadeusFlightProvider(FlightProvider):
    """Live Flight Provider using Amadeus Self-Service Test API."""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def search_flights(
        self,
        source: str,
        destination: str,
        travelers: int = 1,
        budget: float = 60000.0,
        departure_date: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=6.0) as client:
                token_res = client.post(
                    "https://test.api.amadeus.com/v1/security/oauth2/token",
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                if token_res.status_code != 200:
                    raise ValueError(f"Amadeus auth failed with status {token_res.status_code}")
                token = token_res.json().get("access_token")

                origin_code = "BOM" if "mumbai" in source.lower() else ("DEL" if "delhi" in source.lower() else "BOM")
                dest_code = "DPS" if "bali" in destination.lower() else ("GOI" if "goa" in destination.lower() else ("DXB" if "dubai" in destination.lower() else "BKK"))

                flight_res = client.get(
                    "https://test.api.amadeus.com/v2/shopping/flight-offers",
                    params={
                        "originLocationCode": origin_code,
                        "destinationLocationCode": dest_code,
                        "departureDate": departure_date or "2026-09-15",
                        "adults": travelers,
                        "max": 3
                    },
                    headers={"Authorization": f"Bearer {token}"}
                )
                if flight_res.status_code == 200:
                    offers = flight_res.json().get("data", [])
                    results = []
                    for idx, off in enumerate(offers):
                        itinerary = off.get("itineraries", [{}])[0]
                        seg = itinerary.get("segments", [{}])[0]
                        total_p = float(off.get("price", {}).get("total", 12000))
                        price_pp = total_p / max(1, travelers)
                        results.append({
                            "airline": seg.get("carrierCode", "Partner Airline"),
                            "flight_number": f"{seg.get('carrierCode', 'AI')}-{seg.get('number', '302')}",
                            "departure_city": source or "Origin Airport",
                            "arrival_city": destination,
                            "departure_time": seg.get("departure", {}).get("at", "06:30")[-8:-3] if "T" in str(seg.get("departure", {}).get("at", "")) else "06:30",
                            "arrival_time": seg.get("arrival", {}).get("at", "14:45")[-8:-3] if "T" in str(seg.get("arrival", {}).get("at", "")) else "14:45",
                            "duration": itinerary.get("duration", "PT6H30M").replace("PT", "").lower(),
                            "stops": len(itinerary.get("segments", [])) - 1,
                            "price_per_person": round(price_pp, 2),
                            "total_price": round(total_p, 2),
                            "is_live_data": True,
                            "is_demo": False,
                            "recommended": idx == 0
                        })

                    if results:
                        return {
                            "options": results,
                            "recommended_flight": results[0],
                            "is_mock": False,
                            "source": "Amadeus Self-Service API (Live)"
                        }
        except Exception as e:
            logger.warning(f"Amadeus Flight search failed: {e}. Falling back to MockFlightProvider.")

        mock = MockFlightProvider()
        return mock.search_flights(source, destination, travelers, budget, departure_date)

class MockFlightProvider(FlightProvider):
    """Demonstration Flight Provider with labeled mock flight records."""

    def search_flights(
        self,
        source: str,
        destination: str,
        travelers: int = 1,
        budget: float = 60000.0,
        departure_date: Optional[str] = None
    ) -> Dict[str, Any]:
        src = source.strip() if source else "Mumbai"
        dest_key = "Bali"
        for k in AIRLINE_FLEET.keys():
            if k.lower() in destination.lower():
                dest_key = k
                break

        fleet = AIRLINE_FLEET.get(dest_key, AIRLINE_FLEET["Bali"])
        times = [("06:15", "14:30"), ("10:45", "19:15"), ("21:30", "06:00")]

        options = []
        for idx, carrier in enumerate(fleet[:3]):
            dep, arr = times[idx % len(times)]
            base_p = carrier["base_price"]
            total_p = base_p * travelers
            options.append({
                "airline": carrier["name"],
                "flight_number": f"{carrier['code']}-{400 + idx * 25}",
                "departure_city": src,
                "arrival_city": destination,
                "departure_time": dep,
                "arrival_time": arr,
                "duration": carrier["duration"],
                "stops": carrier["stops"],
                "price_per_person": float(base_p),
                "total_price": float(total_p),
                "is_live_data": False,
                "is_demo": True,
                "recommended": idx == 0
            })

        max_flight_budget = budget * 0.45
        options.sort(key=lambda x: (
            0 if x["total_price"] <= max_flight_budget else 1,
            x["total_price"],
            x["stops"]
        ))
        for idx, opt in enumerate(options):
            opt["recommended"] = (idx == 0)

        return {
            "options": options,
            "recommended_flight": options[0] if options else {},
            "is_mock": True,
            "source": "Demo flight data"
        }

def get_flight_provider() -> FlightProvider:
    client_id = getattr(settings, 'AMADEUS_CLIENT_ID', '')
    client_secret = getattr(settings, 'AMADEUS_CLIENT_SECRET', '')
    if client_id and client_secret and client_id.strip() and client_secret.strip():
        return AmadeusFlightProvider(client_id.strip(), client_secret.strip())
    return MockFlightProvider()
