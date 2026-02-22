Description
REST API for contact management.

Implemented Features

CRUD operations

Input validation and error handling

Swagger documentation

Docker support

Pagination and email filtering

Run Locally
pip install -r requirements.txt
python -m app.main

Docker
docker build -t contacts-api .
docker run -p 5000:5000 contacts-api

API Documentation
Swagger available at:
http://localhost:5000/apidocs