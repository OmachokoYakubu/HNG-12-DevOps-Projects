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

# ... (your is_prime, is_armstrong, digit_sum, get_fun_fact functions)

# Safe evaluation function (limited to basic math operations)
def safe_eval(expression: str) -> Union[int, float]:
    allowed_chars = "0123456789+-*/^.()"  # Allowed characters for safe evaluation
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters in expression")

    try:
        # Use ast.literal_eval for safe evaluation of basic math operations
        import ast
        return ast.literal_eval(expression)

    except (SyntaxError, TypeError, ValueError):
        raise ValueError("Invalid mathematical expression")


@app.get("/api/classify-number")
def classify_number(number: str = Query(..., description="Enter a number or a basic mathematical expression")):  # number is now a string
    try:
        number = safe_eval(number)  # Evaluate the expression safely
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"number": number, "error": str(e)})

    properties: List[str] = []
    is_armstrong_num = is_armstrong(number)
    is_odd = int(number) % 2 != 0 if isinstance(number, (int, float)) else False # Check if number is odd or even

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
        "is_prime": is_prime(int(number) if isinstance(number, (int, float)) else False),
        "is_perfect": False,
        "properties": properties,
        "digit_sum": digit_sum(int(number) if isinstance(number, (int, float)) else 0),
        "fun_fact": get_fun_fact(int(number) if isinstance(number, (int, float)) else 0),
    }
