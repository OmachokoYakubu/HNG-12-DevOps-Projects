from fastapi import FastAPI, Query, HTTPException
import requests
from typing import Union, List

app = FastAPI()

# ... (your other functions: is_prime, is_armstrong, digit_sum, get_fun_fact)

@app.get("/api/classify-number")
def classify_number(number: Union[int, float] = Query(..., description="Enter a number")):
    try:
        # Attempt conversion to int first
        try:
            number = int(number)
        except ValueError:
            try:
                number = float(number)
            except ValueError:
                raise HTTPException(status_code=400, detail={"number": number, "error": "Invalid input: Number must be an integer or float"})

        if not isinstance(number, (int, float)):  # Redundant check, but good practice
            raise HTTPException(status_code=400, detail={"number": number, "error": "Invalid input: Number must be an integer or float"})

    except HTTPException as e: # Re-raise HTTPExceptions to be handled by FastAPI
        raise e

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
