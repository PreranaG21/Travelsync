import pytest
from utils.geo import haversine_distance, get_destination_coords, cluster_attractions_by_proximity

def test_haversine_distance_known_points():
    # Distance between Gateway of India (18.9220, 72.8347) and CSMT Mumbai (18.9400, 72.8354)
    # Approx 2.0 km
    dist = haversine_distance(18.9220, 72.8347, 18.9400, 72.8354)
    assert 1.5 < dist < 2.5

def test_haversine_same_point():
    dist = haversine_distance(10.0, 20.0, 10.0, 20.0)
    assert dist == 0.0

def test_destination_coords():
    lat, lon = get_destination_coords("Bali")
    assert -9.0 < lat < -8.0
    assert 114.5 < lon < 116.0

def test_cluster_attractions():
    attractions = [
        {"name": "A", "latitude": -8.5, "longitude": 115.2},
        {"name": "B", "latitude": -8.7, "longitude": 115.1},
        {"name": "C", "latitude": -8.8, "longitude": 115.0},
        {"name": "D", "latitude": -8.6, "longitude": 115.3},
    ]
    clusters = cluster_attractions_by_proximity(attractions, 2)
    assert len(clusters) == 2
    assert sum(len(c) for c in clusters) == 4
