import httpx


async def get_joke() -> str:
    url = "https://api.jokes.one/jod"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    title = data["contents"]["jokes"][0]["joke"]["title"]
    text = data["contents"]["jokes"][0]["joke"]["text"]

    return f"{title}\n\n{text}\n🤣🤣🤣"
