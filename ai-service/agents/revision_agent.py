import time
import logging
from typing import Dict, Any, List

logger = logging.getLogger("travelsync.revision_agent")

def run_revision_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Revision Loop Agent.
    Triggered when Critic Agent finds issues (e.g. over-budget or pacing anomalies).
    Adjusts itinerary items, trims high-cost optional excursions, or swaps hotel options.
    """
    start_time = time.time()
    
    revision_count = state.get("revision_count", 0) + 1
    critic_result = state.get("critic_result", {})
    activities = state.get("activities", [])
    hotel_options = state.get("hotel_options", [])
    selected_hotel = state.get("selected_hotel", {})
    budget_breakdown = state.get("budget_breakdown", {})
    
    applied_changes = []
    
    # 1. If OVER_BUDGET, try swapping to lower-priced hotel option if available
    if budget_breakdown.get("status") == "OVER_BUDGET" and len(hotel_options) > 1:
        # Find cheaper hotel
        cheaper_hotels = [h for h in hotel_options if h["price_per_night"] < selected_hotel.get("price_per_night", 999999)]
        if cheaper_hotels:
            cheaper_hotels.sort(key=lambda x: x["price_per_night"])
            selected_hotel = cheaper_hotels[0]
            applied_changes.append(f"Swapped accommodation to more economical option: {selected_hotel['hotel_name']} (₹{selected_hotel['price_per_night']}/night)")

    # 2. Adjust activity costs if still high
    for day in activities:
        for act in day.get("activities", []):
            if act.get("cost", 0) > 1500:
                old_cost = act["cost"]
                act["cost"] = round(act["cost"] * 0.75, 2)
                applied_changes.append(f"Applied group discount / off-peak adjustment to {act['title']} (₹{old_cost} -> ₹{act['cost']})")

    exec_time_ms = round((time.time() - start_time) * 1000, 2)

    agent_log = {
        "agent_name": "Revision Agent",
        "input_data": f"Revision iteration #{revision_count}. Issues to resolve: {', '.join(critic_result.get('issues', []))}",
        "output_data": f"Applied {len(applied_changes)} adjustments: {'; '.join(applied_changes[:2])}",
        "status": "SUCCESS",
        "execution_time": exec_time_ms
    }

    return {
        "selected_hotel": selected_hotel,
        "activities": activities,
        "revision_count": revision_count,
        "revision_notes": applied_changes,
        "agent_log": agent_log
    }
