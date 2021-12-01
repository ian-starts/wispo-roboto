from datetime import date

import requests
import telegram

# https://developer.weatherunlocked.com/documentation/skiresort/resources#response-fields
TELEGRAM_API_KEY = "2120742951:AAF308uoeBHAhOASiVlBBNK8VQskGfeVLbY"
TELEGRAM_CHAT_ID = -509915845
WEATHER_API_KEY = "b70d028fde6bce370cd3e58d5e428e86"
WEATHER_API_ID = "e4f7f0bf"
RESORT_ID = 333010


def make_forcast(resp: dict) -> str:
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
    days = (date(2022, 1, 14) - date.today()).days
    msg = (
        "Hi there!\n\n"
        "Here is your daily weather update for Les Deux Alpes. Todays forecast is  Currently, the temperature "
        f"ranges from {temp_base}°C at the base of the mountain to {temp_top}°C at the top. "
        f"There will be {fresh_snow:.0f}cm of fresh fresh GNARLY POWDAH today and {snow_fall}mm of snow fall.\n\n"
        f"It is only {days} days left! ⛷🏂"
    )

    if (days - 30) <= 5 and (days-30) > 0:
        msg += 2*"\n"
        msg += f"❗️❗️HEADS-Up❗️❗️ The cancelation fee will be raised in {days-30} days!"

    return msg


def send_message(bot: telegram.Bot, msg: str, chat_id: int):
    bot.send_message(text=msg, chat_id=chat_id)


def get_snow_height(resort_id: int, app_id: int, api_key: str) -> dict:
    resp = requests.get(
        "http://api.weatherunlocked.com/"
        f"api/resortforecast/{resort_id}?app_id={app_id}&app_key={api_key}"
    )
    return resp


def main():
    bot = telegram.Bot(token=TELEGRAM_API_KEY)

    resp = get_snow_height(RESORT_ID, WEATHER_API_ID, WEATHER_API_KEY)

    send_message(bot, make_forcast(resp.json()), TELEGRAM_CHAT_ID)


if __name__ == "__main__":
    main()
