import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from database.db import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.id"), nullable=True, index=True)  # null = anonymous
    title = Column(String(200), nullable=True)
    user_request = Column(Text, nullable=False)
    source = Column(String(128), default="Mumbai")
    destination = Column(String(128), nullable=False)
    duration_days = Column(Integer, default=5)
    travelers = Column(Integer, default=2)
    budget = Column(Float, default=60000.0)
    currency = Column(String(8), default="INR")
    interests = Column(Text, default="[]")       # JSON serialised list
    travel_style = Column(String(32), default="balanced")
    transport_mode = Column(String(32), default="flight")  # flight, train, bus, personal_vehicle
    transport_data = Column(Text, nullable=True)           # JSON serialized transport summary
    status = Column(String(32), default="upcoming")  # upcoming, past, draft
    is_saved = Column(Boolean, default=True)
    share_token = Column(String(64), unique=True, nullable=True, index=True)
    is_public = Column(Boolean, default=False)
    start_date = Column(String(32), nullable=True)
    end_date = Column(String(32), nullable=True)
    notes = Column(Text, nullable=True)
    tags = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # relationships
    user = relationship("User", back_populates="trips")
    flights = relationship("Flight", back_populates="trip", cascade="all, delete-orphan")
    hotels = relationship("HotelRecord", back_populates="trip", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="trip", cascade="all, delete-orphan")
    itinerary = relationship("Itinerary", back_populates="trip", uselist=False, cascade="all, delete-orphan")
    agent_logs = relationship("AgentLog", back_populates="trip", cascade="all, delete-orphan")


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(64), ForeignKey("trips.id"), nullable=False, index=True)
    airline = Column(String(128))
    flight_number = Column(String(32))
    departure_city = Column(String(128))
    arrival_city = Column(String(128))
    departure_time = Column(String(16))
    arrival_time = Column(String(16))
    duration = Column(String(32))
    stops = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    is_recommended = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="flights")


class Hotel(Base):
    """
    Static hotel dataset seeded at startup (45+ hotels across 8 cities).
    Used by the Hotel Agent as primary lookup source.
    """
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    location = Column(String(300))
    rating = Column(Float, default=4.0)
    price_per_night = Column(Float, nullable=False)
    room_type = Column(String(100))
    amenities = Column(Text)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    distance_from_center = Column(Float, default=1.0)


class HotelRecord(Base):
    """Per-trip hotel selection stored when a trip is generated."""
    __tablename__ = "hotel_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(64), ForeignKey("trips.id"), nullable=False, index=True)
    hotel_name = Column(String(200))
    city = Column(String(100))
    rating = Column(Float, default=4.0)
    price_per_night = Column(Float, default=0.0)
    total_price = Column(Float, default=0.0)
    room_type = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="hotels")


class Attraction(Base):
    """
    Static attractions dataset seeded at startup (45+ attractions across 8 cities).
    Used by the Activity Planner Agent.
    """
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    attraction_name = Column(String(200), nullable=False)
    destination = Column(String(100), nullable=False, index=True)
    category = Column(String(64))
    estimated_visit_duration = Column(Float, default=2.0)  # hours
    estimated_cost = Column(Float, default=500.0)          # INR per person
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)


class Activity(Base):
    """Per-trip scheduled activity slot stored when a trip is generated."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(64), ForeignKey("trips.id"), nullable=False, index=True)
    day_number = Column(Integer, default=1)
    activity_name = Column(String(300))
    location = Column(String(300))
    category = Column(String(64))
    start_time = Column(String(10))
    end_time = Column(String(10))
    estimated_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="activities")


class Itinerary(Base):
    """Final consolidated itinerary JSON blob and budget summary per trip."""
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(64), ForeignKey("trips.id"), nullable=False, unique=True, index=True)
    final_plan = Column(Text)          # JSON serialised full itinerary
    total_cost = Column(Float, default=0.0)
    budget_status = Column(String(32), default="UNDER_BUDGET")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="itinerary")


class AgentLog(Base):
    """Execution telemetry for each agent node in the LangGraph pipeline."""
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(64), ForeignKey("trips.id"), nullable=False, index=True)
    agent_name = Column(String(100))
    input_data = Column(Text)
    output_data = Column(Text)
    status = Column(String(32), default="SUCCESS")
    execution_time = Column(Float, default=0.0)   # milliseconds
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="agent_logs")


class User(Base):
    """Application user — used by authentication system and settings."""
    __tablename__ = "users"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(320), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    profile_picture = Column(String(500), nullable=True)
    phone = Column(String(32), nullable=True)
    two_factor_enabled = Column(Boolean, default=False)
    
    # JSON-encoded preferences
    travel_preferences = Column(Text, default="{}")        # home_airport, home_city, currency, pace, vibe, focus_areas, dietary, accessibility, loyalty, custom_ai_instructions
    notification_preferences = Column(Text, default="{}")  # price_drops, itinerary_updates, flight_status, marketing_emails
    appearance_preferences = Column(Text, default="{}")    # theme, mode, accent, density, dynamic
    privacy_preferences = Column(Text, default="{}")       # ai_data_retention, export_history, share_analytics
    travel_documents = Column(Text, default="{}")          # passport/insurance/flyer numbers (vault)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # relationships
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    saved_places = relationship("SavedPlace", back_populates="user", cascade="all, delete-orphan")


class SavedPlace(Base):
    """Bookmarked places / Wishlist for hotels, restaurants, attractions."""
    __tablename__ = "saved_places"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.id"), nullable=False, index=True)
    place_type = Column(String(32), default="attraction")  # hotel, restaurant, attraction, destination
    name = Column(String(200), nullable=False)
    destination = Column(String(100), nullable=False, index=True)
    category = Column(String(64), nullable=True)
    rating = Column(Float, default=4.5)
    estimated_price = Column(Float, default=0.0)
    photo_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    list_name = Column(String(64), default="Favorites")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="saved_places")
