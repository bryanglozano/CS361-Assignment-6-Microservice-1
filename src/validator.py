from typing import Any, Dict, List, Tuple

def _non_empty_string(x: Any) -> bool:
    return isinstance(x, str) and x.strip() != ""

def validate_auth(auth_token: Any) -> Tuple[bool, List[str]]:
    if not _non_empty_string(auth_token):
        return False, ["unauthorized"]
    if auth_token != "VALID":
        return False, ["unauthorized"]
    return True, []

def validate_fitness(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    for k in ["date", "exercise_name", "duration_minutes"]:
        if k not in payload:
            errors.append(f"{k} missing")

    if "exercise_name" in payload and not _non_empty_string(payload["exercise_name"]):
        errors.append("exercise_name must be a non-empty string")

    if "duration_minutes" in payload:
        try:
            val = float(payload["duration_minutes"])
            if val <= 0:
                errors.append("duration_minutes must be > 0")
        except (TypeError, ValueError):
            errors.append("duration_minutes must be a number")

    if "date" in payload and not _non_empty_string(payload["date"]):
        errors.append("date must be a non empty string")
    
    return (len(errors) == 0), errors


def validate_diet(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    for k in ["meal_name", "calories"]:
        if k not in payload:
            errors.append(f"{k} missing")

    if "meal_name" in payload and not _non_empty_string(payload["meal_name"]):
        errors.append("meal_name must be a non-empty string")

    if "calories" in payload:
        try:
            cals = float(payload["calories"])
            if cals < 0:
                errors.append("calories must be >= 0")
        except (TypeError, ValueError):
            errors.append("calories must be a number")

    return (len(errors) == 0), errors


def validate_request(req: Dict[str, Any]) -> Tuple[bool, List[str]]:
    ok, auth_errors = validate_auth(req.get("auth_token"))
    if not ok:
        return False, auth_errors
    
    service = req.get("service")
    payload = req.get("payload")

    if service not in ("fitness", "diet"):
        return False, ["service must be a 'fitness' or 'diet'"]
    if not isinstance(payload, dict):
        return False, ["payload must be an object"]
    
    if service == "fitness":
        return validate_fitness(payload)
    return validate_diet(payload)
