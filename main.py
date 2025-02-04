from fastapi import FastAPI, Query, HTTPException
import requests
from typing import Union, List

app = FastAPI()

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    digits = list(map(int, str(n)))
    power = len(digits)
    return sum(d**power for d in digits) == n

def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        return "No fun fact available."  # Handle API errors gracefully

@app.get("/api/classify-number")
def classify_number(number: Union[int, float] = Query(..., description="Enter a number")):
    try:
        number = int(number) if isinstance(number, str) and number.isdigit() else float(number)
        if not isinstance(number, (int, float)):  # Check if it's a valid number (int or float)
            raise ValueError("Invalid input: Number must be an integer or float")
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"number": str(number), "error": str(e)})

    number = int(number) # Convert number to int for calculations

    properties: List[str] = [] # Type hint properties as a List of strings
    is_armstrong_num = is_armstrong(number)
    is_odd = number % 2 != 0

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
        "is_prime": is_prime(number),
        "is_perfect": False,  # Implement if needed
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number),
    }
