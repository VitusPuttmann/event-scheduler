### Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin)
- Docker daemon running

Quick check:

```powershell
docker --version
docker compose version
docker info
```

### Clone the repository

```powershell
git clone https://github.com/VitusPuttmann/event-scheduler.git
cd event-scheduler
```

### Configuration

Create your `.env` file before running containers:

```powershell
Copy-Item .env.example .env
```

Fill in the required values in `.env` (LLM, Tavily, Telegram, etc.).

### Build and run the HTTP container

```powershell
docker compose up --build server
```

The health endpoint is available at http://localhost:8001.

### Run the scheduler CLI in Docker

Use the optional `cli` profile service for the full Telegram workflow:

```powershell
docker compose run --rm cli
```

This command uses environment variables from `.env`.
