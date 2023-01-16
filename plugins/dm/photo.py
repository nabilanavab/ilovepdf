# fileName : plugins/dm/photo.py
# copyright ©️ 2021 nabilanavab

HD = {}

import os
from pdf import PDF
from PIL import Image
from logger import logger
from .generate import _GEN
from pyrogram import enums
from pyrogram import filters
from configs.config import settings
from pyrogram import Client as ILovePDF
from plugins.util import getLang, translate

# ===============================| REPLY TO /HD |======================================================================================================================
@ILovePDF.on_message((filters.private | filters.group) & filters.command("hd") & filters.incoming)
async def _hd(bot, message):
    try:
        if isinstance(PDF.get(message.chat.id), list):
            del PDF[message.chat.id]
        if message.chat.id in HD:
            return await message.delete()
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await getLang(message.chat.id)
        tTXT, tBTN = await translate(text="document['setHdImg']", button="document['setDefault']", lang_code=lang_code)
        imageReply = await message.reply_text(text=tTXT, reply_markup=tBTN, quote=True)
        HD[message.chat.id] = [imageReply.id]
        return await message.delete()
    except Exception as e:
        logger.debug("plugins/dm/photo: %s" %(e), exc_info=True)

# =======================================================================================================| REPLY TO PHOTOS |===========================================
@ILovePDF.on_message(filters.photo & filters.private & filters.incoming)
async def images(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await getLang(message.chat.id)
        if message.chat.id in HD:
            if len(HD[message.chat.id]) >= 16:
                return
            HD[message.chat.id].append(message.photo.file_id)
            generateCB = "document['generate']" if settings.DEFAULT_NAME else  "document['generateRN']"
            tTXT, tBTN = await translate(text="document['imageAdded']", button=generateCB, lang_code=lang_code)
            return await message.reply_text(tTXT.format(len(HD[message.chat.id])-1, message.chat.id)+" [HD] 🔰", reply_markup=tBTN, quote=True)
        
        tTXT, tBTN = await translate(text="PROGRESS['dlImage']", lang_code=lang_code)
        imageReply = await message.reply_text(tTXT, quote=True)
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id] = []
        await message.download(f"work/{message.chat.id}/{message.chat.id}.jpg")
        img = Image.open(
            f"work/{message.chat.id}/{message.chat.id}.jpg"
        ).convert("RGB")
        PDF[message.chat.id].append(img)
        generateCB = "document['generate']" if settings.DEFAULT_NAME else  "document['generateRN']"
        tTXT, tBTN = await translate(text="document['imageAdded']", button=generateCB, lang_code=lang_code)
        await imageReply.edit(
            tTXT.format(len(PDF[message.chat.id]), message.chat.id), reply_markup = tBTN
        )
    except Exception as e:
        logger.exception("plugins/dm/photo: %s" %(e), exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
