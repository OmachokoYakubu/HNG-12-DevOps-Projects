from fastapi import FastAPI, Query, HTTPException
import requests
from typing import Union, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration (customize as needed)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "*",  # Allows requests from any origin (USE WITH CAUTION IN PRODUCTION)
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
        response = requests.get(f"http://numbersapi.com/{n}/math")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return "No fun fact available."

@app.get("/api/classify-number")
def classify_number(number: str = Query(..., description="Enter a number")):
    try:
        number = int(float(number))  # Convert input to an integer, even if in float form
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "number": number,  # Keep the original invalid input
                "error": "Invalid input: Number must be an integer"
            }
        )

    is_negative = number < 0
    abs_number = abs(number)

    properties: List[str] = []
    is_armstrong_num = is_armstrong(abs_number)
    is_odd = abs_number % 2 != 0

    if is_armstrong_num and is_odd:
        properties = ["armstrong", "odd"]
    elif is_armstrong_num and not is_odd:
        properties = ["armstrong", "even"]
    elif is_odd:
        properties = ["odd"]
    else:
        properties = ["even"]

    return {
        "number": number,
        "is_prime": is_prime(abs_number),
        "is_perfect": False,
        "properties": properties,
        "digit_sum": digit_sum(abs_number),
        "fun_fact": get_fun_fact(abs_number),
    }

# Proper Uvicorn entry point for running the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

