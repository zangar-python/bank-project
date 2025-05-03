# bot.py
import asyncio
import os
import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

# Импорт Django моделей (если нужно)
# from yo.models import TelegramLog

# Токен бота
bot = Bot(token=os.getenv("8133212786:AAEI5qoZ-QEpv6CWFQP9ZBqKLQCkuLaDwxU"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я связан с Django!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
