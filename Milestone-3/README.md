# AI Travel & Weather Assistant

A simple AI assistant that helps employees plan trips, check weather forecasts and get useful travel suggestions. It also remembers previous chat messages.

## Setup

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your PostgreSQL details.

## Start Services

- Start PostgreSQL.
- Start Redis: `docker start travel-redis`
- Make sure Ollama is running with `qwen2.5:3b`.

## Run the Project

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to access the APIs.

## Test

Use Swagger UI to try:

- `POST /trips` – Create a trip.
- `GET /trips/{trip_id}` – View trip details.
- `POST /chat` – Ask travel and weather questions.

Try a follow-up question with the same session ID to test chat memory.

**Note:** This project uses PostgreSQL, Redis, Open-Meteo, LangChain and Ollama.