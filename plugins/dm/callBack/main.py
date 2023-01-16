# fileName : plugins/dm/callBack/main.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/main.py"

import os, time, shutil, asyncio

from .process       import *
from plugins.util   import *
from plugins.render import *
from configs.config import images
from logger         import logger
from pyromod        import listen
from plugins.work   import work as w
from pyrogram.types import ForceReply
from plugins.fncta  import thumbName, formatThumb
from pyrogram       import enums, filters, Client as ILovePDF

if nabilanavab == False:
    from plugins.dm.callBack.process import ocrPDF

work = filters.create(lambda _, __, query: query.data.startswith("work"))
@ILovePDF.on_callback_query(work)
async def _pdf(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.from_user.id)
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        CHUNK, _ = await translate(text="work", lang_code=lang_code)
        data = callbackQuery.data.split("|")[1]
        if data == "rot360":
            return await callbackQuery.answer(CHUNK["rot360"])
        
        # Never Work OCR if nabilanavab==True
        # Deploy From Docker Files (else OCR never works)
        if data == "ocr":
            if nabilanavab:
                return await callbackQuery.answer(CHUNK["ocrError"])
            if "•" in callbackQuery.message.text:
                number_of_pages = callbackQuery.message.text.split("•")[1]
                if int(number_of_pages) >= 5:
                    return await callbackQuery.answer(CHUNK["largeNo"])
        
        # PDF A4 Formatter
        if data == "format" and "•" in callbackQuery.message.text:
            number_of_pages = callbackQuery.message.text.split("•")[1]
            if int(number_of_pages) >= 5:
                return await callbackQuery.answer(CHUNK["largeNo"])
        
        if data == "decrypt" and "•" in callbackQuery.message.text and "🔐" not in callbackQuery.message.text:
            _, __ = await translate(text="cbAns[3]", lang_code=lang_code)
            return await callbackQuery.answer(_)
        
        cDIR = await w(callbackQuery, "create", False)
        if not cDIR:    # CHECKS IF BOT DOING ANY WORK
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        if "•" in callbackQuery.message.text:
            known = True
            number_of_pages = int(callbackQuery.message.text.split("•")[1])
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
        
        # fileNm continues false(if not rename) and take org. name as fileName
        fileNm = False
        # Asks newFile Name [renamePdf]
        if data == "rename":
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            newName = await bot.ask(
                chat_id = callbackQuery.from_user.id, reply_to_message_id = callbackQuery.message.id,
                text = CHUNK["pyromodASK_2"],
                filters = filters.text, reply_markup = ForceReply(True, "New PDF Name..")
            )
            # CANCEL RENAME PROCESS IF MESSAGE == /exit
            if newName.text == "/exit":
                return await newName.reply(CHUNK["exit"], quote = True)
            else:
                if newName.text[-4:] == ".pdf": fileNm = newName.text
                else: fileNm = newName.text + ".pdf"
        clBTN = await createBUTTON(CHUNK["button"])
        # DOWNLOAD MESSSAGE
        dlMSG = await callbackQuery.message.reply_text(
            CHUNK["download"], reply_markup = clBTN, quote = True
        )
        
        # input and output file paths
        input_file, output_file = f"{cDIR}/inPut.pdf", f"{cDIR}/outPut.pdf"
        # Bot not using os.rename, just send input file with new name ;)
        if data == "rename":
            output_file = input_file
        # Output file name of pdf to .txt, html, json file
        elif data == "T": output_file = f"{cDIR}/outPut.txt"
        elif data == "J": output_file = f"{cDIR}/outPut.json"
        elif data == "H": output_file = f"{cDIR}/outPut.html"
        
        # Output fileName
        if not fileNm:
            fileNm = callbackQuery.message.reply_to_message.document.file_name
            fileNm, fileExt = os.path.splitext(fileNm)        # seperates name & extension
            if data == "T": fileNm = f"{fileNm}.txt"
            elif data == "J": fileNm = f"{fileNm}.json"
            elif data == "H": fileNm = f"{fileNm}.html"
            else: fileNm = f"{fileNm}.pdf"
        
        # STARTED DOWNLOADING
        downloadLoc = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = input_file, progress = progress,
            progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )
        # CHECKS PDF DOWNLOADED OR NOT
        if os.path.getsize(downloadLoc) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        await dlMSG.edit(CHUNK["takeTime"], reply_markup = clBTN)
        # CHECK PDF OR NOT(HERE compressed, SO PG UNKNOWN)
        if data == "decrypt" or "•" not in callbackQuery.message.text:
            # check file encryption, codec.
            checked, number_of_pages = await checkPdf(input_file, callbackQuery)
            if data == "decrypt" and checked != "encrypted":
                await dlMSG.edit(CHUNK["notENCRYPTED"])
                return await w(callbackQuery, "delete", False)
            if data != "decrypt" and checked != "pass":
                return await dlMSG.delete()
        
        if await w(callbackQuery, "check", False): # or (data == "decrypt"):
            if data == "compress":
                await dlMSG.edit(CHUNK["compress"], reply_markup = clBTN)
                caption = await compressPDF(dlMSG, cDIR, lang_code)
                if not caption:
                    return await w(callbackQuery, "delete", False)
            elif data == "decrypt":
                await dlMSG.edit(CHUNK["decrypt"], reply_markup = clBTN)
                caption = await decryptPDF(dlMSG, cDIR, password, lang_code)
                if not caption:
                    return await w(callbackQuery, "delete", False)
            elif data == "encrypt":
                await dlMSG.edit(CHUNK["encrypt"], reply_markup = clBTN)
                caption = await encryptPDF(cDIR, password, lang_code)
                if not caption:
                    return await w(callbackQuery, "delete", False)
            elif data == "ocr":
                if number_of_pages>5:
                    await dlMSG.edit(CHUNK["largeNo"])
                    return await w(callbackQuery, "delete", False)
                else:
                    await dlMSG.edit(CHUNK["ocr"], reply_markup = clBTN)
                    caption = await ocrPDF(dlMSG, cDIR, lang_code)
                    if not caption:
                        return await w(callbackQuery, "delete", False)
            elif data == "format":
                if number_of_pages>5:
                    await dlMSG.edit(CHUNK["largeNo"])
                    return await w(callbackQuery, "delete", False)
                else:
                    await dlMSG.edit(CHUNK["format"], reply_markup = clBTN)
                    caption = await formatterPDF(dlMSG, cDIR, lang_code)
                    if not caption:
                        return await w(callbackQuery, "delete", False)
            elif data == "rename":
                await dlMSG.edit(CHUNK["rename"], reply_markup = clBTN)
                await asyncio.sleep(1)
            elif data.startswith("rot"):
                await dlMSG.edit(CHUNK["rot"], reply_markup = clBTN)
                caption = await rotatePDF(data, cDIR, lang_code)
                if not caption:
                    return await w(callbackQuery, "delete", False)
            else:
                await dlMSG.edit(CHUNK["pdfTxt"], reply_markup = clBTN)
                caption = await textPDF(
                    callbackQuery, dlMSG, cDIR, lang_code
                )
                if not caption:
                    await w(callbackQuery, "delete", False)
                    return await dlMSG.delete()
        else:
            return await w(callbackQuery, "delete", False)
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, fileNm)
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(
                message = THUMBNAIL, file_name = f"{cDIR}/thumb.jpeg"
            )
            THUMBNAIL = await formatThumb(location)
        
        if data == "rename":
            caption = CHUNK["fileNm"].format(callbackQuery.message.reply_to_message.document.file_name, FILE_NAME)
        
        await dlMSG.edit(CHUNK["upload"], reply_markup=clBTN)
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        if await w(callbackQuery, "check", False):
            with open(output_file, "rb") as output:
                await callbackQuery.message.reply_document(
                    file_name = FILE_NAME, quote = True, document = output,
                    thumb = THUMBNAIL, caption = f"{caption}\n\n{FILE_CAPT}", progress = uploadProgress,
                    progress_args = (dlMSG, time.time())
                )
        if not(data == "M"): await dlMSG.delete()
        return await w(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        return await w(callbackQuery, "delete", False)
        await dlMSG.edit(CHUNK["document['error']"], reply_markup=clBTN)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
