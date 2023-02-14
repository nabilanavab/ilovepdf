# fileName : plugins/dm/callBack/index.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/index.py"


# LOGGING INFO: DEBUG
from logger           import logger

import os, time
from plugins.utils          import *
from plugins.work     import work
from pyromod          import listen
from configs.config   import images
from pyrogram.types   import ForceReply
from plugins.fncta    import thumbName, formatThumb
from pyrogram         import enums, filters, Client as ILovePDF

from .drawPDF import drawPDF
from .saturatePDF import saturatePDF
from .splitSinglePage import splitSinglePage
from .blackAndWhitePdf import blackAndWhitePdf
from .combineSinglePage import combineSinglePage

if nabilanavab == False:
    from .ocrPDF import ocrPDF

index = filters.create(lambda _, __, query: query.data.startswith("#"))
@ILovePDF.on_callback_query(index)
async def watermark(bot, callbackQuery):
    try:
        data = callbackQuery.data[1:]
        lang_code = await getLang(callbackQuery.message.chat.id)

        if await header(bot, callbackQuery, lang_code = lang_code):
            return
        
        elif data == "rot360":
            return await callbackQuery.answer(CHUNK["rot360"])
        
        # Never Work OCR if nabilanavab==True
        # Deploy From Docker Files (else OCR never works)
        elif data == "ocr":
            if nabilanavab:
                return await callbackQuery.answer(CHUNK["ocrError"])
            if "•" in callbackQuery.message.text:
                number_of_pages = callbackQuery.message.text.split("•")[1]
                if int(number_of_pages) >= 5:
                    return await callbackQuery.answer(CHUNK["largeNo"])
            
        # PDF A4 Formatter
        elif data == "format" and "•" in callbackQuery.message.text:
            number_of_pages = callbackQuery.message.text.split("•")[1]
            if int(number_of_pages) >= 5:
                return await callbackQuery.answer(CHUNK["largeNo"])
        
        elif data == "decrypt" and "•" in callbackQuery.message.text and "🔐" not in callbackQuery.message.text:
            _, __ = await translate(text = "cbAns[3]", lang_code = lang_code)
            return await callbackQuery.answer(_)
        
        # -------------------GET TEXT 
        
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])

        # -------------------DOWNLOAD MESSAGE

        input_path = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = progress, progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )

        # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
        if os.path.getsize(input_file) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        # --------------------DOWNLOAD COMPLETED
        if "•" not in callbackQuery.message.text:
            known = False
            checked, number_of_pages = await checkPdf(input_file, callbackQuery)
            if checked == "encrypted":
                await work(callbackQuery, "delete", False)
                return await dlMSG.delete()
        else:
            known = True
            number_of_pages = int(callbackQuery.message.text.split("•")[1])
        
        if data == "baw":
            output_path = await blackAndWhitePdf(cDIR = cDIR, input_file = input_path)
        
        elif data == "sat":
            output_path = await saturatePDF(cDIR = cDIR, input_file = input_path)
        
        elif data == "comb":
            output_path = await combineSinglePage(cDIR = cDIR, input_file = input_path)
        
        elif data == "draw":
            output_path = await drawPDF(cDIR = cDIR, input_file = input_path)
        
        elif data == "zoom":
            output_path = await splitSinglePage(cDIR = cDIR, input_file = input_path)
        
        
        if "•" in callbackQuery.message.text:
            
        else:
            known = False
        
        # Asks password for encryption, decryption
        if data in ["decrypt", "encrypt"]:
            work = "Decryption" if data == "decrypt" else "Encryption"
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            password = await bot.ask(
                chat_id = callbackQuery.from_user.id, reply_to_message_id = callbackQuery.message.id,
                text = CHUNK["pyromodASK_1"].format(work),
                filters = filters.text, reply_markup = ForceReply(True, "Enter Password..")
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if password.text == "/exit":
                return await password.reply(CHUNK["exit"], quote = True)
        
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
            file_name = FILE_NAME, quote = True, document = output_path, thumb = THUMBNAIL,
            caption = FILE_CAPT, progress = uploadProgress, progress_args = (dlMSG, time.time()) 
        )
        await dlMSG.delete()
        await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)
