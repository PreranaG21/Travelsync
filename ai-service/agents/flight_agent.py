import time
import logging
from typing import Dict, Any
from providers.flight_provider import get_flight_provider

logger = logging.getLogger("travelsync.flight_agent")

def run_flight_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 2: Flight Agent.
    Evaluates origin-destination routes, applies traveler multipliers,
    ranks available flight options, and selects the recommended flight within budget.
    """
    start_time = time.time()
    source = state.get("source", "Mumbai")
    destination = state.get("destination", "Bali")
    travelers = state.get("travelers", 2)
    budget = state.get("budget", 60000.0)
    start_date = state.get("start_date")

    provider = get_flight_provider()
    flight_result = provider.search_flights(
        source=source,
        destination=destination,
        travelers=travelers,
        budget=budget,
        departure_date=start_date
    )

    options = flight_result.get("options", [])
    recommended = flight_result.get("recommended_flight", {})

    exec_time_ms = round((time.time() - start_time) * 1000, 2)
    
    agent_log = {
        "agent_name": "Flight Agent",
        "input_data": f"Route: {source} -> {destination}, Travelers: {travelers}, Budget: ₹{budget:,.0f}",
        "output_data": f"Retrieved {len(options)} options via {flight_result.get('source')}. Recommended: {recommended.get('airline')} ({recommended.get('flight_number')}) for ₹{recommended.get('total_price', 0):,.0f}",
        "status": "SUCCESS",
        "execution_time": exec_time_ms
    }

    return {
        "flight_options": options,
        "selected_flight": recommended,
        "flight_source": flight_result.get("source"),
        "is_mock_flight": flight_result.get("is_mock", True),
        "agent_log": agent_log
    }
