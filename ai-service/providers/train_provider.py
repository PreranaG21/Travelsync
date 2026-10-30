"""
TravelSync Train Provider
Handles rail transit searches, timetables, classes, fares, and IRCTC verification links.
"""

import math
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from utils.geo import get_destination_coords, haversine_distance

logger = logging.getLogger("travelsync.providers.train")

# Famous express trains lookup for key corridors
PREMIER_TRAIN_CORRIDORS = {
    ("mumbai", "delhi"): [
        {"name": "Mumbai CSMT Rajdhani Express", "number": "22221", "dep": "16:00", "arr": "09:55", "duration": "17h 55m", "type": "Rajdhani"},
        {"name": "August Kranti Tejas Rajdhani", "number": "12953", "dep": "17:10", "arr": "10:55", "duration": "17h 45m", "type": "Tejas Rajdhani"},
        {"name": "Mumbai Central - New Delhi Vande Bharat Spl", "number": "09001", "dep": "06:00", "arr": "21:30", "duration": "15h 30m", "type": "Vande Bharat"}
    ],
    ("pune", "goa"): [
        {"name": "Pune - Madgaon Vande Bharat Express", "number": "20670", "dep": "05:45", "arr": "13:50", "duration": "8h 05m", "type": "Vande Bharat"},
        {"name": "Goa Express", "number": "12780", "dep": "16:35", "arr": "05:40", "duration": "13h 05m", "type": "Superfast Express"},
        {"name": "Poorvottar Sampark Kranti Exp", "number": "12450", "dep": "23:20", "arr": "11:45", "duration": "12h 25m", "type": "Sampark Kranti"}
    ],
    ("mumbai", "goa"): [
        {"name": "Mumbai CSMT - Madgaon Vande Bharat Express", "number": "22229", "dep": "05:25", "arr": "13:10", "duration": "7h 45m", "type": "Vande Bharat"},
        {"name": "Tejas Express (CSMT - MAO)", "number": "22119", "dep": "05:50", "arr": "14:40", "duration": "8h 50m", "type": "Tejas Express"},
        {"name": "Mandovi Express", "number": "10103", "dep": "07:10", "arr": "19:10", "duration": "12h 00m", "type": "Express"},
        {"name": "Konkan Kanya Express", "number": "20111", "dep": "23:05", "arr": "10:45", "duration": "11h 40m", "type": "Superfast"}
    ],
    ("mumbai", "pune"): [
        {"name": "Deccan Queen Superfast", "number": "12123", "dep": "17:10", "arr": "20:25", "duration": "3h 15m", "type": "Intercity Superfast"},
        {"name": "CSMT - Solapur Vande Bharat", "number": "22225", "dep": "16:05", "arr": "19:10", "duration": "3h 05m", "type": "Vande Bharat"},
        {"name": "Pragati Express", "number": "12125", "dep": "16:25", "arr": "19:50", "duration": "3h 25m", "type": "Express"}
    ],
    ("delhi", "jaipur"): [
        {"name": "New Delhi - Ajmer Vande Bharat", "number": "20978", "dep": "06:10", "arr": "10:00", "duration": "3h 50m", "type": "Vande Bharat"},
        {"name": "Ajmer Shatabdi Express", "number": "12015", "dep": "06:10", "arr": "10:40", "duration": "4h 30m", "type": "Shatabdi"},
        {"name": "Double Decker Express", "number": "12986", "dep": "17:35", "arr": "22:00", "duration": "4h 25m", "type": "AC Double Decker"}
    ],
    ("delhi", "varanasi"): [
        {"name": "New Delhi - Varanasi Vande Bharat Express", "number": "22436", "dep": "06:00", "arr": "14:00", "duration": "8h 00m", "type": "Vande Bharat"},
        {"name": "Kashi Vishwanath Express", "number": "15128", "dep": "11:35", "arr": "04:45", "duration": "17h 10m", "type": "Mail/Express"},
        {"name": "Shiv Ganga Express", "number": "12560", "dep": "20:05", "arr": "06:10", "duration": "10h 05m", "type": "Superfast"}
    ],
    ("bengaluru", "chennai"): [
        {"name": "MGR Chennai Central Vande Bharat", "number": "20608", "dep": "05:45", "arr": "10:10", "duration": "4h 25m", "type": "Vande Bharat"},
        {"name": "Chennai Shatabdi Express", "number": "12028", "dep": "06:00", "arr": "11:00", "duration": "5h 00m", "type": "Shatabdi"},
        {"name": "Brindavan Express", "number": "12640", "dep": "15:10", "arr": "21:15", "duration": "6h 05m", "type": "Intercity"}
    ],
    ("bengaluru", "mysuru"): [
        {"name": "KSR Bengaluru - Mysuru Vande Bharat", "number": "20607", "dep": "10:30", "arr": "12:15", "duration": "1h 45m", "type": "Vande Bharat"},
        {"name": "Chamundi Express", "number": "16216", "dep": "18:15", "arr": "21:05", "duration": "2h 50m", "type": "Express"},
        {"name": "Tippu Superfast Express", "number": "12614", "dep": "15:00", "arr": "17:45", "duration": "2h 45m", "type": "Superfast"}
    ],
    ("paris", "london"): [
        {"name": "Eurostar High Speed", "number": "ES-9021", "dep": "08:12", "arr": "09:30", "duration": "2h 18m", "type": "High Speed Rail"},
        {"name": "Eurostar Express", "number": "ES-9035", "dep": "13:12", "arr": "14:30", "duration": "2h 18m", "type": "High Speed Rail"}
    ],
    ("tokyo", "kyoto"): [
        {"name": "Tokaido Shinkansen Nozomi", "number": "NZ-41", "dep": "08:00", "arr": "10:15", "duration": "2h 15m", "type": "Bullet Train"},
        {"name": "Tokaido Shinkansen Hikari", "number": "HK-507", "dep": "10:33", "arr": "13:10", "duration": "2h 37m", "type": "Bullet Train"}
    ],
    ("zurich", "interlaken"): [
        {"name": "SBB Swiss Federal InterCity", "number": "IC-61", "dep": "09:02", "arr": "10:58", "duration": "1h 56m", "type": "Scenic Alpine Rail"},
        {"name": "SBB Panoramic Express", "number": "PE-812", "dep": "14:02", "arr": "15:58", "duration": "1h 56m", "type": "Scenic Panoramic"}
    ]
}


class TrainProvider(ABC):
    """Abstract Base Class for Rail Transport Providers."""

    @abstractmethod
    def search_trains(
        self,
        source: str,
        destination: str,
        travelers: int = 1,
        budget: float = 60000.0,
        departure_date: Optional[str] = None
    ) -> Dict[str, Any]:
        pass


class DemoTrainProvider(TrainProvider):
    """
    High-fidelity Train Provider.
    Calculates realistic railway routes, class fares, timings, seat availability,
    and links to the official IRCTC portal.
    """

    def search_trains(
        self,
        source: str,
        destination: str,
        travelers: int = 1,
        budget: float = 60000.0,
        departure_date: Optional[str] = None
    ) -> Dict[str, Any]:
        src_clean = source.strip().lower() if source else "mumbai"
        dest_clean = destination.strip().lower() if destination else "goa"

        # Calculate approximate distance for realistic speed/pricing
        c1 = get_destination_coords(src_clean)
        c2 = get_destination_coords(dest_clean)
        dist_km = max(80.0, haversine_distance(c1[0], c1[1], c2[0], c2[1]))

        # Look up preset corridor or generate realistic trains
        corridor_key = (src_clean, dest_clean)
        reverse_key = (dest_clean, src_clean)

        raw_options = []
        if corridor_key in PREMIER_TRAIN_CORRIDORS:
            raw_options = PREMIER_TRAIN_CORRIDORS[corridor_key]
        elif reverse_key in PREMIER_TRAIN_CORRIDORS:
            raw_options = PREMIER_TRAIN_CORRIDORS[reverse_key]
        else:
            # Generate realistic train options based on distance
            hours = max(2, int(dist_km / 65))
            mins = int((dist_km % 65) / 65 * 60)
            dur_str = f"{hours}h {mins:02d}m"

            raw_options = [
                {
                    "name": f"{source.title()} - {destination.title()} Vande Bharat Express",
                    "number": "20891",
                    "dep": "06:00",
                    "arr": f"{(6 + hours) % 24:02d}:{mins:02d}",
                    "duration": dur_str,
                    "type": "Vande Bharat Express"
                },
                {
                    "name": f"{source.title()} - {destination.title()} Superfast Express",
                    "number": "12485",
                    "dep": "14:30",
                    "arr": f"{(14 + hours + 1) % 24:02d}:{(mins + 20) % 60:02d}",
                    "duration": f"{hours + 1}h {(mins + 20) % 60:02d}m",
                    "type": "Superfast Express"
                },
                {
                    "name": f"{destination.title()} SF Mail Express",
                    "number": "12902",
                    "dep": "21:45",
                    "arr": f"{(21 + hours + 2) % 24:02d}:{(mins + 45) % 60:02d}",
                    "duration": f"{hours + 2}h {(mins + 45) % 60:02d}m",
                    "type": "Overnight Express"
                }
            ]

        # Calculate class fares (Base rates per km)
        # 3A ~ ₹1.2/km, 2A ~ ₹1.7/km, 1A/EC ~ ₹2.6/km, CC ~ ₹1.1/km, SL ~ ₹0.45/km
        is_international = any(country in destination.lower() for country in ["paris", "london", "rome", "tokyo", "kyoto", "zurich", "interlaken"])
        currency_multiplier = 4.5 if is_international else 1.0

        options = []
        availability_statuses = [
            "AVAILABLE - 48", "AVAILABLE - 22", "RAC 04", "AVAILABLE - 12", "AVAILABLE - 95"
        ]

        for idx, train in enumerate(raw_options):
            # Determine base fare
            if "Vande Bharat" in train["name"] or "Shatabdi" in train["name"] or "Tejas" in train["name"]:
                fare_pp = max(950.0, round(dist_km * 1.85 * currency_multiplier, -1))
                classes = ["CC (Chair Car)", "EC (Executive Class)"]
                coach = "CC"
            elif "Rajdhani" in train["name"] or "Bullet" in train["name"] or "Eurostar" in train["name"]:
                fare_pp = max(1800.0, round(dist_km * 2.3 * currency_multiplier, -1))
                classes = ["3A (3rd AC)", "2A (2nd AC)", "1A (1st AC)"]
                coach = "3A"
            else:
                fare_pp = max(550.0, round(dist_km * 1.2 * currency_multiplier, -1))
                classes = ["SL (Sleeper)", "3A (3rd AC)", "2A (2nd AC)"]
                coach = "3A"

            total_fare = fare_pp * travelers

            # Class upgrades available
            class_breakdown = {
                "SL": round(fare_pp * 0.45, 0),
                "3A": round(fare_pp * 1.0, 0),
                "2A": round(fare_pp * 1.45, 0),
                "1A": round(fare_pp * 2.2, 0),
                "CC": round(fare_pp * 0.9, 0),
                "EC": round(fare_pp * 1.75, 0),
            }

            options.append({
                "train_name": train["name"],
                "train_number": train["number"],
                "train_type": train["type"],
                "source_station": f"{source.title()} Junction",
                "destination_station": f"{destination.title()} Central",
                "departure_time": train["dep"],
                "arrival_time": train["arr"],
                "duration": train["duration"],
                "distance_km": round(dist_km, 1),
                "preferred_class": coach,
                "available_classes": classes,
                "class_fares": class_breakdown,
                "price_per_person": float(fare_pp),
                "total_price": float(total_fare),
                "availability_status": availability_statuses[idx % len(availability_statuses)],
                "is_live_data": False,
                "is_demo": True,
                "source": "IRCTC Partner Schedule (Estimated / Demo)",
                "official_booking_url": "https://www.irctc.co.in/",
                "recommended": idx == 0
            })

        # Rank recommended option
        options.sort(key=lambda x: (
            0 if "Vande Bharat" in x["train_name"] or "Rajdhani" in x["train_name"] or "Eurostar" in x["train_name"] else 1,
            x["total_price"]
        ))
        for idx, opt in enumerate(options):
            opt["recommended"] = (idx == 0)

        recommended = options[0] if options else {}

        return {
            "transport_mode": "train",
            "options": options,
            "recommended_train": recommended,
            "is_mock": True,
            "is_live_data": False,
            "source": "IRCTC & Rail Schedule Data (Estimated / Demo)",
            "official_portal": "https://www.irctc.co.in/",
            "official_booking_url": "https://www.irctc.co.in/"
        }


def get_train_provider() -> TrainProvider:
    """Factory returning configured train provider."""
    return DemoTrainProvider()
