# TravelSync — AI Travel Planner Using Multi-Agent System

> **Plan Smarter. Travel Better.**  
> An autonomous agentic travel planning platform powered by LangGraph, Google Gemini LLM, Open-Meteo REST API, Amadeus Flight API, PostgreSQL datasets, and deterministic financial calculations.

---

## 1. Problem Statement & Objectives

Traditional online travel planners rely on static rule engines or basic single-prompt LLM chatbots. These approaches suffer from:
- **Context Overloading**: Single LLM prompts fail when coordinating multiple complex domains (flights, hotels, weather, distances, financial constraints).
- **Mathematical Hallucinations**: LLMs frequently make arithmetic mistakes when summing multi-category travel budgets.
- **Unrealistic Schedules**: Chatbots often schedule attractions that are geographically far apart on the same day or clash with rain forecasts.
- **Lack of Verification**: Once an itinerary is generated, no self-correcting critique is performed to ensure feasibility.

### TravelSync Solutions:
1. **Multi-Agent Decomposition**: Separates travel planning into 7 autonomous, cooperating agents managed via LangGraph.
2. **Deterministic Financial Budgeting**: Financial math (flights, hotels, activities, local transit, food) is calculated strictly in Python, avoiding LLM arithmetic errors.
3. **Geographical Optimization**: Uses the **Haversine formula** to cluster attractions and prevent impossible daily travel leaps (>30km/day).
4. **Real-time Weather Integration**: Leverages the Open-Meteo REST API to adapt itineraries to rain probabilities.
5. **Self-Correction (Critic & Revision Loop)**: A Critic Agent audits the itinerary against 10 realism criteria and conditionally triggers an automated revision loop in LangGraph.

---

## 2. System Architecture

```mermaid
graph TD
    User["User Web Browser"] --> Frontend["React 18 + Vite + Tailwind CSS"]
    Frontend -->|REST API (Port 5000)| Gateway["Node.js / Express API Gateway"]
    Gateway -->|HTTP JSON (Port 8000)| AIService["FastAPI Multi-Agent AI Service"]
    Gateway --> Database[(PostgreSQL Database / SQLite Fallback)]
    AIService --> Database
    AIService -->|Real-time Weather| OpenMeteo["Open-Meteo API"]
    AIService -->|Flight Search & Rates| Amadeus["Amadeus Flight Service / Mock Engine"]
    AIService -->|LLM Reasoning| Gemini["Google Gemini API"]

    subgraph LangGraph Multi-Agent State Machine
        IntentAgent["1. Intent Agent"] --> FlightAgent["2. Flight Agent"]
        FlightAgent --> HotelAgent["3. Hotel Agent"]
        HotelAgent --> WeatherTool["4. Weather Tool"]
        WeatherTool --> ActivityAgent["5. Activity Planner (Haversine Clustering)"]
        ActivityAgent --> BudgetAgent["6. Budget Agent (Deterministic Math)"]
        BudgetAgent --> CriticAgent["7. Critic / Validator Agent"]
        CriticAgent -->|Valid or Max 2 Revisions| FinalNode["8. Final Assembly Agent"]
        CriticAgent -->|Invalid & Revision < 2| RevisionNode["9. Revision Node"]
        RevisionNode --> BudgetAgent
    end
```

---

## 3. The 7 Specialized Agents & Roles

| Agent / Node | Primary Responsibility | Technology / Tools |
| :--- | :--- | :--- |
| **1. Intent Agent** | Extracts structured travel parameters (`destination`, `duration`, `travelers`, `budget`, `interests`, `style`) from natural language. | Google Gemini API (`gemini-1.5-flash` / `gemini-2.0-flash`) + Pydantic |
| **2. Flight Agent** | Searches airline routes, layovers, durations, and ranks options based on budget. | Amadeus Test API / Mock Airline Fleet |
| **3. Hotel Agent** | Queries database for properties matching destination, rating, room type, and price limits. | PostgreSQL / SQLAlchemy ORM |
| **4. Weather Tool** | Retrieves 5-day temperature forecasts and rain probabilities. | Open-Meteo REST API |
| **5. Activity Planner** | Groups attractions into daily routes minimizing transit distance; adapts to rain forecasts. | Haversine Distance Formula |
| **6. Budget Agent** | Calculates exact itemized costs for flights, hotels, activities, transit, and dining against budget. | Deterministic Python Engine (Zero LLM Hallucinations) |
| **7. Critic Agent** | Audits itinerary realism (budget status, schedule packing, duplicate visits, weather clashes). | Rule-based Multi-point Validator |
| **8. Revision Loop** | Auto-corrects budget excess or overloaded days and feeds back into the budget evaluator. | LangGraph Conditional Routing |

---

## 4. Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, Axios, React Router.
- **Backend API Gateway**: Node.js, Express.js, Axios, CORS, Morgan, Dotenv.
- **AI & Agent Service**: Python 3.13+, FastAPI, LangGraph, LangChain, Google GenAI SDK (`google-genai`).
- **Database**: PostgreSQL (SQLAlchemy ORM + Psycopg2 with automatic SQLite local fallback).
- **External Services**: Open-Meteo (Free weather REST API), Amadeus Self-Service Test API.

---

## 5. Database Design

```sql
-- Core PostgreSQL Tables
1. trips        (id, user_request, source, destination, duration_days, travelers, budget, interests, travel_style, created_at)
2. flights      (id, trip_id, airline, flight_number, departure_city, arrival_city, departure_time, arrival_time, duration, stops, price, is_recommended)
3. hotels       (id, hotel_name, city, location, rating, price_per_night, room_type, amenities, latitude, longitude, distance_from_center)
4. attractions  (id, attraction_name, destination, latitude, longitude, category, estimated_visit_duration, estimated_cost)
5. activities   (id, trip_id, day_number, activity_name, location, category, start_time, end_time, estimated_cost)
6. itineraries  (id, trip_id, final_plan, total_cost, budget_status, created_at)
7. agent_logs   (id, trip_id, agent_name, input_data, output_data, status, execution_time, created_at)
```

The database comes pre-seeded with **45+ verified hotels** and **45+ attractions** across **Bali, Goa, Mumbai, Delhi, Jaipur, Bangkok, Singapore, and Dubai**.

---

## 6. Installation & Quick Start

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- PostgreSQL (Optional; defaults to local SQLite automatically if PostgreSQL server is not active)

---

### Step 1: Clone and Configure Environment

```bash
cd travelsync
cp .env.example .env
```

Edit `.env` and set your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### Step 2: Start the Python AI Service

```bash
cd ai-service
pip install -r requirements.txt
python main.py
```
> AI Service runs at: **http://127.0.0.1:8000**  
> Interactive OpenAPI Docs: **http://127.0.0.1:8000/docs**

---

### Step 3: Start the Node.js API Gateway

```bash
cd backend
npm install
npm start
```
> API Gateway runs at: **http://localhost:5000**  
> Health Check: **http://localhost:5000/api/health**

---

### Step 4: Start the React Frontend

```bash
cd frontend
npm install
npm run dev
```
> React Frontend runs at: **http://localhost:3000**

---

## 7. Running Automated Tests

TravelSync includes comprehensive unit and integration tests:

```bash
cd ai-service
pytest tests/ -v
```

Test Coverage:
- `test_intent.py`: Natural language entity extraction for various travel scenarios.
- `test_budget.py`: Deterministic financial calculations and budget compliance.
- `test_geo.py`: Haversine formula calculation and attraction clustering.
- `test_critic.py`: Schedule realism audit and constraint violation detection.
- `test_workflow.py`: End-to-end LangGraph Multi-Agent execution pipeline.

---

## 8. Flagship Demonstration Scenario

Enter the following prompt into the TravelSync Planner:

> **"Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food."**

### What Happens Behind the Scenes:
1. **Intent Agent** parses: Destination = Bali, Duration = 5 Days, Travelers = 2, Budget = ₹60,000, Interests = Beaches, Adventure, Food.
2. **Flight Agent** searches routes from Mumbai to Bali (DPS) and recommends VietJet Air (₹19,000 total).
3. **Hotel Agent** queries PostgreSQL and selects *Grandmas Plus Hotel Seminyak* / *Amnaya Resort Kuta* within budget.
4. **Weather Tool** queries Open-Meteo and confirms clear tropical conditions (~29°C).
5. **Activity Planner** uses Haversine distance to cluster Uluwatu Temple, Seminyak Beach, Ubud Monkey Forest, and Tegallalang Rice Terraces across 5 days.
6. **Budget Agent** calculates: Flights (₹19,000) + Hotel (₹7,800) + Activities (₹4,800) + Transit (₹3,750) + Food (₹9,000) = **₹44,350 Total Cost (UNDER_BUDGET, ₹15,650 saved)**.
7. **Critic Agent** audits all 6 dimensions, awards a **96/100 Realism Score**, and compiles the final dashboard.

---

## 9. Academic Viva & Interview Defense Guide

### Q1: What is an AI Agent and why use a Multi-Agent Architecture?
> **Answer**: An AI Agent is an autonomous program that uses LLM reasoning, state memory, and external tools to accomplish goals. Single-prompt systems suffer from context overloading and math hallucinations. Decomposing into specialized agents (Intent, Flight, Hotel, Activity, Budget, Critic) ensures modularity, verifiable tool execution, and deterministic financial calculations.

### Q2: Why choose LangGraph over traditional linear chains?
> **Answer**: LangGraph models stateful, cyclic graphs with conditional branching. When the Critic Agent identifies budget excess or scheduling anomalies, LangGraph routes back into a **Revision Loop** to re-balance the plan. Linear pipelines cannot perform cyclic re-planning.

### Q3: Why are budget calculations kept deterministic?
> **Answer**: Large Language Models are probabilistic and prone to arithmetic hallucinations. Financial budgeting must be exact (Flight + Hotel + Activities + Transport + Food = Total Cost) to prevent misleading users.

### Q4: How does the Haversine formula optimize the itinerary?
> **Answer**: It calculates the spherical distance between latitude/longitude points on Earth. The Activity Planner clusters geographically close attractions onto the same day, preventing impossible transit distances.

---

## 10. License & Academic Disclaimer

This project is developed for educational and academic demonstration purposes as an MCA capstone project. It is not intended for commercial flight or hotel booking.
