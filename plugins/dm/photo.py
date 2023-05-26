# fileName : plugins/dm/photo.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/photo.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

HD = {}

import os
from plugins.utils     import *
from pdf               import PDF
from .generate         import _GEN
from PIL               import Image
from configs.config    import settings
from pyrogram          import Client as ILovePDF, filters, enums

# =========================================| REPLY TO /HD |=======================================
@ILovePDF.on_message((filters.private | filters.group) & filters.command("hd") & filters.incoming)
async def _hd(bot, message):
    try:
        if isinstance(PDF.get(message.chat.id), list):
            del PDF[message.chat.id]
        if message.chat.id in HD:
            return await message.delete()
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await util.getLang(message.chat.id)
        tTXT, tBTN = await util.translate(
            text = "DOCUMENT['setHdImg']", button = "DOCUMENT['setDefault']", lang_code = lang_code
        )
        imageReply = await message.reply_text(text = tTXT, reply_markup = tBTN, quote = True)
        HD[message.chat.id] = [imageReply.id]
        return await message.delete()
    except Exception as e:
        logger.exception("1️⃣: 🐞 %s: %s" %(file_name, e), exc_info = True)

# ===============================| REPLY TO PHOTOS |==========================
@ILovePDF.on_message(filters.private & filters.incoming & filters.media_group)
async def imgAlbum(bot, message):
    try:
        for i in message:
            logger.debug(f"😎{i}\n\n")
    except Exception as Error:
        logger.exception("2️⃣: 🐞 %s: %s" %(file_name, Error), exc_info = True)
        

@ILovePDF.on_message(filters.photo & filters.private & filters.incoming)
async def images(bot, message):
    try:
        # ignore images from inline results
        if message.via_bot and message.via_bot.is_self:
            return
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await util.getLang(message.chat.id)
        if message.chat.id in HD:
            if len(HD[message.chat.id]) >= 16:
                return
            HD[message.chat.id].append(message.photo.file_id)
            generateCB = "DOCUMENT['generate']" if settings.DEFAULT_NAME else  "DOCUMENT['generateRN']"
            tTXT, tBTN = await util.translate(
                text = "DOCUMENT['imageAdded']", button = generateCB, lang_code = lang_code
            )
            return await message.reply_text(
                tTXT.format(len(HD[message.chat.id])-1, message.chat.id)+" [HD] 🔰",
                reply_markup = tBTN, quote = True
            )
        
        tTXT, tBTN = await util.translate(text = "DOCUMENT['dlImage']", lang_code = lang_code)
        imageReply = await message.reply_text(tTXT, quote = True)
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id] = []
        await message.download(f"work/{message.chat.id}/{message.chat.id}.jpg")
        img = Image.open(
            f"work/{message.chat.id}/{message.chat.id}.jpg"
        ).convert("RGB")
        PDF[message.chat.id].append(img)
        generateCB = "DOCUMENT['generate']" if settings.DEFAULT_NAME else  "DOCUMENT['generateRN']"
        tTXT, tBTN = await util.translate(
            text = "DOCUMENT['imageAdded']", button = generateCB, lang_code = lang_code
        )
        await imageReply.edit(
            tTXT.format(len(PDF[message.chat.id]), message.chat.id), reply_markup = tBTN
        )
    except Exception as e:
        logger.exception("3️⃣: 🐞 %s: %s" %(file_name, e), exc_info = True)

# Author: @nabilanavab
