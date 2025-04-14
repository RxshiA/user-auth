# User Authentication Microservice

This microservice handles user registration, login, and profile retrieval using Flask, JWT, and SQLite.

## Endpoints

- `POST /register`: Register a new user.
- `POST /login`: Authenticate a user and return a JWT token.
- `GET /profile`: Retrieve the authenticated user's profile (requires a valid token).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Build and run with Docker:
   ```bash
   docker build -t user-auth .
   docker run -p 5000:5000 user-auth
   ```

## Deployment

This service is designed to be deployed on AWS ECS with Fargate. Use the provided GitHub Actions workflow for CI/CD.