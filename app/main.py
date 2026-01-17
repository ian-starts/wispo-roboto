from datetime import date, timedelta
from typing import Any

import httpx
import telegram
from fastapi import FastAPI, Response

from app.amy import (
    get_address,
    get_addresshotel,
    get_back,
    get_flip,
    get_manly,
    get_name,
    get_rng,
    get_travel_distance_message,
)
from app.array_extensions import key_exists
from app.forecast import send_daily_forecast
from app.joke import get_joke
from app.secrets import get_skaping_api_key, get_telegram_api_key
from app.wispo_storage import set_location

app = FastAPI()

JSON_MEDIA_TYPE = "application/json"


@app.post("/message")
async def message_stuff(request_data: dict[str, Any]) -> Response:
    print(request_data)
    request_data["message"] = get_message_or_update(request_data)

    if key_exists(request_data["message"], "location"):
        set_location(
            request_data["message"]["from"]["id"],
            request_data["message"]["location"]["latitude"],
            request_data["message"]["location"]["longitude"],
        )
        return Response(status_code=202, media_type=JSON_MEDIA_TYPE)

    if not key_exists(request_data["message"], "text") or not request_data["message"]["text"].startswith("/"):
        return Response(status_code=202, media_type=JSON_MEDIA_TYPE)

    bot = telegram.Bot(token=get_telegram_api_key())

    if "lol" in request_data["message"]["text"]:
        await send_message(bot, "lol to you, nerd!", request_data["message"]["chat"]["id"])
    elif "joke" in request_data["message"]["text"]:
        joke = await get_joke()
        await send_message(bot, joke, request_data["message"]["chat"]["id"])
    elif "mountainview" in request_data["message"]["text"]:
        mountain_image_data = await get_mountain_image()
        await send_image(
            bot,
            mountain_image_data["medias"][0]["urls"]["large"],
            request_data["message"]["chat"]["id"],
            mountain_image_data["medias"][0]["date"],
        )
    elif "rng" in request_data["message"]["text"]:
        number = get_rng(request_data["message"]["text"])
        await send_message(bot, number, request_data["message"]["chat"]["id"])
    elif "dishes" in request_data["message"]["text"]:
        name = get_name()
        text = "Today, " + name + " will be doing the dishes!! LOL loser 😙"
        await send_message(bot, text, request_data["message"]["chat"]["id"])
    elif "manly" in request_data["message"]["text"]:
        size = get_manly()
        await send_message(bot, size, request_data["message"]["chat"]["id"])
    elif "dist" in request_data["message"]["text"]:
        distance = get_travel_distance_message(request_data["message"]["from"]["id"])
        await send_message(bot, distance, request_data["message"]["chat"]["id"])
    elif "addresshotel" in request_data["message"]["text"]:
        msg = get_addresshotel()
        await send_message(bot, msg, request_data["message"]["chat"]["id"])
    elif "address" in request_data["message"]["text"]:
        msg = get_address()
        await send_message(bot, msg, request_data["message"]["chat"]["id"])
    elif "flip" in request_data["message"]["text"]:
        msg = get_flip()
        await send_message(bot, msg, request_data["message"]["chat"]["id"])
    elif "back" in request_data["message"]["text"]:
        msg = get_back()
        await send_message(bot, msg, request_data["message"]["chat"]["id"])

    return Response(status_code=202, media_type=JSON_MEDIA_TYPE)


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


async def send_message(bot: telegram.Bot, msg: str, chat_id: int) -> None:
    await bot.send_message(text=msg, chat_id=chat_id)


async def send_image(bot: telegram.Bot, photo: str, chat_id: int, caption: str) -> None:
    await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)


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
