import asyncio
import base64
import logging
import os
import random
import re
import string 
import string as rohit
import time
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from plugins.autoDelete import auto_del_notification, delete_message
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from plugins.FORMATS import *
from database.database import db
from config import *
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from datetime import datetime, timedelta
from pytz import timezone

            
        
                   
@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    owner_id = is_admin  # Fetch the owner's ID from config

    # Check if the user is the owner
    if id == owner_id:
        # Owner-specific actions
        # You can add any additional actions specific to the owner here
        await message.reply("You are the owner! Additional actions can be added here.")

    else:
        if not await db.present_user(id):
            try:
                await db.add_user(id)
            except:
                pass

        verify_status = await db.get_verify_status(id)
        if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await db.update_verify_status(id, is_verified=False)

        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                return await message.reply("Your token is invalid or Expired. Try again by clicking /start")
            await db.update_verify_status(id, is_verified=True, verified_time=time.time())
            if verify_status["link"] == "":
                reply_markup = None
            await message.reply(f"Your token successfully verified and valid for: 24 Hour", reply_markup=reply_markup, protect_content=False, quote=True)

        elif len(message.text) > 7 and verify_status['is_verified']:
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start, end+1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return
            temp_msg = await message.reply("```こんにちは ❤```")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()

            AUTO_DEL, DEL_TIMER, HIDE_CAPTION, CHNL_BTN, PROTECT_MODE = await asyncio.gather(
                db.get_auto_delete(), db.get_del_timer(), db.get_hide_caption(), db.get_channel_button(), db.get_protect_content()
            )
            if CHNL_BTN:
                button_name, button_link = await db.get_channel_button_link()

            for idx, msg in enumerate(messages):
                original_caption = msg.caption.html if msg.caption else ""
                if CUSTOM_CAPTION and msg.document:
                    caption = CUSTOM_CAPTION.format(previouscaption=original_caption, filename=msg.document.file_name)
                elif HIDE_CAPTION and (msg.document or msg.audio):
                    caption = f"{original_caption}\n\n{CUSTOM_CAPTION}"
                else:
                    caption = original_caption

                if CHNL_BTN:
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=button_name, url=button_link)]]) if (msg.document or msg.photo or msg.video or msg.audio) else None
                else:
                    reply_markup = msg.reply_markup

                try:
                    copied_msg = await msg.copy(chat_id=id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_MODE)
                    await asyncio.sleep(0.1)

                    if AUTO_DEL:
                        asyncio.create_task(delete_message(copied_msg, DEL_TIMER))
                        if idx == len(messages) - 1:
                            last_message = copied_msg

                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    copied_msg = await msg.copy(chat_id=id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_MODE)
                    await asyncio.sleep(0.1)

                    if AUTO_DEL:
                        asyncio.create_task(delete_message(copied_msg, DEL_TIMER))
                        if idx == len(messages) - 1:
                            last_message = copied_msg

            if AUTO_DEL and last_message:
                asyncio.create_task(auto_del_notification(client.username, last_message, DEL_TIMER, message.command[1]))

        elif verify_status['is_verified']:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("About Me", callback_data="about"),
                  InlineKeyboardButton("Close", callback_data="close")]]
            )
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
            message_effect_id=5104841245755180586  # 🔥
        )

        else:
            verify_status = await db.get_verify_status(id)
            if not verify_status['is_verified']:
                short_url = f"api.shareus.io"
                full_tut_url = f"https://t.me/neprosz/3"
                token = ''.join(random.choices(rohit.ascii_letters + string.digits, k=10))
                await db.update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_API_URL, SHORTLINK_API_KEY,f'https://telegram.dog/{client.username}?start=verify_{token}')
                btn = [
                [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 😉", url=link),
                InlineKeyboardButton('ᴛᴜᴛᴏʀɪᴀʟ 🥰', url=TUT_VID)],
                [InlineKeyboardButton("ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ 😎", callback_data="buy_prem")]
                ]
                await message.reply(f"<blockquote>Your Ads token is expired, refresh your token and try again.</blockquote>\n\n<blockquote>Token Timeout: {get_exp_time(VERIFY_EXPIRE)}</blockquote>\n\n<blockquote>What is the token?</blockquote>\n\n<blockquote>This is an ads token. If you pass 1 ad, you can use the bot for 10 Mins after passing the ad.</blockquote>", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)

    
#=====================================================================================#

WAIT_MSG = """<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message without any spaces.</code>"""

#=====================================================================================#

# Create a global dictionary to store chat data
chat_data_cache = {}

@Bot.on_message(filters.command('start') & filters.private & ~banUser)
async def not_joined(client: Client, message: Message):
    temp = await message.reply(f"<b>??</b>")

    user_id = message.from_user.id

    REQFSUB = await db.get_request_forcesub()
    buttons = []
    count = 0

    try:
        for total, chat_id in enumerate(await db.get_all_channels(), start=1):
            await message.reply_chat_action(ChatAction.PLAYING)

            # Show the join button of non-subscribed Channels.....
            if not await is_userJoin(client, user_id, chat_id):
                try:
                    # Check if chat data is in cache
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]  # Get data from cache
                    else:
                        data = await client.get_chat(chat_id)  # Fetch from API
                        chat_data_cache[chat_id] = data  # Store in cache

                    cname = data.title

                    # Handle private channels and links
                    if REQFSUB and not data.username: 
                        link = await db.get_stored_reqLink(chat_id)
                        await db.add_reqChannel(chat_id)

                        if not link:
                            link = (await client.create_chat_invite_link(chat_id=chat_id, creates_join_request=True)).invite_link
                            await db.store_reqLink(chat_id, link)
                    else:
                        link = data.invite_link

                    # Add button for the chat
                    buttons.append([InlineKeyboardButton(text=cname, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Can't Export Channel Name and Link..., Please Check If the Bot is admin in the FORCE SUB CHANNELS:\nProvided Force sub Channel:- {chat_id}")
                    return await temp.edit(f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @JeffySama</i></b>\n<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")

        try:
            buttons.append([InlineKeyboardButton(text='♻️ Tʀʏ Aɢᴀɪɴ', url=f"https://t.me/{client.username}?start={message.command[1]}")])
        except IndexError:
            pass

        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
    message_effect_id=5104841245755180586  # Add the effect ID here
        )
    except Exception as e:
        print(f"Error: {e}")  # Print the error message for debugging
        # Optionally, send an error message to the user or handle further actions here
        await temp.edit(f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @rohit_1888</i></b>\n<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")
    
@Bot.on_message(filters.command('ch2l') & filters.private)
async def gen_link_encoded(client: Bot, message: Message):
    try:
        hash = await client.ask(text="Enter the code here... \n /cancel to cancel the operation",chat_id = message.from_user.id, timeout=60)
    except Exception as e:
        print(e)
        await hash.reply(f"<blockquote>😔 some error occurred {e}</blockquote>")
        return
    if hash.text == "/cancel":
        await hash.reply("<blockquote>Cancelled 😉!</blockquote>")
        return
    link = f"https://t.me/{client.username}?start={hash.text}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🎉 Click Here ", url=link)]])
    await hash.reply_text(f"<b>🧑‍💻 Here is your generated link", quote=True, reply_markup=reply_markup)
    return
        

@Bot.on_message(filters.command('users') & filters.private & is_admin)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & is_admin)
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await db.full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time ⌚</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await db.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed 🟢</u>
                
                Total Users: <code>{total}</code>
                Successful: <code>{successful}</code>
                Blocked Users: <code>{blocked}</code>
                Deleted Accounts: <code>{deleted}</code>
                Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
    return

@Bot.on_message(filters.command('auth') & filters.private)
async def auth_command(client: Bot, message: Message):
    await client.send_message(
        chat_id=OWNER_ID,
        text=f"Message for @{OWNER_TAG}\n<code>{message.from_user.id}</code>\n/add_admin <code>{message.from_user.id}</code> 🤫",
    )

    await message.reply("<blockquote>Please wait for verification from the owner. 🫣</blockquote>")
    return



@Bot.on_message(filters.command('ping')  & filters.private)
async def check_ping_command(client: Bot, message: Message):
    start_t = time.time()
    rm = await message.reply_text("<blockquote>Pinging....</blockquote>", quote=True)
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"<blockquote>Ping 🔥!</blockquote>\n<blockquote>{time_taken_s:.3f} ms</blockquote>")
    return


@Bot.on_message(filters.private & filters.command('restart') & filters.user(OWNER_ID))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i><blockquote>Trying To Restarting.....</blockquote></i>",
        quote=True
    )
    await asyncio.sleep(5)
    await msg.edit("<i>Server Restarted Successfully ✅</i>")
    try:
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        print(e)

@Bot.on_message(filters.command('add_prem') & filters.private & is_admin)
async def add_user_premium_command(client: Bot, message: Message):
    # Prompt the admin to input the user ID
    while True:
        try:
            user_id_message = await client.ask(
                text="<blockquote>Enter the ID of the user \n/cancel to cancel:</blockquote>", 
                chat_id=message.from_user.id, 
                timeout=60
            )
        except Exception as e:
            print(e)
            return  # Exit if there's an error (e.g., timeout)

        if user_id_message.text == "/cancel":
            await client.send_message(chat_id=message.chat.id, text="<blockquote>Cancelled 😉!</blockquote>")  # Notify about the cancellation
            return

        try:
            await Bot.get_users(user_ids=user_id_message.text, self=client)
            break  # Exit the loop if the user ID is valid
        except:
            await client.send_message(
                chat_id=message.chat.id, 
                text="<blockquote>❌ Error 😖\n\nThe user ID is incorrect.</blockquote>"  # Notify about the error
            )
            continue

    user_id = int(user_id_message.text)  # Extract the user ID

    # Prompt the admin to choose the premium duration
    while True:
        try:
            timeforprem_message = await client.ask(
                text=(
                    "<blockquote>Enter the duration for the premium subscription:\n"
                    "Choose correctly, as it's not reversible.\n\n"
                    "⁕ <code>1</code> for 7 days\n"
                    "⁕ <code>2</code> for 1 Month\n"
                    "⁕ <code>3</code> for 3 Months\n"
                    "⁕ <code>4</code> for 6 Months\n"
                    "⁕ <code>5</code> for 1 Year 🤑</blockquote>"
                ), 
                chat_id=message.from_user.id, 
                timeout=60
            )
        except Exception as e:
            print(e)
            return  # Exit if there's an error (e.g., timeout)

        if not int(timeforprem_message.text) in [1, 2, 3, 4, 5]:
            await client.send_message(chat_id=message.chat.id, text="You have given an incorrect input. 😖")
            continue
        else:
            break

    timeforprem = int(timeforprem_message.text)

    # Map the input to a readable duration string
    timestring = {
        1: "7 days",
        2: "1 month",
        3: "3 months",
        4: "6 months",
        5: "1 year"
    }[timeforprem]

    # Attempt to update the user's premium status
    try:
        await increasepremtime(user_id, timeforprem)  # Update the database/backend
        await client.send_message(chat_id=message.chat.id, text="<blockquote>Premium added! 🤫</blockquote>")  # Notify the admin

        # Notify the target user
        await client.send_message(
            chat_id=user_id,
            text=f"<blockquote>Update for you\n\nPremium plan of {timestring} has been added to your account. 🤫</blockquote>"
        )
    except Exception as e:
        print(e)
        await client.send_message(
            chat_id=message.chat.id, 
            text="<blockquote>Some error occurred.\nCheck logs.. 😖\nIf the user received the premium message, then it's okay.</blockquote>"
        )
