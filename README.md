# Containerized LLM Deployment

This repository teaches how to package an asynchronous LLM API in Docker and
deploy it to [Render](https://render.com/docs) with explicit health checks,
resource, scaling, caching, and cost decisions. The API, Dockerfile, and
deployment configuration are supplied. Start with the local stub so you can
observe the service behavior without an API key or cloud account. The hosted
walkthrough can be followed as a configuration review or an instructor demo.

## Learning Objectives

By the end of this repository, you should be able to:

- Deploy a containerized LLM API to Render with explicit resource, health, and
  secret configuration.
- Configure and justify manual or automatic scaling for variable inference
  load.
- Diagnose cold starts, memory pressure, provider latency, and request
  timeouts.
- Measure exact-match cache behavior and estimate fixed plus token-based cost.

## Learning Path

| File / Folder | Description |
|---|---|
| [**01 - Container Contract**](01-container-contract.md) | Build the image, run the container, and verify health and readiness from the host. |
| [**02 - Render Deployment**](02-render-deployment.md) | Map the same container contract to a Render Blueprint and follow the optional hosted verification. |
| [**03 - Scaling and Failures**](03-scaling-and-failures.md) | Reuse the running container to compare a healthy load run with a controlled outage and diagnose the failure. |
| [**04 - Caching and Cost**](04-caching-and-cost.md) | Inspect a cache hit and connect token usage, instance hours, and cost to what you would measure before scaling. |

### Additional Folders and Files

| File / Folder | Description |
|---|---|
| [**assets**](assets/) | Visual aids referenced in the repository. |
| [**Autoscaling Example**](deployment/) | Optional paid Render autoscaling configuration. |
| [**scripts/load_test.py**](scripts/load_test.py) | Load probe that reports throughput, p95 latency, and error rate. |
| [**Dockerfile**](Dockerfile) | Container image for the API. |
| [**docker-compose.yaml**](docker-compose.yaml) | Local service definition with runtime settings and a health check. |
| [**render.yaml**](render.yaml) | Render Blueprint for the hosted deployment. |
| [**.env.example**](.env.example) | Provider configuration template and service limits. |
| [**pyproject.toml**](pyproject.toml) | Project configuration and dependencies. |
| [**uv.lock**](uv.lock) | Dependency lock file. |

## Prerequisites

- **Docker Desktop**: required to build the API image and run the container with `docker compose`. Follow the [installation instructions](https://docs.docker.com/get-docker/) if you do not have it yet. Make sure it is **installed and running** before you start [01 - Container Contract](01-container-contract.md).

> [!NOTE]
> **Windows Users:** The commands in this walkthrough use bash syntax. Use **Git Bash** (installed with [Git for Windows](https://git-scm.com/downloads/win)) instead of PowerShell to run them.

## Setup

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13.5 or newer
and Python 3.13.17 or a newer 3.13 patch release, as defined in
[`.python-version`](.python-version).

> [!NOTE]
> Throughout these steps, text in angle brackets like `<repo-name>` is a **placeholder**. Replace it, including the `< >` brackets, with your own value. For example, `cd <repo-name>` becomes `cd mle-containerized-llm-deployment`.

### 1. Create the Repository from the Template

Click **Use this template** on GitHub.

When creating the repository:

- Set yourself as the **Owner**
- Choose a repository name
- Disable **Include all branches**
- Click **Create repository**

> [!IMPORTANT]
> If you are working in pairs or groups, only **one person** should complete this step.

---

### 2. Add Collaborators (Pairs/Groups Only)

If working with teammates:

1. Open the repository on GitHub
2. Go to **Settings → Collaborators**
3. Add your teammates as collaborators
4. Share the repository link with your team

Teammates should accept the invitation before continuing.

---

### 3. Clone the Repository

Copy the SSH URL from the **Code** button on GitHub, then run:

```bash
git clone <copied-ssh-url>
```

The copied SSH URL will look like `git@github.com:<your-username>/<repo-name>.git`.

---

### 4. Move into the Project Folder and Install Dependencies

This installs all dependencies and creates a virtual environment in `.venv/`.

```bash
cd <repo-name>
uv sync
```

---

### 5. Set Up Environment Variables

Copy the provider settings and service limits:

```bash
cp .env.example .env
```

The guides explicitly set `MODEL_PROVIDER=dry` for the local walkthrough, so no keys are needed. For live calls, keep `MODEL_PROVIDER=groq` and fill in `GROQ_API_KEY`.

> [!CAUTION]
> Never commit `.env`. It is git-ignored because environment files often hold secrets. Only `.env.example`, with placeholder or default values, belongs in the repository.

---

### 6. Open the Repository in VS Code

> [!NOTE]
> Make sure you open VS Code from the project root so it automatically detects the environment created by `uv sync`.

Launch VS Code in the project root folder:

```bash
code .
```

Select the Python interpreter in `.venv/` created by `uv sync`. Run all commands in the lessons from the repository root.

## Run Without Docker

For a quick API check, run the same app directly from Python. Use this
instead of the container on port 8000, not alongside it.

```bash
MODEL_PROVIDER=dry uv run --locked uvicorn deployment_service.app:app --app-dir src
```

Use the requests in [step 01](01-container-contract.md#verify-the-api). Stop
the process with Ctrl+C before switching to Docker. Run the isolated test
suite with `uv run --locked pytest`; it does not require Docker or API keys.

For an optional live run, the default provider is Groq. Choose `groq`,
`mistral`, `openrouter`, `google`, or `openai` in `.env` and supply the
matching key and model from [`.env.example`](.env.example). Provider and Render
charges are separate; review pricing and protect public endpoints before
enabling paid inference.

## References & Further Reading

- Render: [Blueprint Specification](https://render.com/docs/blueprint-spec) / [Health Checks](https://render.com/docs/health-checks) / [Scaling](https://render.com/docs/scaling)
- [FastAPI Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/)
