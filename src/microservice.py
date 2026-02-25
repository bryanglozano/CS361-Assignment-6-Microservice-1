import json
import time
from pathlib import Path
from validator import validate_request

PIPE_DIR = Path("pipe")
REQ = PIPE_DIR / "validate_request.txt"
RES = PIPE_DIR / "validate_response.txt"

POLL_SECONDS = 0.1

def write_response(valid: bool, errors: list[str]) -> None:
    RES.write_text(json.dumps({"valid": valid, "errors": errors}, indent=2))

def main() -> None:
    PIPE_DIR.mkdir(parents=True, exist_ok=True)
    REQ.touch(exist_ok=True)
    RES.touch(exist_ok=True)

    print("Input validation Microservice running...")
    print(f"Reequest File: {REQ}")
    print(f"Response file: {RES}")

    while True:
        raw = REQ.read_text().strip()
        if not raw:
            time.sleep(POLL_SECONDS)
            continue

        try:
            req = json.loads(raw)
        except json.JSONDecodeError:
            write_response(False, ["request must be valid JSON"])
            REQ.write_text("")
            continue

        valid, errors = validate_request(req)
        write_response(valid, errors)

        REQ.write_text("") 

if __name__ == "__main__":
    main()
