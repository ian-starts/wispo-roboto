## Getting Started with wispo-roboto
### Last updated: January 2026

#### Project Structure
The main project folder (<project_root>) can contain the following files:

* **pyproject.toml** - Contains the project configuration and dependencies. Uses uv for package management.
* **Dockerfile** - Used for building the container image for Cloud Run deployment.
* **cloudbuild.yaml** - CI/CD configuration for Google Cloud Build.
* **.python-version** - Specifies the Python version for uv.
* **app/** - Contains the FastAPI application code.
  * **main.py** - Main FastAPI application with Telegram webhook endpoint.
  * **secrets.py** - Module for reading secrets from Google Cloud Secret Manager.
  * **wispo_storage.py** - Storage module using Google Cloud Firestore.
  * **forecast.py** - Daily weather forecast functionality.
  * **mother_of_all_file.py** - Various bot command implementations.
  * **joke.py** - Joke of the day functionality.
  * **array_extensions.py** - Utility functions.

#### Prerequisites

1. Install [uv](https://github.com/astral-sh/uv):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

#### Local Development

```bash
# Install dependencies
uv sync

# Set required environment variable
export GCP_PROJECT_ID=your-project-id

# Authenticate with GCP for local testing
gcloud auth application-default login

# Run the development server
uv run uvicorn app.main:app --reload --port 8080
```

#### Testing the Bot Locally

You can test the webhook endpoint locally using curl:

```bash
curl -X POST http://localhost:8080/message \
  -H "Content-Type: application/json" \
  -d '{"message": {"from": {"id": 123}, "chat": {"id": 456}, "text": "/joke"}}'
```

#### Deploying to GCP

See the main README.md for detailed GCP setup and deployment instructions.
