import uuid
import json
import logging
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from config.settings import settings
from database.db import get_db, init_db
from database.models import Trip, Flight, Hotel, HotelRecord, Activity, Itinerary, AgentLog, Attraction, User
from database.seed_data import seed_database_if_empty
from graph.workflow import travel_planner_app
from utils.auth import hash_password, verify_password

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("travelsync.api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB and seed datasets
    logger.info("Initializing TravelSync database and seeding default data...")
    seed_database_if_empty()
    yield
    logger.info("Shutting down TravelSync AI Service.")

app = FastAPI(
    title="TravelSync AI Service",
    description="Multi-Agent AI Travel Planning Service powered by LangGraph, Gemini, Open-Meteo, Amadeus & StayingAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# Request & Response Schemas
# ----------------------------------------------------------------------

class UserRegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class PlanTripRequest(BaseModel):
    user_request: str = Field(..., example="Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food.")
    user_id: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    travelers: Optional[int] = None
    budget: Optional[float] = None
    interests: Optional[List[str]] = None
    travel_style: Optional[str] = None
    transport_mode: Optional[str] = "flight"

class PlanTripResponse(BaseModel):
    trip_id: str
    destination: str
    source: str
    duration_days: int
    travelers: int
    budget: float
    transport_mode: str = "flight"
    transport_data: Dict[str, Any] = {}
    selected_transport: Dict[str, Any] = {}
    transport_options: List[Dict[str, Any]] = []
    selected_flight: Dict[str, Any] = {}
    flight_options: List[Dict[str, Any]] = []
    selected_hotel: Dict[str, Any]
    hotel_options: List[Dict[str, Any]]
    weather: Dict[str, Any]
    activities: List[Dict[str, Any]]
    budget_breakdown: Dict[str, Any]
    critic_result: Dict[str, Any]
    revision_count: int
    agent_logs: List[Dict[str, Any]]
    is_mock_flight: bool

# ----------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------

@app.get("/")
@app.get("/health")
@app.get("/ai/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TravelSync AI Multi-Agent Service",
        "version": "1.0.0",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "amadeus_configured": bool(settings.AMADEUS_CLIENT_ID and settings.AMADEUS_CLIENT_SECRET),
        "stayingapi_configured": bool(getattr(settings, 'STAYINGAPI_KEY', '')),
        "database": settings.DATABASE_URL.split("://")[0]
    }

# ----------------------------------------------------------------------
# Auth Endpoints
# ----------------------------------------------------------------------

@app.post("/ai/auth/register")
def register_user(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """Registers a new user with secure password hashing."""
    email_clean = req.email.strip().lower()
    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    user = User(
        id=user_id,
        name=req.name.strip(),
        email=email_clean,
        password_hash=hash_password(req.password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else ""
    }

@app.post("/ai/auth/login")
def login_user(req: UserLoginRequest, db: Session = Depends(get_db)):
    """Validates user credentials."""
    email_clean = req.email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not verify_password(user.password_hash, req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else ""
    }

@app.get("/ai/auth/user/{user_id}")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Retrieves user profile information."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else ""
    }

# ----------------------------------------------------------------------
# Trip Generation Endpoint
# ----------------------------------------------------------------------

@app.post("/ai/plan-trip", response_model=PlanTripResponse)
def plan_trip(req: PlanTripRequest, db: Session = Depends(get_db)):
    """
    Main endpoint for generating travel itineraries using the LangGraph multi-agent workflow.
    """
    trip_id = f"trip_{uuid.uuid4().hex[:10]}"
    logger.info(f"Generating travel itinerary for trip {trip_id}: '{req.user_request}'")

    initial_state = {
        "trip_id": trip_id,
        "user_request": req.user_request,
        "agent_logs": [],
        "revision_count": 0
    }

    # Override user-specified explicit parameters if provided
    if req.source:
        initial_state["source"] = req.source
    if req.destination:
        initial_state["destination"] = req.destination
    if req.duration_days:
        initial_state["duration_days"] = req.duration_days
    if req.travelers:
        initial_state["travelers"] = req.travelers
    if req.budget:
        initial_state["budget"] = req.budget
    if req.interests:
        initial_state["interests"] = req.interests
    if req.travel_style:
        initial_state["travel_style"] = req.travel_style
    if req.transport_mode:
        initial_state["transport_mode"] = req.transport_mode

    try:
        # Execute LangGraph Multi-Agent Workflow
        result_state = travel_planner_app.invoke(initial_state)
    except Exception as e:
        logger.error(f"LangGraph execution failure: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"AI Agent execution failed: {str(e)}")

    final_plan = result_state.get("final_itinerary", {})
    agent_logs = result_state.get("agent_logs", [])
    budget_breakdown = result_state.get("budget_breakdown", {})
    transport_mode = result_state.get("transport_mode", "flight")
    transport_data = result_state.get("transport_data", {})
    selected_transport = result_state.get("selected_transport", {})
    transport_options = result_state.get("transport_options", [])
    selected_flight = result_state.get("selected_flight", {})
    selected_hotel = result_state.get("selected_hotel", {})
    activities = result_state.get("activities", [])

    # Store Trip and Artifacts in Database
    try:
        trip_record = Trip(
            id=trip_id,
            user_id=req.user_id,
            user_request=req.user_request,
            source=result_state.get("source", "Mumbai"),
            destination=result_state.get("destination", "Bali"),
            duration_days=result_state.get("duration_days", 5),
            travelers=result_state.get("travelers", 2),
            budget=result_state.get("budget", 60000.0),
            currency=result_state.get("currency", "INR"),
            interests=json.dumps(result_state.get("interests", [])),
            travel_style=result_state.get("travel_style", "balanced"),
            transport_mode=transport_mode,
            transport_data=json.dumps(transport_data) if transport_data else "{}"
        )
        db.add(trip_record)

        # Store Flight ONLY if transport mode is flight (never fabricate flight records for trains/buses/cars)
        if transport_mode == "flight" and selected_flight:
            flight_record = Flight(
                trip_id=trip_id,
                airline=selected_flight.get("airline", "IndiGo"),
                flight_number=selected_flight.get("flight_number", "6E-400"),
                departure_city=result_state.get("source", "Mumbai"),
                arrival_city=result_state.get("destination", "Bali"),
                departure_time=selected_flight.get("departure_time", "06:15"),
                arrival_time=selected_flight.get("arrival_time", "14:30"),
                duration=selected_flight.get("duration", "8h 15m"),
                stops=selected_flight.get("stops", 1),
                price=selected_flight.get("total_price", 0.0),
                is_recommended=True
            )
            db.add(flight_record)

        # Store Hotel Record
        if selected_hotel:
            hotel_record = HotelRecord(
                trip_id=trip_id,
                hotel_name=selected_hotel.get("hotel_name", "Selected Resort"),
                city=result_state.get("destination", "Bali"),
                rating=float(selected_hotel.get("rating", 4.5)),
                price_per_night=float(selected_hotel.get("price_per_night", 2500.0)),
                total_price=float(selected_hotel.get("total_price", 10000.0)),
                room_type=selected_hotel.get("room_type", "Standard Deluxe Room")
            )
            db.add(hotel_record)

        # Store Scheduled Activities
        for day in activities:
            day_num = day.get("day", 1)
            for act in day.get("activities", []):
                act_record = Activity(
                    trip_id=trip_id,
                    day_number=day_num,
                    activity_name=act.get("title", ""),
                    location=act.get("location", ""),
                    category=act.get("category", "sightseeing"),
                    start_time=act.get("start_time", "10:00"),
                    end_time=act.get("end_time", "12:00"),
                    estimated_cost=act.get("cost", 0.0)
                )
                db.add(act_record)

        # Store Consolidated Itinerary
        itinerary_record = Itinerary(
            trip_id=trip_id,
            final_plan=json.dumps(final_plan),
            total_cost=budget_breakdown.get("total_cost", 0.0),
            budget_status=budget_breakdown.get("status", "UNDER_BUDGET")
        )
        db.add(itinerary_record)

        # Store Agent Transparency Logs
        for log in agent_logs:
            log_record = AgentLog(
                trip_id=trip_id,
                agent_name=log.get("agent_name", "Agent"),
                input_data=log.get("input_data", ""),
                output_data=log.get("output_data", ""),
                status=log.get("status", "SUCCESS"),
                execution_time=log.get("execution_time", 0.0)
            )
            db.add(log_record)

        db.commit()
        logger.info(f"Trip {trip_id} successfully persisted in database with transport_mode='{transport_mode}'.")
    except Exception as e:
        db.rollback()
        logger.warning(f"Failed to persist trip records in DB: {e}")

    return {
        "trip_id": trip_id,
        "destination": result_state.get("destination", "Bali"),
        "source": result_state.get("source", "Mumbai"),
        "duration_days": result_state.get("duration_days", 5),
        "travelers": result_state.get("travelers", 2),
        "budget": result_state.get("budget", 60000.0),
        "transport_mode": transport_mode,
        "transport_data": transport_data,
        "selected_transport": selected_transport,
        "transport_options": transport_options,
        "selected_flight": selected_flight,
        "flight_options": result_state.get("flight_options", []),
        "selected_hotel": selected_hotel,
        "hotel_options": result_state.get("hotel_options", []),
        "weather": result_state.get("weather", {}),
        "activities": activities,
        "budget_breakdown": budget_breakdown,
        "critic_result": result_state.get("critic_result", {}),
        "revision_count": result_state.get("revision_count", 0),
        "agent_logs": agent_logs,
        "is_mock_flight": result_state.get("is_mock_flight", True)
    }

@app.get("/ai/trips")
def list_trips(limit: int = 30, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieves past generated trips, optionally filtered by user_id."""
    query = db.query(Trip)
    if user_id:
        query = query.filter(Trip.user_id == user_id)
    trips = query.order_by(Trip.created_at.desc()).limit(limit).all()
    results = []
    for t in trips:
        itin = db.query(Itinerary).filter(Itinerary.trip_id == t.id).first()
        t_data = {}
        if t.transport_data:
            try:
                t_data = json.loads(t.transport_data)
            except Exception:
                pass
        results.append({
            "id": t.id,
            "user_id": t.user_id,
            "user_request": t.user_request,
            "source": t.source,
            "destination": t.destination,
            "duration_days": t.duration_days,
            "travelers": t.travelers,
            "budget": float(t.budget),
            "currency": t.currency,
            "transport_mode": t.transport_mode or "flight",
            "transport_data": t_data,
            "total_cost": float(itin.total_cost) if itin else float(t.budget),
            "budget_status": itin.budget_status if itin else "UNDER_BUDGET",
            "created_at": t.created_at.isoformat() if t.created_at else ""
        })
    return results

@app.get("/ai/trips/{trip_id}")
def get_trip_details(trip_id: str, db: Session = Depends(get_db)):
    """Retrieves full trip details including itinerary, transport details, and agent execution logs."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    itin = db.query(Itinerary).filter(Itinerary.trip_id == trip_id).first()
    logs = db.query(AgentLog).filter(AgentLog.trip_id == trip_id).all()
    
    parsed_plan = json.loads(itin.final_plan) if itin and itin.final_plan else {}
    t_data = {}
    if trip.transport_data:
        try:
            t_data = json.loads(trip.transport_data)
        except Exception:
            pass

    return {
        "trip": {
            "id": trip.id,
            "user_id": trip.user_id,
            "user_request": trip.user_request,
            "source": trip.source,
            "destination": trip.destination,
            "duration_days": trip.duration_days,
            "travelers": trip.travelers,
            "budget": float(trip.budget),
            "transport_mode": trip.transport_mode or "flight",
            "transport_data": t_data,
            "created_at": trip.created_at.isoformat() if trip.created_at else ""
        },
        "itinerary": parsed_plan,
        "agent_logs": [
            {
                "agent_name": l.agent_name,
                "input_data": l.input_data,
                "output_data": l.output_data,
                "status": l.status,
                "execution_time": float(l.execution_time),
                "created_at": l.created_at.isoformat() if l.created_at else ""
            }
            for l in logs
        ]
    }

@app.get("/ai/destinations")
def get_destinations(
    query: Optional[str] = None,
    country: Optional[str] = None,
    region: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Searchable destinations catalogue featuring 50 Indian + 25 International destinations.
    """
    from utils.destinations_data import search_destinations, get_all_destinations
    if query or country or region or category:
        return search_destinations(query=query or "", region=region or "", category=category or "", country=country or "")
    return get_all_destinations()

@app.get("/ai/route-directions")
def get_route_directions(
    source: str = Query(..., description="Origin city / start point"),
    destination: str = Query(..., description="Destination city / end point"),
    travelers: int = Query(2, description="Number of travelers"),
    is_round_trip: bool = Query(True, description="Whether to compute round-trip distance")
):
    """
    Direct endpoint for real OSRM drivable route calculation, polyline, directions, and fuel/toll assumptions.
    """
    from providers.vehicle_provider import get_vehicle_provider
    provider = get_vehicle_provider()
    return provider.generate_route(source=source, destination=destination, travelers=travelers, is_round_trip=is_round_trip)

@app.get("/ai/hotels")
def get_hotels(city: Optional[str] = None, max_price: Optional[float] = None, db: Session = Depends(get_db)):
    """Queries hotel dataset."""
    query = db.query(Hotel)
    if city:
        query = query.filter(Hotel.city.ilike(f"%{city}%"))
    if max_price:
        query = query.filter(Hotel.price_per_night <= max_price)
    hotels = query.order_by(Hotel.rating.desc()).all()
    return [
        {
            "id": h.id,
            "hotel_name": h.hotel_name,
            "city": h.city,
            "location": h.location,
            "rating": float(h.rating),
            "price_per_night": float(h.price_per_night),
            "room_type": h.room_type,
            "amenities": h.amenities,
            "latitude": float(h.latitude),
            "longitude": float(h.longitude),
            "distance_from_center": float(h.distance_from_center or 0.0)
        }
        for h in hotels
    ]

@app.get("/ai/attractions")
def get_attractions(destination: Optional[str] = None, db: Session = Depends(get_db)):
    """Queries attractions dataset."""
    query = db.query(Attraction)
    if destination:
        query = query.filter(Attraction.destination.ilike(f"%{destination}%"))
    attrs = query.all()
    return [
        {
            "id": a.id,
            "attraction_name": a.attraction_name,
            "destination": a.destination,
            "category": a.category,
            "estimated_visit_duration": float(a.estimated_visit_duration),
            "estimated_cost": float(a.estimated_cost),
            "latitude": float(a.latitude),
            "longitude": float(a.longitude)
        }
        for a in attrs
    ]

@app.get("/ai/agent-logs/{trip_id}")
def get_agent_logs(trip_id: str, db: Session = Depends(get_db)):
    """Fetches agent transparency logs for a specific trip."""
    logs = db.query(AgentLog).filter(AgentLog.trip_id == trip_id).order_by(AgentLog.id.asc()).all()
    return [
        {
            "agent_name": l.agent_name,
            "input_data": l.input_data,
            "output_data": l.output_data,
            "status": l.status,
            "execution_time": float(l.execution_time),
            "created_at": l.created_at.isoformat() if l.created_at else ""
        }
        for l in logs
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.AI_HOST, port=settings.AI_PORT, reload=True)
