import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import choose_city, add_device, check_device, start, add_city

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(choose_city.router)
dp.include_router(check_device.router)
dp.include_router(add_city.router)
dp.include_router(add_device.router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())