from fastapi import FastAPI, Query, HTTPException
import requests
from typing import Union, List
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

app = FastAPI()

# CORS configuration (customize as needed)
origins = [
    "http://localhost",  # Allows requests from localhost
    "http://localhost:8080",  # Allows requests from localhost on port 8080
    "*", # Allows requests from any origin (USE WITH CAUTION IN PRODUCTION)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    num_str = str(abs(n))
    digits = [int(d) for d in num_str]
    power = len(digits)
    return sum(d**power for d in digits) == abs(n)

def digit_sum(n: int) -> int:
    num_str = str(abs(n))
    return sum(int(d) for d in num_str)

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")  # Use /math endpoint
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        return "No fun fact available."

@app.get("/api/classify-number")
def classify_number(number: Union[int, float] = Query(..., description="Enter a number")):
    try:
        try:
            number = int(number)
        except ValueError:
            try:
                number = float(number)
            except ValueError:
                raise HTTPException(status_code=400, detail={"number": number, "error": "Invalid input: Number must be an integer or float"})

        if not isinstance(number, (int, float)):
            raise HTTPException(status_code=400, detail={"number": number, "error": "Invalid input: Number must be an integer or float"})

    except HTTPException as e:
        raise e

    is_negative = number < 0
    number = abs(number)

    properties: List[str] = []
    is_armstrong_num = is_armstrong(number)
    is_odd = int(number) % 2 != 0

    if is_armstrong_num and is_odd:
        properties = ["armstrong", "odd"]
    elif is_armstrong_num and not is_odd:
        properties = ["armstrong", "even"]
    elif is_odd:
        properties = ["odd"]
    else:
        properties = ["even"]

    return {
        "number": ( -number if is_negative else number),
        "is_prime": is_prime(number),
        "is_perfect": False,
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number),
    }

# To run the app using Uvicorn:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
