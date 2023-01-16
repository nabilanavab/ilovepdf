# fileName : plugins/dm/callBack/merge.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/merge.py"

MERGE = {}
MERGEsize = {}

import os, time, asyncio, fitz

from plugins.render  import *
from plugins.work    import work
from logger          import logger
from pyromod         import listen
from pyrogram        import enums, filters
from configs.config  import images, settings
from pyrogram        import Client as ILovePDF
from plugins.util    import getLang, translate
from plugins.fncta   import thumbName, formatThumb

if settings.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * (10 ** 6)
else:
    MAX_FILE_SIZE = False

merge = filters.create(lambda _, __, query: query.data == "merge")

@ILovePDF.on_callback_query(merge)
async def _merge(bot, callbackQuery):
    try:
        chat_id = callbackQuery.message.chat.id
        lang_code = await getLang(chat_id)
        if await header(bot, callbackQuery, lang_code = lang_code):
            return
        
        CHUNK, cancel = await translate(text = "merge", button = "document['cancelCB']", lang_code = lang_code)
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer()
        
        fileNm = callbackQuery.message.reply_to_message.document.file_name
        _, fileExt = os.path.splitext(fileNm)        # seperates name & extension
        # ADDING FILE ID & SIZE TO MERGE, MERGEsize LIST (FOR FUTURE USE)
        MERGE[chat_id] = [callbackQuery.message.reply_to_message.document.file_id]
        MERGEsize[chat_id] = [callbackQuery.message.reply_to_message.document.file_size]
        
        # REQUEST FOR OTHER PDFS FOR MERGING
        nabilanavab = True; size = 0
        while(nabilanavab):
            if len(MERGE[chat_id]) >= 10:
                await callbackQuery.message.reply(CHUNK["load"], quote=True)
                nabilanavab = False
                break
            askPDF = await bot.ask(
                text = CHUNK["pyromodASK"].format(len(MERGE[chat_id])),
                chat_id = chat_id, reply_to_message_id = callbackQuery.message.id, filters = None
            )
            if askPDF.text == "/exit":
                await askPDF.reply(CHUNK["exit"], quote=True)
                await work(callbackQuery, "delete", False)
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
                    if (MAX_FILE_SIZE and MAX_FILE_SIZE_IN_kiB <= int(size)) or int(size) >= 2000000000:
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
            return await work(callbackQuery, "delete", False)
        
        # GET /merge, REACHES MAX FILE SIZE OR MAX NO OF PDF
        if nabilanavab == False:
            # DISPLAY TOTAL PDFS FOR MERGING
            dlMSG = await askPDF.reply_text(
                CHUNK["total"].format(len(MERGE[chat_id])),
                quote = True, reply_markup = cancel
            )
            await asyncio.sleep(.5); i = 0
            # ITERATIONS THROUGH FILE ID'S AND DOWNLOAD
            for iD in MERGE[chat_id]:
                await dlMSG.edit(
                    CHUNK["current"].format({i+1}), reply_markup = cancel
                )
                downloadLoc = await bot.download_media(
                    message = iD, file_name = f"{cDIR}/{i}.pdf",
                    progress = progress, progress_args = (
                        MERGEsize[chat_id][i], dlMSG, time.time()
                    )
                )
                # CHECKS PDF CODEC, ENCRYPTION..
                checked, noOfPg = await checkPdf(f"{cDIR}/{i}.pdf", callbackQuery)
                # REMOVE FILE FROM DIRECTORY IF FILE NOT ENCRYPTED OR CODECERROR
                if not(checked=="pass"):
                    os.remove(f"{cDIR}/{i}.pdf")
                i += 1
            
            directory = f'{cDIR}'
            pdfList = [os.path.join(directory, file) for file in os.listdir(directory)]
            # SORT DIRECTORY PATH BY ITS MODIFIED TIME
            pdfList.sort(key = os.path.getctime)
            numbPdf = len(pdfList)
            # MERGING STARTED
            await dlMSG.edit(CHUNK["started"], reply_markup = cancel)
            output_pdf = f"{cDIR}/merge.pdf"
            
            with fitz.open() as result:
                for pdf in pdfList:
                    with fitz.open(pdf) as mfile:
                        result.insert_pdf(mfile)
                result.save(output_pdf)
            
            FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, fileNm)
            if images.PDF_THUMBNAIL != THUMBNAIL:
                location = await bot.download_media(
                    message = THUMBNAIL,
                    file_name = f"{cDIR}/{callbackQuery.message.id}.jpeg"
                )
                THUMBNAIL = await formatThumb(location)
            
            await dlMSG.edit(CHUNK["upload"], reply_markup = cancel)
            if await work(callbackQuery, "check", False):
                await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                with open(output_pdf, "rb") as outPut:
                    await askPDF.reply_document(
                        file_name = FILE_NAME, quote = True, document = outPut, thumb = THUMBNAIL,
                        caption = f"{CHUNK['caption']}\n\n{FILE_CAPT}", progress = uploadProgress,
                        progress_args = ( dlMSG, time.time() )
                    )
            await dlMSG.delete()
            await work(callbackQuery, "delete", False)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)

# ==================================================================================================================================[ NABIL A NAVAB -> TG: nabilanavab]
