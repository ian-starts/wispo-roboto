import re
import random
import requests
from app.wispo_storage import get_location

# Je kan de namen niet opvragen in de Telegram API :(((
names = ["Amy", "Yoni", "Rutger", "Irene", "Tijs"]


def get_rng(message_text):
    if message_text == "rng":
        output = "please use this function as follows: rng{number}, for the random number generator"
    elif "rng" in message_text:
        try:
            new = re.findall(r'rng(\w+)', message_text)[0]
            components = re.split('(\d+)', new)
            output = "The magic number is : " + str(
                random.randint(1, [int(word) for word in components if word.isdigit()][0]))
        except:
            output = "You are probably doing something wrong, you fool. Format: rng{number}"
    else:
        output = "yeeez, just use it the way you are supposed to, idiot. Format: rng{number}"
    return output


def get_name():
    return random.choice(names)


def get_manly():
    nmb = random.randint(1, 30)
    return ("8" + nmb * '=' + "D")


def get_flip():
    return '(╯°□°)╯︵ ┻━┻'


def get_back():
    return '┬─┬ノ( º _ ºノ)'


def get_travel_distance_message(user_id):
    try:
        api_key = 'fY6o1AeYGyi55iMzO9q_A1EPhcuawutvHKJSQ6Mx4dY'
        location = get_location(user_id)
        car_route_url = "https://router.hereapi.com/v8/routes"
        car_route_params = {'apikey': api_key, 'transportMode': 'car', 'origin': f"{location['Lat']},{location['Long']}",
                            'destination': '47.23179, 11.88093', 'return': 'summary'}
        route_req = requests.get(url=car_route_url, params=car_route_params)
        print(route_req)
        route_data = route_req.json()
        travel_time = route_data["routes"][0]["sections"][0]["summary"]["duration"] / 3600
        travel_distance = route_data["routes"][0]["sections"][0]["summary"]["length"] / 1000
        return "You are " + str(round(travel_time, 2)) + " hours and " + str(
            round(travel_distance)) + " kilometers away by car from your WISPO destination: Zell am Ziller ⛷️🏂"
    except:
        return "Something went fucky, did you share your location with me?"


def get_address():
    msg = "Chalet Alpina, Place de Venosc, 38860 Les Deux Alpes - France"
    return msg


def get_addresshotel():
    msg = "4 Allee Du Chanoine Drioton, Nancy, 54000, France"
    return msg


def get_packlist():
    # TO DO
    return None
