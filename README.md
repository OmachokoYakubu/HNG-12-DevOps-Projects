# Number Classification API

This API takes a number as input and returns interesting mathematical properties about it, along with a fun fact.

## 📌 Features
- Checks if the number is **Prime**
- Determines if the number is an **Armstrong number**
- Classifies as **Odd or Even**
- Calculates the **Sum of Digits**
- Retrieves a **Fun Fact** from the Numbers API

## 📌 Technologies Used
- **FastAPI** - Python framework for building APIs
- **Uvicorn** - ASGI server to run the FastAPI application
- **Requests** - For fetching data from the Numbers API
- **Nginx** - Reverse proxy for handling HTTP requests

## 📌 API Endpoints
### ✅ **Classify a Number**
- **URL:** `GET /api/classify-number?number=<int>`
- **Example:** `https://13.60.180.189/api/classify-number?number=371`
- **Response (200 OK)**
  ```json
  {
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
  }

#Response (400 Bad Request)

{
  "number": "alphabet",
  "error": true
}

#📌 How to Install and Run Locally

#Clone the Repository

git clone https://github.com/OmachokoYakubu/HNG-12-DevOps-Projects.git
cd HNG-12-DevOps-Projects

#Install Dependencies

pip install fastapi uvicorn requests

#Run the Server

uvicorn main:app --host 0.0.0.0 --port 8000

#Access the API Documentation

Open http://127.0.0.1:8000/docs in your browser

#📌 Deployment on AWS

#Launch an EC2 Instance (Ubuntu 22.04 LTS)
#SSH into the instance

ssh -i ~/.ssh/HNG-12APIServerKP.pem ubuntu@13.60.180.189

#Clone this repository and install dependencies
#Run Uvicorn to start the API
#Configure Nginx as a reverse proxy
#Access the API using your public IP!#

#📌 Live Deployment

🌍 Public API URL: https://13.60.180.189/api/classify-number?number=371

#📌 Author

Omachoko Yakubu
GitHub: OmachokoYakubu
