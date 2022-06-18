# fileName : plugins/dm/callBack/_main_.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import time
import shutil
import asyncio
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from plugins.checkPdf import checkPdf
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from plugins.footer import footer, header
from plugins.progress import progress, uploadProgress
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Importing Pdf Process Funs.
from plugins.dm.callBack.process import (
                                        textPDF,
                                        rotatePDF,
                                        encryptPDF,
                                        decryptPDF,
                                        compressPDF,
                                        formatterPDF
                                        )

# checks if ocr works (nabilanavab==False)
from plugins.dm.callBack.process import nabilanavab
if nabilanavab == False:
    from plugins.dm.callBack.process import ocrPDF

#--------------->
#--------> LOCAL VARIABLES
#------------------->

cancelBtn = InlineKeyboardMarkup([[InlineKeyboardButton("« Cancel »", callback_data = "closeme")]])

#--------------->
#--------> PYRO FILTERS
#------------------->

M = filters.create(lambda _, __, query: query.data in ["M", "KM"])
T = filters.create(lambda _, __, query: query.data in ["T", "KT"])
J = filters.create(lambda _, __, query: query.data in ["J", "KJ"])
H = filters.create(lambda _, __, query: query.data in ["H", "KH"])

rot360 = filters.create(lambda _, __, query: query.data=="rot360")
pdfInfo = filters.create(lambda _, __, query: query.data.startswith("KpdfInfo"))
rot = filters.create(lambda _, __, query: query.data in ["rot90", "rot180", "rot270"])
ocr = filters.create(lambda _, __, query: query.data.startswith(tuple(["ocr", "Kocr"])))
rename = filters.create(lambda _, __, query: query.data.startswith(tuple(["rename", "Krename"])))
decrypt = filters.create(lambda _, __, query: query.data.startswith(tuple(["decrypt", "Kdecrypt"])))
encrypt = filters.create(lambda _, __, query: query.data.startswith(tuple(["encrypt", "Kencrypt"])))
formatter = filters.create(lambda _, __, query: query.data.startswith(tuple(["format", "Kformat"])))
compress = filters.create(lambda _, __, query: query.data.startswith(tuple(["compress", "Kcompress"])))

#--------------->
#--------> CALLBACK QUERY
#------------------->

@ILovePDF.on_callback_query(
    pdfInfo | ocr | compress | decrypt | encrypt | formatter | rename | rot | rot360 | M | T | J | H
)
async def _pdf(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.message_id
        
        if callbackQuery.data == "rot360":
            return await callbackQuery.answer(
                                      "You have Some big Problem..🙂"
                                      )
        
        # Never Work OCR if nabilanavab==True
        # Deploy From Docker Files (else OCR never works)
        if callbackQuery.data.startswith(tuple(["ocr", "Kocr"])):
            if nabilanavab:
                return await callbackQuery.answer(
                                                "Owner Restricted 😎🤏"
                                                 )
            if callbackQuery.data[0] == "K":
                _, number_of_pages = callbackQuery.data.split("|")
                if int(number_of_pages) >= 5:
                    return await callbackQuery.answer(
                                                     "send a pdf file less than 5 pages.. 🙄"
                                                     )
        
        # PDF A4 Formatter
        if callbackQuery.data.startswith(tuple(["Kformat"])):
            _, number_of_pages = callbackQuery.data.split("|")
            if int(number_of_pages) >= 5:
                return await callbackQuery.answer(
                                          "send a pdf file less than 5 pages.. 🙄"
                                          )
        
        # Known MetaData
        if callbackQuery.data.startswith("KpdfInfo"):
            _, number_of_pages = callbackQuery.data.split("|")
            return await callbackQuery.answer(
                                      "♎ TOTAL {} PAGES ♎".format(number_of_pages)
                                      )
        
        # CHECKS IF BOT DOING ANY WORK
        if chat_id in PROCESS:
            return await callbackQuery.answer(
                                             "Work in progress.. 🙇"
                                             )
        
        # ↓ ADD TO PROCESS       ↓ CALLBACK DATA
        PROCESS.append(chat_id); data = callbackQuery.data
        await callbackQuery.answer(
                                  "⚙️ Processing..."
                                  )
        
        if (data[0] == "K") and ("|" in data):
            _, number_of_pages = callbackQuery.data.split("|")
        
        # Asks password for encryption, decryption
        if data.startswith(tuple(["decrypt", "Kdecrypt", "encrypt", "Kencrypt"])):
            work = "Decryption" if data.startswith(tuple(["decrypt", "Kdecrypt"])) else "Encryption"
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            password = await bot.ask(
                                    chat_id = chat_id,
                                    reply_to_message_id = message_id,
                                    text = f"__PDF {work} »\n"
                                            "Now, please enter the password :__\n\n"
                                            "/exit __to cancel__",
                                    filters = filters.text,
                                    reply_markup = ForceReply(True)
                                    )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if password.text == "/exit":
                await password.reply(
                                    "`process canceled.. `😏",
                                    quote = True
                                    )
                PROCESS.remove(chat_id)
                return
        
        # fileNm continues false(if not rename) and take org. name as fileName
        fileNm = False
        # Asks newFile Name [renamePdf]
        if data.startswith(tuple(["rename", "Krename"])):
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            newName = await bot.ask(
                                   chat_id = chat_id,
                                   reply_to_message_id = message_id,
                                   text = "__Rename PDF »\n"
                                          "Now, please enter the new name:__\n\n"
                                          "/exit __to cancel__",
                                   filters = filters.text,
                                   reply_markup = ForceReply(True)
                                   )
            # CANCEL RENAME PROCESS IF MESSAGE == /exit
            if newName.text == "/exit":
                await newName.reply(
                                   "`process canceled.. `😏",
                                   quote = True
                                   )
                PROCESS.remove(chat_id)
                return
            else:
                if newName.text[-4:] == ".pdf":
                    fileNm = newName[-4:]
                else:
                    fileNm = newName.text + ".pdf"
        
        # DOWNLOAD MESSSAGE
        downloadMessage = await callbackQuery.message.reply_text(
                                                                "`Downloding your pdf..` 📩", 
                                                                reply_markup = cancelBtn,
                                                                quote = True
                                                                )
        
        # input and output file paths
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        # Bot not using os.rename, just send input file with new name ;)
        if data.startswith(tuple(["rename", "Krename"])):
            output_file = input_file
            caption = f"__New Name:__ `{fileNm}`"
        # Output file name of pdf to .txt, html, json file
        elif data in ["T", "KT"]:
            output_file = f"{message_id}/outPut.txt"
        elif data in ["J", "KJ"]:
            output_file = f"{message_id}/outPut.json"
        elif data in ["H", "KH"]:
            output_file = f"{message_id}/outPut.html"
        
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        # Output fileName
        if not fileNm:
            fileNm = callbackQuery.message.reply_to_message.document.file_name
            fileNm, fileExt = os.path.splitext(fileNm)        # seperates name & extension
            if data in ["T", "KT"]:
                fileNm = f"{fileNm}.txt"
            elif data in ["J", "KJ"]:
                fileNm = f"{fileNm}.json"
            elif data in ["H", "KH"]:
                fileNm = f"{fileNm}.html"
            else:
                fileNm = f"{fileNm}.pdf"
        
        # STARTED DOWNLOADING
        c_time = time.time()
        downloadLoc = await bot.download_media(
                                              message = file_id,
                                              file_name = input_file,
                                              progress = progress,
                                              progress_args = (
                                                              fileSize,
                                                              downloadMessage,
                                                              c_time
                                                              )
                                              )
        # CHECKS PDF DOWNLOADED OR NOT
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        
        await downloadMessage.edit(
                                  "⚙️ `Started Processing.. \nIt might take some time..`💛",
                                  reply_markup = cancelBtn
                                  )
        # CHECK PDF OR NOT(HERE compressed, SO PG UNKNOWN)
        if (data[0] != 'K') or not (data in ["rot180", "rot90", "rot270"]):
            # check file encryption, codec.
            checked, number_of_pages = await checkPdf(input_file, callbackQuery)
            if data.startswith("decrypt"):
                if not(checked == "encrypted"):
                    await downloadMessage.edit(
                                              "`File Not Encrypted..`🙏🏻"
                                              )
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            else:
                if not(checked == "pass"):
                    await downloadMessage.delete()
                    return
        
        if chat_id in PROCESS:
            if data.startswith(tuple(["compress", "Kcompress"])):
                await downloadMessage.edit(
                                          "⚙️ `Started Compressing.. 🌡️\nIt might take some time..`💛", 
                                          reply_markup = cancelBtn
                                          )
                caption = await compressPDF(
                                           downloadMessage,
                                           message_id
                                           )
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            if data.startswith(tuple(["decrypt", "Kdecrypt"])):
                await downloadMessage.edit(
                                          "⚙️ `Started Decrypting.. 🔓\nIt might take some time..`💛",
                                          reply_markup = cancelBtn
                                          )
                caption = await decryptPDF(
                                          downloadMessage,
                                          message_id,
                                          password
                                          )
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            if data.startswith(tuple(["encrypt", "Kencrypt"])):
                await downloadMessage.edit(
                                          "⚙️ `Started Encrypting.. 🔐\nIt might take some time..`💛",
                                          reply_markup = cancelBtn
                                          )
                caption = await encryptPDF(
                                          message_id,
                                          password
                                          )
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            if data.startswith(tuple(["ocr", "Kocr"])):
                if number_of_pages>5:
                    await downloadMessage.edit(
                                              "__Send me a file less than 5 images__ 😅"
                                              )
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f"{message_id}")
                    return
                else:
                    await downloadMessage.edit(
                                              "⚙️ `Adding OCR Layer.. ✍️\nIt might take some time..`💛",
                                              reply_markup = cancelBtn
                                              )
                    caption = await ocrPDF(
                                          downloadMessage,
                                          message_id
                                          )
                    if not caption:
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
            if data.startswith(tuple(["format", "Kformat"])):
                if number_of_pages>5:
                    await downloadMessage.edit(
                                              "__Send me a file less than 5 images__ 😅"
                                              )
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f"{message_id}")
                    return
                else:
                    await downloadMessage.edit(
                                              "⚙️ `Started Formatting.. 🤘\nIt might take some time..`💛",
                                              reply_markup = cancelBtn
                                              )
                    caption = await formatterPDF(
                                                downloadMessage,
                                                message_id
                                                )
                    if not caption:
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
            if data.startswith(tuple(["rename", "Krename"])):
                await downloadMessage.edit(
                                          "⚙️ `Renameing PDf.. ✏️\nIt might take some time..`💛",
                                          reply_markup = cancelBtn
                                          )
                await asyncio.sleep(1)
            if data.startswith(tuple(["rot90", "rot180", "rot270"])):
                await downloadMessage.edit(
                                          "⚙️ `Rotating PDf.. 🤸\nIt might take some time..`💛",
                                          reply_markup = cancelBtn
                                          )
                caption = await rotatePDF(
                                         data,
                                         message_id
                                         )
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            if data in ["T", "H", "J", "M", "KT", "KH", "KJ", "KM"]:
                await downloadMessage.edit(
                                          "⚙️ `Extracting Text.. 🐾\nIt might take some time..`💛",
                                          reply_markup=cancelBtn 
                                          )
                caption = await textPDF(
                                       data,
                                       downloadMessage,
                                       message_id
                                       )
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    downloadMessage.delete(); return
        else:
            shutil.rmtree(f"{message_id}")
            return
        
        # Getting thumbnail
        thumbnail, fileName = await thumbName(callbackQuery.message, fileNm)
        if PDF_THUMBNAIL != thumbnail:
            location = await bot.download_media(
                                    message = thumbnail,
                                    file_name = f"{callbackQuery.message.message_id}.jpeg"
                                    )
            thumbnail = await formatThumb(location)
        
        await downloadMessage.edit(
                                  "⚙️ `Started Uploading..` 📤",
                                  reply_markup = cancelBtn
                                  )
        await callbackQuery.message.reply_chat_action(
                                                     "upload_document"
                                                     )
        c_time = time.time()
        if chat_id in PROCESS:
            with open(output_file, "rb") as output:
                await callbackQuery.message.reply_document(
                                                           file_name = fileName,
                                                           quote = True,
                                                           document = output,
                                                           thumb = thumbnail,
                                                           caption = caption,
                                                           progress = uploadProgress,
                                                           progress_args = (
                                                                           downloadMessage,
                                                                           c_time
                                                                           )
                                                           )
        await downloadMessage.delete()
        PROCESS.remove(chat_id)
        try:
            os.remove(location)
        except Exception: pass
        shutil.rmtree(f"{message_id}")
        await footer(callbackQuery.message, False)
    except Exception as e:
        logger.exception(
                        "CB/_MAIN_:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            await downloadMessage.edit(
                                      f"{e}",
                                      reply_markup=cancelBtn
                                      )
            shutil.rmtree(f"{message_id}")
            PROCESS.remove(chat_id)
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
