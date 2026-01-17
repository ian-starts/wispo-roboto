# wispo-roboto

Telegram chatbot for the WISPO group, deployed on Google Cloud Platform.

## Tech Stack

- **Framework**: FastAPI
- **Package Manager**: uv
- **Deployment**: Google Cloud Run
- **Storage**: Google Cloud Firestore
- **Secrets**: Google Cloud Secret Manager
- **CI/CD**: Google Cloud Build

## Local Development

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Google Cloud SDK (for local testing with GCP services)

### Setup

```bash
# Install dependencies
uv sync

# Copy the example env file and fill in your values
cp .env.example .env

# Run locally
uv run uvicorn app.main:app --reload --port 8080
```

### Environment Variables

For local development, copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

The `.env` file supports two modes:

**1. Local secrets mode** (no GCP required):
```bash
USE_LOCAL_SECRETS=true
TELEGRAM_API_KEY=your-telegram-bot-api-key
HERE_API_KEY=your-here-maps-api-key
SKAPING_API_KEY=your-skaping-api-key
WEATHER_API_ID=your-weather-api-id
WEATHER_API_KEY=your-weather-api-key
```

**2. GCP Secret Manager mode** (requires GCP authentication):
```bash
USE_LOCAL_SECRETS=false
GCP_PROJECT_ID=your-project-id
```

For GCP mode, authenticate with:

```bash
gcloud auth application-default login
```

## GCP Setup

### 1. Create Secrets in Secret Manager

Create the following secrets in Google Cloud Secret Manager:

```bash
# Telegram Bot API Key
echo -n "your-telegram-api-key" | gcloud secrets create telegram-api-key --data-file=-

# HERE Maps API Key (for distance calculations)
echo -n "your-here-api-key" | gcloud secrets create here-api-key --data-file=-

# Skaping API Key (for mountain images)
echo -n "your-skaping-api-key" | gcloud secrets create skaping-api-key --data-file=-

# Weather API credentials (for daily forecasts)
echo -n "your-weather-api-id" | gcloud secrets create weather-api-id --data-file=-
echo -n "your-weather-api-key" | gcloud secrets create weather-api-key --data-file=-
```

### 2. Create Firestore Database

```bash
gcloud firestore databases create --location=europe-west1
```

### 3. Grant Cloud Run Service Account Access

```bash
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

# Grant Secret Manager access
gcloud secrets add-iam-policy-binding telegram-api-key \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding here-api-key \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding skaping-api-key \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding weather-api-id \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding weather-api-key \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"

# Grant Firestore access
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/datastore.user"
```

### 4. Deploy to Cloud Run

#### Manual Deployment

```bash
gcloud run deploy wispo-roboto \
    --source . \
    --region europe-west1 \
    --allow-unauthenticated \
    --set-env-vars GCP_PROJECT_ID=$(gcloud config get-value project)
```

#### CI/CD with Cloud Build

Connect your repository to Cloud Build and it will automatically deploy on push using the `cloudbuild.yaml` configuration.

```bash
# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Grant Cloud Build permissions to deploy to Cloud Run
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
    --member="serviceAccount:$(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
    --member="serviceAccount:$(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 5. Set Up Daily Forecast (Cloud Scheduler)

To trigger the daily weather forecast at 5:00 AM:

```bash
# Enable Cloud Scheduler API
gcloud services enable cloudscheduler.googleapis.com

# Get Cloud Run URL
CLOUD_RUN_URL=$(gcloud run services describe wispo-roboto --region europe-west1 --format='value(status.url)')

# Create scheduled job
gcloud scheduler jobs create http wispo-daily-forecast \
    --location europe-west1 \
    --schedule "0 5 * * *" \
    --uri "${CLOUD_RUN_URL}/forecast" \
    --http-method POST \
    --oidc-service-account-email $(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')-compute@developer.gserviceaccount.com
```

### 6. Set Up Telegram Webhook

After deploying, set your Telegram bot webhook to point to Cloud Run:

```bash
CLOUD_RUN_URL=$(gcloud run services describe wispo-roboto --region europe-west1 --format='value(status.url)')

curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=${CLOUD_RUN_URL}/message"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/message` | POST | Telegram webhook endpoint |
| `/forecast` | POST | Trigger daily weather forecast |
| `/health` | GET | Health check endpoint |

## Bot Commands

- `/lol` - Get a lol response
- `/joke` - Get joke of the day
- `/mountainview` - Get a mountain image
- `/rng{number}` - Random number generator (1 to number)
- `/dishes` - Pick someone to do the dishes
- `/manly` - Generate a... size indicator
- `/dist` - Distance to WISPO destination
- `/address` - Get the WISPO address
- `/addresshotel` - Get the hotel address
- `/flip` - Flip a table
- `/back` - Put the table back
