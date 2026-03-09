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

The health endpoint is available at http://localhost:8000.

### Run the scheduler CLI in Docker

Use the optional `cli` profile service for the full Telegram workflow:

```powershell
docker compose run --rm cli
```

This command uses environment variables from `.env`.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)