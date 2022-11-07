# fileName : plugins/dm/callBack/merge.py
# copyright ©️ 2021 nabilanavab

MERGE = {}
MERGEsize = {}

import fitz
from pdf import PROCESS
from logger import logger
from pyromod import listen
from plugins.render import *
import os, time, shutil, asyncio
from pyrogram import enums, filters
from pyrogram import Client as ILovePDF
from configs.config import images, settings
from plugins.util import getLang, translate
from plugins.thumbName import thumbName, formatThumb

if settings.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * (10 ** 6)
else:
    MAX_FILE_SIZE = False

merge = filters.create(lambda _, __, query: query.data == "merge")
@ILovePDF.on_callback_query(merge)
async def _merge(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        CHUNK, cancel = await translate(text="merge", button="document['cancelCB']", lang_code=lang_code)
        
        if await header(bot, callbackQuery):
            return
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.id
        
        # CHECK IF BOT DOING ANY WORK
        if chat_id in PROCESS:
            return await callbackQuery.answer(CHUNK["inWork"])
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
                await callbackQuery.message.reply(CHUNK["load"], quote=True)
                nabilanavab = False
                break
            askPDF = await bot.ask(
                text = CHUNK["pyromodASK"].format(len(MERGE[chat_id])),
                chat_id = chat_id, reply_to_message_id = message_id, filters = None
            )
            if askPDF.text == "/exit":
                await askPDF.reply(CHUNK["exit"], quote=True)
                PROCESS.remove(chat_id)
                del MERGE[chat_id]
                del MERGEsize[chat_id]
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
                            CHUNK["sizeLoad"] %(MAX_FILE_SIZE if MAX_FILE_SIZE else "1.8Gb")
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
                CHUNK["total"].format(len(MERGE[chat_id])),
                quote = True, reply_markup = cancel
            )
            await asyncio.sleep(.5); i = 0
            # ITERATIONS THROUGH FILE ID'S AND DOWNLOAD
            for iD in MERGE[chat_id]:
                await downloadMessage.edit(CHUNK["current"].format({i+1}), reply_markup=cancel)
                downloadLoc = await bot.download_media(
                    message = iD, file_name = f"merge{chat_id}/{i}.pdf",
                    progress = progress, progress_args = (
                        MERGEsize[chat_id][i], downloadMessage, time.time()
                    )
                )
                # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
                if downloadLoc is None:
                    PROCESS.remove(chat_id)
                    await callbackQuery.message.reply_text(CHUNK["cancel"], quote=True)
                    shutil.rmtree(f"merge{chat_id}")
                    return
                # CHECKS PDF CODEC, ENCRYPTION..
                checked, noOfPg = await checkPdf(f"merge{chat_id}/{i}.pdf", callbackQuery)
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
            await downloadMessage.edit(CHUNK["started"], reply_markup=cancel)
            output_pdf = f"merge{chat_id}/merge.pdf"
            
            with fitz.open() as result:
                for pdf in pdfList:
                    with fitz.open(pdf) as mfile:
                        result.insert_pdf(mfile)
                result.save(output_pdf)
            
            FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, fileNm)
            if images.PDF_THUMBNAIL != THUMBNAIL:
                location = await bot.download_media(message = THUMBNAIL, file_name = f"{callbackQuery.message.id}.jpeg")
                THUMBNAIL = await formatThumb(location)
            
            await downloadMessage.edit(CHUNK["upload"], reply_markup=cancel)
            if chat_id in PROCESS:
                await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                with open(output_pdf, "rb") as outPut:
                    await askPDF.reply_document(
                        file_name = FILE_NAME, quote = True, document = outPut, thumb = THUMBNAIL,
                        caption = f"{CHUNK['caption']}\n\n{FILE_CAPT}", progress = uploadProgress,
                        progress_args = ( downloadMessage, time.time() )
                    )
            await downloadMessage.delete()
            try:
                os.remove(location)
            except Exception: pass
            shutil.rmtree(f"merge{chat_id}")
            PROCESS.remove(chat_id)
    except Exception as e:
        logger.exception("plugins/dm/callBack/merge: %s" %(e), exc_info=True)
        try:
            shutil.rmtree(f"merge{chat_id}")
            PROCESS.remove(chat_id); os.remove(location)
        except Exception:
            pass

# ==================================================================================================================================[ NABIL A NAVAB -> TG: nabilanavab]
