**Input Validation Microservice**
Description: This microservice validates input data for two main programs:
  - Fitness tracker
  - Diet Tracker

It ensures:
  - Required Fields are present
  - Values are correctly formatted
  - Unauthorized requests are rejected

The microservices communicates using text files not directly calling other programs. The test file
simulates a main program using the microservice. 

Communication Contract:
This is a text-file based communication, meaning:
  - Request file: pipe/validate_request.txt
  - Response file: pipe/validate_response.txt
Both are json formatted text.

How to REQUEST Data:
1. Open pipe/validate_request.txt
2. write json object
3. save & close the file
*Request format*

{
  "service": "fitness" | "diet",
  "auth_token": "VALID",
  "payload": { ... }
}

*Example*
{
  "service": "fitness",
  "auth_token": "VALID",
  "payload": {
    "date": "2026-02-25",
    "exercise_name": "Run",
    "duration_minutes": 30
  }
}

*Example request (diet)*
{
  "service": "diet",
  "auth_token": "VALID",
  "payload": {
    "meal_name": "Lunch",
    "calories": 600
  }
}

How to RECIEVE Data:
The microservice should write a json response to:
  pipe/validate_response.txt

*Respones Format*
{
  "valid": true | false,
  "errors": ["error message if any"]
}

*Example unauthorized response*
{
  "valid": false,
  "errors": ["unauthorized"]
}

**How to run**
1. Clone the repository
2. Make sure you're in the correct folder/directory. Do not be in /src, /tests, or /pipe
3. Open a command prompt/terminal and enter these command(s):
   - python3 src/microservice.py (Linux/Mac)
   - python3 src\microservice.py (Windows)
4. Output should look like this:
    Input Validation Microservice running...
    Request file:  pipe\validate_request.txt
    Response file: pipe\validate_response.txt
5. Open a second command prompt/terminal and enter these command(s):
   - python3 tests/test_client.py (Linux/Mac)
   - python3 src\microservice.py (Windows)
6. Output should look like this:
   Fitness valid -> {'valid': True, 'errors': []}
   Diet missing calories -> {'valid': False, 'errors': ['calories missing']}
   Unauthorized -> {'valid': False, 'errors': ['unauthorized']}

***IMPORTANT NOTE FOR WINDOWS***
Use \ in paths
Make sure you're in the repo root folder before running
if python or python3 does not work, try:
  - py src\microservice.py
  - py tests\test_client.py
