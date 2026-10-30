"""
TravelSync Personal Vehicle / Road Trip Provider
Integrates with Open Source Routing Machine (OSRM) for real drivable road routes,
turn-by-turn maneuvers, polyline coordinates, fuel/toll calculations, and external navigation links.
"""

import math
import logging
import httpx
from typing import Dict, Any, List, Optional, Tuple
from utils.geo import get_destination_coords, haversine_distance

logger = logging.getLogger("travelsync.providers.vehicle")

# Fuel and vehicle assumptions
DEFAULT_MILEAGE_KMPL = 14.0       # Average mileage for passenger cars in India
DEFAULT_FUEL_PRICE_PER_L = 102.50  # Average petrol rate (INR/L)
DEFAULT_TOLL_RATE_PER_KM = 1.80   # Estimated toll per km on National Highways/Expressways


class VehicleProvider:
    """
    Personal Vehicle Routing Provider powered by OSRM API
    with fallback Haversine road model and transparent cost estimation.
    """

    def generate_route(
        self,
        source: str,
        destination: str,
        travelers: int = 2,
        budget: float = 60000.0,
        mileage_kmpl: float = DEFAULT_MILEAGE_KMPL,
        fuel_price: float = DEFAULT_FUEL_PRICE_PER_L,
        is_round_trip: bool = True
    ) -> Dict[str, Any]:
        """
        Calculates a real drivable route between source and destination.
        """
        src_clean = source.strip() if source else "Pune"
        dest_clean = destination.strip() if destination else "Goa"

        # 1. Resolve coordinates
        lat1, lon1 = get_destination_coords(src_clean)
        lat2, lon2 = get_destination_coords(dest_clean)

        logger.info(f"Generating personal vehicle route: {src_clean} ({lat1}, {lon1}) -> {dest_clean} ({lat2}, {lon2})")

        # 2. Query OSRM Driving Router
        osrm_url = (
            f"http://router.project-osrm.org/route/v1/driving/"
            f"{lon1:.6f},{lat1:.6f};{lon2:.6f},{lat2:.6f}"
            f"?overview=full&geometries=geojson&steps=true&annotations=distance,duration"
        )

        distance_km = 0.0
        duration_mins = 0
        coordinates: List[List[float]] = []
        steps: List[Dict[str, Any]] = []
        is_live_osrm = False
        error_details = None

        try:
            with httpx.Client(timeout=8.0) as client:
                resp = client.get(osrm_url)
                if resp.status_code == 200:
                    data = resp.json()
                    routes = data.get("routes", [])
                    if routes:
                        primary_route = routes[0]
                        distance_meters = float(primary_route.get("distance", 0))
                        duration_sec = float(primary_route.get("duration", 0))

                        distance_km = round(distance_meters / 1000.0, 1)
                        duration_mins = int(duration_sec / 60)

                        # Extract GeoJSON coordinates [[lon, lat], ...] -> [[lat, lon], ...]
                        raw_coords = primary_route.get("geometry", {}).get("coordinates", [])
                        coordinates = [[pt[1], pt[0]] for pt in raw_coords]

                        # Extract maneuver steps
                        legs = primary_route.get("legs", [])
                        if legs:
                            raw_steps = legs[0].get("steps", [])
                            for st in raw_steps:
                                man = st.get("maneuver", {})
                                name = st.get("name", "").strip() or "Highway Segment"
                                dist_st = round(st.get("distance", 0) / 1000.0, 1)
                                if dist_st > 0.3 or len(steps) < 5:
                                    instruction = self._format_instruction(man.get("type"), man.get("modifier"), name)
                                    steps.append({
                                        "instruction": instruction,
                                        "road_name": name,
                                        "distance_km": dist_st,
                                        "duration_mins": max(1, int(st.get("duration", 0) / 60))
                                    })

                        is_live_osrm = True
                        logger.info(f"OSRM Route successfully fetched: {distance_km} km, {duration_mins} mins, {len(coordinates)} polyline points")
                else:
                    error_details = f"OSRM returned HTTP {resp.status_code}"
        except Exception as e:
            error_details = f"OSRM service connection error: {str(e)}"
            logger.warning(f"OSRM Routing failed for {src_clean} -> {dest_clean}: {e}. Employing intelligent road network fallback.")

        # 3. Fallback Route Calculation if OSRM is unreachable
        if not is_live_osrm or distance_km == 0:
            direct_dist = haversine_distance(lat1, lon1, lat2, lon2)
            # Apply typical road curvature factor (~1.26x in India / mountain passes)
            distance_km = max(35.0, round(direct_dist * 1.26, 1))
            # Average driving speed ~58 km/h on Indian highway network
            duration_mins = int((distance_km / 58.0) * 60)

            # Generate interpolated polyline waypoints
            num_pts = min(30, max(5, int(distance_km / 20)))
            coordinates = []
            for i in range(num_pts + 1):
                ratio = i / float(num_pts)
                # Introduce slight realistic curve
                mid_offset = math.sin(ratio * math.pi) * 0.08
                pt_lat = lat1 + (lat2 - lat1) * ratio + mid_offset
                pt_lon = lon1 + (lon2 - lon1) * ratio
                coordinates.append([round(pt_lat, 5), round(pt_lon, 5)])

            steps = [
                {"instruction": f"Depart from {src_clean} city center towards the main highway bypass", "road_name": "City Arterial", "distance_km": round(distance_km * 0.08, 1), "duration_mins": int(duration_mins * 0.1)},
                {"instruction": f"Continue along National / State Highway towards {dest_clean}", "road_name": "NH / Express Highway", "distance_km": round(distance_km * 0.76, 1), "duration_mins": int(duration_mins * 0.75)},
                {"instruction": f"Arrive at {dest_clean} destination area", "road_name": "Destination Approach", "distance_km": round(distance_km * 0.16, 1), "duration_mins": int(duration_mins * 0.15)}
            ]

        # 4. Formatted duration string
        dur_hours = duration_mins // 60
        dur_rem_mins = duration_mins % 60
        duration_formatted = f"{dur_hours}h {dur_rem_mins:02d}m" if dur_hours > 0 else f"{dur_rem_mins} mins"

        # 5. Deterministic Fuel & Toll Cost Estimation
        effective_dist_km = distance_km * (2.0 if is_round_trip else 1.0)
        fuel_liters_needed = round(effective_dist_km / mileage_kmpl, 1)
        fuel_cost = round(fuel_liters_needed * fuel_price, 2)
        toll_cost = round(effective_dist_km * DEFAULT_TOLL_RATE_PER_KM, 2)
        total_vehicle_expense = round(fuel_cost + toll_cost, 2)

        # 6. Working External Navigation Links
        google_maps_url = (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={lat1:.6f},{lon1:.6f}"
            f"&destination={lat2:.6f},{lon2:.6f}"
            f"&travelmode=driving"
        )
        osm_directions_url = (
            f"https://www.openstreetmap.org/directions?"
            f"engine=fossgis_osrm_car&route={lat1:.6f}%2C{lon1:.6f}%3B{lat2:.6f}%2C{lon2:.6f}"
        )
        waze_url = f"https://waze.com/ul?ll={lat2:.6f},{lon2:.6f}&navigate=yes"

        # Recommendations & Road Trip Pitstops
        suggested_pitstops = []
        if distance_km > 300:
            suggested_pitstops = [
                {"name": "Midway Highway Food Plaza / Fuel Station", "distance": f"{round(distance_km * 0.45, 0)} km from origin", "type": "Restroom & Meal Stop"},
                {"name": "Scenic Valley / Ghat Lookout", "distance": f"{round(distance_km * 0.75, 0)} km from origin", "type": "Viewpoint & Tea"}
            ]
        elif distance_km > 100:
            suggested_pitstops = [
                {"name": "Expressway Midway Oasis", "distance": f"{round(distance_km * 0.5, 0)} km from origin", "type": "Coffee & Fuel"}
            ]

        return {
            "transport_mode": "personal_vehicle",
            "source": src_clean,
            "destination": dest_clean,
            "distance_km": distance_km,
            "round_trip_distance_km": round(effective_dist_km, 1),
            "is_round_trip": is_round_trip,
            "duration": duration_formatted,
            "duration_minutes": duration_mins,
            "start_coords": {"latitude": lat1, "longitude": lon1},
            "destination_coords": {"latitude": lat2, "longitude": lon2},
            "route_polyline": coordinates,
            "steps": steps[:12],  # Key navigation steps
            "pitstops": suggested_pitstops,
            "is_live_route": is_live_osrm,
            "routing_engine": "OSRM (Open Source Routing Machine)" if is_live_osrm else "Haversine Curvature Road Model (Fallback)",
            "error_details": error_details,
            "can_retry": True,
            # Cost breakdown & Stated Assumptions
            "pricing": {
                "fuel_cost": fuel_cost,
                "toll_cost": toll_cost,
                "total_price": total_vehicle_expense,
                "fuel_liters": fuel_liters_needed,
                "assumed_mileage_kmpl": mileage_kmpl,
                "assumed_fuel_rate": fuel_price,
                "assumed_toll_rate_per_km": DEFAULT_TOLL_RATE_PER_KM,
                "assumptions_summary": f"Calculated based on {mileage_kmpl} km/L car mileage @ ₹{fuel_price:.2f}/L fuel + ₹{DEFAULT_TOLL_RATE_PER_KM:.2f}/km highway tolls ({'Round-trip' if is_round_trip else 'One-way'})."
            },
            # External Navigation Links
            "navigation_links": {
                "google_maps": google_maps_url,
                "openstreetmap": osm_directions_url,
                "waze": waze_url
            },
            # Commercial ticket flag (NEVER show tickets for personal vehicle)
            "is_commercial_ticket": False
        }

    def _format_instruction(self, step_type: Optional[str], modifier: Optional[str], road_name: str) -> str:
        """Helper to create human-readable navigation directions from OSRM maneuvers."""
        if not step_type:
            return f"Proceed on {road_name}"
        if step_type == "depart":
            return f"Head out on {road_name}"
        if step_type == "arrive":
            return f"Arrive at destination on {road_name}"
        if step_type in ["turn", "fork", "end of road"]:
            mod_str = modifier.replace("_", " ").title() if modifier else ""
            return f"Turn {mod_str} onto {road_name}"
        if step_type == "roundabout":
            return f"At the roundabout, take the exit onto {road_name}"
        if step_type == "merge":
            return f"Merge onto {road_name}"
        return f"Continue on {road_name}"


def get_vehicle_provider() -> VehicleProvider:
    """Factory returning configured Personal Vehicle Provider."""
    return VehicleProvider()
