from flask import Flask,request, Response
from datetime import date
import requests
import telegram
from app.joke import get_joke

app = Flask(__name__)

TELEGRAM_API_KEY = "2120742951:AAF308uoeBHAhOASiVlBBNK8VQskGfeVLbY"


@app.route("/message", methods=["post"])
def message_stuff():
    bot = telegram.Bot(token=TELEGRAM_API_KEY)
    request_data = request.get_json()
    print(request_data)
    if 'lol' in request_data['message']['text']:
        send_message(bot, "lol to you, nerd!",request_data['message']['chat']['id'])
    if "joke" in request_data["message"]["text"]:
        joke = get_joke()
        send_message(bot, joke, request_data["message"]["chat"]["id"])
    if 'mountainview' in request_data['message']['text']:
        send_image(bot, get_mountain_image() ,request_data['message']['chat']['id'])
    return Response("", status=202, mimetype='application/json')


def get_mountain_image():
    request_data = {
            'types': 'image',
            'api_key': 'wJYTf-gyLNX-tk7ll-cGviT',
            'center': (date.today() + date.timedelta(days=1)).strftime('%Y-%m-%d'),
            'count' : 1
        }
    resp = requests.post(
        "https://api.skaping.com//media/search",data=request_data)
    return resp["medias"][0]["urls"]["large"]

def send_message(bot: telegram.Bot, msg: str, chat_id: int):
    bot.send_message(text=msg, chat_id=chat_id)

def send_image(bot: telegram.Bot, photo: str, chat_id: int):
    bot.send_photo(chat_id=chat_id, photo=photo)