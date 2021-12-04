import re
import random
import requests
import geopy.distance

# Je kan de namen niet opvragen in de Telegram API :(((
names = ["Joost", "Yoni", "Rutger", "AmyO", "AmyL", "Thijs", "Joshiwa", "Lenne"]


def get_rng(input):
    if input == "rng":
        output = "please use this function as follows: rng{number}, for the random number generator"
    elif "rng" in input:
        try:
            new = re.findall(r'rng(\w+)', input)[0]
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


def get_location(input):
    try:
        location = re.findall(r'dist(\w+)', input)[0]
    except:
        output = "You did not enter your text correctly. Format /dist{location} e.g. Rotterdam"

    try:
        URL = "https://geocode.search.hereapi.com/v1/geocode"
        api_key = '91Rke_Qm2yDiF-zEvHEJfN9-U0FKeK4bjF4I2S1Je7A'  # Acquire from developer.here.com
        PARAMS = {'apikey': api_key, 'q': location}

        r = requests.get(url=URL, params=PARAMS)
        data = r.json()

        latitude = data['items'][0]['position']['lat']
        longitude = data['items'][0]['position']['lng']
        coords_1 = (latitude, longitude)
        coords_2 = (45.01331, 6.12471)  # coord les deux alpes

        output = "You are " + str(round(geopy.distance.distance(coords_1,
                                                                coords_2).km)) + " kilometers away from your WISPO destination: Les Deux Alpes ⛷️🏂"

    except:
        output = "You did not enter a existing location. Format /dist{location} e.g. Rotterdam"

    return output
