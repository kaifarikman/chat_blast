from aiogram import Dispatcher

from bot.bot import bot
from bot.handlers import router

import logging
import sys
import asyncio

import bot.db.db as db
import bot.mailer as mailer
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main():
    db.create_tables()
    dp = Dispatcher()
    dp.include_router(router)
    shed = AsyncIOScheduler(timezone='Europe/Moscow')
    shed.add_job(mailer.mailer, "cron", hour=10, minute=0, second=0)
    shed.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except Exception as exception:
        print(f"Exit - {exception}!")
