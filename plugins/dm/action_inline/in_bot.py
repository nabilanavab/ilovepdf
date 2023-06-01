# fileName : plugins/dm/action_inline/in_bot.py
# copyright ©️ 2021 nabilanavab

fileName = "plugins/dm/action_inline/in_bot.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from plugins.utils        import *
from configs.log          import log
from plugins.utils.work   import work
from pyrogram             import errors
from logger               import logger
from libgenesis           import Libgen
from plugins.utils.util   import getLang, translate
from pyrogram.types       import InlineKeyboardMarkup, InlineKeyboardButton

async def download(current, total, bot, message):
    try:
        await bot.edit_inline_reply_markup(
            inline_message_id = message,
            reply_markup = InlineKeyboardMarkup(
                [[ 
                    InlineKeyboardButton(
                        "📥 DOWNLOADED {:.2f}% 📥".format(current/total*100), callback_data="https://t.me/ilovepdf_bot"
                    )
                ]] 
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
        if getMSG.empty and not getMSG.photo:
            return await message.reply("❌", quote=True)
        
        if await work(message, "check", True):
            return await message.answer(trCHUNK['inWork'])
        cDIR = await work(message, "create", True)
        
        photo=await bot.copy_message(
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
            link, dest_folder=cDIR, progress=download, progress_args=[bot, photo.id]
        )
        
        await bot.edit_inline_reply_markup(
            inline_message_id = photo.id,
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton("🐍 STARTED UPLOADING 🐍", callback_data="https://t.me/ilovepdf_bot")]]
            )
        )
        
        await message.reply_document(
            document=file, caption=caption, progress=render.cbPRO, progress_args = (message, 0, "UPLOADED", True)
        )
        
        return await work(message, "delete", True)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)
      
