# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/configs/log.py"

import os
import asyncio
from logger import logger
from plugins.utils import *
from pyrogram.enums import ChatType
from configs.config import settings
from pyrogram.errors import FloodWait
from configs.db import dataBASE, myID
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

if dataBASE.MONGODB_URI:
    from database import db


class log:

    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", False)  # Log Channel (Optional)

    LOG_FILE = os.environ.get("LOG_FILE", False)  # "nabilanavab.log"

    LOG_TEXT = "#newUser @nabilanavab/ILovePDF\n\nID: `{}`\nView Profile: {}"

    LOG_TEXT_C = "#newChat @nabilanavab/ILovePDF\n\nID: `{}`\nGroup Title: {}\nTotal Users: {}\nUserName: {}"

    async def newUser(bot, message, lang_code, referID):
        if message.chat.type != ChatType.PRIVATE:
            if not await db.is_chat_exist(message.chat.id):
                await db.add_chat(message.chat.id, message.chat.title)
                if log.LOG_CHANNEL:
                    total = await bot.get_chat_members_count(message.chat.id)
                    await bot.send_message(
                        chat_id = int(log.LOG_CHANNEL),
                        text = log.LOG_TEXT_C.format(
                            message.chat.id,
                            message.chat.title,
                            total,
                            message.chat.username if message.chat.username else "❌",
                        ),
                        reply_markup = InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton("✅ B@N ✅", callback_data=f"banC|{message.chat.id}",)
                            ]]
                        ),
                    )

        elif message.chat.type == ChatType.PRIVATE:
            if not await db.is_user_exist(message.from_user.id):
                if referID:
                    totalUSRref = await db.get_key(int(referID), "refer")
                    await db.set_key(
                        int(referID), "refer",
                        f"{referID}"
                        if totalUSRref is None
                        else f"{totalUSRref}|{referID}",
                    )
                await db.add_user(
                    message.from_user.id, message.from_user.first_name, lang_code
                )
                if log.LOG_CHANNEL:
                    for i in range(200):
                        try:
                            return await bot.send_message(
                                chat_id=int(log.LOG_CHANNEL),
                                text=log.LOG_TEXT.format(
                                    message.from_user.id, message.from_user.mention
                                )
                                + (
                                    f"\nRefered By : [{referID}](tg://user?id={referID})"
                                    if referID
                                    else ""
                                ),
                                reply_markup=InlineKeyboardMarkup(
                                    [[
                                        InlineKeyboardButton("✅ B@N USER ✅", callback_data=f"banU|{message.from_user.id}",)
                                    ]]
                                ),
                            )
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except Exception as e:
                            logger.debug(f"Error in new User Log: {e}")
                            return
            else:
                if lang_code == settings.DEFAULT_LANG:
                    await db.dlt_key(message.from_user.id, "lang")
                if lang_code != settings.DEFAULT_LANG:
                    await db.set_key(message.from_user.id, "lang", lang_code)

    async def footer(message, input=None, output=None, lang_code=settings.DEFAULT_LANG, coffee=False):
        # input here means /check will be message so file will be replied message
        file = (
            input.reply_to_message if input else output
        )

        # feedBack Message
        if settings.COFFEE and coffee:
            # coffee=True: it only sends once the work is done
            await asyncio.sleep(1)
            tTXT, tBTN = await util.translate(
                text="feedbackMsg['message']", button="feedbackMsg['button']", lang_code=lang_code
            )
            await message.reply(tTXT, reply_markup=tBTN)

        if log.LOG_CHANNEL and file:
            if message.chat.type == ChatType.PRIVATE:
                banUserCB = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("✅ B@N USER ✅", callback_data=f"banU|{file.chat.id}")
                    ]]
                )
                captionLOG = f"""#newFile @nabilanavab/ILovePDF
#{myID[0].username}

__chat type:__ `private 👤`
__user profile:__ [{file.chat.first_name}](tg://user?id={file.chat.id})
__user ID:__ `{file.chat.id}`
{'__username:__ @{}'.format(file.chat.username) if file.chat.username else " "}"""

            else:
                banUserCB = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("✅ B@N USER ✅", callback_data=f"banU|{file.from_user.id}",)
                    ],[
                        InlineKeyboardButton("✅ B@N CHAT ✅", callback_data=f"banC|{file.chat.id}")
                    ],]
                )
                captionLOG = f"""#newFile @nabilanavab/ILovePDF
#{myID[0].username}

__chat type:__ `{file.chat.type} 👥`
__chat title:__ `{file.chat.title}`
{'__username:__ @{}'.format(file.chat.username) if {file.chat.username} is not None else ' '}

__user profile:__ {file.from_user.mention}
__user ID:__ `{file.from_user.id}`"""

            for i in range(200):
                try:
                    return await file.copy(
                        chat_id = int(log.LOG_CHANNEL),
                        caption = captionLOG,
                        reply_markup = banUserCB if dataBASE.MONGODB_URI else None,
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.wait)
                except Exception as e:
                    logger.debug(f"Error in new User Log: {e}")
                    return

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
