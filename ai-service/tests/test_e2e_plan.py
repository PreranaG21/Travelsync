import pytest
from database.db import init_db, SessionLocal
from database.seed_data import seed_database_if_empty
from main import plan_trip, PlanTripRequest

def test_flagship_bali_trip_generation():
    init_db()
    seed_database_if_empty()
    db = SessionLocal()

    try:
        request = PlanTripRequest(
            user_request="Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food.",
            source="Mumbai",
            user_id=None
        )

        response = plan_trip(request, db)
        assert response is not None
        assert response["destination"] == "Bali"
        assert response["duration_days"] == 5
        assert response["travelers"] == 2
        assert response["budget"] == 60000.0

        # Verify flight
        assert response["selected_flight"] is not None
        assert response["selected_flight"].get("total_price", 0) > 0

        # Verify hotel
        assert response["selected_hotel"] is not None
        assert response["selected_hotel"].get("hotel_name") is not None
        assert response["selected_hotel"].get("total_price", 0) > 0

        # Verify weather
        assert response["weather"] is not None
        assert len(response["weather"].get("forecast", [])) == 5

        # Verify activities
        assert len(response["activities"]) == 5

        # Verify budget breakdown
        assert response["budget_breakdown"] is not None
        assert response["budget_breakdown"].get("total_cost", 0) > 0
        assert response["budget_breakdown"].get("status") in ["UNDER_BUDGET", "ON_BUDGET", "OVER_BUDGET"]

        # Verify agent logs
        assert len(response["agent_logs"]) >= 7
        log_names = [l.get("agent_name") for l in response["agent_logs"]]
        assert "Intent Agent" in log_names
        assert "Flight Agent" in log_names
        assert "Hotel Agent" in log_names
        assert "Activity Planner Agent" in log_names
        assert "Budget Agent" in log_names
        assert "Critic Agent" in log_names
    finally:
        db.close()
