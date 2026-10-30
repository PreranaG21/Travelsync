from typing import TypedDict, List, Dict, Any, Optional

class TravelState(TypedDict, total=False):
    # User Input & Intent
    trip_id: str
    user_request: str
    source: str
    destination: str
    start_date: str
    end_date: str
    duration_days: int
    travelers: int
    budget: float
    currency: str
    interests: List[str]
    travel_style: str
    transport_mode: str  # 'flight', 'train', 'bus', 'personal_vehicle'

    # Multi-Mode Transport Data
    transport_data: Dict[str, Any]
    selected_transport: Dict[str, Any]
    transport_options: List[Dict[str, Any]]

    # Flight Data (Preserved for backward compatibility)
    flight_options: List[Dict[str, Any]]
    selected_flight: Dict[str, Any]
    flight_source: str
    is_mock_flight: bool

    # Hotel Data
    hotel_options: List[Dict[str, Any]]
    selected_hotel: Dict[str, Any]

    # Weather Data
    weather: Dict[str, Any]

    # Activities & Attractions
    attractions: List[Dict[str, Any]]
    activities: List[Dict[str, Any]]
    total_activity_cost: float

    # Budget Calculation
    budget_breakdown: Dict[str, Any]
    total_cost: float
    budget_status: str

    # Critic & Validation
    critic_result: Dict[str, Any]
    is_valid: bool
    revision_count: int
    revision_notes: List[str]

    # Final Output
    final_itinerary: Dict[str, Any]
    warnings: List[str]

    # Multi-Agent Transparency Logs
    agent_logs: List[Dict[str, Any]]
