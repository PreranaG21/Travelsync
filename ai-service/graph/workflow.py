import time
import logging
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END

from graph.state import TravelState
from agents.intent_agent import run_intent_agent
from agents.transport_agent import run_transport_agent
from agents.hotel_agent import run_hotel_agent
from providers.weather_provider import get_weather_provider
from agents.activity_agent import run_activity_agent
from agents.budget_agent import run_budget_agent
from agents.critic_agent import run_critic_agent
from agents.revision_agent import run_revision_agent

logger = logging.getLogger("travelsync.workflow")

# ----------------------------------------------------------------------
# Node Definitions
# ----------------------------------------------------------------------

def intent_node(state: TravelState) -> Dict[str, Any]:
    """Node 1: Parses natural language user request into structured state."""
    start_t = time.time()
    user_req = state.get("user_request", "")
    explicit_dest = state.get("destination")
    explicit_transport = state.get("transport_mode")
    extracted = run_intent_agent(user_req, explicit_destination=explicit_dest, explicit_transport=explicit_transport)
    
    # Strictly preserve explicit parameters passed from user or frontend
    if explicit_dest and explicit_dest.strip():
        extracted["destination"] = explicit_dest.strip()
    if explicit_transport and explicit_transport.strip():
        extracted["transport_mode"] = explicit_transport.strip().lower()

    for param in ["source", "duration_days", "travelers", "budget", "interests", "travel_style", "trip_type", "transport_mode"]:
        if state.get(param) is not None:
            extracted[param] = state[param]

    exec_time = round((time.time() - start_t) * 1000, 2)
    log_entry = {
        "agent_name": "Intent Agent",
        "input_data": f"Prompt: '{user_req}'",
        "output_data": f"Extracted: Destination: {extracted['destination']}, Mode: {extracted.get('transport_mode', 'flight').upper()}, Duration: {extracted['duration_days']}d, Travelers: {extracted['travelers']}, Budget: ₹{extracted['budget']:,.0f}, Interests: {', '.join(extracted.get('interests', []))}",
        "status": "SUCCESS",
        "execution_time": exec_time
    }
    
    logs = list(state.get("agent_logs", []))
    logs.append(log_entry)
    
    return {
        **extracted,
        "agent_logs": logs
    }

def transport_node(state: TravelState) -> Dict[str, Any]:
    """Node 2: Finds and ranks transport options according to selected mode (Flight, Train, Bus, Vehicle)."""
    res = run_transport_agent(state)
    logs = list(state.get("agent_logs", []))
    if "agent_log" in res:
        logs.append(res["agent_log"])
    return {
        "transport_mode": res.get("transport_mode", "flight"),
        "transport_data": res.get("transport_data", {}),
        "selected_transport": res.get("selected_transport", {}),
        "transport_options": res.get("transport_options", []),
        # Backward compatibility for flight consumers
        "flight_options": res.get("flight_options", []),
        "selected_flight": res.get("selected_flight", {}),
        "flight_source": res.get("flight_source", ""),
        "is_mock_flight": res.get("is_mock_flight", True),
        "agent_logs": logs
    }

def flight_node(state: TravelState) -> Dict[str, Any]:
    """Alias for transport_node for backward compatibility with existing tests."""
    return transport_node(state)

def hotel_node(state: TravelState) -> Dict[str, Any]:
    """Node 3: Queries HotelProvider for optimal hotel properties."""
    res = run_hotel_agent(state)
    logs = list(state.get("agent_logs", []))
    if "agent_log" in res:
        logs.append(res["agent_log"])
    return {
        "hotel_options": res.get("hotel_options", []),
        "selected_hotel": res.get("selected_hotel", {}),
        "agent_logs": logs
    }

def weather_node(state: TravelState) -> Dict[str, Any]:
    """Node 4: Retrieves real-time weather from WeatherProvider (Open-Meteo)."""
    start_t = time.time()
    dest = state.get("destination", "Bali")
    days = state.get("duration_days", 5)
    
    weather_provider = get_weather_provider()
    weather_data = weather_provider.get_forecast(dest, days)
    
    exec_time = round((time.time() - start_t) * 1000, 2)
    log_entry = {
        "agent_name": "Weather Tool",
        "input_data": f"Query: {dest}, Forecast Days: {days}",
        "output_data": f"{weather_data.get('source')}: {weather_data.get('summary')}",
        "status": "SUCCESS",
        "execution_time": exec_time
    }
    
    logs = list(state.get("agent_logs", []))
    logs.append(log_entry)
    
    return {
        "weather": weather_data,
        "agent_logs": logs
    }

def activity_node(state: TravelState) -> Dict[str, Any]:
    """Node 5: Clusters attractions using OpenStreetMap and Haversine distance."""
    res = run_activity_agent(state)
    logs = list(state.get("agent_logs", []))
    if "agent_log" in res:
        logs.append(res["agent_log"])
    return {
        "activities": res.get("activities", []),
        "total_activity_cost": res.get("total_activity_cost", 0.0),
        "agent_logs": logs
    }

def budget_node(state: TravelState) -> Dict[str, Any]:
    """Node 6: Deterministically calculates total travel budget."""
    res = run_budget_agent(state)
    logs = list(state.get("agent_logs", []))
    if "agent_log" in res:
        logs.append(res["agent_log"])
    return {
        "budget_breakdown": res.get("budget_breakdown", {}),
        "total_cost": res.get("total_cost", 0.0),
        "budget_status": res.get("budget_status", "UNDER_BUDGET"),
        "agent_logs": logs
    }

def critic_node(state: TravelState) -> Dict[str, Any]:
    """Node 7: Audits itinerary realism, budget constraints, and conflicts."""
    res = run_critic_agent(state)
    logs = list(state.get("agent_logs", []))
    if "agent_log" in res:
        logs.append(res["agent_log"])
    return {
        "critic_result": res.get("critic_result", {}),
        "is_valid": res.get("is_valid", True),
        "agent_logs": logs
    }

def revision_node(state: TravelState) -> Dict[str, Any]:
    """Node 8: Adjusts itinerary parameters when Critic flags issues."""
    res = run_revision_agent(state)
    logs = list(state.get("agent_logs", []))
    if "agent_log" in res:
        logs.append(res["agent_log"])
    return {
        "selected_hotel": res.get("selected_hotel", state.get("selected_hotel")),
        "activities": res.get("activities", state.get("activities")),
        "revision_count": res.get("revision_count", 1),
        "revision_notes": res.get("revision_notes", []),
        "agent_logs": logs
    }

def final_itinerary_node(state: TravelState) -> Dict[str, Any]:
    """Node 9: Consolidates the complete polished travel plan."""
    start_t = time.time()
    
    trip_summary = {
        "trip_id": state.get("trip_id", ""),
        "destination": state.get("destination", "Bali"),
        "source": state.get("source", "Mumbai"),
        "duration_days": state.get("duration_days", 5),
        "travelers": state.get("travelers", 2),
        "budget": state.get("budget", 60000.0),
        "interests": state.get("interests", []),
        "travel_style": state.get("travel_style", "balanced"),
        "transport_mode": state.get("transport_mode", "flight"),
        "transport_data": state.get("transport_data", {}),
        "selected_transport": state.get("selected_transport", {}),
        "transport_options": state.get("transport_options", []),
        "selected_flight": state.get("selected_flight", {}),
        "flight_options": state.get("flight_options", []),
        "selected_hotel": state.get("selected_hotel", {}),
        "hotel_options": state.get("hotel_options", []),
        "weather": state.get("weather", {}),
        "activities": state.get("activities", []),
        "budget_breakdown": state.get("budget_breakdown", {}),
        "critic_result": state.get("critic_result", {}),
        "revision_count": state.get("revision_count", 0),
        "revision_notes": state.get("revision_notes", [])
    }
    
    exec_time = round((time.time() - start_t) * 1000, 2)
    log_entry = {
        "agent_name": "Final Assembly Agent",
        "input_data": "Consolidated state from all 7 upstream agents",
        "output_data": f"Finalized comprehensive {trip_summary['duration_days']}-day {trip_summary['destination']} itinerary. Total: ₹{trip_summary['budget_breakdown'].get('total_cost', 0):,.0f}",
        "status": "SUCCESS",
        "execution_time": exec_time
    }
    
    logs = list(state.get("agent_logs", []))
    logs.append(log_entry)
    
    return {
        "final_itinerary": trip_summary,
        "agent_logs": logs
    }

# ----------------------------------------------------------------------
# Conditional Routing Logic
# ----------------------------------------------------------------------

def should_revise(state: TravelState) -> Literal["revision_node", "final_itinerary_node"]:
    """
    Evaluates whether the itinerary must be revised or proceeded to final output.
    Maximum 2 revision loops to avoid infinite execution cycles.
    """
    is_valid = state.get("is_valid", True)
    revision_count = state.get("revision_count", 0)
    
    if not is_valid and revision_count < 2:
        logger.info(f"Critic detected issues. Triggering Revision Node (attempt {revision_count + 1}).")
        return "revision_node"
    
    return "final_itinerary_node"

# ----------------------------------------------------------------------
# Build & Compile StateGraph
# ----------------------------------------------------------------------

def create_travel_planner_graph():
    """Builds and compiles the complete LangGraph Multi-Agent Travel Planner."""
    builder = StateGraph(TravelState)

    # Register Nodes
    builder.add_node("intent_node", intent_node)
    builder.add_node("flight_node", flight_node)
    builder.add_node("hotel_node", hotel_node)
    builder.add_node("weather_node", weather_node)
    builder.add_node("activity_node", activity_node)
    builder.add_node("budget_node", budget_node)
    builder.add_node("critic_node", critic_node)
    builder.add_node("revision_node", revision_node)
    builder.add_node("final_itinerary_node", final_itinerary_node)

    # Define Linear Flow
    builder.add_edge(START, "intent_node")
    builder.add_edge("intent_node", "flight_node")
    builder.add_edge("flight_node", "hotel_node")
    builder.add_edge("hotel_node", "weather_node")
    builder.add_edge("weather_node", "activity_node")
    builder.add_edge("activity_node", "budget_node")
    builder.add_edge("budget_node", "critic_node")

    # Conditional Routing from Critic
    builder.add_conditional_edges(
        "critic_node",
        should_revise,
        {
            "revision_node": "revision_node",
            "final_itinerary_node": "final_itinerary_node"
        }
    )

    # Feedback edge from revision back into budgeting and validation
    builder.add_edge("revision_node", "budget_node")
    builder.add_edge("final_itinerary_node", END)

    return builder.compile()

# Global compiled graph instance
travel_planner_app = create_travel_planner_graph()
