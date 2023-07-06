# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/photo.py"

HD = {}

from pdf import PDF
from PIL import Image
from plugins import *
from .generate import _GEN
from plugins.utils import *
from configs.config import settings
from pyrogram import filters, enums

#  REPLY TO /HD 
@ILovePDF.on_message(
    (filters.private | filters.group) & filters.command("hd") & filters.incoming
)
async def _hd(bot, message):
    try:
        if isinstance(PDF.get(message.chat.id), list):
            del PDF[message.chat.id]
        if message.chat.id in HD:
            return await message.delete()
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await util.getLang(message.chat.id)
        tTXT, tBTN = await util.translate(
            text="DOCUMENT['setHdImg']",
            button="DOCUMENT['setDefault']",
            lang_code=lang_code,
        )
        imageReply = await message.reply_text(text=tTXT, reply_markup=tBTN, quote=True)
        HD[message.chat.id] = [imageReply.id]
        return await message.delete()
    except Exception as Error:
        logger.exception("1️⃣: 🐞 %s: %s" % (file_name, Error), exc_info=True)


#  REPLY TO PHOTOS 
@ILovePDF.on_message(filters.photo & filters.private & filters.incoming)
async def images(bot, message):
    try:
        # ignore images from inline results
        if message.via_bot and message.via_bot.is_self:
            return
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await util.getLang(message.chat.id)
        if message.chat.id in HD:
            if len(HD[message.chat.id]) >= 26:
                return
            HD[message.chat.id].append(message.photo.file_id)
            generateCB = (
                "DOCUMENT['generate']"
                if settings.DEFAULT_NAME
                else "DOCUMENT['generateRN']"
            )
            tTXT, tBTN = await util.translate(
                text="DOCUMENT['imageAdded']", button=generateCB, lang_code=lang_code
            )
            return await message.reply_text(
                tTXT.format(len(HD[message.chat.id]) - 1, message.chat.id) + " [HD] 🔰",
                reply_markup=tBTN,
                quote=True,
            )

        tTXT, tBTN = await util.translate(
            text="DOCUMENT['dlImage']", lang_code=lang_code
        )
        imageReply = await message.reply_text(tTXT, quote=True)
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id] = []
        path = await message.download(f"work/{message.chat.id}/{message.id}.jpg")
        img = Image.open(path).convert("RGB")
        PDF[message.chat.id].append(img)
        generateCB = (
            "DOCUMENT['generate']"
            if settings.DEFAULT_NAME
            else "DOCUMENT['generateRN']"
        )
        tTXT, tBTN = await util.translate(
            text="DOCUMENT['imageAdded']", button=generateCB, lang_code=lang_code
        )
        await imageReply.edit(
            tTXT.format(len(PDF[message.chat.id]), message.chat.id), reply_markup=tBTN
        )
        os.remove(path)
    except Exception as Error:
        logger.exception("2️⃣: 🐞 %s: %s" % (file_name, Error), exc_info=True)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
