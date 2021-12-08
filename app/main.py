from flask import Flask, request, Response
from datetime import date, timedelta
import requests
import telegram
from app.joke import get_joke
from app.wispo_redis import set_location
from app.amy import get_manly, get_name, get_rng, get_location
from app.array_extensions import key_exists

app = Flask(__name__)

TELEGRAM_API_KEY = "2120742951:AAF308uoeBHAhOASiVlBBNK8VQskGfeVLbY"


@app.route("/message", methods=["post"])
def message_stuff():
    request_data = request.get_json()
    print(request_data)
    request_data['message'] = get_message_or_update(request_data)

    # check if the message has a location
    if key_exists(request_data['message'], 'location'):
        set_location(request_data['message']['from']['id'], request_data['message']['location']['latitude'],
                     request_data['message']['location']['longitude'])
        return Response("", status=202, mimetype='application/json')

    # if not, check if it's a command
    if not key_exists(request_data['message'], 'text') or not request_data['message']['text'].startswith("/"):
        return Response("", status=202, mimetype='application/json')
    bot = telegram.Bot(token=TELEGRAM_API_KEY)

    # Do commands
    if 'lol' in request_data['message']['text']:
        send_message(bot, "lol to you, nerd!", request_data['message']['chat']['id'])
    elif "joke" in request_data["message"]["text"]:
        joke = get_joke()
        send_message(bot, joke, request_data["message"]["chat"]["id"])
    elif 'mountainview' in request_data['message']['text']:
        mountain_image_data = get_mountain_image()
        send_image(bot, mountain_image_data["medias"][0]["urls"]["large"], request_data['message']['chat']['id'],
                   mountain_image_data["medias"][0]["date"])
    elif "rng" in request_data['message']['text']:
        number = get_rng(request_data['message']['text'])
        send_message(bot, number, request_data["message"]["chat"]["id"])
    elif "dishes" in request_data['message']['text']:
        name = get_name()
        text = "Today, " + name + " will be doing the dishes!! LOL loser 😙"
        send_message(bot, text, request_data["message"]["chat"]["id"])
    elif "size" in request_data['message']['text']:
        size = get_manly()
        send_message(bot, size, request_data['message']['chat']['id'])
    elif "dist" in request_data['message']['text']:
        distance = get_location(request_data['message']['from']['id'])
        send_message(bot, distance, request_data['message']['chat']['id'])
    return Response("", status=202, mimetype='application/json')


def get_mountain_image():
    request_data = {
        'types': 'image',
        'api_key': 'wJYTf-gyLNX-tk7ll-cGviT',
        'center': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'count': 1
    }
    resp = requests.post(
        "https://api.skaping.com//media/search", data=request_data).json()
    return resp


def send_message(bot: telegram.Bot, msg: str, chat_id: int):
    bot.send_message(text=msg, chat_id=chat_id)


def send_image(bot: telegram.Bot, photo: str, chat_id: int, caption: str):
    bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)


def get_message_or_update(update):
    message = None
    if key_exists(update, 'edited_message'):
        message = update['edited_message']
    else:
        message = update['message']
    return message
