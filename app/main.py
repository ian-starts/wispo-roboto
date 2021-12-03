from flask import Flask,request, Response
from datetime import date, timedelta
import requests
import telegram
from app.joke import get_joke
from app.amy import get_manly, get_name, get_rng

app = Flask(__name__)

TELEGRAM_API_KEY = "2120742951:AAF308uoeBHAhOASiVlBBNK8VQskGfeVLbY"


@app.route("/message", methods=["post"])
def message_stuff():
    bot = telegram.Bot(token=TELEGRAM_API_KEY)
    request_data = request.get_json()
    print(request_data)
    if 'lol' in request_data['message']['text']:
        send_message(bot, "lol to you, nerd!",request_data['message']['chat']['id'])
    elif "joke" in request_data["message"]["text"]:
        joke = get_joke()
        send_message(bot, joke, request_data["message"]["chat"]["id"])
    elif 'mountainview' in request_data['message']['text']:
        mountain_image_data = get_mountain_image()
        send_image(bot, mountain_image_data["medias"][0]["urls"]["large"], request_data['message']['chat']['id'], mountain_image_data["medias"][0]["date"])
    elif "rng" in request_data['message']['text']:
        number = get_rng(request_data['message']['text'])
        send_message(bot, number, request_data["message"]["chat"]["id"])
    elif "dishes" in request_data['message']['text']:
        name = get_name()
        text = "Today, " + name + " will be doing the dishes!! LOL loser 😙" 
        send_message(bot, text, request_data["message"]["chat"]["id"])
    elif "size" in request_data['message']['text']:
        size = get_manly()
        send_message(bot, size,request_data['message']['chat']['id'])
    return Response("", status=202, mimetype='application/json')


def get_mountain_image():
    request_data = {
            'types': 'image',
            'api_key': 'wJYTf-gyLNX-tk7ll-cGviT',
            'center': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'count' : 1
        }
    resp = requests.post(
        "https://api.skaping.com//media/search",data=request_data).json()
    return resp

def send_message(bot: telegram.Bot, msg: str, chat_id: int):
    bot.send_message(text=msg, chat_id=chat_id)

def send_image(bot: telegram.Bot, photo: str, chat_id: int, caption: str):
    bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)