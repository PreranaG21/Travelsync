import time
import logging
from typing import Dict, Any

logger = logging.getLogger("travelsync.budget_agent")

def run_budget_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 6: Budget Agent.
    CRITICAL RULE: Calculations are strictly deterministic (Python math, not LLM).
    Computes transport (Flight / Train / Bus / Personal Vehicle), hotels, activities, local transit,
    and food expenses against user budget.
    """
    start_time = time.time()
    
    budget = float(state.get("budget", 60000.0))
    travelers = int(state.get("travelers", 2))
    duration_days = int(state.get("duration_days", 5))
    transport_mode = state.get("transport_mode", "flight")

    # 1. Transport Cost (Mode-Aware)
    intercity_transport_cost = 0.0
    transport_type_label = "Flight"
    transport_assumptions = ""
    is_live_transport = False

    if transport_mode == "train":
        transport_type_label = "Train (IRCTC)"
        selected_train = state.get("selected_transport", {}) or state.get("transport_data", {}).get("recommended", {})
        intercity_transport_cost = float(selected_train.get("total_price", 0.0))
        if intercity_transport_cost == 0.0 and selected_train.get("price_per_person"):
            intercity_transport_cost = float(selected_train.get("price_per_person")) * travelers
        is_live_transport = selected_train.get("is_live_data", False)
        transport_assumptions = f"Train fare for {travelers} traveler(s) in {selected_train.get('preferred_class', '3A')} class."

    elif transport_mode == "bus":
        transport_type_label = "Intercity Bus"
        selected_bus = state.get("selected_transport", {}) or state.get("transport_data", {}).get("recommended", {})
        intercity_transport_cost = float(selected_bus.get("total_price", 0.0))
        if intercity_transport_cost == 0.0 and selected_bus.get("price_per_person"):
            intercity_transport_cost = float(selected_bus.get("price_per_person")) * travelers
        is_live_transport = selected_bus.get("is_live_data", False)
        transport_assumptions = f"Bus ticket for {travelers} traveler(s) ({selected_bus.get('bus_type', 'AC Sleeper')})."

    elif transport_mode == "personal_vehicle":
        transport_type_label = "Personal Vehicle (Fuel & Tolls)"
        veh_data = state.get("transport_data", {})
        pricing = veh_data.get("pricing", {})
        intercity_transport_cost = float(pricing.get("total_price", 0.0))
        is_live_transport = veh_data.get("is_live_route", False)
        transport_assumptions = pricing.get("assumptions_summary", f"Calculated based on 14 km/L fuel efficiency @ ₹102.50/L + highway tolls for {veh_data.get('round_trip_distance_km', 0)} km round-trip.")

    else:
        # Default Flight
        transport_type_label = "Flight"
        selected_flight = state.get("selected_flight", {}) or state.get("selected_transport", {})
        flight_cost = float(selected_flight.get("total_price", 0.0))
        if flight_cost == 0.0 and selected_flight.get("price_per_person"):
            flight_cost = float(selected_flight.get("price_per_person")) * travelers
        intercity_transport_cost = flight_cost
        is_live_transport = selected_flight.get("is_live_data", False)
        transport_assumptions = f"Airfare for {travelers} traveler(s) round-trip."
        is_live_transport = selected_flight.get("is_live_data", False)
        transport_assumptions = f"Airfare for {travelers} traveler(s) round-trip."

    # 2. Hotel Cost
    selected_hotel = state.get("selected_hotel", {})
    hotel_cost = float(selected_hotel.get("total_price", 0.0))
    if hotel_cost == 0.0 and selected_hotel.get("price_per_night"):
        nights = max(1, duration_days - 1 if duration_days > 1 else 1)
        hotel_cost = float(selected_hotel.get("price_per_night")) * nights

    # 3. Activity Cost
    activities = state.get("activities", [])
    activity_cost = 0.0
    for day in activities:
        for act in day.get("activities", []):
            activity_cost += float(act.get("cost", 0.0))
            
    # 4. Local Transit Allowance (reduced if using personal vehicle since vehicle is already with traveler)
    if transport_mode == "personal_vehicle":
        local_transit_cost = float(250.0 * duration_days) # local parking/tolls
    else:
        local_transit_cost = float(750.0 * duration_days)
    
    # 5. Food & Snacks Allowance (deterministic estimate: ₹900/person/day)
    food_cost = float(900.0 * travelers * duration_days)

    # 6. Total Calculation (No Double Counting)
    total_cost = round(intercity_transport_cost + hotel_cost + activity_cost + local_transit_cost + food_cost, 2)
    remaining_budget = round(budget - total_cost, 2)

    # 7. Status Classification
    if total_cost <= (budget * 0.95):
        status = "UNDER_BUDGET"
    elif total_cost <= (budget * 1.05):
        status = "ON_BUDGET"
    else:
        status = "OVER_BUDGET"

    budget_breakdown = {
        "transport_mode": transport_mode,
        "transport_type": transport_type_label,
        "intercity_transport_cost": intercity_transport_cost,
        "flight_cost": intercity_transport_cost if transport_mode == "flight" else 0.0,
        "train_cost": intercity_transport_cost if transport_mode == "train" else 0.0,
        "bus_cost": intercity_transport_cost if transport_mode == "bus" else 0.0,
        "vehicle_cost": intercity_transport_cost if transport_mode == "personal_vehicle" else 0.0,
        "hotel_cost": hotel_cost,
        "activity_cost": round(activity_cost, 2),
        "local_transit_cost": local_transit_cost,
        "transport_cost": local_transit_cost,  # Preserved for backward compatibility (local mobility)
        "food_cost": food_cost,
        "total_cost": total_cost,
        "budget": budget,
        "remaining_budget": remaining_budget,
        "currency": state.get("currency", "INR"),
        "status": status,
        "savings_percentage": round((remaining_budget / budget) * 100, 1) if budget > 0 else 0.0,
        "assumptions": {
            "transport": transport_assumptions,
            "hotel": f"{nights if 'nights' in locals() else duration_days - 1} nights stay for {travelers} traveler(s)",
            "food": f"₹900/day per person for {travelers} traveler(s)",
            "local_transit": f"₹{'250' if transport_mode == 'personal_vehicle' else '750'}/day local mobility"
        },
        "is_live_transport": is_live_transport
    }

    exec_time_ms = round((time.time() - start_time) * 1000, 2)

    agent_log = {
        "agent_name": "Budget Agent",
        "input_data": f"{transport_type_label}: ₹{intercity_transport_cost:,.0f}, Hotel: ₹{hotel_cost:,.0f}, Activities: ₹{activity_cost:,.0f}, Budget: ₹{budget:,.0f}",
        "output_data": f"Total Cost: ₹{total_cost:,.0f} | Budget Status: {status} (Remaining: ₹{remaining_budget:,.0f})",
        "status": "SUCCESS",
        "execution_time": exec_time_ms
    }

    return {
        "budget_breakdown": budget_breakdown,
        "total_cost": total_cost,
        "budget_status": status,
        "agent_log": agent_log
    }
