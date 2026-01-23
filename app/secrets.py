import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

SECRET_ID_TO_ENV_VAR = {
    "telegram-api-key": "TELEGRAM_API_KEY",
    "skaping-api-key": "SKAPING_API_KEY",
}


def _use_local_secrets() -> bool:
    return os.environ.get("USE_LOCAL_SECRETS", "").lower() == "true"


@lru_cache
def get_secret_manager_client():
    from google.cloud import secretmanager

    return secretmanager.SecretManagerServiceClient()


def get_secret(secret_id: str) -> str:
    if _use_local_secrets():
        env_var = SECRET_ID_TO_ENV_VAR.get(secret_id, secret_id.upper().replace("-", "_"))
        value = os.environ.get(env_var)
        if not value:
            raise ValueError(f"Environment variable {env_var} is not set")
        return value

    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is not set")

    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


@lru_cache
def get_telegram_api_key() -> str:
    return get_secret("telegram-api-key")


@lru_cache
def get_skaping_api_key() -> str:
    return get_secret("skaping-api-key")
