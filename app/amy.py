import re
import random
import requests
import geopy.distance

# Je kan de namen niet opvragen in de Telegram API :(((
names = ["Joost", "Yoni", "Rutger", "AmyO", "AmyL", "Thijs", "Joshiwa", "Lenne"]


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


def get_location(message_text):
    try:
        location = re.findall(r'dist(\w+)', message_text)[0]
    except:
        return "You did not enter your text correctly. Format /dist{location} e.g. Rotterdam"

    try:
        URL = "https://geocode.search.hereapi.com/v1/geocode"
        api_key = 'fY6o1AeYGyi55iMzO9q_A1EPhcuawutvHKJSQ6Mx4dY'  # Acquire from developer.here.com
        PARAMS = {'apikey': api_key, 'q': location}

        r = requests.get(url=URL, params=PARAMS)
        data = r.json()

        latitude = data['items'][0]['position']['lat']
        longitude = data['items'][0]['position']['lng']

        car_route_url = "https://router.hereapi.com/v8/routes"
        car_route_params = {'apikey': api_key, 'transportMode': 'car', 'origin': f"{latitude},{longitude}",
                            'destination': '45.01331, 6.12471', 'return': 'summary'}
        route_req = requests.get(url=car_route_url, params=car_route_params)
        route_data = route_req.json()
        travel_time = route_data["routes"][0]["sections"][0]["summary"]["duration"] / 3600
        travel_distance = route_data["routes"][0]["sections"][0]["summary"]["length"] / 1000
        return "You are " + str(round(travel_time, 2)) + " hours and " + str(
            round(travel_distance)) + " kilometers away by car from your WISPO destination: Les Deux Alpes ⛷️🏂"

    except:
        return "You did not enter a existing location. Format /dist{location} e.g. Rotterdam"
