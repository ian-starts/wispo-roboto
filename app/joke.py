import json

import requests


def get_joke():
    url = "https://api.jokes.one/jod"

    response = requests.request("GET", url)

    response = json.loads(response.text)

    title = response["contents"]["jokes"][0]["joke"]["title"]
    text = response["contents"]["jokes"][0]["joke"]["text"]

    return f"{title}\n\n{text}\n🤣🤣🤣"
