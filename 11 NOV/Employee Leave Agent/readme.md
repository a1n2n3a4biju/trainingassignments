# Employee Leave Policy Agent

## Project Overview

The **Employee Leave Policy Agent** is an AI-powered assistant designed to answer employee queries based on an organization's leave policy documentation.

The project uses **Microsoft Foundry** to configure and deploy the AI agent, **Azure AI tracing** to monitor agent interactions, and **Redis** to maintain conversational history across multiple messages within a session.

## Tech Stack

- **Microsoft Foundry** – Agent creation and configuration
- **Python** – Backend development
- **Azure AI Project Endpoint** – Connects the Python application to the Foundry project
- **Redis** – Session-based conversation history storage
- **FastAPI** – API development and endpoint testing
- **Docker** – Running Redis as a container
- **PyCharm** – Development environment

---

## Implementation Steps

### Phase 1: Create and Configure the Agent in Microsoft Foundry

1. Open the [Microsoft Foundry Portal](https://ai.azure.com/).
2. Create a new Foundry resource/project.
3. Navigate to the **Foundry Portal**.
4. Create a new agent for the Employee Leave Policy use case.
5. Configure the agent instructions with the Employee Leave Policy guidelines.
6. Upload the Employee Leave Policy document as the agent's knowledge source.
7. Configure the appropriate guardrails to ensure the agent provides safe, relevant, and policy-compliant responses.
8. Add sample questions to test the agent's responses.
9. Navigate to **Traces** to monitor agent execution and interactions.
10. Create the required resource and complete the setup.

### Phase 2: Integrate Microsoft Foundry with Python

1. Open the project in PyCharm.
2. Copy the `FOUNDRY_PROJECT_ENDPOINT` from Microsoft Foundry.
3. Add the endpoint to the project's `.env` file.

   ```env
   FOUNDRY_PROJECT_ENDPOINT=your_foundry_project_endpoint
   ```

4. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Update `main.py` to establish a connection with the Microsoft Foundry agent and process employee leave-related queries.

6. Open the PyCharm terminal and configure Azure authentication.

   **Step 1: Configure Azure CLI for Windows**

   ```bash
   az config set core.enable_broker_on_windows=false
   ```

   **Step 2: Log in to Azure**

   ```bash
   az login
   ```

7. Run the Python application:

   ```bash
   python main.py
   ```

8. Enter the sample employee leave policy questions in the terminal and verify the agent's responses.

9. Return to the Microsoft Foundry Portal and navigate to **Traces**.

10. Verify that the agent interactions and execution traces are being recorded successfully.

### Phase 3: Integrate Redis Using Docker

Redis is used to maintain conversation history so that the agent can remember previous messages within the same session.

**Step 1: Start Docker Desktop**

Make sure Docker Desktop is installed, running, and ready to execute containers.

**Step 2: Update Project Dependencies**

Add the required Redis dependencies to `requirements.txt` and install them:

```bash
pip install -r requirements.txt
```

**Step 3: Update Environment Variables**

Add the Redis connection URL to the `.env` file:

```env
REDIS_URL=redis://localhost:6379
```

**Step 4: Start the Redis Container**

Run the following command in the terminal:

```bash
docker run -d \
  --name retail-redis \
  -p 127.0.0.1:6379:6379 \
  -v retail_redis_data:/data \
  redis:7-alpine \
  redis-server --appendonly yes
```

This command:

- Runs Redis in detached mode.
- Creates a container named `retail-redis`.
- Exposes Redis on port `6379` locally.
- Creates a persistent Docker volume named `retail_redis_data`.
- Enables Redis Append-Only File (AOF) persistence.

**Step 5: Start the FastAPI Application**

Open a new PyCharm terminal and execute:

```bash
python -m uvicorn main:app --reload
```

The application will be available at:

- API Base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

### Phase 4: Test Session-Based Conversation History

Use Swagger UI to verify that Redis stores and retrieves conversation history correctly.

**Step 1: Send the First Message**

1. Open http://127.0.0.1:8000/docs.
2. Locate the `POST /message` endpoint.
3. Enter an employee leave policy question.
4. Execute the request.
5. Copy the generated `session_id` from the response.

**Step 2: Continue the Conversation**

1. Send another message using the same `session_id`.
2. Ask a follow-up question related to the previous conversation.
3. Verify that the agent can maintain conversational context.
4. Copy the session ID for history retrieval.

**Step 3: Retrieve Conversation History**

1. Locate the `GET /history/{session_id}` endpoint.
2. Paste the session ID obtained from the previous requests.
3. Execute the endpoint.
4. Verify that the conversation history is returned successfully.

**Step 4: Verify Redis Storage**

Open another PyCharm terminal and execute:

```bash
docker exec -it retail-redis redis-cli
```

Inside the Redis CLI, run:

```redis
KEYS retail:*
```

The command should display the Redis keys associated with the stored conversation histories.

To inspect a particular key:

```redis
TYPE retail:your_session_key
```

Use the appropriate Redis command for the returned data type to inspect its contents.

---

## Expected Outcome

After completing the implementation:

- The AI agent answers employee queries using the uploaded leave policy document.
- Guardrails help restrict responses to the intended policy scope.
- Microsoft Foundry traces provide visibility into agent execution.
- The Python application communicates with the deployed Foundry agent.
- Redis stores conversation history against individual session IDs.
- Employees can continue conversations while maintaining session context.
- FastAPI exposes endpoints for sending messages and retrieving conversation history.
- Docker provides a persistent Redis environment for conversation storage.

## Environment Configuration

Create a `.env` file in the project root:

```env
FOUNDRY_PROJECT_ENDPOINT=your_foundry_project_endpoint
REDIS_URL=redis://localhost:6379
```

**Important:** Never commit your actual `.env` file, Azure credentials, or API keys to GitHub. Add `.env` to `.gitignore` and provide a `.env.example` file containing placeholder values.

## Useful Commands

| Purpose | Command |
|---|---|
| Install dependencies | `pip install -r requirements.txt` |
| Azure login | `az login` |
| Run Python application | `python main.py` |
| Start FastAPI | `python -m uvicorn main:app --reload` |
| Start Redis container | `docker start retail-redis` |
| Check running containers | `docker ps` |
| Open Redis CLI | `docker exec -it retail-redis redis-cli` |
| View Redis keys | `KEYS retail:*` |
| Stop Redis container | `docker stop retail-redis` |

---

## Conclusion

The Employee Leave Policy Agent demonstrates the integration of Microsoft Foundry, Python, FastAPI, and Redis to build an AI-powered employee support solution. It combines document-based question answering, guardrails, agent tracing, and session-based conversational memory into a single application.
