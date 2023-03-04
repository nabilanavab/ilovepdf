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
async def __index__(bot, callbackQuery):
    try:
        data = callbackQuery.data[1:]
        logger.debug(data)
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        
        if await render.header(bot, callbackQuery, lang_code = lang_code):
            return
        
        CHUNK, _ = await util.translate(text = "common", button="common['button']", lang_code = lang_code)
        
        if data == "rot360":
            # Rotating a PDF by 360 degrees will result in the same orientation as the original document.
            # Therefore, returning a useless callback answer
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
            return await callbackQuery.answer(CHUNK['notEncrypt'])
        
        # create a brand new directory to store all of your important user data
        cDIR = await work.work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        # Asks password for encryption, decryption
        password = False
        if data in ["decrypt", "encrypt"]:
            _work = "Decryption 🔓" if data == "decrypt" else "Encryption 🔐"
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            password = await bot.ask(
                chat_id = callbackQuery.from_user.id,
                reply_to_message_id = callbackQuery.message.id,
                text = CHUNK["pyromodASK_1"].format(_work),
                filters = filters.text,
                reply_markup = ForceReply(True, "Enter Password..")
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if password.text == "/exit":
                return await password.reply(CHUNK["exit"], quote = True)
        
        if callbackQuery.message.reply_to_message and callbackQuery.message.reply_to_message.document:
            dlMSG = await callbackQuery.message.reply_text(CHUNK["download"], reply_markup = _, quote = True)
        else:
            return await callbackQuery.message.reply_text("#old_queue\n\n`try by sending new file`", reply_markup = _, quote = True)
        
        # download the mentioned PDF file with progress updates
        input_file = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = render.progress, progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )
        
        await dlMSG.edit(text = CHUNK["completed"], reply_markup = _)
        
        # The program checks the size of the file and the file on the server to avoid errors when canceling the download
        if os.path.getsize(input_file) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work.work(callbackQuery, "delete", False)
        
        # The program is designed to check the presence of the "•" character in the message callback query.
        # If it is present,The file has been manipulated one or more times on the server and has attached metadata..
        # If not, the program prompts the user to add metadata to the file.
        # This helps to ensure the proper handling of the file and prevent errors during the manipulation process.
        if "•" not in callbackQuery.message.text:
            checked, number_of_pages = await render.checkPdf(input_file, callbackQuery, lang_code)
            if data == "decrypt" and checked != "encrypted":
                await work.work(callbackQuery, "delete", False)
                return await dlMSG.edit(CHUNK['notEncrypt'])
        else:
            number_of_pages = int(callbackQuery.message.text.split("•")[1])
        
        if data == "metaData":
            # After the metadata has been added, the progress message will be deleted
            await work.work(callbackQuery, "delete", False)
            return await dlMSG.delete()
        
        elif data == "baw":
            isSuccess, output_file = await blackAndWhitePdf.blackAndWhitePdf(cDIR = cDIR, input_file = input_file)
        
        elif data == "sat":
            isSuccess, output_file = await saturatePDF.saturatePDF(cDIR = cDIR, input_file = input_file)
        
        elif data == "comb":
            isSuccess, output_file = await combineSinglePage.combineSinglePage(cDIR = cDIR, input_file = input_file)
        
        elif data == "draw":
            isSuccess, output_file = await drawPDF.drawPDF(cDIR = cDIR, input_file = input_file)
        
        elif data == "zoom":
            isSuccess, output_file = await splitSinglePage.splitSinglePage(cDIR = cDIR, input_file = input_file)
        
        elif data == "encrypt":
            isSuccess, output_file = await encryptPDF.encryptPDF(cDIR = cDIR, input_file = input_file, password = password.text)
        
        elif data == "decrypt":
            isSuccess, output_file = await decryptPDF.decryptPDF(cDIR = cDIR, input_file = input_file, password = password.text)
        
        elif data == "compress":
            isSuccess, output_file = await compressPDF.compressPDF(cDIR = cDIR, input_file = input_file)
        
        elif data == "preview":
            isSuccess, output_file = await previewPDF.previewPDF(cDIR = cDIR, input_file = input_file)
        
        if not isSuccess:
            await work.work(callbackQuery, "delete", False)
            if data == "decrypt":
                return await dlMSG.edit(text = CHUNK["decrypt_error"].format(output_file), reply_markup = _)
            return await dlMSG.edit(text = CHUNK["error"].format(output_file), reply_markup = _)
        
        _caption = await caption.caption(
            data = data, lang_code = lang_code,
            args = [number_of_pages, password.text] if password else None
        )
        
        # getting thumbnail
        FILE_NAME, FILE_CAPT, THUMBNAIL = await fncta.thumbName(
            callbackQuery.message, callbackQuery.message.reply_to_message.document.file_name
        )
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(message = THUMBNAIL, file_name = f"{cDIR}/temp.jpeg")
            THUMBNAIL = await formatThumb(location)
        
        await dlMSG.edit(CHUNK['upload'], reply_markup = _)
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await callbackQuery.message.reply_document(
            file_name = FILE_NAME, quote = True, document = output_file, thumb = THUMBNAIL,
            caption = f"{_caption}\n\n{FILE_CAPT}", progress = render._progress, progress_args = (dlMSG, time.time()) 
        )
        await dlMSG.delete()
        await work.work(callbackQuery, "delete", False)
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        await work.work(callbackQuery, "delete", False)
