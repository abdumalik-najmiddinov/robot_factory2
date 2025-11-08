from aiogram import types, Bot, Dispatcher, F
import asyncio
from aiogram.filters import Command
from environs import Env

env = Env()
env.read_env()

API_TOKEN = env.str("API_TOKEN")
CHAT_ID = env.str("CHAT_ID")
WEBHOOK_URL = env.str("WEBHOOK_URL")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()



@dp.message(Command("start"))
async def send_message(message: types.Message):
    await message.answer(text="Salom Alini botiga xush kelibsiz")


async def setup_webhook():
    await bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True)

