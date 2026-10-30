import time
import logging
from typing import Dict, Any, List
from providers.hotel_provider import get_hotel_provider

logger = logging.getLogger("travelsync.hotel_agent")

def run_hotel_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 3: Hotel Agent.
    Utilizes HotelProvider (StayingAPI / MockHotelProvider fallback) to retrieve
    verified accommodations matching destination, style, and budget constraints.
    """
    start_time = time.time()
    destination = state.get("destination", "Bali")
    duration_days = state.get("duration_days", 5)
    travelers = state.get("travelers", 2)
    budget = state.get("budget", 60000.0)
    travel_style = state.get("travel_style", "balanced")
    start_date = state.get("start_date")

    nights = max(1, duration_days - 1 if duration_days > 1 else 1)
    hotel_budget_target = budget * (0.45 if travel_style == "luxury" else (0.25 if travel_style == "budget" else 0.35))
    max_price_per_night = max(1500.0, hotel_budget_target / nights)

    provider = get_hotel_provider()
    hotel_list = provider.search_hotels(
        destination=destination,
        duration_days=duration_days,
        travelers=travelers,
        budget=budget,
        travel_style=travel_style,
        start_date=start_date
    )

    # Sort and rank options
    if travel_style == "luxury":
        hotel_list.sort(key=lambda x: (-x.get("rating", 4.0), -x.get("price_per_night", 0)))
    elif travel_style == "budget":
        hotel_list.sort(key=lambda x: (x.get("price_per_night", 0), -x.get("rating", 4.0)))
    else:
        hotel_list.sort(key=lambda x: (abs(x.get("price_per_night", 0) - (max_price_per_night * 0.7)), -x.get("rating", 4.0)))

    # Select top 3 options
    options = hotel_list[:3]
    for idx, opt in enumerate(options):
        opt["is_selected"] = (idx == 0)
        if idx == 0:
            opt["recommendation_reason"] = "Best match for your budget and travel style"
        elif idx == 1:
            opt["recommendation_reason"] = "Top-rated alternative stay"
        else:
            opt["recommendation_reason"] = "Economical accommodation option"

    selected_hotel = options[0] if options else {}
    exec_time_ms = round((time.time() - start_time) * 1000, 2)
    
    agent_log = {
        "agent_name": "Hotel Agent",
        "input_data": f"Destination: {destination}, Nights: {nights}, Budget Allocation: ~₹{hotel_budget_target:,.0f}",
        "output_data": f"Recommended: {selected_hotel.get('hotel_name')} ({selected_hotel.get('rating')}★) at ₹{selected_hotel.get('price_per_night', 0):,.0f}/night via {selected_hotel.get('source', 'Hotel Engine')} (Total: ₹{selected_hotel.get('total_price', 0):,.0f})",
        "status": "SUCCESS",
        "execution_time": exec_time_ms
    }

    return {
        "hotel_options": options,
        "selected_hotel": selected_hotel,
        "agent_log": agent_log
    }
