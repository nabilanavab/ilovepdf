# fileName : plugins/footer.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )
from asyncio import sleep
from configs.dm import Config
from pyrogram.types import Message
from configs.db import LOG_CHANNEL
from configs.db import isMONGOexist
from configs.images import FEEDBACK
from configs.group import groupConfig
from pyrogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup
                           )

ONLY_GROUP_ADMIN = groupConfig.ONLY_GROUP_ADMIN

async def header(bot, callbackQuery):
    # callBack Message delete if User Deletes pdf
    try:
        fileExist = callbackQuery.message.reply_to_message
        
        if callbackQuery.message.chat.type != "private":
            if callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id:
                if callbackQuery.from_user.id in Config.ADMINS:
                    pass
                else:
                    userStat = await bot.get_chat_member(
                                                  callbackQuery.message.chat.id,
                                                  callbackQuery.from_user.id
                                                  )
                    if userStat.status not in ["administrator", "creator"]:
                        await callbackQuery.answer(
                                                  "Message Not For You.. :("
                                                  )
                        return True
        return False
    except Exception as e:
        logger.exception(
                        "HEADER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        await callbackQuery.message.delete()
        return "delete"

async def footer(message, file):
    try:
        await sleep(3)
        await message.reply(
                           f"[Write a Feedback]({FEEDBACK})"
                           )
        if LOG_CHANNEL and file:
            banUserCB = InlineKeyboardMarkup(
                   [[
                       InlineKeyboardButton("B@N",callback_data = f"banU|{message.chat.id}")
                   ]]
            )
            username = message.chat.username
            await file.copy(
                           chat_id = int(LOG_CHANNEL),
                           caption = f"#newFile @nabilanavab/ILovePDF\n\n"
                                     f"__Chat Type:__ {message.chat.type}\n"
                                     f"__Chat ID:__ @{message.chat.username}\n"
                                     f"__User Name:__ {message.from_user.mention}\n"
                                     f"__User ID:__ `{message.chat.id}`\n"
                                     f"__Username:__ @{message.from_user.username}",
                           reply_markup = banUserCB if isMONGOexist else None
                           )
    except Exception as e:
        logger.exception(
                        "FOOTER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
