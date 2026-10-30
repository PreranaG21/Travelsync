import logging
import httpx
from typing import Dict, Any, List
from config.settings import settings

logger = logging.getLogger("travelsync.flight")

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
    ]
}

def search_amadeus_flights(source: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """Attempts live search via Amadeus Test API if configured."""
    client_id = settings.AMADEUS_CLIENT_ID
    client_secret = settings.AMADEUS_CLIENT_SECRET
    
    if not client_id or not client_secret:
        return []
        
    try:
        with httpx.Client(timeout=5.0) as client:
            token_res = client.post(
                "https://test.api.amadeus.com/v1/security/oauth2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if token_res.status_code != 200:
                return []
            token = token_res.json().get("access_token")
            
            # Simple airport code resolution fallback
            origin_code = "BOM" if "mumbai" in source.lower() else ("DEL" if "delhi" in source.lower() else "BOM")
            dest_code = "DPS" if "bali" in destination.lower() else ("GOI" if "goa" in destination.lower() else "BKK")
            
            flight_res = client.get(
                "https://test.api.amadeus.com/v2/shopping/flight-offers",
                params={
                    "originLocationCode": origin_code,
                    "destinationLocationCode": dest_code,
                    "departureDate": date or "2026-09-15",
                    "adults": 1,
                    "max": 3
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            if flight_res.status_code == 200:
                offers = flight_res.json().get("data", [])
                results = []
                for off in offers:
                    itinerary = off.get("itineraries", [{}])[0]
                    seg = itinerary.get("segments", [{}])[0]
                    price_val = float(off.get("price", {}).get("total", 12000))
                    results.append({
                        "airline": seg.get("carrierCode", "Amadeus Partner"),
                        "flight_number": f"{seg.get('carrierCode', 'AI')}-{seg.get('number', '302')}",
                        "departure_city": source or "Origin Airport",
                        "arrival_city": destination,
                        "departure_time": seg.get("departure", {}).get("at", "06:30"),
                        "arrival_time": seg.get("arrival", {}).get("at", "14:45"),
                        "duration": itinerary.get("duration", "PT6H30M").replace("PT", "").lower(),
                        "stops": len(itinerary.get("segments", [])) - 1,
                        "price_per_person": price_val,
                        "is_live_data": True
                    })
                return results
    except Exception as e:
        logger.warning(f"Amadeus search failed: {e}. Switching to mock data.")
    return []

def get_flight_options(source: str, destination: str, travelers: int = 1, budget: float = 60000.0) -> Dict[str, Any]:
    """
    Retrieves flights for the given source and destination.
    Uses Amadeus test API or generates realistic fallback flight options ranked by budget and duration.
    """
    src = source.strip() if source else "Mumbai"
    dest_key = "Bali"
    for k in AIRLINE_FLEET.keys():
        if k.lower() in destination.lower():
            dest_key = k
            break
            
    fleet = AIRLINE_FLEET.get(dest_key, AIRLINE_FLEET["Bali"])
    
    # Try Amadeus first
    live_flights = search_amadeus_flights(src, destination, "")
    
    flight_options: List[Dict[str, Any]] = []
    
    if live_flights:
        for idx, f in enumerate(live_flights):
            total_price = f["price_per_person"] * travelers
            flight_options.append({
                "airline": f["airline"],
                "flight_number": f["flight_number"],
                "departure_city": src,
                "arrival_city": destination,
                "departure_time": f["departure_time"],
                "arrival_time": f["arrival_time"],
                "duration": f["duration"],
                "stops": f["stops"],
                "price_per_person": f["price_per_person"],
                "total_price": total_price,
                "is_live_data": True,
                "recommended": idx == 0
            })
    else:
        # Generate realistic mock options
        times = [("06:15", "14:30"), ("10:45", "19:15"), ("21:30", "06:00")]
        for idx, carrier in enumerate(fleet[:3]):
            dep, arr = times[idx % len(times)]
            base_p = carrier["base_price"]
            # Adjust price slightly for realism
            price_person = base_p
            total_price = price_person * travelers
            flight_options.append({
                "airline": carrier["name"],
                "flight_number": f"{carrier['code']}-{400 + idx * 25}",
                "departure_city": src,
                "arrival_city": destination,
                "departure_time": dep,
                "arrival_time": arr,
                "duration": carrier["duration"],
                "stops": carrier["stops"],
                "price_per_person": price_person,
                "total_price": total_price,
                "is_live_data": False,
                "recommended": False
            })

    # Sort options by price first when budget is constrained, while balancing stops
    # Priority: flight total price <= (budget * 0.45)
    max_flight_budget = budget * 0.45
    flight_options.sort(key=lambda x: (
        0 if x["total_price"] <= max_flight_budget else 1,
        x["total_price"],
        x["stops"]
    ))
    if flight_options:
        for opt in flight_options:
            opt["recommended"] = False
        flight_options[0]["recommended"] = True
        recommended_flight = flight_options[0]
    else:
        recommended_flight = {}

    return {
        "options": flight_options,
        "recommended_flight": recommended_flight,
        "is_mock": not bool(live_flights),
        "source": "Amadeus Self-Service API" if live_flights else "Demonstration Flight Engine"
    }
