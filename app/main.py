from datetime import date, timedelta
from typing import Any

import httpx
import telegram
from fastapi import FastAPI, Response

from app.array_extensions import key_exists
from app.commands import handle_command, command, send_message
from app.forecast import send_daily_forecast
from app.secrets import get_skaping_api_key, get_telegram_api_key
from app.wispo_storage import set_location

app = FastAPI()

JSON_MEDIA_TYPE = "application/json"


@command("mountainview", "Get a mountain image")
async def handle_mountainview(bot: telegram.Bot, message: dict) -> None:
    mountain_image_data = await get_mountain_image()
    await bot.send_photo(
        chat_id=message["chat"]["id"],
        photo=mountain_image_data["medias"][0]["urls"]["large"],
        caption=mountain_image_data["medias"][0]["date"],
    )


async def get_mountain_image() -> dict:
    request_data = {
        "types": "image",
        "api_key": get_skaping_api_key(),
        "center": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "count": 1,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://api.skaping.com//media/search", data=request_data)
        return resp.json()


@app.post("/message")
async def message_stuff(request_data: dict[str, Any]) -> Response:
    print(request_data)
    message = get_message_or_update(request_data)

    if key_exists(message, "location"):
        set_location(
            message["from"]["id"],
            message["location"]["latitude"],
            message["location"]["longitude"],
        )
        return Response(status_code=202, media_type=JSON_MEDIA_TYPE)

    if not key_exists(message, "text") or not message["text"].startswith("/"):
        return Response(status_code=202, media_type=JSON_MEDIA_TYPE)

    bot = telegram.Bot(token=get_telegram_api_key())
    await handle_command(bot, message)

    return Response(status_code=202, media_type=JSON_MEDIA_TYPE)


def get_message_or_update(update: dict) -> dict:
    if key_exists(update, "edited_message"):
        return update["edited_message"]
    return update["message"]


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/forecast")
async def trigger_forecast() -> dict[str, str]:
    await send_daily_forecast()
    return {"status": "forecast sent"}
