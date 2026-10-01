# Investment Platform Backend

## Project

FastAPI backend for a Bangladesh-focused platform where small businesses can
submit investment opportunities and potential investors can discover them.

## Current implementation

Only the backend foundation and health API are currently implemented. No
business domains, database integration, or authentication exist yet.

The current endpoint is:

```text
GET /api/v1/health
```

## Requirements

- Python 3.12

## Setup

Run these commands from the `backend` directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

The values in `.env.example` are local development examples. Update the copied
`.env` file for your environment; never commit real credentials.

## Run

Start the development server from the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

## Test

```bash
pytest
```

## Lint

```bash
ruff check .
```

## Format check

```bash
ruff format --check .
```

## API documentation

While the local server is running, FastAPI provides interactive Swagger UI at
`http://127.0.0.1:8000/docs`, ReDoc at `http://127.0.0.1:8000/redoc`, and the
OpenAPI document at `http://127.0.0.1:8000/openapi.json`.
