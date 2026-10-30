import pytest
from database.seed_data import seed_database_if_empty
from graph.workflow import travel_planner_app

def test_full_langgraph_workflow_bali():
    # Ensure database is seeded
    seed_database_if_empty()

    initial_state = {
        "trip_id": "test_trip_101",
        "user_request": "Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food.",
        "agent_logs": [],
        "revision_count": 0
    }

    result = travel_planner_app.invoke(initial_state)

    # Assertions
    assert result["destination"] == "Bali"
    assert result["duration_days"] == 5
    assert result["travelers"] == 2
    assert result["budget"] == 60000.0
    
    # Assert flights found
    assert len(result["flight_options"]) > 0
    assert result["selected_flight"]["airline"] is not None

    # Assert hotel selected
    assert result["selected_hotel"]["hotel_name"] is not None
    assert result["selected_hotel"]["city"] == "Bali"

    # Assert weather retrieved
    assert "forecast" in result["weather"]
    assert len(result["weather"]["forecast"]) > 0

    # Assert activities scheduled
    assert len(result["activities"]) == 5

    # Assert budget calculated deterministically
    assert "budget_breakdown" in result
    assert result["budget_breakdown"]["total_cost"] > 0
    assert result["budget_breakdown"]["status"] in ["UNDER_BUDGET", "ON_BUDGET", "OVER_BUDGET"]

    # Assert multi-agent logs generated
    agent_names = [log["agent_name"] for log in result["agent_logs"]]
    assert "Intent Agent" in agent_names
    assert "Flight Agent" in agent_names
    assert "Hotel Agent" in agent_names
    assert "Weather Tool" in agent_names
    assert "Activity Planner Agent" in agent_names
    assert "Budget Agent" in agent_names
    assert "Critic Agent" in agent_names
    assert "Final Assembly Agent" in agent_names
