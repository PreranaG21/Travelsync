import pytest
from agents.critic_agent import run_critic_agent

def test_critic_agent_valid_scenario():
    state = {
        "duration_days": 2,
        "budget_breakdown": {
            "status": "UNDER_BUDGET",
            "total_cost": 45000.0,
            "remaining_budget": 15000.0
        },
        "activities": [
            {
                "day": 1,
                "activities": [
                    {"title": "Checkin", "category": "logistics", "cost": 0},
                    {"title": "Beach", "category": "beaches", "cost": 200}
                ],
                "weather": {"is_outdoor_suitable": True, "condition": "Sunny"}
            },
            {
                "day": 2,
                "activities": [
                    {"title": "Temple", "category": "culture", "cost": 400},
                    {"title": "Market", "category": "shopping", "cost": 100}
                ],
                "weather": {"is_outdoor_suitable": True, "condition": "Partly Cloudy"}
            }
        ]
    }
    res = run_critic_agent(state)
    assert res["is_valid"] is True
    assert res["critic_result"]["realism_score"] >= 80

def test_critic_agent_catches_over_budget():
    state = {
        "duration_days": 2,
        "budget_breakdown": {
            "status": "OVER_BUDGET",
            "total_cost": 75000.0,
            "remaining_budget": -15000.0
        },
        "activities": [
            {"day": 1, "activities": [{"title": "Tour"}], "weather": {}},
            {"day": 2, "activities": [{"title": "Tour 2"}], "weather": {}}
        ]
    }
    res = run_critic_agent(state)
    assert res["is_valid"] is False
    assert any("exceeds requested budget" in issue for issue in res["critic_result"]["issues"])
