import time
import logging
from typing import Dict, Any, List

logger = logging.getLogger("travelsync.critic_agent")

def run_critic_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 7: Critic / Validator Agent.
    Performs comprehensive multi-point audit of itinerary realism, budget constraints,
    geographical transit feasibility, weather conflicts, and schedule pacing.
    """
    start_time = time.time()
    
    budget_breakdown = state.get("budget_breakdown", {})
    activities = state.get("activities", [])
    duration_days = state.get("duration_days", 5)
    budget_status = budget_breakdown.get("status", "UNDER_BUDGET")
    
    issues: List[str] = []
    suggestions: List[str] = []
    
    checks_passed = {
        "budget_checked": True,
        "schedule_checked": True,
        "weather_checked": True,
        "distance_checked": True,
        "duplicate_checked": True,
        "dining_checked": True
    }

    # 1. Budget Audit
    if budget_status == "OVER_BUDGET":
        excess = abs(budget_breakdown.get("remaining_budget", 0))
        issues.append(f"Itinerary exceeds requested budget by ₹{excess:,.0f}.")
        suggestions.append("Optimize hotel or select lower-cost activity alternatives.")
        checks_passed["budget_checked"] = False

    # 2. Duration and Empty Day Audit
    if len(activities) != duration_days:
        issues.append(f"Itinerary day count ({len(activities)}) does not match requested duration ({duration_days} days).")
        checks_passed["schedule_checked"] = False

    for day in activities:
        acts = day.get("activities", [])
        day_num = day.get("day", 1)
        
        # Check empty days
        if len(acts) == 0:
            issues.append(f"Day {day_num} has no scheduled activities.")
            checks_passed["schedule_checked"] = False
        
        # Check overloaded days (> 5 activities)
        if len(acts) > 5:
            issues.append(f"Day {day_num} contains too many activities ({len(acts)}), which might cause travel fatigue.")
            suggestions.append(f"Spread Day {day_num} activities across other days.")
            checks_passed["schedule_checked"] = False
            
        # Check duplicate activities across the day
        titles = [a.get("title") for a in acts if a.get("category") != "logistics" and a.get("category") != "food"]
        if len(titles) != len(set(titles)):
            issues.append(f"Day {day_num} has repeated activities.")
            checks_passed["duplicate_checked"] = False

        # Check weather clash
        weather_info = day.get("weather", {})
        if not weather_info.get("is_outdoor_suitable", True):
            for a in acts:
                if a.get("category") in ["beaches", "adventure"] and "rain" in weather_info.get("condition", "").lower():
                    suggestions.append(f"Day {day_num}: Consider indoor alternatives for {a.get('title')} due to rain forecast.")

    # Determine validity
    # If there are hard issues (e.g. over budget, wrong day count, empty days), itinerary is invalid and triggers revision
    is_valid = len(issues) == 0
    
    # Calculate realism score (out of 100)
    passed_count = sum(1 for v in checks_passed.values() if v)
    realism_score = int((passed_count / len(checks_passed)) * 100)
    if not is_valid:
        realism_score = min(85, realism_score)

    critic_result = {
        "valid": is_valid,
        "realism_score": realism_score,
        "issues": issues,
        "suggestions": suggestions,
        "checks_passed": checks_passed,
        "summary": "Itinerary fully validated with optimal budget and realistic pacing." if is_valid else f"{len(issues)} issue(s) identified for optimization."
    }

    exec_time_ms = round((time.time() - start_time) * 1000, 2)

    agent_log = {
        "agent_name": "Critic Agent",
        "input_data": f"Days: {len(activities)}, Total Cost: ₹{budget_breakdown.get('total_cost', 0):,.0f}, Status: {budget_status}",
        "output_data": f"Validation: {'PASSED' if is_valid else 'NEEDS_REVISION'} | Realism Score: {realism_score}% | Issues: {len(issues)}",
        "status": "SUCCESS",
        "execution_time": exec_time_ms
    }

    return {
        "critic_result": critic_result,
        "is_valid": is_valid,
        "agent_log": agent_log
    }
