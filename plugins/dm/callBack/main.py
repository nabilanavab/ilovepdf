# fileName : plugins/dm/callBack/main.py
# copyright ©️ 2021 nabilanavab

import os, time
from .process import *
import shutil, asyncio
from pdf import PROCESS
from logger import logger
from pyromod import listen
from plugins.util import *
from plugins.render import *
from configs.config import images
from pyrogram.types import ForceReply
from plugins.thumbName import thumbName, formatThumb
from pyrogram import enums, filters, Client as ILovePDF

if nabilanavab == False:
    from plugins.dm.callBack.process import ocrPDF

work = filters.create(lambda _, __, query: query.data.startswith("work"))
@ILovePDF.on_callback_query(work)
async def _pdf(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        CHUNK, _ = await translate(text="work", lang_code=lang_code)
        
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.from_user.id; message_id = callbackQuery.message.id
        
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
        
        if chat_id in PROCESS:    # CHECKS IF BOT DOING ANY WORK
            return await callbackQuery.answer(CHUNK["inWork"])

        PROCESS.append(chat_id)    # ↓ ADD TO PROCESS
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
                chat_id = chat_id, reply_to_message_id = message_id, text = CHUNK["pyromodASK_1"].format(work),
                filters = filters.text, reply_markup = ForceReply(True, "Enter Password..")
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if password.text == "/exit":
                PROCESS.remove(chat_id)
                return await password.reply(CHUNK["exit"], quote = True)
        
        # fileNm continues false(if not rename) and take org. name as fileName
        fileNm = False
        # Asks newFile Name [renamePdf]
        if data == "rename":
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            newName = await bot.ask(
                chat_id = chat_id, reply_to_message_id = message_id, text = CHUNK["pyromodASK_2"],
                filters = filters.text, reply_markup = ForceReply(True, "New PDF Name..")
            )
            # CANCEL RENAME PROCESS IF MESSAGE == /exit
            if newName.text == "/exit":
                PROCESS.remove(chat_id)
                return await newName.reply(CHUNK["exit"], quote = True)
            else:
                if newName.text[-4:] == ".pdf": fileNm = newName.text
                else: fileNm = newName.text + ".pdf"
        cancelBtn = await createBUTTON(CHUNK["button"])
        # DOWNLOAD MESSSAGE
        downloadMessage = await callbackQuery.message.reply_text(CHUNK["download"], reply_markup=cancelBtn, quote=True)
        
        # input and output file paths
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        file_name = callbackQuery.message.reply_to_message.document.file_name
        # Bot not using os.rename, just send input file with new name ;)
        if data == "rename":
            output_file = input_file
        # Output file name of pdf to .txt, html, json file
        elif data == "T": output_file = f"{message_id}/outPut.txt"
        elif data == "J": output_file = f"{message_id}/outPut.json"
        elif data == "H": output_file = f"{message_id}/outPut.html"
        
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        # Output fileName
        if not fileNm:
            fileNm = file_name
            fileNm, fileExt = os.path.splitext(fileNm)        # seperates name & extension
            if data == "T": fileNm = f"{fileNm}.txt"
            elif data == "J": fileNm = f"{fileNm}.json"
            elif data == "H": fileNm = f"{fileNm}.html"
            else: fileNm = f"{fileNm}.pdf"
        
        # STARTED DOWNLOADING
        downloadLoc = await bot.download_media(
            message = file_id, file_name = input_file, progress = progress,
            progress_args = (fileSize, downloadMessage, time.time())
        )
        # CHECKS PDF DOWNLOADED OR NOT
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        await downloadMessage.edit(CHUNK["takeTime"], reply_markup=cancelBtn)
        # CHECK PDF OR NOT(HERE compressed, SO PG UNKNOWN)
        if data=="decrypt" or "•" not in callbackQuery.message.text:
            # check file encryption, codec.
            checked, number_of_pages = await checkPdf(input_file, callbackQuery)
            if data == "decrypt" and checked != "encrypted":
                await downloadMessage.edit(CHUNK["notENCRYPTED"])
                PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                return
            if data != "decrypt" and checked != "pass":
                return await downloadMessage.delete()
        
        if (chat_id in PROCESS): # or (data == "decrypt"):
            if data == "compress":
                await downloadMessage.edit(CHUNK["compress"], reply_markup=cancelBtn)
                caption = await compressPDF(downloadMessage, message_id, lang_code)
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            elif data == "decrypt":
                await downloadMessage.edit(CHUNK["decrypt"], reply_markup=cancelBtn)
                caption = await decryptPDF(downloadMessage, message_id, password, lang_code)
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            elif data == "encrypt":
                await downloadMessage.edit(CHUNK["encrypt"], reply_markup=cancelBtn)
                caption = await encryptPDF(message_id, password, lang_code)
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            elif data == "ocr":
                if number_of_pages>5:
                    await downloadMessage.edit(CHUNK["largeNo"])
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
                else:
                    await downloadMessage.edit(CHUNK["ocr"], reply_markup=cancelBtn)
                    caption = await ocrPDF(downloadMessage, message_id, lang_code)
                    if not caption:
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
            elif data == "format":
                if number_of_pages>5:
                    await downloadMessage.edit(CHUNK["largeNo"])
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
                else:
                    await downloadMessage.edit(CHUNK["format"], reply_markup=cancelBtn)
                    caption = await formatterPDF(downloadMessage, message_id, lang_code)
                    if not caption:
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
            elif data == "rename":
                await downloadMessage.edit(CHUNK["rename"], reply_markup=cancelBtn)
                await asyncio.sleep(1)
            elif data.startswith("rot"):
                await downloadMessage.edit(CHUNK["rot"], reply_markup=cancelBtn)
                caption = await rotatePDF(data, message_id, lang_code)
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            else:
                await downloadMessage.edit(CHUNK["pdfTxt"], reply_markup=cancelBtn)
                caption = await textPDF(callbackQuery, downloadMessage, message_id, lang_code)
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    await downloadMessage.delete(); return
        else:
            shutil.rmtree(f"{message_id}")
            return
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, fileNm)
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(message = THUMBNAIL, file_name = f"{callbackQuery.message.id}.jpeg")
            THUMBNAIL = await formatThumb(location)
        
        if data == "rename":
            caption = CHUNK["fileNm"].format(file_name, FILE_NAME)
        
        await downloadMessage.edit(CHUNK["upload"], reply_markup=cancelBtn)
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        if chat_id in PROCESS:
            with open(output_file, "rb") as output:
                await callbackQuery.message.reply_document(
                    file_name = FILE_NAME, quote = True, document = output,
                    thumb = THUMBNAIL, caption = f"{caption}\n\n{FILE_CAPT}", progress = uploadProgress,
                    progress_args = (downloadMessage, time.time())
                )
        if not(data == "M"): await downloadMessage.delete()
        PROCESS.remove(chat_id)
        try: os.remove(location)
        except Exception: pass
        shutil.rmtree(f"{message_id}")
    except Exception as e:
        logger.exception("CB/_MAIN_:CAUSES %s ERROR" %(e), exc_info=True)
        try:
            await downloadMessage.edit(CHUNK["document['error']"], reply_markup=cancelBtn)
            shutil.rmtree(f"{message_id}")
            PROCESS.remove(chat_id)
        except Exception: pass

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
