from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

# Function to calculate the sum of digits
def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

# Function to get a fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

# API Endpoint
@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="Enter a valid integer")):
    try:
        properties = ["even" if number % 2 == 0 else "odd"]

        if is_armstrong(number):
            properties.append("armstrong")

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": False,  # You can implement this if needed
            "properties": properties,
            "digit_sum": digit_sum(number),
            "fun_fact": get_fun_fact(number),
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input. Please enter a valid integer.")


