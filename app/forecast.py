import logging
from datetime import date

import httpx
import telegram

from app.secrets import get_telegram_api_key, get_secret

TELEGRAM_CHAT_ID = -509915845
RESORT_ID = 333046


def get_weather_api_credentials() -> tuple[str, str]:
    app_id = get_secret("weather-api-id")
    api_key = get_secret("weather-api-key")
    return app_id, api_key


def make_forecast(resp: dict) -> str:
    forecast_today = resp["forecast"][0]
    temp_base = forecast_today["base"]["temp_c"]
    temp_top = forecast_today["upper"]["temp_c"]
    fresh_snow = (
        (
            forecast_today["base"]["freshsnow_cm"]
            + forecast_today["mid"]["freshsnow_cm"]
            + forecast_today["upper"]["freshsnow_cm"]
        )
        / 3
        // 1
    )
    snow_fall = forecast_today["snow_mm"]
    days = (date(2026, 2, 4) - date.today()).days
    msg = (
        "Hi there!\n\n"
        "Here is your daily weather update for Saalbach Hinterglemm. Todays forecast is  Currently, the temperature "
        f"ranges from {temp_base}°C at the base of the mountain to {temp_top}°C at the top. "
        f"There will be {fresh_snow:.0f}cm of fresh fresh GNARLY POWDAH today and {snow_fall}mm of snow fall.\n\n"
        f"It is only {days} days left! ⛷🏂"
    )
    return msg


async def send_message(bot: telegram.Bot, msg: str, chat_id: int) -> None:
    await bot.send_message(text=msg, chat_id=chat_id)


async def get_snow_height(resort_id: int, app_id: str, api_key: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"http://api.weatherunlocked.com/api/resortforecast/{resort_id}",
            params={"app_id": app_id, "app_key": api_key},
        )
        logging.info(resp)
        return resp.json()


async def send_daily_forecast() -> None:
    logging.info("Sending daily forecast")
    bot = telegram.Bot(token=get_telegram_api_key())

    app_id, api_key = get_weather_api_credentials()
    resp = await get_snow_height(RESORT_ID, app_id, api_key)

    await send_message(bot, make_forecast(resp), TELEGRAM_CHAT_ID)
