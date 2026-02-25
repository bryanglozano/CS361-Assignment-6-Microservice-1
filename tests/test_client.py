import json
import time
from pathlib import Path

PIPE_DIR = Path("pipe")
REQ = PIPE_DIR / "validate_request.txt"
RES = PIPE_DIR / "validate_response.txt"

POLL_SECONDS = 0.1

def send(req: dict) -> None:
    REQ.write_text(json.dumps(req))

def wait_for_response(timeout: float = 5.0) -> dict:
    start = time.time()
    while time.time() - start < timeout:
        raw = RES.read_text().strip()
        if raw:
            return json.loads(raw)
        time.sleep(POLL_SECONDS)
    raise TimeoutError("TIMED OUT waiting for response.")

def clear_response() -> None:
    RES.write_text("")

def main() -> None:
    PIPE_DIR.mkdir(parents=True, exist_ok=True)
    REQ.touch(exist_ok=True)
    RES.touch(exist_ok=True)
    clear_response()

    send({
        "service": "fitness",
        "auth_token": "VALID",
        "payload": {"date": "2026-02-25", "exercise_name": "Run", "duration_minutes": 30}
    })
    print("Fitness valid ->", wait_for_response())
    clear_response()

    send({
        "service": "diet", 
        "auth_token": "VALID",
        "payload": {"meal_name": "lunch"}
    })
    print("Diet missing calories ->", wait_for_response())
    clear_response()
    
    send({
        "service": "fitness",
        "auth_token": "",
        "payload": {"date": "2026-02-24", "exercise_name": "Lift", "duration_minutes": 45}
    })
    print("Unauthorized ->", wait_for_response())
    clear_response()

if __name__ == "__main__":
    main()
