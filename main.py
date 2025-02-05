from fastapi import FastAPI, Query, HTTPException
import requests
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration (same as before)
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

# ... (is_prime, is_armstrong, digit_sum, get_fun_fact functions - same as before)

@app.get("/api/classify-number")
def classify_number(number: str = Query(..., description="Enter a number")):
    """API endpoint to classify a number."""
    original_input = number  # Store the exact user input

    try:
        # Attempt conversion to int first
        try:
            parsed_number = int(number)  
        except ValueError:
            try:
                parsed_number = int(float(number))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={"number": str(original_input), "error": True}  # Use original_input here
                )

        is_negative = parsed_number < 0
        abs_number = abs(parsed_number)

        # ... (rest of the code: properties, is_armstrong_num, etc. - same as before)

    except HTTPException as e:
        raise e

    return {
        "number": parsed_number,
        "is_prime": is_prime(abs_number),
        "is_perfect": False, 
        "properties": properties,
        "digit_sum": digit_sum(abs_number),
        "fun_fact": get_fun_fact(abs_number),
    }

# Run the app with Uvicorn (same as before)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
