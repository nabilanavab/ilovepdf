# fileName : plugins/dm/action_inline/in_bot.py
# copyright ©️ 2021 nabilanavab

fileName = "plugins/dm/action_inline/in_bot.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from plugins.utils        import *
from configs.log          import log
from plugins.utils.work   import work
from configs.db           import myID
from typing               import Union
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

async def openInBot( bot, message, md5: Union[str, int] ) -> bool:
    try:
        lang_code=await getLang(message.chat.id)
        trCHUNK, _ = await translate(text="INLINE", lang_code=lang_code)
        
        if isinstance(md5, int):
            getMSG = await bot.get_messages(chat_id=int(log.LOG_CHANNEL), message_ids=md5)
            if getMSG.empty or getMSG.media!=MessageMediaType.PHOTO:
                return await messaage.reply(trCHUNK['old'])
            
        if await work(message, "check", True):
            return await message.reply(
                text=trCHUNK['inWork'], quote=True, reply_markup=InlineKeyboardMarkup(
                [[ InlineKeyboardButton("♻", callback_data=f"refresh{f'-m{md5}' if isinstance(md5, int) else ''}")]])
            )
        cDIR=await work(message, "create", True)
        
        markup=InlineKeyboardMarkup([[ InlineKeyboardButton("⚠️ DOWNLOADING ⚠️", url="https://t.me/ilovepdf_bot")]])
        if isinstance(md5, int):
            reply=await bot.copy_message(
                chat_id=message.chat.id, from_chat_id=int(log.LOG_CHANNEL),
                message_id=md5, reply_to_message_id=message.id, reply_markup=markup
            )
            caption=getMSG.caption
            md5=caption.splitlines()[0].split(':')[1].strip()
        else:
            data=await Libgen().search(
                query=md5, search_field='md5',
                return_fields=[
                    'title', 'author', 'publisher', 'year', 'language',
                    'volumeinfo', 'filesize', 'extension', 'timeadded',
                    'timelastmodified', 'coverurl'
                ]
            )
            caption=''
            for key, value in data[list(data.keys())[0]].items():
                caption += f"**{key}**: __{value}__\n"
            reply=await message.reply_photo(data[list(data.keys())[0]]['coverurl'], caption=caption, reply_markup=markup)
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
        return await work(message, "delete", True)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)
        return await work(message, "delete", True)
