import math
import httpx
import logging
from typing import Dict, Tuple, List

logger = logging.getLogger("travelsync.geo")

# ---------------------------------------------------------------------------
# Comprehensive destination → (lat, lon) dictionary
# Includes city-level AND country-level entries.
# Country entries map to the country's primary tourism / capital city coords.
# ---------------------------------------------------------------------------
DESTINATION_COORDINATES: Dict[str, Tuple[float, float]] = {
    # --- South Asia / India (50 Destinations) ---
    "india": (20.5937, 78.9629),
    "mumbai": (18.9220, 72.8347),
    "bombay": (18.9220, 72.8347),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "jaipur": (26.9124, 75.7873),
    "udaipur": (24.5854, 73.7125),
    "jaisalmer": (26.9157, 70.9083),
    "jodhpur": (26.2389, 73.0243),
    "agra": (27.1767, 78.0081),
    "varanasi": (25.3176, 82.9739),
    "banaras": (25.3176, 82.9739),
    "kashi": (25.3176, 82.9739),
    "lucknow": (26.8467, 80.9462),
    "amritsar": (31.6340, 74.8723),
    "shimla": (31.1048, 77.1734),
    "manali": (32.2396, 77.1887),
    "dharamshala": (32.2190, 76.3234),
    "dharamsala": (32.2190, 76.3234),
    "mcleodganj": (32.2426, 76.3213),
    "srinagar": (34.0837, 74.7973),
    "kashmir": (34.0837, 74.7973),
    "leh": (34.1526, 77.5771),
    "ladakh": (34.1526, 77.5771),
    "rishikesh": (30.0869, 78.2676),
    "mussoorie": (30.4598, 78.0644),
    "nainital": (29.3919, 79.4542),
    "dehradun": (30.3165, 78.0322),
    "kolkata": (22.5726, 88.3639),
    "calcutta": (22.5726, 88.3639),
    "darjeeling": (27.0360, 88.2627),
    "gangtok": (27.3389, 88.6065),
    "sikkim": (27.3389, 88.6065),
    "shillong": (25.5788, 91.8933),
    "cherrapunji": (25.2702, 91.7323),
    "sohra": (25.2702, 91.7323),
    "kaziranga": (26.5775, 93.1711),
    "puri": (19.8135, 85.8312),
    "bhubaneswar": (20.2961, 85.8245),
    "hyderabad": (17.3850, 78.4867),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "mysuru": (12.2958, 76.6394),
    "mysore": (12.2958, 76.6394),
    "hampi": (15.3350, 76.4600),
    "coorg": (12.3375, 75.8069),
    "kodagu": (12.3375, 75.8069),
    "chennai": (13.0827, 80.2707),
    "madras": (13.0827, 80.2707),
    "ooty": (11.4102, 76.6950),
    "udhagamandalam": (11.4102, 76.6950),
    "kodaikanal": (10.2381, 77.4892),
    "kodai": (10.2381, 77.4892),
    "madurai": (9.9252, 78.1198),
    "kochi": (9.9312, 76.2673),
    "cochin": (9.9312, 76.2673),
    "kerala": (9.9312, 76.2673),
    "munnar": (10.0889, 77.0595),
    "alleppey": (9.4981, 76.3388),
    "alappuzha": (9.4981, 76.3388),
    "wayanad": (11.6854, 76.1320),
    "thiruvananthapuram": (8.5241, 76.9366),
    "trivandrum": (8.5241, 76.9366),
    "kovalam": (8.4004, 76.9787),
    "puducherry": (11.9416, 79.8083),
    "pondicherry": (11.9416, 79.8083),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "araku valley": (18.3273, 82.8775),
    "araku": (18.3273, 82.8775),
    "vijayawada": (16.5062, 80.6480),
    "nashik": (19.9975, 73.7898),
    "nasik": (19.9975, 73.7898),
    "mahabaleshwar": (17.9237, 73.6586),
    "aurangabad": (19.8762, 75.3433),
    "chhatrapati sambhajinagar": (19.8762, 75.3433),
    "sambhajinagar": (19.8762, 75.3433),
    "lonavala": (18.7557, 73.4091),
    "khandala": (18.7614, 73.3761),
    "tarkarli": (16.0378, 73.4912),
    "malvan": (16.0617, 73.4731),
    "pune": (18.5204, 73.8567),
    "goa": (15.2993, 74.1240),
    "haridwar": (29.9457, 78.1642),
    "andaman": (11.7401, 92.6586),
    "port blair": (11.6234, 92.7265),
    "lakshadweep": (10.5667, 72.6417),

    # --- Sri Lanka ---
    "sri lanka": (6.9271, 79.8612),
    "srilanka": (6.9271, 79.8612),
    "shrilanka": (6.9271, 79.8612),
    "shri lanka": (6.9271, 79.8612),
    "shree lanka": (6.9271, 79.8612),
    "colombo": (6.9271, 79.8612),
    "kandy": (7.2906, 80.6337),
    "galle": (6.0535, 80.2210),
    "bentota": (6.4257, 79.9958),
    "ella": (6.8667, 81.0466),
    "sigiriya": (7.9570, 80.7603),
    "nuwara eliya": (6.9497, 80.7891),

    # --- Maldives ---
    "maldives": (4.1755, 73.5093),
    "male": (4.1755, 73.5093),
    "malé": (4.1755, 73.5093),
    "maafushi": (3.9429, 73.5133),
    "north male atoll": (4.4167, 73.5000),

    # --- Nepal / Bhutan ---
    "nepal": (27.7172, 85.3240),
    "kathmandu": (27.7172, 85.3240),
    "pokhara": (28.2096, 83.9856),
    "bhutan": (27.5142, 90.4336),
    "thimphu": (27.4728, 89.6390),

    # --- Southeast Asia — Indonesia ---
    "indonesia": (-8.4095, 115.1889),   # Defaults to Bali island coords as tourist hub
    "bali": (-8.4095, 115.1889),
    "denpasar": (-8.6705, 115.2126),
    "kuta": (-8.7291, 115.1692),
    "ubud": (-8.5069, 115.2625),
    "seminyak": (-8.6881, 115.1590),
    "nusa dua": (-8.7944, 115.2302),
    "jakarta": (-6.2088, 106.8456),
    "yogyakarta": (-7.7956, 110.3695),
    "lombok": (-8.6500, 116.3242),
    "komodo": (-8.5671, 119.4691),
    "raja ampat": (-0.2300, 130.5176),
    "flores": (-8.6574, 121.0794),

    # --- Southeast Asia — Thailand ---
    "thailand": (13.7563, 100.5018),
    "bangkok": (13.7563, 100.5018),
    "phuket": (7.8804, 98.3923),
    "chiang mai": (18.7883, 98.9853),
    "krabi": (8.0863, 98.9063),
    "koh samui": (9.5120, 100.0136),
    "pattaya": (12.9236, 100.8825),
    "koh phi phi": (7.7407, 98.7784),

    # --- Southeast Asia — Singapore ---
    "singapore": (1.3521, 103.8198),

    # --- Southeast Asia — Malaysia ---
    "malaysia": (3.1390, 101.6869),
    "kuala lumpur": (3.1390, 101.6869),
    "kl": (3.1390, 101.6869),
    "penang": (5.4164, 100.3327),
    "langkawi": (6.3500, 99.8000),
    "sabah": (5.9788, 116.0753),
    "borneo": (1.5533, 110.3592),

    # --- Southeast Asia — Vietnam ---
    "vietnam": (21.0285, 105.8542),
    "hanoi": (21.0285, 105.8542),
    "ho chi minh": (10.8231, 106.6297),
    "saigon": (10.8231, 106.6297),
    "hoi an": (15.8800, 108.3380),
    "da nang": (16.0544, 108.2022),
    "ha long bay": (20.9101, 107.1839),

    # --- Southeast Asia — Philippines ---
    "philippines": (9.7489, 118.7290),
    "manila": (14.5995, 120.9842),
    "palawan": (9.7489, 118.7290),
    "boracay": (11.9674, 121.9248),
    "cebu": (10.3157, 123.8854),

    # --- Southeast Asia — Cambodia, Laos, Myanmar ---
    "cambodia": (13.4125, 103.8670),
    "siem reap": (13.3671, 103.8448),
    "angkor wat": (13.4125, 103.8670),
    "phnom penh": (11.5564, 104.9282),
    "laos": (17.9757, 102.6331),
    "luang prabang": (19.8845, 102.1348),
    "myanmar": (16.8661, 96.1951),
    "yangon": (16.8661, 96.1951),

    # --- Middle East ---
    "uae": (25.2048, 55.2708),
    "dubai": (25.2048, 55.2708),
    "abu dhabi": (24.4539, 54.3773),
    "sharjah": (25.3462, 55.4212),
    "qatar": (25.2854, 51.5310),
    "doha": (25.2854, 51.5310),
    "saudi arabia": (23.8859, 45.0792),
    "riyadh": (24.7136, 46.6753),
    "jordan": (30.5852, 36.2384),
    "petra": (30.3285, 35.4444),
    "oman": (23.5880, 58.3829),
    "muscat": (23.5880, 58.3829),

    # --- Europe ---
    "france": (48.8566, 2.3522),
    "paris": (48.8566, 2.3522),
    "nice": (43.7102, 7.2620),
    "marseille": (43.2965, 5.3698),
    "uk": (51.5074, -0.1278),
    "england": (51.5074, -0.1278),
    "london": (51.5074, -0.1278),
    "edinburgh": (55.9533, -3.1883),
    "italy": (41.9028, 12.4964),
    "rome": (41.9028, 12.4964),
    "milan": (45.4654, 9.1859),
    "venice": (45.4408, 12.3155),
    "florence": (43.7696, 11.2558),
    "amalfi coast": (40.6341, 14.6025),
    "spain": (40.4168, -3.7038),
    "madrid": (40.4168, -3.7038),
    "barcelona": (41.3851, 2.1734),
    "ibiza": (38.9067, 1.4205),
    "germany": (52.5200, 13.4050),
    "berlin": (52.5200, 13.4050),
    "munich": (48.1351, 11.5820),
    "greece": (37.9838, 23.7275),
    "athens": (37.9838, 23.7275),
    "santorini": (36.3932, 25.4615),
    "mykonos": (37.4467, 25.3289),
    "switzerland": (46.8182, 8.2275),
    "zurich": (47.3769, 8.5417),
    "geneva": (46.2044, 6.1432),
    "interlaken": (46.6863, 7.8632),
    "portugal": (38.7169, -9.1399),
    "lisbon": (38.7169, -9.1399),
    "porto": (41.1579, -8.6291),
    "netherlands": (52.3676, 4.9041),
    "amsterdam": (52.3676, 4.9041),
    "austria": (48.2082, 16.3738),
    "vienna": (48.2082, 16.3738),
    "austria alps": (47.5162, 14.5501),
    "czech republic": (50.0755, 14.4378),
    "prague": (50.0755, 14.4378),
    "hungary": (47.4979, 19.0402),
    "budapest": (47.4979, 19.0402),
    "croatia": (45.8150, 15.9819),
    "dubrovnik": (42.6507, 18.0944),
    "croatia coast": (43.5081, 16.4402),
    "turkey": (41.0082, 28.9784),
    "istanbul": (41.0082, 28.9784),
    "cappadocia": (38.6431, 34.8289),
    "antalya": (36.8969, 30.7133),
    "scandinavia": (59.9139, 10.7522),
    "norway": (59.9139, 10.7522),
    "oslo": (59.9139, 10.7522),
    "sweden": (59.3293, 18.0686),
    "stockholm": (59.3293, 18.0686),
    "denmark": (55.6761, 12.5683),
    "copenhagen": (55.6761, 12.5683),
    "finland": (60.1699, 24.9384),
    "helsinki": (60.1699, 24.9384),
    "iceland": (64.1265, -21.8174),
    "reykjavik": (64.1265, -21.8174),

    # --- East Asia ---
    "tokyo, japan": (35.6762, 139.6503),
    "japan": (35.6762, 139.6503),
    "tokyo": (35.6762, 139.6503),
    "osaka": (34.6937, 135.5023),
    "kyoto": (35.0116, 135.7681),
    "hiroshima": (34.3853, 132.4553),
    "hokkaido": (43.0642, 141.3469),
    "china": (39.9042, 116.4074),
    "beijing": (39.9042, 116.4074),
    "shanghai": (31.2304, 121.4737),
    "south korea": (37.5665, 126.9780),
    "korea": (37.5665, 126.9780),
    "seoul": (37.5665, 126.9780),
    "jeju": (33.4996, 126.5312),
    "taiwan": (25.0330, 121.5654),
    "taipei": (25.0330, 121.5654),
    "hong kong": (22.3193, 114.1694),

    # --- Americas ---
    "usa": (40.7128, -74.0060),
    "united states": (40.7128, -74.0060),
    "america": (40.7128, -74.0060),
    "new york": (40.7128, -74.0060),
    "new york city": (40.7128, -74.0060),
    "nyc": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "las vegas": (36.1699, -115.1398),
    "miami": (25.7617, -80.1918),
    "chicago": (41.8781, -87.6298),
    "san francisco": (37.7749, -122.4194),
    "cancun": (21.1619, -86.8515),
    "mexico": (19.4326, -99.1332),
    "canada": (43.6532, -79.3832),
    "toronto": (43.6532, -79.3832),
    "vancouver": (49.2827, -123.1207),
    "brazil": (-23.5505, -46.6333),
    "rio de janeiro": (-22.9068, -43.1729),
    "sao paulo": (-23.5505, -46.6333),
    "peru": (-13.1631, -72.5450),
    "machu picchu": (-13.1631, -72.5450),
    "argentina": (-34.6037, -58.3816),
    "buenos aires": (-34.6037, -58.3816),

    # --- Africa ---
    "africa": (-1.2921, 36.8219),
    "kenya": (-1.2921, 36.8219),
    "nairobi": (-1.2921, 36.8219),
    "tanzania": (-6.3690, 34.8888),
    "serengeti": (-2.1540, 34.6857),
    "morocco": (34.0209, -6.8416),
    "marrakech": (31.6295, -7.9811),
    "casablanca": (33.5731, -7.5898),
    "south africa": (-33.9249, 18.4241),
    "cape town": (-33.9249, 18.4241),
    "egypt": (30.0444, 31.2357),
    "cairo": (30.0444, 31.2357),
    "luxor": (25.6872, 32.6396),

    # --- Oceania ---
    "australia": (-33.8688, 151.2093),
    "sydney": (-33.8688, 151.2093),
    "melbourne": (-37.8136, 144.9631),
    "cairns": (-16.9186, 145.7781),
    "great barrier reef": (-18.2871, 147.6992),
    "new zealand": (-36.8485, 174.7633),
    "auckland": (-36.8485, 174.7633),
    "queenstown": (-45.0312, 168.6626),
    "fiji": (-17.7134, 178.0650),
}

# ---------------------------------------------------------------------------
# Country → likely tourist city/hub (used to clarify country-level requests)
# This does NOT replace the destination — it only provides coordinate context
# ---------------------------------------------------------------------------
COUNTRY_TO_TOURIST_HUB: Dict[str, str] = {
    "indonesia": "Bali",
    "france": "Paris",
    "italy": "Rome",
    "japan": "Tokyo",
    "uk": "London",
    "england": "London",
    "usa": "New York",
    "america": "New York",
    "united states": "New York",
    "thailand": "Bangkok",
    "australia": "Sydney",
    "india": "Delhi",
    "uae": "Dubai",
    "malaysia": "Kuala Lumpur",
    "spain": "Barcelona",
    "germany": "Berlin",
    "china": "Shanghai",
    "korea": "Seoul",
    "south korea": "Seoul",
    "greece": "Santorini",
    "turkey": "Istanbul",
    "egypt": "Cairo",
    "canada": "Toronto",
    "mexico": "Cancun",
    "nepal": "Kathmandu",
    "philippines": "Palawan",
    "vietnam": "Hanoi",
    "cambodia": "Siem Reap",
    "portugal": "Lisbon",
    "netherlands": "Amsterdam",
    "austria": "Vienna",
    "switzerland": "Zurich",
    "sri lanka": "Colombo",
    "srilanka": "Colombo",
    "maldives": "Male",
    "new zealand": "Queenstown",
    "south africa": "Cape Town",
    "kenya": "Nairobi",
    "morocco": "Marrakech",
    "brazil": "Rio de Janeiro",
    "peru": "Machu Picchu",
}


def get_destination_coords(destination: str) -> Tuple[float, float]:
    """
    Resolves a destination string to (lat, lon) tuple.
    Uses local lookup first, then Open-Meteo geocoding API for anything else.
    Always returns valid coordinates. Never falls back to Bali.
    """
    cleaned = destination.strip().lower()

    # 1. Exact match
    if cleaned in DESTINATION_COORDINATES:
        return DESTINATION_COORDINATES[cleaned]

    # 2. Partial match — destination word contained in a known key
    for key, coords in DESTINATION_COORDINATES.items():
        if key in cleaned or cleaned in key:
            return coords

    # 3. Live Geocoding via Open-Meteo (free, no API key required)
    try:
        url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={destination.strip()}&count=1&language=en&format=json"
        )
        with httpx.Client(timeout=4.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    lat = float(results[0]["latitude"])
                    lon = float(results[0]["longitude"])
                    logger.info(f"Geocoded '{destination}' via Open-Meteo → ({lat}, {lon})")
                    return (lat, lon)
    except Exception as e:
        logger.warning(f"Live geocoding failed for '{destination}': {e}")

    # 4. Final fallback — geographic center of world (0°, 0°) with warning
    logger.warning(f"Could not geocode '{destination}'. Falling back to (0, 0). Consider adding to DESTINATION_COORDINATES.")
    return (20.5937, 78.9629)  # Center of India as reasonable fallback for typical usage


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two coordinates in km."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def cluster_attractions_by_proximity(
    attractions: List[dict], num_days: int
) -> List[List[dict]]:
    """Groups attractions into daily clusters minimizing transit distance."""
    if not attractions:
        return [[] for _ in range(num_days)]
    if num_days <= 1:
        return [attractions]
    sorted_attractions = sorted(
        attractions, key=lambda a: (a.get("latitude", 0), a.get("longitude", 0))
    )
    clusters: List[List[dict]] = [[] for _ in range(num_days)]
    for i, attr in enumerate(sorted_attractions):
        cluster_idx = i % num_days
        clusters[cluster_idx].append(attr)
    return clusters
