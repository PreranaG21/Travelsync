import json
import re
import logging
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from config.settings import settings

logger = logging.getLogger("travelsync.intent_agent")

class ExtractedIntent(BaseModel):
    source: str = Field(default="Mumbai", description="Starting city/departure point")
    destination: str = Field(default="Bali", description="Destination city or region")
    start_date: str = Field(default="", description="Start date (YYYY-MM-DD) if specified")
    end_date: str = Field(default="", description="End date (YYYY-MM-DD) if specified")
    duration_days: int = Field(default=5, description="Number of days for the trip")
    travelers: int = Field(default=2, description="Number of people traveling")
    budget: float = Field(default=60000.0, description="Total budget amount")
    currency: str = Field(default="INR", description="Currency symbol/code")
    interests: List[str] = Field(default_factory=lambda: ["sightseeing", "food"], description="Interests and preferences")
    travel_style: str = Field(default="balanced", description="Travel style: budget, balanced, or luxury")
    transport_mode: str = Field(default="flight", description="Transport mode: flight, train, bus, personal_vehicle")

def rule_based_fallback_intent(user_prompt: str, explicit_destination: str = None, explicit_transport: str = None) -> Dict[str, Any]:
    """
    High-precision rule-based parser that handles natural-language travel requests
    even without an external LLM connection.
    Strictly preserves user-entered and requested destinations and transport modes.
    """
    text = user_prompt.lower()

    if explicit_destination and explicit_destination.strip():
        detected_dest = explicit_destination.strip()
    else:
        from utils.geo import DESTINATION_COORDINATES
        
        # Sort known destinations by length descending so longer phrases match first
        known_destinations = sorted(list(DESTINATION_COORDINATES.keys()) + ["tokyo, japan"], key=len, reverse=True)
        detected_dest = None
        
        for d in known_destinations:
            pattern = r'\b' + re.escape(d) + r'\b'
            if re.search(pattern, text):
                detected_dest = ', '.join([part.strip().title() for part in d.split(',')])
                break
        
        if not detected_dest:
            # Preposition-based extraction: "trip to <dest>", "travel to <dest>", "to <dest>"
            m = re.search(
                r'(?:trip|travel|journey|vacation|holiday|tour|visit)?\s*(?:to|in|visiting)\s+([A-Za-z\s,]+?)(?:\s+for|\s+with|\s+under|\s+from|\s+by|\s+on|\.|\?|!|$)',
                user_prompt,
                re.IGNORECASE
            )
            if m:
                cand = m.group(1).strip().rstrip(',').strip()
                stop_words = {'a', 'the', 'some', 'my', 'beach', 'beaches', 'hotel', 'resort', 'train', 'flight', 'bus', 'car', 'vehicle'}
                if cand.lower() not in stop_words and len(cand) >= 3:
                    detected_dest = ', '.join([part.strip().title() for part in cand.split(',')])

        if not detected_dest:
            detected_dest = "Bali"

    # Transport Mode Detection
    transport_mode = "flight"
    if explicit_transport and explicit_transport.strip():
        transport_mode = explicit_transport.strip().lower()
    else:
        if any(term in text for term in ["train", "rail", "railway", "irctc", "vande bharat", "rajdhani", "shatabdi"]):
            transport_mode = "train"
        elif any(term in text for term in ["bus", "sleeper bus", "volvo bus", "redbus", "intercity bus", "coach"]):
            transport_mode = "bus"
        elif any(term in text for term in ["car", "road trip", "driving", "drive", "personal vehicle", "self drive", "by vehicle", "by car"]):
            transport_mode = "personal_vehicle"
        elif any(term in text for term in ["flight", "fly", "plane", "air", "airline"]):
            transport_mode = "flight"

    # Normalize mode
    if transport_mode in ["car", "drive", "driving", "road_trip", "vehicle"]:
        transport_mode = "personal_vehicle"
    elif transport_mode in ["rail", "railway"]:
        transport_mode = "train"

    # 2. Duration (e.g. "5-day", "5 days", "3 nights")
    duration = 5
    day_match = re.search(r'(\d+)\s*(?:-|–|\s)*(?:day|days|d)', text)
    if day_match:
        duration = max(1, min(14, int(day_match.group(1))))
        
    # 3. Travelers (e.g. "2 people", "2 travelers", "couple", "solo", "family of 4")
    travelers = 2
    if "solo" in text or "1 person" in text:
        travelers = 1
    elif "couple" in text:
        travelers = 2
    else:
        trav_match = re.search(r'(\d+)\s*(?:people|persons|travelers|travellers|friends|adults)', text)
        if trav_match:
            travelers = max(1, min(10, int(trav_match.group(1))))
            
    # 4. Budget (e.g. "₹60,000", "60000", "60k", "under 50,000", "budget 80k")
    budget = 60000.0
    k_match = re.search(r'(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*k\b', text)
    if k_match:
        budget = float(k_match.group(1)) * 1000.0
    else:
        budget_match = re.search(r'(?:₹|rs\.?|inr|under|budget|around)?\s*([0-9]{1,3}(?:,[0-9]{3})+|[0-9]{4,7})', text)
        if budget_match:
            raw_val = budget_match.group(1).replace(",", "")
            budget = max(5000.0, float(raw_val))
            
    # 5. Interests
    interest_keywords = {
        "beaches": ["beach", "beaches", "coast", "ocean", "sea", "snorkeling", "surfing"],
        "adventure": ["adventure", "trek", "trekking", "watersports", "hiking", "safari"],
        "local food": ["food", "culinary", "dining", "local food", "street food", "cuisine", "cafe"],
        "culture": ["temple", "culture", "heritage", "palace", "museum", "history", "spiritual"],
        "nature": ["nature", "forest", "wildlife", "waterfall", "park", "greenery"],
        "nightlife": ["nightlife", "party", "clubs", "bars", "music"]
    }
    extracted_interests = []
    for category, kws in interest_keywords.items():
        if any(kw in text for kw in kws):
            extracted_interests.append(category)
    if not extracted_interests:
        extracted_interests = ["beaches", "adventure", "local food"]
        
    # 6. Travel Style
    travel_style = "balanced"
    if "luxury" in text or "5 star" in text or "premium" in text:
        travel_style = "luxury"
    elif "budget" in text or "cheap" in text or "hostel" in text:
        travel_style = "budget"
        
    # 7. Source
    source = "Mumbai"
    from_match = re.search(r'from\s+([a-zA-Z\s]+?)(?:\s+to|\s+for|\s+under|\s+by|\.|$)', text)
    if from_match:
        candidate_src = from_match.group(1).strip().capitalize()
        if candidate_src:
            source = candidate_src

    return {
        "source": source,
        "destination": detected_dest,
        "start_date": "",
        "end_date": "",
        "duration_days": duration,
        "travelers": travelers,
        "budget": budget,
        "currency": "INR",
        "interests": extracted_interests,
        "travel_style": travel_style,
        "transport_mode": transport_mode
    }

def run_intent_agent(user_request: str, explicit_destination: str = None, explicit_transport: str = None) -> Dict[str, Any]:
    """
    Agent 1: Extracts structured travel requirements from natural language.
    Attempts Gemini API execution first, gracefully falling back to rule-based parser.
    Ensures user-entered destination and transport choices are strictly preserved.
    """
    api_key = settings.GEMINI_API_KEY
    if api_key:
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            dest_hint = f' Destination must be: "{explicit_destination}".' if explicit_destination else ''
            trans_hint = f' Transport mode must be: "{explicit_transport}".' if explicit_transport else ''
            prompt = f"""
You are the Intent Agent of TravelSync AI.
Extract the structured travel requirements from the user's travel request.{dest_hint}{trans_hint}

User Request: "{user_request}"

Return ONLY valid JSON matching this schema:
{{
  "source": "departure city or Mumbai if not stated",
  "destination": "destination city/region e.g. Indonesia, Bali, Tokyo, Japan, etc.",
  "start_date": "YYYY-MM-DD or empty string",
  "end_date": "YYYY-MM-DD or empty string",
  "duration_days": integer between 1 and 14 (default 5 if unspecified),
  "travelers": integer number of travelers (default 2),
  "budget": numeric budget amount (default 60000.0),
  "currency": "INR",
  "interests": ["list", "of", "interests"],
  "travel_style": "budget" or "balanced" or "luxury",
  "transport_mode": "flight" or "train" or "bus" or "personal_vehicle"
}}
"""
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            parsed = json.loads(response.text)
            if explicit_destination and explicit_destination.strip():
                parsed["destination"] = explicit_destination.strip()
            if explicit_transport and explicit_transport.strip():
                parsed["transport_mode"] = explicit_transport.strip().lower()
            # Validate with Pydantic
            validated = ExtractedIntent(**parsed)
            return validated.model_dump()
        except Exception as e:
            logger.warning(f"Gemini Intent extraction encountered error: {e}. Utilizing rule-based fallback.")
            
    return rule_based_fallback_intent(user_request, explicit_destination=explicit_destination, explicit_transport=explicit_transport)
