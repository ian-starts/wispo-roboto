from flask import Flask,request
import requests
import telegram

app = Flask(__name__)

TELEGRAM_API_KEY = "2120742951:AAF308uoeBHAhOASiVlBBNK8VQskGfeVLbY"
TELEGRAM_CHAT_ID = -509915845
WEATHER_API_KEY = "b70d028fde6bce370cd3e58d5e428e86"
WEATHER_API_ID = "e4f7f0bf"
RESORT_ID = 333010
 
@app.route("/message", methods=['post'])
def message_stuff():
    bot = telegram.Bot(token=TELEGRAM_API_KEY)
    request_data = request.get_json()
    if ('lol' in request_data['message']['text']):
        send_message(bot, "lol to you, nerd!",request_data['message']['chat']['id'])


def send_message(bot: telegram.Bot, msg: str, chat_id: int):
    bot.send_message(text=msg, chat_id=chat_id)