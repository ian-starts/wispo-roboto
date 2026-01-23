from dataclasses import dataclass
from typing import Callable, Awaitable

import telegram

from app.mother_of_all_file import (
    get_address,
    get_addresshotel,
    get_back,
    get_flip,
    get_manly,
    get_mansplain,
    get_name,
    get_rng,
)
from app.joke import get_joke

CommandHandler = Callable[[telegram.Bot, dict], Awaitable[None]]


@dataclass
class Command:
    name: str
    description: str
    handler: CommandHandler


COMMANDS: dict[str, Command] = {}


def command(name: str, description: str):
    def decorator(func: CommandHandler) -> CommandHandler:
        COMMANDS[name] = Command(name=name, description=description, handler=func)
        return func
    return decorator


async def send_message(bot: telegram.Bot, msg: str, chat_id: int) -> None:
    await bot.send_message(text=msg, chat_id=chat_id)


def generate_help_message() -> str:
    lines = ["🤖 *Available Commands*\n"]
    for cmd in COMMANDS.values():
        lines.append(f"/{cmd.name} - {cmd.description}")
    return "\n".join(lines)


@command("help", "Show all available commands")
async def handle_help(bot: telegram.Bot, message: dict) -> None:
    help_text = generate_help_message()
    await bot.send_message(
        text=help_text,
        chat_id=message["chat"]["id"],
        parse_mode="Markdown",
    )


@command("lol", "Get a lol response")
async def handle_lol(bot: telegram.Bot, message: dict) -> None:
    await send_message(bot, "lol to you, nerd!", message["chat"]["id"])


@command("joke", "Get joke of the day")
async def handle_joke(bot: telegram.Bot, message: dict) -> None:
    joke = await get_joke()
    await send_message(bot, joke, message["chat"]["id"])


@command("rng", "Random number generator (usage: /rng{number})")
async def handle_rng(bot: telegram.Bot, message: dict) -> None:
    number = get_rng(message["text"])
    await send_message(bot, number, message["chat"]["id"])


@command("dishes", "Pick someone to do the dishes")
async def handle_dishes(bot: telegram.Bot, message: dict) -> None:
    name = get_name()
    text = f"Today, {name} will be doing the dishes!! LOL loser 😙"
    await send_message(bot, text, message["chat"]["id"])


@command("manly", "Generate a... size indicator")
async def handle_manly(bot: telegram.Bot, message: dict) -> None:
    size = get_manly()
    await send_message(bot, size, message["chat"]["id"])


@command("addresshotel", "Get the hotel address")
async def handle_addresshotel(bot: telegram.Bot, message: dict) -> None:
    await send_message(bot, get_addresshotel(), message["chat"]["id"])


@command("address", "Get the WISPO address")
async def handle_address(bot: telegram.Bot, message: dict) -> None:
    await send_message(bot, get_address(), message["chat"]["id"])


@command("flip", "Flip a table")
async def handle_flip(bot: telegram.Bot, message: dict) -> None:
    await send_message(bot, get_flip(), message["chat"]["id"])


@command("back", "Put the table back")
async def handle_back(bot: telegram.Bot, message: dict) -> None:
    await send_message(bot, get_back(), message["chat"]["id"])


@command("mansplain", "Get a mansplain")
async def handle_mansplain(bot: telegram.Bot, message: dict) -> None:
    await send_message(bot, get_mansplain(), message["chat"]["id"])

async def handle_command(bot: telegram.Bot, message: dict) -> bool:
    text = message.get("text", "")
    for cmd_name, cmd in COMMANDS.items():
        if cmd_name in text:
            await cmd.handler(bot, message)
            return True
    return False
