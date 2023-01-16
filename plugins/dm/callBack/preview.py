# fileName : plugins/dm/callBack/preview.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/preview.py"

media = {}

import os, fitz, time
from plugins.util   import *
from plugins.work   import work
from PIL            import Image
from asyncio        import sleep
from logger         import logger
from pdf            import pyTgLovePDF
from pyrogram       import enums, filters
from telebot.types  import InputMediaPhoto
from pyrogram       import Client as ILovePDF
from plugins.render import header, checkPdf, progress

preview = filters.create(lambda _, __, query: query.data == "preview")

@ILovePDF.on_callback_query(preview)
async def _preview(bot, callbackQuery):
    try:
        chat_id = callbackQuery.message.chat.id
        lang_code = await getLang(chat_id)
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        CHUNK, _ = await translate(text="preview", button="document['cancelCB']", lang_code=lang_code)
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        dlMSG = await callbackQuery.message.reply_text(
            CHUNK["download"], reply_markup = _, quote = True
        )
        downloadLoc = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = progress,
            progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )
        if os.path.getsize(downloadLoc) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        if "•" not in  callbackQuery.message.text:
            checked, numOfPgs = await checkPdf(f"{cDIR}/inPut.pdf", callbackQuery)
            if checked != "pass":
                return await dlMSG.delete()
        
        with fitz.open(f"{cDIR}/inPut.pdf") as doc:
            numOfPgs = doc.page_count
            pglist = list(range(numOfPgs + 1))
            if numOfPgs <= 10:
                totalPgList = range(1, numOfPgs + 1)
                caption = CHUNK["_"].format(numOfPgs)
            elif numOfPgs % 2 == 1:
                totalPgList = pglist[1:4] + \
                              [(numOfPgs//2), (numOfPgs//2)+1, (numOfPgs//2)+2] + \
                              pglist[-3:numOfPgs+1]
                caption = CHUNK["__"].format(totalPgList)
            elif numOfPgs % 2 == 0:
                totalPgList = pglist[1:4] + \
                              [(numOfPgs//2)-1, (numOfPgs//2), (numOfPgs//2)+1, (numOfPgs//2)+2] + \
                              pglist[-3:numOfPgs+1]
                caption = CHUNK["__"].format(totalPgList)
            await dlMSG.edit(CHUNK["total"].format(totalPgList), reply_markup=_)
            
            metaData = doc.metadata
            if metaData != None:
                for i in metaData:
                    if metaData[i] != "":
                        caption += f"`{i}: {metaData[i]}`\n"
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            os.mkdir(f'{cDIR}/pgs')
            for pageNo in totalPgList:
                page = doc.load_page(int(pageNo) - 1)
                pix = page.get_pixmap(matrix = mat)
                # SAVING PREVIEW IMAGE
                with open(f'{cDIR}/pgs/{pageNo}.jpg','wb'):
                    pix.save(f'{cDIR}/pgs/{pageNo}.jpg')
        
        await dlMSG.edit(CHUNK["album"], reply_markup = _)
        directory = f'{cDIR}/pgs'
        # RELATIVE PATH TO ABS. PATH
        imag = [os.path.join(directory, file) for file in os.listdir(directory)]
        # SORT FILES BY MODIFIED TIME
        imag.sort(key = os.path.getctime)
        # LIST TO SAVE GROUP IMAGE OBJ.
        media[chat_id] = []
        for file in imag:
            await sleep(0.5)
            # COMPRESSION QUALITY
            qualityRate = 95
            # JUST AN INFINITE LOOP
            for i in range(200):
                # print("size: ",file, " ",os.path.getsize(file)) LOG MESSAGE
                # FILES WITH 10MB+ SIZE SHOWS AN ERROR FROM TELEGRAM 
                # SO COMPRESS UNTIL IT COMES LESS THAN 10MB.. :(
                if os.path.getsize(file) >= 1000000:
                    picture = Image.open(file)
                    picture.save(
                        file, "JPEG", optimize = True, quality = qualityRate
                    )
                    qualityRate -= 5
                # ADDING TO GROUP MEDIA IF POSSIBLE
                else:
                    if len(media[chat_id]) == 1:
                        media[chat_id].append(
                            InputMediaPhoto(
                                media = open(file, "rb"),
                                caption = caption, parse_mode = "Markdown"
                                )
                            )
                    else:
                        media[chat_id].append(
                            InputMediaPhoto(media = open(file, "rb"))
                            )
                    break
        if await work(callbackQuery, "check", False):
            await dlMSG.edit(CHUNK["upload"], reply_markup = _)
            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
            await pyTgLovePDF.send_media_group(
                chat_id, media[chat_id], reply_to_message_id = callbackQuery.message.id
            )
        await dlMSG.delete(); del media[chat_id]
        await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)
        await dlMSG.edit(CHUNK["error"].format(e), reply_markup = _)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
