from flask import Flask,request, Response
import requests
import telegram

app = Flask(__name__)

TELEGRAM_API_KEY = "2120742951:AAF308uoeBHAhOASiVlBBNK8VQskGfeVLbY"
 
@app.route("/message", methods=['post'])
def message_stuff():
    bot = telegram.Bot(token=TELEGRAM_API_KEY)
    request_data = request.get_json()
    print(request_data)
    if ('lol' in request_data['message']['text']):
        send_message(bot, "lol to you, nerd!",request_data['message']['chat']['id'])
    return Response("", status=202, mimetype='application/json')


def send_message(bot: telegram.Bot, msg: str, chat_id: int):
    bot.send_message(text=msg, chat_id=chat_id)