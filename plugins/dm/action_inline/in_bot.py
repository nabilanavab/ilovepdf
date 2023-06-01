# fileName : plugins/dm/action_inline/in_bot.py
# copyright ©️ 2021 nabilanavab

fileName = "plugins/dm/action_inline/in_bot.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from plugins.utils        import *
from configs.log          import log
from plugins.utils.work   import work
from configs.db           import myID
from pyrogram             import errors
from logger               import logger
from libgenesis           import Libgen
from pyrogram.enums       import MessageMediaType
from plugins.utils.util   import getLang, translate
from pyrogram.types       import InlineKeyboardMarkup, InlineKeyboardButton

async def download(current, total, bot, message):
    try:
        await message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                [[ InlineKeyboardButton(
                    "📥 DOWNLOADED {:.2f}% 📥".format(current/total*100), callback_data="https://t.me/ilovepdf_bot"
                ) ]] 
            ))
    except errors.MessageNotModified as e:
        logger.debug("🐞 %s: %s" %(fileName, e))
    except errors.FloodWait as e:
        logger.debug("🐞 %s: %s" %(fileName, e))
        await asyncio.sleep(e.x)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)

async def openInBot( bot, message, message_id: int ) -> bool:
    try:
        lang_code=await getLang(message.chat.id)
        trCHUNK, _ = await translate(text="INLINE", lang_code=lang_code)
        
        getMSG = await bot.get_messages(chat_id=int(log.LOG_CHANNEL), message_ids=int(message_id))
        logger.debug(getMSG.media!=MessageMediaType.PHOTO)
        if getMSG.empty or getMSG.media!=MessageMediaType.PHOTO:
            return await callbackQuery.answer(trCHUNK['old'])
        
        if await work(message, "check", True):
            return await message.reply(
                text=trCHUNK['inWork'], quote=True, reply_markup=InlineKeyboardMarkup(
                [[ InlineKeyboardButton("♻", url=f"https://t.me/{myID[0].username}?start=-m{message_id}")]])
            )
        cDIR=await work(message, "create", True)
        
        reply=await bot.copy_message(
            chat_id=message.chat.id, from_chat_id=int(log.LOG_CHANNEL),
            message_id=int(message_id), reply_to_message_id=message.id,
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton("⚠️ DOWNLOADING ⚠️", url="https://t.me/ilovepdf_bot")]]
            )
        )
        
        caption=getMSG.caption
        md5=caption.splitlines()[0].split(':')[1].strip()
        link=f'http://library.lol/main/{md5}'
        
        file = await Libgen().download(
            link, dest_folder=cDIR, progress=download, progress_args=[bot, reply]
        )
        
        await reply.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                [[ InlineKeyboardButton("🐍 STARTED UPLOADING 🐍", callback_data="https://t.me/ilovepdf_bot")]]
            )
        )
        
        await reply.reply_document(
            document=file, caption=caption, progress=render.cbPRO, progress_args=(reply, 0, "UPLOADED", True)
        )
        
        await reply.edit_reply_markup(reply_markup=None)
        
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)
        
    finally:
        return await work(message, "delete", True)
      
