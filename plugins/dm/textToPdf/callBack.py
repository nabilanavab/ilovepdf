file_name = "plugins/dm/textToPdf/callBack.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

import                   os
from plugins.utils       import *
from configs.log         import log
from fpdf                import FPDF
from logger              import logger
from pyrogram.types      import InputMediaPhoto
from configs.config      import settings, images
from .                   import FONT, COLOR, PAGE_SIZE
from pyrogram            import filters, Client as ILovePDF

@ILovePDF.on_callback_query(filters.regex("^t2p"))
async def text_to_pdf_cb(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return
        await callbackQuery.answer()
        
        if len(callbackQuery.data.split("|")) == 1:
            # callbackQuery.data = t2p|{text_font}
            tTXT, _ = await util.translate(text="pdf2TXT['size_btn']", lang_code=lang_code)
            tTXT = await util.createBUTTON(tTXT, "121")
            return await callbackQuery.edit_message_media(
                media=InputMediaPhoto(media="https://graph.org/file/c301b7af1e637f642a520.jpg",
                                      caption=callbackQuery.message.caption), reply_markup=tTXT
            )
        
        else:
            if len(data) == 2
                # callbackQuery.data = t2p|{text_font}
                tTXT, _ = await util.translate(text="pdf2TXT['fifteen']", lang_code=lang_code)
            tTXT = await util.editDICT(inDir=tTXT, value=f"{callbackQuery.data}")
            tTXT = await util.createBUTTON(tTXT, "12121")
            return await callbackQuery.edit_message_media(
                media=InputMediaPhoto(media="https://graph.org/file/c301b7af1e637f642a520.jpg",
                                      caption=callbackQuery.message.caption), reply_markup=tTXT
            )
        
    except Exception as Error:
        logger.exception("1️⃣ 🐞 %s: %s" %(file_name, Error), exc_info=True)

# CONTACT AUTHOR: nabilanavab@gmail.com
