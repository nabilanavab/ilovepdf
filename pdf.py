# This file is part of nabilanavab/iLovePDF [a completely free software]

__author__ = "nabilanavab"
__email__ = "nabilanavab@gmail.com"
__telegram__ = "telegram.dog/nabilanavab"
__copyright__ = "Copyright 2021, nabilanavab"

iLovePDF = '''
  _   _                  ___  ___  ____ ™
 | | | |   _____ _____  | _ \|   \|  __| 
 | | | |__/ _ \ V / -_) |  _/| |) |  _|  
 |_| |___,\___/\_/\___| |_|  |___/|_|    
                         ❤ [Nabil A Navab] 
                         ❤ Email: nabilanavab@gmail.com
                         ❤ Telegram: @nabilanavab
'''

import asyncio
from configs.db import *
from logger import logger
from lang import __users__
from pyromod import listen
from configs.log import log
from plugins.util import translate
from pyrogram import Client as ILovePDF
from telebot.async_telebot import AsyncTeleBot
from configs.config import bot, settings, images
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
)

if dataBASE.MONGODB_URI:
    from database import db

# GLOBAL VARIABLES
PDF = {}            # save images for generating pdf
PROCESS = []        # to check current process

pyTgLovePDF = AsyncTeleBot(bot.API_TOKEN, parse_mode="Markdown")    # TELEBOT (pyTelegramBotAPI) Asyncio [for uploading group doc, imgs]

# PYROGRAM
class Bot(ILovePDF):
    
    def __init__(self):
        super().__init__(
            name = "ILovePDF",
            api_id = bot.API_ID,
            api_hash = bot.API_HASH,
            bot_token = bot.API_TOKEN,
            plugins = {"root": "plugins"}
        )
    
    async def start(self):
        if dataBASE.MONGODB_URI:
            # ------------------------------------------------------------------------------------------------------- Loads Banned UsersId to List --------------------
            b_users, b_chats = await db.get_banned()
            BANNED_USR_DB.extend(b_users)
            BANNED_GRP_DB.extend(b_chats)
            
            # ---------------- Loads UsersId with custom THUMBNAIL ----------------------------------------------------------------------------------------------------
            users = await db.get_all_users()   # Get all user Data
            async for user in users:
                if user.get("thumb", False):
                    CUSTOM_THUMBNAIL_U.append(user["id"]) 
            
            groups = await db.get_all_chats()
            async for group in groups:
                if group.get("thumb", False):
                    CUSTOM_THUMBNAIL_C.append(group["id"])
            
            # -------------------------------------------------------------- Loads Lang Codes -------------------------------------------------------------------------
            if settings.MULTI_LANG_SUP:
                users = await db.get_all_users()   # Get all user Data
                async for user in users:
                    lang = user.get("lang", False)
                    if (lang != False) and (lang != settings.DEFAULT_LANG):
                        __users__.userLang[user.get("id")] = f"{lang}"
            
            # -------------------------------------------------------------------------------------- Loads Other Necessay Datas ---------------------------------------
            users = await db.get_all_users()
            async for user in users:
                if user.get("api", False) or user.get("fname", False) or user.get("capt", False):
                    DATA[user.get("id")] = [0, 0, 0]
                    if user.get("api", False):
                        DATA[user.get("id")][0] = 1
                    if user.get("fname", False):
                        DATA[user.get("id")][1] = 1
                    if user.get("capt", False):
                        DATA[user.get("id")][2] = 1
        
        # -----> Telebot/Pyrogram Client Starting <-----
        await super().start()
        myID = await app.get_me()
        
        command, _ = await translate(text="BOT_COMMAND", lang_code=settings.DEFAULT_LANG)
        await app.set_bot_commands([BotCommand(i, command[i]) for i in command ],language_code = "en")
        # -----> SETTING FORCE SUBSCRIPTION <-----
        if settings.UPDATE_CHANNEL:
            try:
                inviteLink = await app.create_chat_invite_link(int(settings.UPDATE_CHANNEL))
                chanlCount = await app.get_chat_members_count(int(settings.UPDATE_CHANNEL))
                invite_link.append(inviteLink.invite_link)
            except Exception as error:
                logger.debug(f"⚠️ FORCE SUBSCRIPTION ERROR : {error}", exc_info=True)
        
        logger.debug(f"\n"
                    f"❤ BOT ID: {myID.id}\n"
                    f"❤ BOT FILENAME: {myID.first_name}\n"
                    f"❤ BOT USERNAME: {myID.username}\n\n"
                    f"❤ SOURCE-CODE By: @nabilanavab 👑\n"
                    f"❤ BOT CHANNEL: t.me/iLovePDF_bot\n\n"
                    f"{iLovePDF}")
        
        # -----> SETTING LOG CHANNEL <-----
        if log.LOG_CHANNEL:
            try:
                if settings.UPDATE_CHANNEL:
                    caption = f"{myID.first_name} get started Successfully ✅\n\n" \
                              f"FORCED CHANNEL:\n" \
                              f"invite_link: {str(invite_link[0]) if invite_link[0] is not None else '❌'}\n" \
                              f"get_member : {str(chanlCount) if invite_link[0] is not None else '❌'}\n"
                else:
                    caption = f"{myID.first_name} get started Successfully ✅"
                if log.LOG_FILE and log.LOG_FILE[-4:]==".log":
                    doc = f"./{log.LOG_FILE}"
                    markUp = InlineKeyboardMarkup([[InlineKeyboardButton("♻️ refresh log ♻️", callback_data = "log")
                             ],[InlineKeyboardButton("◍ close ◍", callback_data = "close|admin")]])
                else:
                    doc = images.PDF_THUMBNAIL
                    markUp = InlineKeyboardMarkup([[InlineKeyboardButton("◍ close ◍", callback_data = "close|admin")]])
                await app.send_document(
                    chat_id = int(log.LOG_CHANNEL), document = doc,
                    caption = caption, reply_markup = markUp
                )
            except Exception as error:
                logger.debug(f"⚠️ ERRROR IN LOG CHANNEL - {error}", exc_info=True)
        
    async def stop(self, *args):
        await super().stop()

if __name__ == "__main__":
    pyTgLovePDF.polling()
    
    app = Bot()
    app.run()

#                                                                                                                                       OPEN SOURCE TELEGRAM PDF BOT 🐍
#                                                                                                                                            by: nabilanavab [iLovePDF]
