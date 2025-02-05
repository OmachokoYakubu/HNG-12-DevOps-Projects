from fastapi import FastAPI, Query, HTTPException  
import requests
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
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
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(abs(n) ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    num_str = str(abs(n))
    digits = [int(d) for d in num_str]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def digit_sum(n: int) -> int:
    """Calculate the sum of the digits of a number."""
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n: int) -> str:
    """Fetch a fun fact about a number from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return "No fun fact available."

@app.get("/api/classify-number")
def classify_number(number: str = Query(..., description="Enter a number")):
    """
    API endpoint to classify a number.
    
    Accepts numbers in different formats (negative, string, float, etc.).
    """
    original_input = number  # Store the exact user input

    try:
        # Convert input to an integer, even if it's a float or string
        parsed_number = int(float(number))  
    except ValueError:
        # Returning the invalid input as part of the response
        raise HTTPException(
            status_code=400,
            detail={"number": original_input, "error": "Invalid input: Number must be an integer or float"}
        )

    is_negative = parsed_number < 0
    abs_number = abs(parsed_number)

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
        "number": parsed_number,
        "is_prime": is_prime(abs_number),
        "is_perfect": False,  # No perfect number check in this version
        "properties": properties,
        "digit_sum": digit_sum(abs_number),
        "fun_fact": get_fun_fact(abs_number),
    }

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

