import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6888938114:AAFCCryLloi8WBWoJEG3elZIMvZIuq8hmhY"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}! Send me a city name and I'll provide you with the current weather.")

import requests
import json
import pprint
from datetime import datetime, timedelta

def get_weather(city):
    key = "6a794ub70i1cj9kthdnngoxnjwyjr16n2wqnm523"
    manzil = f"https://www.meteosource.com/api/v1/free/point?place_id={city}&sections=current&timezone=GMT&language=en&units=metric&key={key}"
    response = requests.get(manzil)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data['current']
    else:
        raise Exception(f"Failed to get weather data, status code: {response.status_code}")

@dp.message()
async def weather_handler(message: types.Message) -> None:
    """
    This handler will receive a city name and respond with the current weather.
    """
    try:
        city = message.text.strip()
        weather = get_weather(city)
        weather_report = f"Current weather in {city.title()}:\n" \
                         f"{weather['summary']} with a temperature of {weather['temperature']}°C\n" \
                         f"Wind: {weather['wind']['speed']} m/s {weather['wind']['dir']}"
        await message.answer(weather_report)
    except Exception as e:
        await message.answer(f"Error: {e}")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())