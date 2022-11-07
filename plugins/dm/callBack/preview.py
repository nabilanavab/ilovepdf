# fileName : plugins/dm/callBack/preview.py
# copyright ©️ 2021 nabilanavab

media = {}

from PIL import Image
from logger import logger
from plugins.util import *
import shutil, os, fitz, time
from pdf import PROCESS, pyTgLovePDF
from pyrogram import enums, filters
from pyrogram import Client as ILovePDF
from telebot.types import InputMediaPhoto
from plugins.render import header, checkPdf, progress

preview = filters.create(lambda _, __, query: query.data in ["preview"])
@ILovePDF.on_callback_query(preview)
async def _preview(bot, callbackQuery):
    try:
        chat_id = callbackQuery.message.chat.id
        lang_code = await getLang(callbackQuery.message.chat.id)
        CHUNK, _ = await translate(text="preview", button="document['cancelCB']", lang_code=lang_code)
        if await header(bot, callbackQuery):
            return
        
        message_id = callbackQuery.message.id
        if chat_id in PROCESS:
            return await callbackQuery.answer(CHUNK["inWork"])
        
        await callbackQuery.answer(CHUNK["process"])
        # ↓ ADD TO PROCESS
        PROCESS.append(chat_id)
        
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        # DOWNLOAD MESSAGE
        downloadMessage = await callbackQuery.message.reply_text(CHUNK["download"], reply_markup=_, quote=True)
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
        downloadLoc = await bot.download_media(
            message = file_id, file_name = input_file, progress = progress,
             progress_args = (fileSize, downloadMessage, time.time())
        )
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        if "•" not in  callbackQuery.message.text:
            checked, number_of_pages = await checkPdf(input_file, callbackQuery)
            if checked != "pass":
                return await downloadMessage.delete()
        with fitz.open(input_file) as doc:
            number_of_pages = doc.page_count
            pglist = list(range(number_of_pages + 1))
            if number_of_pages <= 10:
                totalPgList = range(1, number_of_pages + 1)
                caption = CHUNK["_"].format(number_of_pages)
            elif number_of_pages % 2 == 1:
                totalPgList = pglist[1:4] + \
                              [(number_of_pages//2), (number_of_pages//2)+1, (number_of_pages//2)+2] + \
                              pglist[-3:number_of_pages+1]
                caption = CHUNK["__"].format(totalPgList)
            elif number_of_pages % 2 == 0:
                totalPgList = pglist[1:4] + \
                              [(number_of_pages//2)-1, (number_of_pages//2), (number_of_pages//2)+1, (number_of_pages//2)+2] + \
                              pglist[-3:number_of_pages+1]
                caption = CHUNK["__"].format(totalPgList)
            await downloadMessage.edit(CHUNK["total"].format(totalPgList), reply_markup=_)
            
            metaData = doc.metadata
            if metaData != None:
                for i in metaData:
                    if metaData[i] != "":
                        caption += f"`{i}: {metaData[i]}`\n"
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            os.mkdir(f'{message_id}/pgs')
            for pageNo in totalPgList:
                page = doc.load_page(int(pageNo) - 1)
                pix = page.get_pixmap(matrix = mat)
                # SAVING PREVIEW IMAGE
                with open(f'{message_id}/pgs/{pageNo}.jpg','wb'):
                    pix.save(f'{message_id}/pgs/{pageNo}.jpg')
        try:
            await downloadMessage.edit(CHUNK["album"], reply_markup=_)
        except Exception: pass
        directory = f'{message_id}/pgs'
        # RELATIVE PATH TO ABS. PATH
        imag = [os.path.join(directory, file) for file in os.listdir(directory)]
        # SORT FILES BY MODIFIED TIME
        imag.sort(key = os.path.getctime)
        # LIST TO SAVE GROUP IMAGE OBJ.
        media[chat_id] = []
        for file in imag:
            # COMPRESSION QUALITY
            qualityRate = 95
            # JUST AN INFINITE LOOP
            for i in range(200):
                # print("size: ",file, " ",os.path.getsize(file)) LOG MESSAGE
                # FILES WITH 10MB+ SIZE SHOWS AN ERROR FROM TELEGRAM 
                # SO COMPRESS UNTIL IT COMES LESS THAN 10MB.. :(
                if os.path.getsize(file) >= 1000000:
                    picture = Image.open(file)
                    picture.save(file, "JPEG", optimize = True, quality = qualityRate)
                    qualityRate -= 5
                # ADDING TO GROUP MEDIA IF POSSIBLE
                else:
                    if len(media[chat_id]) == 1:
                        media[chat_id].append(InputMediaPhoto(media=open(file, "rb"), caption=caption, parse_mode="Markdown"))
                    else:
                        media[chat_id].append(InputMediaPhoto(media=open(file, "rb")))
                    break
        if chat_id in PROCESS:
            await downloadMessage.edit(CHUNK["upload"], reply_markup=_)
            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
            await pyTgLovePDF.send_media_group(chat_id, media[chat_id], reply_to_message_id=message_id)
        await downloadMessage.delete(); del media[chat_id]
        PROCESS.remove(chat_id); shutil.rmtree(f'{message_id}')
    except Exception as e:
        logger.exception("plugins/dm/callBack/preview: %s" %(e), exc_info=True)
        try:
            PROCESS.remove(chat_id)
            await downloadMessage.edit(CHUNK["error"].format(e), reply_markup=_)
            shutil.rmtree(f'{message_id}')
        except Exception: pass

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
