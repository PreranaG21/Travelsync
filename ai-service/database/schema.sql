-- TravelSync PostgreSQL Database Schema
-- Multi-Agent AI Travel Planning System

-- Enable UUID extension if on PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Trips Table
CREATE TABLE IF NOT EXISTS trips (
    id VARCHAR(64) PRIMARY KEY,
    user_request TEXT NOT NULL,
    source VARCHAR(100),
    destination VARCHAR(100) NOT NULL,
    start_date VARCHAR(20),
    end_date VARCHAR(20),
    duration_days INTEGER NOT NULL DEFAULT 3,
    travelers INTEGER NOT NULL DEFAULT 1,
    budget NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    interests TEXT, -- Stored as comma-separated or JSON string
    travel_style VARCHAR(50) DEFAULT 'balanced',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Hotels Table (Dataset for Hotel Agent)
CREATE TABLE IF NOT EXISTS hotels (
    id SERIAL PRIMARY KEY,
    hotel_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    rating NUMERIC(3, 1) NOT NULL,
    price_per_night NUMERIC(10, 2) NOT NULL,
    room_type VARCHAR(100) NOT NULL,
    amenities TEXT NOT NULL,
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    distance_from_center NUMERIC(5, 2) DEFAULT 0.0
);

-- 3. Attractions Table (Dataset for Activity Planner Agent)
CREATE TABLE IF NOT EXISTS attractions (
    id SERIAL PRIMARY KEY,
    attraction_name VARCHAR(150) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    category VARCHAR(50) NOT NULL, -- beaches, culture, adventure, food, nature, nightlife
    estimated_visit_duration NUMERIC(4, 1) NOT NULL, -- in hours
    estimated_cost NUMERIC(10, 2) NOT NULL DEFAULT 0.0
);

-- 4. Flights Table (Generated flight options for trips)
CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR(64) REFERENCES trips(id) ON DELETE CASCADE,
    airline VARCHAR(100) NOT NULL,
    flight_number VARCHAR(30) NOT NULL,
    departure_city VARCHAR(100) NOT NULL,
    arrival_city VARCHAR(100) NOT NULL,
    departure_time VARCHAR(30) NOT NULL,
    arrival_time VARCHAR(30) NOT NULL,
    duration VARCHAR(30) NOT NULL,
    stops INTEGER NOT NULL DEFAULT 0,
    price NUMERIC(10, 2) NOT NULL,
    is_recommended BOOLEAN DEFAULT FALSE
);

-- 5. Activities Table (Scheduled items in trip itinerary)
CREATE TABLE IF NOT EXISTS activities (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR(64) REFERENCES trips(id) ON DELETE CASCADE,
    day_number INTEGER NOT NULL,
    activity_name VARCHAR(150) NOT NULL,
    location VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    start_time VARCHAR(20) NOT NULL,
    end_time VARCHAR(20) NOT NULL,
    estimated_cost NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6)
);

-- 6. Itineraries Table (Final consolidated plan and budget status)
CREATE TABLE IF NOT EXISTS itineraries (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR(64) REFERENCES trips(id) ON DELETE CASCADE UNIQUE,
    final_plan JSON NOT NULL, -- Full structured itinerary JSON
    total_cost NUMERIC(12, 2) NOT NULL,
    budget_status VARCHAR(30) NOT NULL, -- UNDER_BUDGET, ON_BUDGET, OVER_BUDGET
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Agent Logs Table (Multi-agent transparency and execution metrics)
CREATE TABLE IF NOT EXISTS agent_logs (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR(64) REFERENCES trips(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    input_data TEXT,
    output_data TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'SUCCESS',
    execution_time NUMERIC(8, 2) NOT NULL, -- execution duration in ms
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices for rapid agent querying
CREATE INDEX IF NOT EXISTS idx_hotels_city ON hotels(city);
CREATE INDEX IF NOT EXISTS idx_hotels_price ON hotels(price_per_night);
CREATE INDEX IF NOT EXISTS idx_attractions_destination ON attractions(destination);
CREATE INDEX IF NOT EXISTS idx_attractions_category ON attractions(category);
CREATE INDEX IF NOT EXISTS idx_agent_logs_trip_id ON agent_logs(trip_id);
CREATE INDEX IF NOT EXISTS idx_activities_trip_id ON activities(trip_id);
