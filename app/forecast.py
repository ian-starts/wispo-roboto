import logging
from datetime import date

import httpx
import telegram

from app.secrets import get_telegram_api_key

TELEGRAM_CHAT_ID = 402877939
SAALBACH_LAT = 47.3917
SAALBACH_LON = 12.6364

# Elevations in meters
VILLAGE_ELEVATION = 1003  # Saalbach village
MOUNTAIN_ELEVATION = 2096  # Schattberg summit


def make_forecast(village: dict, mountain: dict) -> str:
    village_temp = village["current"]["temperature_2m"]
    village_snow_m = village["current"].get("snow_depth", 0) or 0
    village_snow = village_snow_m * 100  # API returns meters, convert to cm
    village_snowfall = village["daily"]["snowfall_sum"][0] or 0
    
    mountain_temp = mountain["current"]["temperature_2m"]
    mountain_snow_m = mountain["current"].get("snow_depth", 0) or 0
    mountain_snow = mountain_snow_m * 100  # API returns meters, convert to cm
    mountain_snowfall = mountain["daily"]["snowfall_sum"][0] or 0
    
    days = (date(2026, 3, 11) - date.today()).days
    
    msg = (
        "Hi there! ⛷🏂\n\n"
        "Here is your daily weather update for Saalbach Hinterglemm:\n\n"
        f"🏘️ *Village* ({VILLAGE_ELEVATION}m)\n"
        f"  • Temperature: {village_temp}°C\n"
        f"  • Snow depth: {village_snow:.0f}cm\n"
        f"  • Fresh snow today: {village_snowfall:.1f}cm\n\n"
        f"🏔️ *Mountain* ({MOUNTAIN_ELEVATION}m)\n"
        f"  • Temperature: {mountain_temp}°C\n"
        f"  • Snow depth: {mountain_snow:.0f}cm\n"
        f"  • Fresh snow today: {mountain_snowfall:.1f}cm\n\n"
        f"Only {days} days left! ❄️"
    )
    return msg


async def get_weather_data(elevation: int) -> dict:
    params = {
        "latitude": SAALBACH_LAT,
        "longitude": SAALBACH_LON,
        "elevation": elevation,
        "current": ["temperature_2m", "snow_depth"],
        "daily": ["snowfall_sum", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "Europe/Berlin",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
        logging.info(f"Weather API response ({elevation}m): {resp.status_code}")
        return resp.json()


async def send_message(bot: telegram.Bot, msg: str, chat_id: int) -> None:
    await bot.send_message(text=msg, chat_id=chat_id)


async def send_daily_forecast() -> None:
    logging.info("Sending daily forecast")
    bot = telegram.Bot(token=get_telegram_api_key())

    village_data = await get_weather_data(VILLAGE_ELEVATION)
    mountain_data = await get_weather_data(MOUNTAIN_ELEVATION)
    await send_message(bot, make_forecast(village_data, mountain_data), TELEGRAM_CHAT_ID)
