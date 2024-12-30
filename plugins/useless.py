from bot import Bot
from pyrogram.types import Message
from pyrogram import filters, Client
from config import *
from datetime import datetime
from helper_func import *
from pytz import timezone

@Bot.on_message(filters.command('stats') & is_admin)
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))



