"""
Purpose: using data from a session, 
produce a result and a reason.

I have reused the structure and some of the code of the analysis.py file from Assignment 1. 
"""

# imports 
import statistics
from .models import MIN_SIGNAL_QUALITY

# Set attributes for the analysis. 
# The number was chosen by me to ensure that there is enough data to make a classification.
# Difference from assignment1, is i now have the set attributes here, insted of in the code. 

MIN_USABLE_TO_CLASSIFY = 3      
MIN_USABLE_FOR_RECOVERY = 4     
RECOVERY_HR_DROP = 3            
RECOVERY_ACTIVITY_DROP = 0.05   

RESTING_MAX_ACTIVITY = 0.25     
RESTING_MAX_HR_DIFF = 12        
MODERATE_MAX_ACTIVITY = 0.68    
MODERATE_MAX_HR_DIFF = 45       


def summarize_values(values): 
    clean = [v for v in values if v is not None]
    if not clean:
        return {"average": None, "min": None, "max": None, "count": 0} 
    return {
        "average": round(statistics.mean(clean), 2),
        "min": min(clean),
        "max": max(clean),
        "count": len(clean),
    }

def compare_baseline(value, baseline):
    if value is None or baseline is None:
        return None 
    return round(value - baseline, 2)

def detect_recovery(session):
    usable = sorted(session.usable_observations, key=lambda obs: obs.timestamp) # lambda sort it in order of timestamp
    if len(usable) < MIN_USABLE_FOR_RECOVERY: # at least four usable observations to compare.
        return False, (f"Not enough usable observations to evaluate recovery. "
                       f"There is ({len(usable)}), but we need at least {MIN_USABLE_FOR_RECOVERY}")
    
    middle = len(usable) // 2
    first_half, second_half = usable[:middle], usable[middle:]

    hr_first = statistics.mean([obs.heart_rate for obs in first_half])
    hr_second = statistics.mean([obs.heart_rate for obs in second_half])
    activity_first = statistics.mean([obs.activity_level for obs in first_half])
    activity_second = statistics.mean([obs.activity_level for obs in second_half])

    # filter out noise measures
    heart_rate_declining = hr_second < hr_first - RECOVERY_HR_DROP
    activity_declining = activity_second < activity_first - RECOVERY_ACTIVITY_DROP

    if heart_rate_declining and activity_declining:
        explanation = (f"Heart rate fell from {hr_first:.1f} to {hr_second:.1f} bpm "
                       f"and activity fell from {activity_first:.2f} to {activity_second:.2f} "
                       "over the second half of the session")
        return True, explanation
    return False, "no significant decline in heart rate and activity toward the end of the session"


def classify_session(session):
    usable = session.usable_observations
    if len(usable) < MIN_USABLE_TO_CLASSIFY:
        return "insufficient data", (
            f"only {len(usable)} of {session.total_count()} observations have "
            f"signal_quality >= {MIN_SIGNAL_QUALITY}; at least {MIN_USABLE_TO_CLASSIFY} are needed")

    is_recovering, recovery_reason = detect_recovery(session)
    if is_recovering:
        return "recovering", recovery_reason

    avg_hr = statistics.mean(obs.heart_rate for obs in usable)
    avg_activity = statistics.mean(obs.activity_level for obs in usable)
    
    hr_diff = avg_hr - session.participant.baseline_heart_rate
    detail = (f"mean heart rate {avg_hr:.1f} bpm is {hr_diff:+.1f} vs baseline "
              f"{session.participant.baseline_heart_rate}, mean activity {avg_activity:.2f}")

    if avg_activity < RESTING_MAX_ACTIVITY and hr_diff < RESTING_MAX_HR_DIFF:
        return "resting", detail
    if avg_activity < MODERATE_MAX_ACTIVITY and hr_diff < MODERATE_MAX_HR_DIFF:
        return "moderate activity", detail
    return "high activity", detail


def generate_session_summary(session): 
    usable = session.usable_observations
    participant = session.participant

    heart_rates_summary = summarize_values([obs.heart_rate for obs in usable])
    skin_response_summary = summarize_values([obs.skin_response for obs in usable])
    temperature_summary = summarize_values([obs.temperature for obs in usable])
    activity_summary = summarize_values([obs.activity_level for obs in usable])

    label, reason = classify_session(session)
    is_recovering, recovery_explanation = detect_recovery(session)


    return {
        "participant_id": participant.participant_id,
        "participant_name": participant.name,
        "session_id": session.session_id,
        "total_observations": session.total_count(),
        "usable_observations": session.usable_count(),
        "low_quality_observations": session.low_quality_count(),
        "heart_rate": heart_rates_summary,
        "skin_response": skin_response_summary,
        "temperature": temperature_summary,
        "activity_level": activity_summary,
        "baseline_differences": {
            "heart_rate": compare_baseline(heart_rates_summary["average"], participant.baseline_heart_rate),
            "skin_response": compare_baseline(skin_response_summary["average"], participant.baseline_skin_response),
            "temperature": compare_baseline(temperature_summary["average"], participant.baseline_temperature),
        },
        "classification": label,
        "classification_reason": reason,
        "recovery_detected": is_recovering,
        "recovery_explanation": recovery_explanation,
    }
