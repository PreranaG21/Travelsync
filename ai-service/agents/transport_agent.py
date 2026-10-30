"""
TravelSync Multi-Mode Transport Agent
Orchestrates transport requests according to the selected mode:
- Flight: FlightProvider (Amadeus live or mock)
- Train: TrainProvider (IRCTC schedule, classes, fares)
- Bus: BusProvider (Intercity buses, operators, RedBus link)
- Personal Vehicle: VehicleProvider (OSRM real driving route, navigation, fuel/toll assumptions)

CRITICAL RULE: Non-flight modes must NEVER invoke the flight agent or generate flight records.
"""

import time
import logging
from typing import Dict, Any
from providers.flight_provider import get_flight_provider
from providers.train_provider import get_train_provider
from providers.bus_provider import get_bus_provider
from providers.vehicle_provider import get_vehicle_provider

logger = logging.getLogger("travelsync.transport_agent")


def run_transport_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes the appropriate transport provider based on transport_mode in state.
    """
    start_time = time.time()
    
    raw_mode = state.get("transport_mode", "flight")
    if not raw_mode:
        raw_mode = "flight"
    mode = raw_mode.strip().lower()

    # Normalize mode alias
    if mode in ["car", "drive", "driving", "personal_vehicle", "road_trip", "vehicle"]:
        mode = "personal_vehicle"
    elif mode in ["rail", "railway", "train"]:
        mode = "train"
    elif mode in ["bus", "coach"]:
        mode = "bus"
    else:
        mode = "flight"

    source = state.get("source", "Mumbai")
    destination = state.get("destination", "Goa")
    travelers = int(state.get("travelers", 2))
    budget = float(state.get("budget", 60000.0))
    start_date = state.get("start_date")

    result: Dict[str, Any] = {
        "transport_mode": mode,
        "transport_data": {},
        "selected_transport": {},
        "transport_options": [],
        # Backward compatibility fields for legacy flight readers
        "flight_options": [],
        "selected_flight": {},
        "flight_source": "",
        "is_mock_flight": True
    }

    if mode == "flight":
        # Mode 1: Flight
        provider = get_flight_provider()
        flight_res = provider.search_flights(
            source=source,
            destination=destination,
            travelers=travelers,
            budget=budget,
            departure_date=start_date
        )
        options = flight_res.get("options", [])
        recommended = flight_res.get("recommended_flight", {})

        result["transport_data"] = {
            "mode": "flight",
            "options": options,
            "recommended": recommended,
            "source": flight_res.get("source", "Flight Partner"),
            "is_live_data": not flight_res.get("is_mock", True),
            "is_demo": flight_res.get("is_mock", True)
        }
        result["selected_transport"] = recommended
        result["transport_options"] = options
        # Legacy compatibility
        result["flight_options"] = options
        result["selected_flight"] = recommended
        result["flight_source"] = flight_res.get("source", "")
        result["is_mock_flight"] = flight_res.get("is_mock", True)

        exec_time_ms = round((time.time() - start_time) * 1000, 2)
        agent_log = {
            "agent_name": "Flight Agent",
            "input_data": f"Route: {source} -> {destination}, Travelers: {travelers}, Budget: ₹{budget:,.0f}",
            "output_data": f"Retrieved {len(options)} flights via {flight_res.get('source')}. Recommended: {recommended.get('airline', 'Flight')} for ₹{recommended.get('total_price', 0):,.0f}",
            "status": "SUCCESS",
            "execution_time": exec_time_ms
        }

    elif mode == "train":
        # Mode 2: Train (IRCTC)
        provider = get_train_provider()
        train_res = provider.search_trains(
            source=source,
            destination=destination,
            travelers=travelers,
            budget=budget,
            departure_date=start_date
        )
        options = train_res.get("options", [])
        recommended = train_res.get("recommended_train", {})

        result["transport_data"] = {
            "mode": "train",
            "options": options,
            "recommended": recommended,
            "source": train_res.get("source", "IRCTC"),
            "official_portal": train_res.get("official_portal", "https://www.irctc.co.in/"),
            "is_live_data": train_res.get("is_live_data", False),
            "is_demo": train_res.get("is_mock", True)
        }
        result["selected_transport"] = recommended
        result["transport_options"] = options

        exec_time_ms = round((time.time() - start_time) * 1000, 2)
        agent_log = {
            "agent_name": "Train Agent",
            "input_data": f"Route: {source} -> {destination}, Travelers: {travelers}, Budget: ₹{budget:,.0f}",
            "output_data": f"Retrieved {len(options)} train options. Recommended: {recommended.get('train_name', 'Train')} ({recommended.get('train_number', '')}) in {recommended.get('preferred_class', '3A')} for ₹{recommended.get('total_price', 0):,.0f} [Verified portal: IRCTC]",
            "status": "SUCCESS",
            "execution_time": exec_time_ms
        }

    elif mode == "bus":
        # Mode 3: Bus (Intercity Buses / RedBus)
        provider = get_bus_provider()
        bus_res = provider.search_buses(
            source=source,
            destination=destination,
            travelers=travelers,
            budget=budget,
            departure_date=start_date
        )
        options = bus_res.get("options", [])
        recommended = bus_res.get("recommended_bus", {})

        result["transport_data"] = {
            "mode": "bus",
            "options": options,
            "recommended": recommended,
            "source": bus_res.get("source", "Bus Partner"),
            "booking_portal": bus_res.get("booking_portal", "https://www.redbus.in/"),
            "is_live_data": bus_res.get("is_live_data", False),
            "is_demo": bus_res.get("is_mock", True)
        }
        result["selected_transport"] = recommended
        result["transport_options"] = options

        exec_time_ms = round((time.time() - start_time) * 1000, 2)
        agent_log = {
            "agent_name": "Bus Agent",
            "input_data": f"Route: {source} -> {destination}, Travelers: {travelers}, Budget: ₹{budget:,.0f}",
            "output_data": f"Retrieved {len(options)} bus operators. Recommended: {recommended.get('operator_name', 'Bus')} ({recommended.get('bus_type', '')}) for ₹{recommended.get('total_price', 0):,.0f} [Partner: RedBus]",
            "status": "SUCCESS",
            "execution_time": exec_time_ms
        }

    else:
        # Mode 4: Personal Vehicle (OSRM Drivable Road Route)
        provider = get_vehicle_provider()
        vehicle_res = provider.generate_route(
            source=source,
            destination=destination,
            travelers=travelers,
            budget=budget,
            is_round_trip=True
        )

        result["transport_data"] = vehicle_res
        result["selected_transport"] = vehicle_res
        result["transport_options"] = [vehicle_res]

        exec_time_ms = round((time.time() - start_time) * 1000, 2)
        pricing = vehicle_res.get("pricing", {})
        routing_engine = vehicle_res.get("routing_engine", "OSRM")
        agent_log = {
            "agent_name": "Personal Vehicle Agent",
            "input_data": f"Driving Route: {source} -> {destination}, Round-trip: Yes",
            "output_data": f"Calculated {vehicle_res.get('distance_km')} km drivable route ({vehicle_res.get('duration')}) via {routing_engine}. Fuel: ₹{pricing.get('fuel_cost', 0):,.0f} + Tolls: ₹{pricing.get('toll_cost', 0):,.0f} = Total: ₹{pricing.get('total_price', 0):,.0f} ({pricing.get('assumptions_summary', '')})",
            "status": "SUCCESS",
            "execution_time": exec_time_ms
        }

    result["agent_log"] = agent_log
    return result
