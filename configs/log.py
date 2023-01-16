# fileName: configs/log.py
# copyright ©️ 2021 nabilanavab

import os
from asyncio import sleep
from logger import logger
from configs.db import dataBASE
from plugins.util import translate
from pyrogram.enums import ChatType
from configs.config import settings
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

if dataBASE.MONGODB_URI:
    from database import db

class log:
    
    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", False)  # Log Channel (Optional)
    
    LOG_FILE = os.environ.get("LOG_FILE", False)  # "nabilanavab.log"
    
    LOG_TEXT = """#newUser @nabilanavab/ILovePDF\n\nID: `{}`\nView Profile: {}"""
    
    LOG_TEXT_C = """#newChat @nabilanavab/ILovePDF\n\nID: `{}`\nGroup Title: {}\nTotal Users: {}\nUserName: {}"""
    
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
                            message.chat.username if message.chat.username else "❌"
                        ),
                        reply_markup = InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton(
                                    "✅ B@N ✅", callback_data = f"banC|{message.chat.id}"
                                )
                            ]]
                        )
                    )
        
        elif message.chat.type == ChatType.PRIVATE:
            if not await db.is_user_exist(message.from_user.id):
                if referID != -1:
                    totalUSRref = await db.get_key(referID, "refer")
                    await db.set_key(referID, "refer", 1 if totalUSRref is None else totalUSRref+1)
                else:
                    referID = None
                await db.add_user(message.from_user.id, message.from_user.first_name, lang_code)
                if log.LOG_CHANNEL:
                    for i in range(200):
                        try:
                            return await bot.send_message(
                                chat_id = int(log.LOG_CHANNEL),
                                text = log.LOG_TEXT.format(
                                    message.from_user.id,
                                    message.from_user.mention) \
                                    + f"\nRefered By : [{referID}](tg://user?id={referID})",
                                reply_markup = InlineKeyboardMarkup(
                                    [[
                                        InlineKeyboardButton(
                                            "✅ B@N USER ✅", callback_data = f"banU|{message.from_user.id}"
                                        )
                                    ]]
                                )
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
    
    async def footer(message, input=None, output=None, lang_code=settings.DEFAULT_LANG):
        file = input.reply_to_message if input else output     # input here means /check will be message so file will be replied message
        #await sleep(10)
        #tTXT, _ = await translate(text="feedbackMsg", lang_code=lang_code)
        #await message.reply(tTXT)
        if log.LOG_CHANNEL and file:
            if message.chat.type == ChatType.PRIVATE:
                banUserCB = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "✅ B@N USER ✅", callback_data = f"banU|{file.chat.id}")
                    ]]
                )
                captionLOG = f"""#newFile @nabilanavab/ILovePDF

__chat type:__ `private 👤`
__username:__ {'@{}'.format(file.chat.username) if file.chat.username else " ❌ "}
__user profile:__ [{file.chat.first_name}](tg://user?id={file.chat.id})
__user ID:__ `{file.chat.id}`"""
            
            else:
                banUserCB = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "✅ B@N USER ✅", callback_data = f"banU|{file.from_user.id}"
                        )
                    ],[
                        InlineKeyboardButton(
                            "✅ B@N CHAT ✅", callback_data = f"banC|{file.chat.id}"
                        )
                    ]]
                )
                captionLOG = f"""#newFile @nabilanavab/ILovePDF

__chat type:__ `{file.chat.type} 👥`
__chat title:__ `{file.chat.title}`
__username:__ {'@{}'.format(file.chat.username) if {file.chat.username} is not None else " ❌ "}

__user profile:__ {file.from_user.mention}
__user ID:__ `{file.from_user.id}`"""
            
            for i in range (200):
                try:
                    return await file.copy(
                        chat_id = int(log.LOG_CHANNEL),
                        caption = captionLOG,
                        reply_markup = banUserCB if dataBASE.MONGODB_URI else None
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.wait)
                except Exception as e:
                    logger.debug(f"Error in new User Log: {e}")
                    return

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
