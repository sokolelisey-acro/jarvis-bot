import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.routers import router

load_dotenv()
token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)

async def main():
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

