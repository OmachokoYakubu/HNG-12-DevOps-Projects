from fastapi import FastAPI, Query, HTTPException
import requests
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ... (CORS configuration and helper functions remain the same)

@app.get("/api/classify-number")
def classify_number(number: str = Query(..., description="Enter a number")):
    """API endpoint to classify a number."""
    original_input = number  # Store the exact user input

    try:
        # Attempt conversion (same as before)
        try:
            parsed_number = int(number)  
        except ValueError:
            try:
                parsed_number = int(float(number))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={"number": original_input, "error": True}  # No "detail" key
                )

        # ... (rest of the code remains the same)

    except HTTPException as e:
        raise e  # Re-raise the exception

    return {
        "number": parsed_number,  # Or original_input if you want to return the original
        "is_prime": is_prime(abs_number),
        "is_perfect": False, 
        "properties": properties,
        "digit_sum": digit_sum(abs_number),
        "fun_fact": get_fun_fact(abs_number),
    }

# ... (Uvicorn run configuration remains the same)
