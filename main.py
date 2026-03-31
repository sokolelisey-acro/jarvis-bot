import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers.routers import router

async def main():
    # Берем токен напрямую из переменных окружения Render
    token = os.environ.get("BOT_TOKEN")
    
    if not token:
        print("ОШИБКА: Токен не найден в Environment Variables!")
        return

    bot = Bot(token=token)
    dp = Dispatcher()
    
    # Подключаем логику Джарвиса
    dp.include_router(router)
    
    print("Системы Джарвиса активны. Поллинг запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"КРИТИЧЕСКИЙ СБОЙ: {e}")
