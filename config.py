from operator import add
import os
import logging


# import dotenv
# dotenv.load_dotenv()


from logging.handlers import RotatingFileHandler

#bot stats
BOT_STATS_TEXT = os.environ.get("BOTS_STATS_TEXT","<blockquote><b>BOT UPTIME 🍀</b>\n{uptime}</blockquote>")
#send custom message when user interact with bot
USER_REPLY_TEXT = os.environ.get("USER_REPLY_TEXT", "<blockquote>ᴀʀᴀ!! ᴀʀᴀ!! ɪᴀᴍ ᴏɴʟʏ ᴡᴏʀᴋ ғᴏʀ ᴍʏ ʟᴏᴠᴇʟʏ ᴋᴀᴡᴀɪɪ 🥰 @JeffreySama !</blockquote>")

#your bot token here from https://telegram.me/BotFather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7412999973:AAHqBRopFlP8EQqddjM2lKJXzOtSHdqSDE4") 
#your api id from https://my.telegram.org/apps
APP_ID = int(os.environ.get("APP_ID", "28744454"))
#your api hash from https://my.telegram.org/apps
API_HASH = os.environ.get("API_HASH", "debd37cef0ad1a1ce45d0be8e8c3c5e7")
#your channel_id from https://t.me/MissRose_bot by forwarding dummy message to rose and applying command `/id` in reply to that message
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002477730488"))
#your id of telegram can be found by https://t.me/MissRose_bot with '/id' command
OWNER_ID = int(os.environ.get("OWNER_ID", "6266529037"))
#port set to default 8080
PORT = os.environ.get("PORT", "8080")
#your database url mongodb only You can use mongo atlas free cloud database
DB_URL = os.environ.get("DB_URL", "mongodb+srv://jeffysamaweekends:jeffysamaweekends@cluster0.ulyfw.mongodb.net/?retryWrites=true&w=majority")
#your database name
DB_NAME = os.environ.get("DB_NAME", "WeekendsMovie1")

#for creating telegram thread for bot to improve performance of the bot
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "60"))
#your start default command message.
START_MSG = os.environ.get("START_MESSAGE", "ᴋᴏɴɪᴄʜɪᴡᴀ {mention}\n\n<blockquote>ᴋᴏɴɪᴄʜɪᴡᴀ ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴀɴɪᴍᴇ/ᴍᴏᴠɪᴇ ғɪʟᴇs ɪɴ @Anime_Weekends ᴄʜᴀɴɴᴇʟ  ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.</blockquote>")
#your telegram tag without @
OWNER_TAG = os.environ.get("OWNER_TAG", "JeffySama")


#Shortner (token system) 
"""
some token verification sites
https://dashboard.shareus.io/
"""


# only shareus service known rightnow rest you can test on your own
SHORTLINK_API_URL = os.environ.get("SHORTLINK_API_URL", "shortxlinks.com")
# SHORTLINK_API_KEY = os.environ.get("SHORTLINK_API_KEY", "")
#use this key if not working ☠️ (jokin!!)
SHORTLINK_API_KEY = os.environ.get("SHORTLINK_API_KEY", "bea2b83467261cec3b811d76a9bd84533234219a")
#add your custom time in secs for shortlink expiration.
# 24hr = 86400
# 12hr = 43200
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', "600")) # Add time in seconds

#Tutorial video for the user of your shortner on how to download.
TUT_VID = os.environ.get("TUT_VID","https://t.me/How_to_Download_7x/32")


START_PIC = os.environ.get("START_PIC", "https://envs.sh/oV8.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://envs.sh/oVJ.jpg")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<blockquote><b>ʙʏ @Anime_Weekends</b></blockquote>")

#Collection of pics for Bot // #Optional but atleast one pic link should be replaced if you don't want predefined links
PICS = (os.environ.get("PICS", "https://envs.sh/oVN.jpg https://envs.sh/oVH.jpg https://envs.sh/oVg.jpg https://envs.sh/oVf.jpg")).split() #Required


UPI_ID = os.environ.get("UPI_ID", "clementrajadurai@okhdfcbank")
#UPI QR CODE IMAGE
UPI_IMAGE_URL = os.environ.get("UPI_IMAGE_URL", "https://envs.sh/JTa.jpg")
#SCREENSHOT URL of ADMIN for verification of payments
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", f"t.me/{OWNER_TAG}")
#Time and its price
#7 Days
PRICE1 = os.environ.get("PRICE1", "10 rs")
#1 Month
PRICE2 = os.environ.get("PRICE2", "49 rs")
#3 Month
PRICE3 = os.environ.get("PRICE3", "149 rs")
#6 Month
PRICE4 = os.environ.get("PRICE4", "299 rs")
#1 Year
PRICE5 = os.environ.get("PRICE5", "599 rs")



#force message for joining the channel
FORCE_MSG = os.environ.get("FORCE_MSG","<blockquote>🥰 Aʀᴀ Aʀᴀ, {mention} ×</blockquote>\n\n<b>Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ {count}/{total} ᴄʜᴀɴɴᴇʟs ʏᴇᴛ. Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟs ᴘʀᴏᴠɪᴅᴇᴅ ʙᴇʟᴏᴡ, ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ.. !\n\n<blockquote expandable>ʜᴀᴘᴘɪɴᴇss ᴀs ᴀ ᴍᴏᴛʜᴇʀ ᴀɴᴅ ʜᴀᴘᴘɪɴᴇss ᴀs ᴀɴ ɪᴅᴏʟ. ɪᴛ ᴍɪɢʜᴛ ʙᴇ ɴᴏʀᴍᴀʟ ᴛᴏ ʜᴀᴠᴇ ᴏɴʟʏ ᴏɴᴇ ʙᴜᴛ ɪ ᴡᴀɴᴛ ʙᴏᴛʜ</blockquote></b>")
#custom caption 

# True for yes False if no
DISABLE_CHANNEL_BUTTON = True if os.environ.get("DISABLE_CHANNEL_BUTTON", "TRUE") == "TRUE" else False
#you can add admin inside the bot(bug right now will fix later)

#add admins with space seperated


LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
