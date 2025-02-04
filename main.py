from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Union, List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; adjust this as necessary
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def is_prime(num: int) -> bool:
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def is_armstrong(num: int) -> bool:
    digits = [int(d) for d in str(num)]
    power = len(digits)
    return num == sum([d ** power for d in digits])

def digit_sum(num: int) -> int:
    return sum([int(d) for d in str(num)])

def get_fun_fact(num: int) -> str:
    response = requests.get(f'http://numbersapi.com/{num}/math')
    if response.status_code == 200:
        return response.text
    return "No fun fact available."

@app.get("/api/classify-number")
def classify_number(number: Union[int, float] = Query(..., description="Enter a number")):
    try:
        number = int(number)
    except ValueError:
        try:
            number = float(number)
        except ValueError:
            raise HTTPException(status_code=400, detail={"number": str(number), "error": True})

    properties: List[str] = []
    is_armstrong_num = is_armstrong(number)
    is_odd = int(number) % 2 != 0  # Convert to int for parity check

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
        "is_prime": is_prime(number),  # No need to convert to int here
        "is_perfect": False,
        "properties": properties,
        "digit_sum": digit_sum(number),  # No need to convert to int here
        "fun_fact": get_fun_fact(number),  # No need to convert to int here
    }

