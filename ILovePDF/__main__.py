# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab


file_name = "ILovePDF/__main__.py"

iLovePDF = '''
  _   _                  ___  ___  ____ ™
 | | | |   _____ _____  | _ \|   \|  __| 
 | | | |__/ _ \ V / -_) |  _/| |) |  _|  
 |_| |___,\___/\_/\___| |_|  |___/|_|    
                         ❤ [Nabil A Navab] 
                         ❤ Email: nabilanavab@gmail.com
                         ❤ Telegram: @nabilanavab
'''

import asyncio, os
import shutil, sys
from pdf import works
from configs.db import *
from logger import logger
from pyromod import listen
from lang import __users__
from plugins.utils import *
from configs.log import log
from configs.beta import BETA
from configs.config import bot, settings, images
from pyrogram import Client as ILovePDF, errors
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand


if dataBASE.MONGODB_URI:
    from database import db

if not bot.API_TOKEN or not bot.API_HASH or not bot.API_ID:
    logger.debug(f"bot.API_TOKEN, bot.API_HASH, bot.API_ID : MANDATORY")
    sys.exit("Error: Missing mandatory bot credentials.")

# PYROGRAM
class Bot(ILovePDF):
    def __init__(self) -> None:
        """
        Initialize the Bot instance with the specified parameters.

        This constructor calls the superclass initializer with the bot's
        name, API ID, API hash, and bot token.
        """
        super().__init__(
            name = "ILovePDF",                  # Type: str
            api_id = bot.API_ID,                # Type: int or str
            api_hash = bot.API_HASH,            # Type: str
            bot_token = bot.API_TOKEN,          # Type: str
            plugins = { "root" : "plugins" }    # Type: dict[str, str]
        )

    async def start(self):
        """Initialize the bot by loading banned users, beta users, and custom thumbnails."""

        if dataBASE.MONGODB_URI:
            # --- Loads Banned UsersId to List -----
            b_users, b_chats = await db.get_banned()
            BANNED_USR_DB.extend(b_users)
            BANNED_GRP_DB.extend(b_chats)

            beta_users = await db.get_beta()
            BETA.extend(beta_users)

            # ------- Loads UsersId with custom THUMBNAIL ---------
            users = await db.get_all_users()  # Get all users' Data
            
            async for user in users:
                if settings.MULTI_LANG_SUP:
                    lang = user.get("lang", False)
                    if (lang != False) and (lang != settings.DEFAULT_LANG):
                        __users__.userLang[user.get("id")] = f"{lang}"

                if user.get("thumb", False):
                    CUSTOM_THUMBNAIL_U.append(user["id"])
            
            # --- Load Groups ---
            groups = await db.get_all_chats()

            async for group in groups:
                GROUPS.append(group["id"])
                if settings.MULTI_LANG_SUP:
                    lang = group.get("lang", False)
                    if (lang != False) and (lang != settings.DEFAULT_LANG):
                        __users__.userLang[group.get("id")] = f"{lang}"
                        
                if group.get("thumb", False):
                    CUSTOM_THUMBNAIL_C.append(group["id"])

            # -- Loads Other Necessary Data --
            users = await db.get_all_users()
            async for user in users:
                user_id = user.get("id")

                # Initialize DATA entry for user if certain fields exist
                if user.get("api") or user.get("fname") or user.get("capt"):
                    DATA[user_id] = [0, 0, 0]

                    DATA[user_id][0] = 1 if user.get("api") else 0
                    DATA[user_id][1] = 1 if user.get("fname") else 0
                    DATA[user_id][2] = 1 if user.get("capt") else 0

        # -----> Telebot/Pyrogram Client Starting <-----
        try:
            await super().start()
        except errors.FloodWait as e:
            logger.debug(f"wait {e.value} seconds.. automtically restarts..")
            
            # Countdown to inform how long to wait
            for time in range(e.value, 0, -10):
                await asyncio.sleep(10)
                if time % 10 == 0:
                    logger.debug(f"Remaining seconds: {time}")
            
            # Restart the bot after waiting
            await super().start()

        # Retrieve and store bot ID
        myID.append(await app.get_me())

        # Set bot commands
        command, _ = await util.translate(
            text = "BOT_COMMAND", lang_code = settings.DEFAULT_LANG
        )
        await app.set_bot_commands(
            [ BotCommand(i, command[i]) for i in command ],
            language_code = "en"
        )

        # -----> SETTING FORCE SUBSCRIPTION <-----
        if settings.UPDATE_CHANNEL:
            try:
                # Fetch the channel's information
                inviteLink = await app.get_chat(int(settings.UPDATE_CHANNEL))
                chanlCount = inviteLink.members_count

                if not inviteLink and inviteLink.username:
                    # Construct the invite link using the username
                    inviteLink = await app.create_chat_invite_link(
                        int(settings.UPDATE_CHANNEL)
                    )
                    inviteLink = inviteLink.invite_link
                else:
                    # Create an invite link if the channel does not have a username
                    inviteLink = f"https://telegram.dog/{inviteLink.username}"

                invite_link.append(inviteLink)

            except errors.ChannelInvalid:
                settings.UPDATE_CHANNEL = False
                logger.debug(f"BoT NoT AdMiN iN UPDATE_CHANNEL")

            except Exception as error:
                logger.debug(f"⚠️ FORCE SUBSCRIPTION ERROR : {error}", exc_info=True)

        logger.debug(
            f"\n"
            f"❤ BOT ID: {myID[0].id}\n"
            f"❤ BOT FILENAME: {myID[0].first_name}\n"
            f"❤ BOT USERNAME: {myID[0].username}\n\n"
            f"❤ SOURCE-CODE By: @nabilanavab 👑\n"
            f"❤ BOT CHANNEL: t.me/iLovePDF_bot\n\n"
            f"{iLovePDF}"
        )

        # ----> NOTIFY. BROKEN WORKS <----
        if settings.SEND_RESTART:
            # Notify users
            if len(works["u"]):
                for u in works["u"]:
                    lang_code = await getLang(int(u))
                    msg, btn = await translate(
                        text = "RESTART['msg']", button = "RESTART['btn']", lang_code = lang_code
                    )
                    await app.send_message(
                        chat_id = int(u), text = msg, reply_markup = btn
                    )

            # Notify groups
            if len(works["g"]):
                for g in works["g"]:
                    await app.send_message(chat_id = int(g[0]), text = f"restarted.. {g[1]}")

        # Send a notification to the log channel about the bot's status.
        if log.LOG_CHANNEL:
            try:
                # Construct the caption based on whether the update channel is set
                if settings.UPDATE_CHANNEL:
                    caption = (
                        f"{myID[0].first_name} get started successfully...✅\n\n"
                        f"FORCED CHANNEL:\n"
                        f"invite_link: {str(invite_link[0]) if invite_link[0] is not None else '❌'}\n"
                        f"get_member : {str(chanlCount) if invite_link[0] is not None else '❌'}\n"
                    )
                else:
                    caption = f"{myID[0].first_name} get started successfully...✅"
                
                # Determine the document to send based on the log file
                if log.LOG_FILE and log.LOG_FILE[-4:] == ".log":
                    doc = f"./{log.LOG_FILE}"
                    markUp = InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("♻️ refresh log ♻️", callback_data = "log")
                        ],[
                            InlineKeyboardButton("◍ Close ◍", callback_data = "close|admin")
                        ],]
                    )
                else:
                    doc = images.THUMBNAIL_URL
                    markUp = InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("◍ close ◍", callback_data = "close|admin")
                        ]]
                    )

                # Send the document to the log channel                
                await app.send_document(
                    chat_id = int(log.LOG_CHANNEL), document = doc,
                    caption = caption, reply_markup = markUp,
                )

            except errors.ChannelInvalid:
                log.LOG_CHANNEL = False
                logger.debug(f"BoT NoT AdMiN iN LoG ChAnNeL")

            except Exception as error:
                logger.debug(f"⚠️ ERROR IN LOG CHANNEL - {error}", exc_info = True)

    async def stop(self, *args):
        await super().stop()


if __name__ == "__main__":
    # Define the path for the work directory
    work_path: str = f"{os.path.abspath(os.getcwd())}/work/nabilanavab"

    # Check if the work directory exists
    if os.path.exists(work_path):

        # Iterate through chats in the directory
        for chat in os.listdir("work/nabilanavab"):

            if f"{chat}".startswith("-100"):
                # Append group chat data
                works["g"].append(
                    [chat, [user for user in os.listdir(f"work/nabilanavab/{chat}")]]
                )
            else:
                works["u"].append(chat)
        
        # Remove the entire work directory
        shutil.rmtree(f"{os.path.abspath(os.getcwd())}/work")

    # Create the work directory again
    os.makedirs("work/nabilanavab")

    # Initialize and run the bot
    app = Bot()
    app.run()


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
