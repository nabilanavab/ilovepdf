# fileName : plugins/dm/callBack/BaWsat.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/BaWsat.py"

import os, time, fitz
from PIL import Image
from logger import logger
from plugins.util import *
from plugins.render import *
from plugins.work import work
from configs.config import images
from plugins.fncta import thumbName, formatThumb
from pyrogram import enums, filters, Client as ILovePDF

BS = filters.create(lambda _, __, query: query.data.startswith(tuple(["baw", "sat"])))

@ILovePDF.on_callback_query(BS)
async def watermark(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        CHUNK, _ = await translate(text = "comb", button = "comb['cancelCB']", lang_code = lang_code)
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        
        dlMSG = await callbackQuery.message.reply_text(
            CHUNK['download'], reply_markup = _, quote = True
        )
        input_file = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = progress,
            progress_args = (
                callbackQuery.message.reply_to_message.document.file_size,
                dlMSG, time.time()
            )
        )
        # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
        if os.path.getsize(input_file) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        await dlMSG.edit(CHUNK['process'], reply_markup = _)
        if "•" not in callbackQuery.message.text:
            checked, number_of_pages = await checkPdf(input_file, callbackQuery)
            if checked == "encrypted":
                await work(callbackQuery, "delete", False)
                return await dlMSG.delete()
        
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:        # empty output PDF
                if callbackQuery.data.startswith("baw"):
                    for pg in range(iNPUT.page_count):
                        iNPUT[pg].get_pixmap().save(f"{cDIR}/temp.png")
                        with Image.open(f"{cDIR}/temp.png") as image:
                            image.convert("1").save(f"{cDIR}/temp.png")
                            rect = iNPUT[pg].rect
                            oUTPUT.new_page(pno = -1, width = rect.width, height = rect.height)
                            oUTPUT[pg].insert_image(rect = rect, filename = f"{cDIR}/temp.png")
                
                elif callbackQuery.data.startswith("sat"):
                    for pg in range(iNPUT.page_count):
                        iNPUT[pg].get_pixmap().save(f"{cDIR}/temp.png")
                        with Image.open(f"{cDIR}/temp.png") as image:
                            image.convert("L").save(f"{cDIR}/temp.png")
                            rect = iNPUT[pg].rect
                            oUTPUT.new_page(pno = -1, width = rect.width, height = rect.height)
                            oUTPUT[pg].insert_image(rect = rect, filename = f"{cDIR}/temp.png")
                
                oUTPUT.save(f"{cDIR}/outPut.pdf", garbage=3, deflate=True)
        
        # Getting thumbnail
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(
            callbackQuery.message, callbackQuery.message.reply_to_message.document.file_name
        )
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(
                message = THUMBNAIL, file_name = f"{cDIR}/temp.jpeg"
            )
            THUMBNAIL = await formatThumb(location)
        
        await dlMSG.edit(CHUNK['upFile'], reply_markup = _)
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await callbackQuery.message.reply_document(
            file_name = FILE_NAME, quote = True, document = f"{cDIR}/outPut.pdf", thumb = THUMBNAIL,
            caption = FILE_CAPT, progress = uploadProgress, progress_args = (dlMSG, time.time()) 
        )
        await dlMSG.delete()
        await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)

#                                                                                                                                                Telegram: @nabilanavab
