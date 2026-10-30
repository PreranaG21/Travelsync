"""
TravelSync Bus Provider
Handles intercity bus transit searches, fleet operators, amenities, pricing, and RedBus/AbhiBus booking links.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from utils.geo import get_destination_coords, haversine_distance

logger = logging.getLogger("travelsync.providers.bus")

BUS_OPERATORS_FLEET = [
    {
        "operator": "IntrCity SmartBus",
        "bus_type": "Volvo 9600 Multi-Axle AC Sleeper (2+1)",
        "rating": 4.8,
        "amenities": ["Air Conditioning", "Personal USB Charging", "Free WiFi", "Mineral Water", "Blanket & Pillow", "Live GPS Tracking"]
    },
    {
        "operator": "Zingbus Premium",
        "bus_type": "BharatBenz AC Sleeper (2+1)",
        "rating": 4.7,
        "amenities": ["Air Conditioning", "Fast Charging", "Complimentary Snacks", "Emergency SOS", "Clean Bedding"]
    },
    {
        "operator": "VRL Travels",
        "bus_type": "Scania Multi-Axle Semi-Sleeper (2+2)",
        "rating": 4.5,
        "amenities": ["Air Conditioning", "Reclining Seats", "Reading Light", "Water Bottle", "Punctuality Guarantee"]
    },
    {
        "operator": "Orange Tours & Travels",
        "bus_type": "Volvo B11R AC Sleeper",
        "rating": 4.6,
        "amenities": ["Air Conditioning", "Charging Point", "WiFi", "Luggage Tagging", "CCTV Surveillance"]
    }
]


class BusProvider(ABC):
    """Abstract Base Class for Bus Providers."""

    @abstractmethod
    def search_buses(
        self,
        source: str,
        destination: str,
        travelers: int = 1,
        budget: float = 60000.0,
        departure_date: Optional[str] = None
    ) -> Dict[str, Any]:
        pass


class DemoBusProvider(BusProvider):
    """
    High-fidelity Bus Transport Provider.
    Calculates realistic bus departure schedules, boarding points, fares, and booking links.
    """

    def search_buses(
        self,
        source: str,
        destination: str,
        travelers: int = 1,
        budget: float = 60000.0,
        departure_date: Optional[str] = None
    ) -> Dict[str, Any]:
        src_clean = source.strip().lower() if source else "mumbai"
        dest_clean = destination.strip().lower() if destination else "goa"

        # Calculate approximate road distance (haversine * 1.25 road curvature factor)
        c1 = get_destination_coords(src_clean)
        c2 = get_destination_coords(dest_clean)
        direct_dist = haversine_distance(c1[0], c1[1], c2[0], c2[1])
        road_km = max(60.0, round(direct_dist * 1.22, 1))

        # Average bus speed ~55 km/h including rest stops
        hours = max(2, int(road_km / 52))
        mins = int((road_km % 52) / 52 * 60)
        dur_str = f"{hours}h {mins:02d}m"

        schedules = [
            {"dep": "20:30", "arr": f"{(20 + hours) % 24:02d}:{mins:02d}", "slot": "Overnight Prime"},
            {"dep": "21:45", "arr": f"{(21 + hours) % 24:02d}:{(mins + 15) % 60:02d}", "slot": "Late Night Express"},
            {"dep": "06:30", "arr": f"{(6 + hours) % 24:02d}:{mins:02d}", "slot": "Early Morning AC Express"},
            {"dep": "17:00", "arr": f"{(17 + hours) % 24:02d}:{(mins + 30) % 60:02d}", "slot": "Evening Volvo"}
        ]

        # Base bus rate: ~₹1.60 to ₹2.10 per km for AC Sleeper
        base_rate_per_km = 1.85
        if road_km > 700:
            base_rate_per_km = 1.45

        options = []
        for idx, carrier in enumerate(BUS_OPERATORS_FLEET):
            sched = schedules[idx % len(schedules)]
            fare_pp = max(450.0, round((road_km * base_rate_per_km) * (1.0 + (idx * 0.08)), -1))
            total_fare = fare_pp * travelers

            options.append({
                "operator_name": carrier["operator"],
                "bus_type": carrier["bus_type"],
                "rating": carrier["rating"],
                "departure_time": sched["dep"],
                "arrival_time": sched["arr"],
                "duration": dur_str,
                "schedule_slot": sched["slot"],
                "distance_km": road_km,
                "boarding_point": f"{source.title()} Central Intercity Terminal",
                "dropping_point": f"{destination.title()} Main Bus Stand",
                "amenities": carrier["amenities"],
                "seats_available": 18 - (idx * 3),
                "price_per_person": float(fare_pp),
                "total_price": float(total_fare),
                "is_live_data": False,
                "is_demo": True,
                "source": "Bus Partner Network (Estimated / Demo)",
                "booking_url": "https://www.redbus.in/",
                "alternative_url": "https://www.abhibus.com/",
                "recommended": idx == 0
            })

        options.sort(key=lambda x: (-x["rating"], x["total_price"]))
        for idx, opt in enumerate(options):
            opt["recommended"] = (idx == 0)

        recommended = options[0] if options else {}

        return {
            "transport_mode": "bus",
            "options": options,
            "recommended_bus": recommended,
            "is_mock": True,
            "is_live_data": False,
            "source": "Intercity Bus Aggregator Data (Estimated / Demo)",
            "booking_portal": "https://www.redbus.in/",
            "booking_url": "https://www.redbus.in/",
            "booking_link": "https://www.redbus.in/"
        }


def get_bus_provider() -> BusProvider:
    """Factory returning configured bus provider."""
    return DemoBusProvider()
