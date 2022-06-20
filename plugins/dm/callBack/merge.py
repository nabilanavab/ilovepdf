# fileName : plugins/dm/callBack/merge.py
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
from configs.dm import Config
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from PyPDF2 import PdfFileMerger
from plugins.checkPdf import checkPdf
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from plugins.footer import footer, header
from plugins.progress import progress, uploadProgress
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

MERGE = {}; MERGEsize = {}

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB=MAX_FILE_SIZE * (10 ** 6)
else:
    MAX_FILE_SIZE = False

#--------------->
#--------> MERGE PDFS
#------------------->

merge = filters.create(lambda _, __, query: query.data == "merge")

@ILovePDF.on_callback_query(merge)
async def _merge(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.message_id
        
        # CHECK IF BOT DOING ANY WORK
        if chat_id in PROCESS:
            return await callbackQuery.answer(
                                             "Work in progress..🙇"
                                             )
        await callbackQuery.answer()
        PROCESS.append(chat_id)
        fileId = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        fileNm = callbackQuery.message.reply_to_message.document.file_name
        _, fileExt = os.path.splitext(fileNm)        # seperates name & extension
        # ADDING FILE ID & SIZE TO MERGE, MERGEsize LIST (FOR FUTURE USE)
        MERGE[chat_id] = [fileId]
        MERGEsize[chat_id] = [fileSize]
        # REQUEST FOR OTHER PDFS FOR MERGING
        nabilanavab = True; size = 0
        while(nabilanavab):
            if len(MERGE[chat_id]) >= 5:
                await callbackQuery.message.reply(
                                                 "__Due to Overload you can only merge 5 pdfs at a time__",
                                                 quote=True
                                                 )
                nabilanavab = False
                break
            askPDF = await bot.ask(
                                text = "__MERGE pdfs » Total pdfs in queue: {}__\n\n"
                                       "/exit __to cancel__\n"
                                       "/merge __to merge__".format(
                                                                   len(MERGE[chat_id])
                                                                   ),
                                chat_id = chat_id,
                                reply_to_message_id = message_id,
                                filters = None
                                )
            if askPDF.text == "/exit":
                await askPDF.reply(
                                  "`Process Cancelled..` 😏",
                                  quote = True
                                  )
                PROCESS.remove(chat_id); del MERGE[chat_id]; del MERGEsize[chat_id]
                break
            if askPDF.text == "/merge":
                nabilanavab = False
                break
            # IS SEND MESSAGE A DOCUMENT
            if askPDF.document:
                file_id = askPDF.document.file_id
                file_size = askPDF.document.file_size
                # CHECKING FILE EXTENSION .pdf OR NOT
                if fileExt == ".pdf":
                    # CHECKING TOTAL SIZE OF MERGED PDF
                    for _ in MERGEsize[chat_id]:
                        size = int(_) + size
                    # CHECKS MAXIMUM FILE SIZE (IF ADDED) ELSE 1.8 GB LIMIT
                    if (MAX_FILE_SIZE and MAX_FILE_SIZE_IN_kiB <= int(size)) or int(size) >= 1800000000:
                        await callbackQuery.message.reply(
                            f"`Due to Overload Bot Only Support %sMb pdfs..`😐"%(MAX_FILE_SIZE if MAX_FILE_SIZE else "1.8Gb")
                        )
                        nabilanavab = False
                        break
                    # ADDING NEWLY ADDED PDF FILE ID & SIZE TO LIST
                    MERGE[chat_id].append(file_id)
                    MERGEsize[chat_id].append(file_size)
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            PROCESS.remove(chat_id)
        # GET /merge, REACHES MAX FILE SIZE OR MAX NO OF PDF
        if nabilanavab == False:
            # DISPLAY TOTAL PDFS FOR MERGING
            downloadMessage = await askPDF.reply_text(
                                                     f"`Total PDF's : {len(MERGE[chat_id])}`.. 💡",
                                                     quote = True
                                                     )
            asyncio.sleep(.5); i = 0
            # ITERATIONS THROUGH FILE ID'S AND DOWNLOAD
            for iD in MERGE[chat_id]:
                await downloadMessage.edit(
                                          f"__Started Downloading Pdf :{i+1} 📥__"
                                          )
                # START DOWNLOAD
                c_time = time.time()
                downloadLoc = await bot.download_media(
                                                    message = iD,
                                                    file_name = f"merge{chat_id}/{i}.pdf",
                                                    progress = progress,
                                                    progress_args = (
                                                                    MERGEsize[chat_id][i],
                                                                    downloadMessage,
                                                                    c_time
                                                                    )
                                                    )
                # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
                if downloadLoc is None:
                    PROCESS.remove(chat_id)
                    await callbackQuery.message.reply_text(
                                                          "`Merge Process Cancelled.. 😏`",
                                                          quote = True
                                                          )
                    shutil.rmtree(f"merge{chat_id}")
                    return
                # CHECKS PDF CODEC, ENCRYPTION..
                checked, noOfPg = await checkPdf(
                                                f"merge{chat_id}/{i}.pdf",
                                                callbackQuery
                                                )
                # REMOVE FILE FROM DIRECTORY IF FILE NOT ENCRYPTED OR CODECERROR
                if not(checked=="pass"):
                    os.remove(f"merge{chat_id}/{i}.pdf")
                i += 1
            directory = f'merge{chat_id}'
            pdfList = [os.path.join(directory, file) for file in os.listdir(directory)]
            # SORT DIRECTORY PATH BY ITS MODIFIED TIME
            pdfList.sort(key = os.path.getctime)
            numbPdf = len(pdfList)
            # MERGING STARTED
            await downloadMessage.edit(
                                      "__Merging Started.. __ 🪄"
                                      )
            output_pdf = f"merge{chat_id}/merge.pdf"
            #PyPDF 2
            merger=PdfFileMerger()
            for i in pdfList:
                merger.append(i)
            merger.write(output_pdf)
            
            # Getting thumbnail
            thumbnail, fileName = await thumbName(callbackQuery.message, fileNm)
            if PDF_THUMBNAIL != thumbnail:
                location = await bot.download_media(
                                        message = thumbnail,
                                        file_name = f"{callbackQuery.message.message_id}.jpeg"
                                        )
                thumbnail = await formatThumb(location)
            
            await downloadMessage.edit(
                                      "`Started Uploading..` 📤"
                                      )
            await callbackQuery.message.reply_chat_action(
                                                         "upload_document"
                                                         )
            c_time = time.time()
            # SEND DOCUMENT
            with open(output_pdf, "rb") as outPut:
                await askPDF.reply_document(
                                           file_name = fileName,
                                           quote = True,
                                           document = outPut,
                                           thumb = thumbnail,
                                           caption = "`merged pdf 🙂`",
                                           progress = uploadProgress,
                                           progress_args = (
                                                           downloadMessage,
                                                           c_time
                                                           )
                                           )
            await downloadMessage.delete()
            try:
                os.remove(location)
            except Exception: pass
            shutil.rmtree(f"merge{chat_id}")
            PROCESS.remove(chat_id)
            await footer(callbackQuery.message, False)
    except Exception as e:
        logger.exception(
                        "MERGE:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            shutil.rmtree(f"merge{chat_id}")
            PROCESS.remove(chat_id)
            os.remove(location)
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
