import time
import logging
from typing import Dict, Any, List
from providers.attraction_provider import get_attraction_provider
from utils.geo import haversine_distance, cluster_attractions_by_proximity

logger = logging.getLogger("travelsync.activity_agent")

def run_activity_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 4: Activity Planner Agent.
    Retrieves attractions via OpenStreetMap / Overpass API and clusters them by geographical proximity
    using Haversine distance calculations and weather awareness.
    """
    start_time = time.time()
    destination = state.get("destination", "Bali")
    duration_days = state.get("duration_days", 5)
    travelers = state.get("travelers", 2)
    interests = state.get("interests", ["beaches", "adventure", "local food"])
    selected_hotel = state.get("selected_hotel", {})
    weather = state.get("weather", {})
    forecast = weather.get("forecast", [])

    hotel_lat = selected_hotel.get("latitude", -8.4095)
    hotel_lon = selected_hotel.get("longitude", 115.1889)

    provider = get_attraction_provider()
    raw_attractions = provider.search_attractions(destination, interests)

    # Calculate distance to hotel and total costs
    all_attractions = []
    for a in raw_attractions:
        dist_to_hotel = haversine_distance(hotel_lat, hotel_lon, a["latitude"], a["longitude"])
        all_attractions.append({
            **a,
            "estimated_cost_total": a.get("estimated_cost_per_person", 200.0) * travelers,
            "distance_from_hotel_km": dist_to_hotel
        })

    # Prioritize attractions matching user interests
    matched_attractions = []
    other_attractions = []
    for attr in all_attractions:
        cat = attr.get("category", "").lower()
        if any(interest.lower() in cat or cat in interest.lower() for interest in interests):
            matched_attractions.append(attr)
        else:
            other_attractions.append(attr)
            
    prioritized_attractions = matched_attractions + other_attractions
    daily_clusters = cluster_attractions_by_proximity(prioritized_attractions, duration_days)
    
    itinerary_days: List[Dict[str, Any]] = []
    total_activity_cost = 0.0

    for day_idx in range(duration_days):
        day_num = day_idx + 1
        day_weather = forecast[day_idx] if day_idx < len(forecast) else {
            "temp_max": 29.0, "condition": "Sunny", "is_outdoor_suitable": True, "rain_probability": 15
        }
        
        day_theme = "Arrival & Wandering Exploration" if day_num == 1 else (
            "Departure & Farewell Journey" if day_num == duration_days else f"Day {day_num} Highlights & Sightseeing"
        )
        
        assigned_attrs = daily_clusters[day_idx] if day_idx < len(daily_clusters) else []
        
        # Weather adaptability check
        if not day_weather.get("is_outdoor_suitable", True):
            assigned_attrs.sort(key=lambda x: 0 if x.get("category") in ["culture", "food"] else 1)

        day_activities = []
        
        # Morning Slot
        if day_num == 1:
            day_activities.append({
                "time": "10:00 - 11:30",
                "start_time": "10:00",
                "end_time": "11:30",
                "title": f"Arrival & Check-in at {selected_hotel.get('hotel_name', 'Hotel')}",
                "location": selected_hotel.get("location", destination),
                "category": "logistics",
                "cost": 0.0,
                "notes": "Settle in, unpack, and freshen up."
            })
        else:
            attr1 = assigned_attrs[0] if len(assigned_attrs) > 0 else None
            title1 = attr1["attraction_name"] if attr1 else f"{destination} Cultural Excursion"
            cost1 = attr1["estimated_cost_total"] if attr1 else 0.0
            loc1 = attr1.get("attraction_name", destination) if attr1 else destination
            cat1 = attr1.get("category", "sightseeing") if attr1 else "culture"
            total_activity_cost += cost1
            day_activities.append({
                "time": "09:30 - 12:00",
                "start_time": "09:30",
                "end_time": "12:00",
                "title": title1,
                "location": loc1,
                "category": cat1,
                "cost": cost1,
                "notes": f"Morning sightseeing. Forecast: {day_weather.get('condition')} ({day_weather.get('temp_max')}°C)."
            })

        # Lunch Slot
        lunch_cost = 550.0 * travelers
        total_activity_cost += lunch_cost
        day_activities.append({
            "time": "12:30 - 14:00",
            "start_time": "12:30",
            "end_time": "14:00",
            "title": f"Authentic Regional Lunch",
            "location": f"Local Cuisine in {destination}",
            "category": "food",
            "cost": lunch_cost,
            "notes": "Savor authentic regional culinary dishes and drinks."
        })

        # Afternoon Slot
        attr2 = assigned_attrs[1] if len(assigned_attrs) > 1 else (assigned_attrs[0] if assigned_attrs else None)
        title2 = attr2["attraction_name"] if attr2 else f"{destination} Landmark Exploration"
        cost2 = attr2["estimated_cost_total"] if attr2 else 250.0 * travelers
        loc2 = attr2.get("attraction_name", destination) if attr2 else destination
        cat2 = attr2.get("category", "adventure") if attr2 else "adventure"
        total_activity_cost += cost2
        day_activities.append({
            "time": "14:30 - 17:30",
            "start_time": "14:30",
            "end_time": "17:30",
            "title": title2,
            "location": loc2,
            "category": cat2,
            "cost": cost2,
            "notes": "Prime afternoon sightseeing session."
        })

        # Evening Slot
        dinner_attr = assigned_attrs[2] if len(assigned_attrs) > 2 else None
        title3 = dinner_attr["attraction_name"] if dinner_attr else f"Sunset Evening & Dinner in {destination}"
        cost3 = (dinner_attr["estimated_cost_total"] if dinner_attr else 700.0 * travelers)
        loc3 = dinner_attr.get("attraction_name", destination) if dinner_attr else destination
        cat3 = dinner_attr.get("category", "nightlife") if dinner_attr else "nightlife"
        total_activity_cost += cost3
        day_activities.append({
            "time": "18:30 - 21:00",
            "start_time": "18:30",
            "end_time": "21:00",
            "title": title3,
            "location": loc3,
            "category": cat3,
            "cost": cost3,
            "notes": "Evening leisure and dining."
        })

        day_total_cost = sum(act["cost"] for act in day_activities)
        
        itinerary_days.append({
            "day": day_num,
            "theme": day_theme,
            "weather": day_weather,
            "activities": day_activities,
            "day_total_cost": day_total_cost
        })

    exec_time_ms = round((time.time() - start_time) * 1000, 2)
    
    agent_log = {
        "agent_name": "Activity Planner Agent",
        "input_data": f"Destination: {destination}, Days: {duration_days}, Interests: {', '.join(interests)}",
        "output_data": f"Scheduled {len(itinerary_days)} days with {sum(len(d['activities']) for d in itinerary_days)} activities (OpenStreetMap + Haversine clustered). Total activity cost: ₹{total_activity_cost:,.0f}",
        "status": "SUCCESS",
        "execution_time": exec_time_ms
    }

    return {
        "activities": itinerary_days,
        "total_activity_cost": total_activity_cost,
        "agent_log": agent_log
    }
