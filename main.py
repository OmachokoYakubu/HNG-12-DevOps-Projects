from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel
import requests
from typing import List

# Define error response model
class ErrorResponse(BaseModel):
    number: str
    error: str

app = FastAPI()

# Function to check for prime, armstrong, etc. remains the same

@app.get("/api/classify-number", response_model=ErrorResponse, status_code=status.HTTP_400_BAD_REQUEST)
def classify_number(number: str = Query(..., description="Enter a number")):
    """
    API endpoint to classify a number.

    Accepts numbers in different formats (negative, string, float, etc.).
    """
    original_input = number  # Store the exact user input

    try:
        # Try to parse the number
        parsed_number = int(float(number))  
    except ValueError:
        # Return the invalid input in the error response
        return {"number": original_input, "error": "Invalid input: Number must be an integer or float"}  # Return invalid input directly

    # Proceed with the rest of the logic if the input is valid
    is_negative = parsed_number < 0
    abs_number = abs(parsed_number)
    properties: List[str] = []

    # Further classification logic here (is_armstrong, is_prime, etc.)
    return {
        "number": parsed_number,
        "is_prime": is_prime(abs_number),
        "is_perfect": False,  # No perfect number check in this version
        "properties": properties,
        "digit_sum": digit_sum(abs_number),
        "fun_fact": get_fun_fact(abs_number),
    }

