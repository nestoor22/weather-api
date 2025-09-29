Weather API

A simple FastAPI-based service that fetches current weather data for a city using OpenWeather API, caches responses in Redis, and stores fetched payloads in S3 (via Localstack in development). The service exposes a single endpoint to retrieve weather by city and includes health check, request tracing, and a rate limiter.

Quick start (Docker Compose)
- Prerequisites:
  - Docker and Docker Compose installed
  - An OpenWeather API key: https://openweathermap.org/api
- Steps:
  1. Create a .env file in the repository root (copy .env.example):
  2. Start the stack:
     docker-compose up --build
  3. Once healthy, the API will be available at:
     - Weather endpoint: http://localhost:8001/weather?city=London
     - Health check: http://localhost:8001/health
     - Swagger UI: http://localhost:8001/docs

Environment variables
- OPEN_WEATHER_API_KEY (required): Your OpenWeather API key.
- REDIS_HOST (required): Redis hostname (use redis when running via docker-compose).
- REDIS_PORT (required): Redis port (default 6379).
- REDIS_USE_SSL (optional): Use SSL for Redis (true/false). Default true in code; set to false for local docker-compose.
- WEATHER_DATA_BUCKET_NAME (optional): S3 bucket name for storing weather JSON objects. Default: weather.
- AWS_ENDPOINT_URL_CUSTOM (optional): Custom S3 endpoint; Localstack uses http://localstack:4566 inside Docker.

Local development tips
- Code reload: The docker-compose mounts ./app into the container so you can edit code locally; restart may be needed for some changes.
- Logs: Service logs show rate limit and tracing details.
- Changing the exposed port: docker-compose maps 8001:8000; adjust docker-compose.yml if needed.

Example request
- CURL:
  curl "http://localhost:8001/weather?city=Paris"

- Possible errors (converted to HTTP errors):
  - 404-like: City not found.
  - 502/503-like: Failed to get coordinates/weather data from OpenWeather.
  - 500: Failed to upload to S3 or unhandled exceptions.

Project structure (high level)
- app/main.py: FastAPI app, middleware, routers, error handlers.
- app/api/weather.py: /weather endpoint definition.
- app/services/weather.py: Orchestrates cache, OpenWeather integration, and S3 upload.
- app/core/integrations/open_weather_integration.py: OpenWeather API calls.
- app/core/integrations/s3_client.py: S3 client via aioboto3 (targets Localstack in dev).
- app/core/caches/*: Redis base client and caches for rate limiting and weather data.
- app/core/middlewares/*: Rate limiting and trace ID propagation.
- app/core/config.py: Pydantic settings (env variables).
