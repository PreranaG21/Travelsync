import pytest
from providers.vehicle_provider import VehicleProvider
from providers.train_provider import TrainProvider, DemoTrainProvider
from providers.bus_provider import BusProvider, DemoBusProvider
from utils.destinations_data import DESTINATIONS_CATALOGUE, search_destinations
from utils.geo import get_destination_coords, haversine_distance

def test_destinations_count():
    indian = [d for d in DESTINATIONS_CATALOGUE if d["country"].lower() == "india"]
    intl = [d for d in DESTINATIONS_CATALOGUE if d["country"].lower() != "india"]
    assert len(indian) >= 50, f"Expected at least 50 Indian destinations, got {len(indian)}"
    assert len(intl) >= 25, f"Expected at least 25 International destinations, got {len(intl)}"

def test_destination_search():
    results = search_destinations(query="Goa")
    assert len(results) > 0
    assert "Goa" in [d["name"] for d in results]
    
    pune = search_destinations(query="Pune")
    assert len(pune) > 0
    
    paris = search_destinations(query="Paris")
    assert len(paris) > 0

def test_pune_to_goa_personal_vehicle_routing():
    provider = VehicleProvider()
    route = provider.generate_route(
        source="Pune",
        destination="Goa",
        travelers=2,
        budget=60000.0
    )
    
    assert route["transport_mode"] == "personal_vehicle"
    assert route["distance_km"] > 350
    assert route["duration_minutes"] > 240
    assert "fuel_cost" in route["pricing"]
    assert "toll_cost" in route["pricing"]
    assert "google_maps" in route["navigation_links"]
    assert route["is_commercial_ticket"] is False

def test_train_provider_demo_and_links():
    provider = DemoTrainProvider()
    train_data = provider.search_trains(source="Mumbai", destination="Goa", travelers=2)
    assert train_data["transport_mode"] == "train"
    assert len(train_data["options"]) > 0
    assert "https://www.irctc.co.in/" in train_data["official_booking_url"]
    assert any(w in train_data["options"][0]["source"].lower() for w in ["live", "estimated", "demo", "irctc"])

def test_bus_provider_demo_and_links():
    provider = DemoBusProvider()
    bus_data = provider.search_buses(source="Bengaluru", destination="Coorg", travelers=2)
    assert bus_data["transport_mode"] == "bus"
    assert len(bus_data["options"]) > 0
    assert "booking_link" in bus_data

