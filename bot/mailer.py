from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
import bot.db.crud.newsletters as crud_newsletters
from bot.bot import bot


async def send_message(client: TelegramClient, chat_id: int, message: str, group_name: str):
    try:
        entity = await client.get_entity(PeerUser(chat_id))
    except:
        try:
            entity = await client.get_entity(PeerChat(chat_id))
        except:
            entity = await client.get_entity(PeerChannel(chat_id))
    try:
        await client.send_message(entity, message)
    except:
        await bot.send_message(
            chat_id=config.superadmin,
            text=f"У группы {group_name} неправильный ID. Измените его"
        )


async def sender(client: TelegramClient):
    import datetime
    active_newsletters = crud_newsletters.get_all_newsletters()
    now = datetime.datetime.now()
    shed = AsyncIOScheduler(timezone='Europe/Moscow')
    for newsletter in active_newsletters:
        if newsletter.status == 1:
            for time_ in newsletter.mailing_times.split():
                hours, minutes = map(int, time_.split(":"))
                time__ = datetime.datetime(
                    year=now.year, month=now.month, day=now.day,
                    hour=hours, minute=minutes, second=0)
                if time__ < now:
                    time__ = datetime.datetime(
                        year=now.year, month=now.month, day=now.day + 1,
                        hour=hours, minute=minutes, second=0
                    )
                shed.add_job(send_message, "date",
                             args=[client, newsletter.group_id, newsletter.text, newsletter.group_name],
                             next_run_time=time__)

    shed.start()


async def mailer():
    client = TelegramClient('anon', config.API_ID, config.API_HASH)
    client.parse_mode = "html"
    await client.start()
    await client.connect()
    await sender(client)
