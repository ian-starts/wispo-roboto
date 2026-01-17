import random
import re

import requests

from app.secrets import get_here_api_key
from app.wispo_storage import get_location

names = ["Amy", "Yoni", "Rutger", "Irene", "Tijs"]


def get_rng(message_text: str) -> str:
    if message_text == "rng":
        output = "please use this function as follows: rng{number}, for the random number generator"
    elif "rng" in message_text:
        try:
            new = re.findall(r"rng(\w+)", message_text)[0]
            components = re.split(r"(\d+)", new)
            output = "The magic number is : " + str(
                random.randint(1, [int(word) for word in components if word.isdigit()][0])
            )
        except Exception:
            output = "You are probably doing something wrong, you fool. Format: rng{number}"
    else:
        output = "yeeez, just use it the way you are supposed to, idiot. Format: rng{number}"
    return output


def get_name() -> str:
    return random.choice(names)


def get_manly() -> str:
    nmb = random.randint(1, 30)
    return "8" + nmb * "=" + "D"


def get_flip() -> str:
    return "(╯°□°)╯︵ ┻━┻"


def get_back() -> str:
    return "┬─┬ノ( º _ ºノ)"


def get_travel_distance_message(user_id: int) -> str:
    try:
        api_key = get_here_api_key()
        location = get_location(user_id)
        car_route_url = "https://router.hereapi.com/v8/routes"
        car_route_params = {
            "apikey": api_key,
            "transportMode": "car",
            "origin": f"{location['lat']},{location['long']}",
            "destination": "47.3917, 12.6364",
            "return": "summary",
        }
        route_req = requests.get(url=car_route_url, params=car_route_params, timeout=30)
        route_data = route_req.json()
        travel_time = route_data["routes"][0]["sections"][0]["summary"]["duration"] / 3600
        travel_distance = route_data["routes"][0]["sections"][0]["summary"]["length"] / 1000
        return (
            "You are "
            + str(round(travel_time, 2))
            + " hours and "
            + str(round(travel_distance))
            + " kilometers away by car from your WISPO destination: Saalbach Hinterglemm ⛷️🏂"
        )
    except Exception:
        return "Something went fucky, did you share your location with me?"


def get_address() -> str:
    return "Chalet Alpina, Place de Venosc, 38860 Les Deux Alpes - France"


def get_addresshotel() -> str:
    return "4 Allee Du Chanoine Drioton, Nancy, 54000, France"


def get_packlist():
    return None
