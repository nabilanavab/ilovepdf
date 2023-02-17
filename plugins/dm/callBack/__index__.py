# fileName : plugins/dm/callBack/index.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/index.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

import os, time
from plugins.utils    import *
from pyromod          import listen
from configs.config   import images
from pyrogram.types   import ForceReply
from pyrogram         import enums, filters, Client as ILovePDF

from .file_process import *

index = filters.create(lambda _, __, query: query.data.startswith("#"))
@ILovePDF.on_callback_query(index)
async def watermark(bot, callbackQuery):
    try:
        data = callbackQuery.data[1:]
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        
        if await render.header(bot, callbackQuery, lang_code = lang_code):
            return
        
        CHUNK, _ = await util.translate(text = "common", lang_code = lang_code)
        
        if data == "rot360":
            text, _ = await util.translate(text = CHUNK['rot360'], lang_code = lang_code)
            return await callbackQuery.answer(text)
        
        elif data in ["ocr"] and "•" in callbackQuery.message.text:
            number_of_pages = callbackQuery.message.text.split("•")[1]
            if int(number_of_pages) >= 5:
                return await callbackQuery.answer(CHUNK["largeNo"])
        
        elif data == "ocr":
            if ocrPDF.nabilanavab:                                      # Never Work OCR if nabilanavab==True
                return await callbackQuery.answer(CHUNK["ocrError"])    # Deploy From Docker Files (else OCR never works)
        
        elif data == "decrypt" and "•" in callbackQuery.message.text and "🔐" not in callbackQuery.message.text:
            _, __ = await translate(text = CHUNK['notEncrypt'], lang_code = lang_code)
            return await callbackQuery.answer(_)
        
        # program will now create a brand new directory to store all of your important user data
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])

        # download the mentioned PDF file with progress updates
        input_path = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = progress, progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )

        # The program checks the size of the file and the file on the server to avoid errors when canceling the download
        if os.path.getsize(input_file) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        # The program is designed to check the presence of the "•" character in the message callback query.
        # If it is present,The file has been manipulated one or more times on the server and has attached metadata..
        # If not, the program prompts the user to add metadata to the file.
        # This helps to ensure the proper handling of the file and prevent errors during the manipulation process.
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
            location = await bot.download_media(message = THUMBNAIL, file_name = f"{cDIR}/temp.jpeg")
            THUMBNAIL = await formatThumb(location)
        
        await dlMSG.edit(CHUNK['upFile'], reply_markup = _)
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await callbackQuery.message.reply_document(
            file_name = FILE_NAME, quote = True, document = output_path, thumb = THUMBNAIL,
            caption = FILE_CAPT, progress = uploadProgress, progress_args = (dlMSG, time.time()) 
        )
        await dlMSG.delete()
        await work.work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(file_name, e), exc_info = True)
        await work.work(callbackQuery, "delete", False)
