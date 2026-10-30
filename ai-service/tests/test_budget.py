import pytest
from agents.budget_agent import run_budget_agent

def test_budget_agent_deterministic_calculation():
    state = {
        "budget": 60000.0,
        "travelers": 2,
        "duration_days": 5,
        "selected_flight": {"total_price": 19000.0},
        "selected_hotel": {"total_price": 16800.0},
        "activities": [
            {"activities": [{"cost": 1000.0}, {"cost": 500.0}]},
            {"activities": [{"cost": 1200.0}, {"cost": 600.0}]}
        ],
        "currency": "INR"
    }
    
    res = run_budget_agent(state)
    bd = res["budget_breakdown"]
    
    # Expected:
    # Flight: 19000
    # Hotel: 16800
    # Activities: 1000+500+1200+600 = 3300
    # Transport: 750 * 5 = 3750
    # Food: 900 * 2 * 5 = 9000
    # Total = 19000 + 16800 + 3300 + 3750 + 9000 = 51850
    # Remaining = 60000 - 51850 = 8150
    assert bd["flight_cost"] == 19000.0
    assert bd["hotel_cost"] == 16800.0
    assert bd["activity_cost"] == 3300.0
    assert bd["transport_cost"] == 3750.0
    assert bd["food_cost"] == 9000.0
    assert bd["total_cost"] == 51850.0
    assert bd["remaining_budget"] == 8150.0
    assert bd["status"] == "UNDER_BUDGET"

def test_budget_agent_over_budget():
    state = {
        "budget": 20000.0,
        "travelers": 2,
        "duration_days": 5,
        "selected_flight": {"total_price": 15000.0},
        "selected_hotel": {"total_price": 12000.0},
        "activities": [],
        "currency": "INR"
    }
    res = run_budget_agent(state)
    bd = res["budget_breakdown"]
    assert bd["status"] == "OVER_BUDGET"
    assert bd["remaining_budget"] < 0
