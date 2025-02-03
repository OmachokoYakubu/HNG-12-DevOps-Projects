from fastapi import FastAPI, Query
import requests

app = FastAPI()

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = list(map(int, str(n)))
    power = len(digits)
    return sum(d ** power for d in digits) == n

def digit_sum(n):
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="Enter a valid integer")):
    if not isinstance(number, int):
        return {"number": number, "error": True}
    
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 else "even")

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": False,  # Implement if needed
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number),
    }
