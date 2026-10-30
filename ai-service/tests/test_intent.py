import pytest
from agents.intent_agent import rule_based_fallback_intent

def test_intent_extraction_bali_flagship():
    prompt = "Plan a 5-day trip to Bali for 2 people under ₹60,000. I like beaches, adventure and local food."
    intent = rule_based_fallback_intent(prompt)
    
    assert intent["destination"].lower() == "bali"
    assert intent["duration_days"] == 5
    assert intent["travelers"] == 2
    assert intent["budget"] == 60000.0
    assert "beaches" in intent["interests"]
    assert "adventure" in intent["interests"]
    assert "local food" in intent["interests"]

def test_intent_extraction_goa_budget():
    prompt = "3 days Goa trip for couple under 25k budget"
    intent = rule_based_fallback_intent(prompt)
    
    assert intent["destination"].lower() == "goa"
    assert intent["duration_days"] == 3
    assert intent["travelers"] == 2
    assert intent["budget"] == 25000.0
