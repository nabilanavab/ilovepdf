# fileName : plugins/dm/callBack/preview.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )
logging.getLogger("PIL.Image").setLevel(logging.ERROR)

import os
import fitz
import time
import shutil
from PIL import Image
from pdf import PROCESS
from pyrogram import filters
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from plugins.footer import footer, header
from pyrogram.types import InputMediaPhoto

media = {}

#--------------->
#--------> PDF TO IMAGES
#------------------->

preview = filters.create(lambda _, __, query: query.data in ["Kpreview", "preview"])

# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(preview)
async def _preview(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.message_id
        
        # CHECK USER PROCESS
        if chat_id in PROCESS:
            return await callbackQuery.answer(
                                      "WORK IN PROGRESS.. 🙇")
        
        await callbackQuery.answer(
                                  "Send Some Random Pages with Metadata 😁"
                                  )
        # ↓ ADD TO PROCESS       ↓ CALLBACK DATA
        PROCESS.append(chat_id); data=callbackQuery.data
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        # DOWNLOAD MESSAGE
        downloadMessage = await callbackQuery.message.reply_text(
                                                                "`Downloding your pdf..` 📥", 
                                                                quote = True
                                                                )
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
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
        # CHECK DOWNLOAD COMPLETED/CANCELLED
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        # CHECK PDF CODEC, ENCRYPTION..
        if data != "Kpreview":
            checked, number_of_pages = await checkPdf(
                                                     input_file,
                                                     callbackQuery
                                                     )
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
        # OPEN PDF WITH FITZ
        doc = fitz.open(input_file)
        number_of_pages = doc.pageCount
        pglist = list(range(number_of_pages + 1))
        if number_of_pages <= 10:
            totalPgList = range(1, number_of_pages + 1)
            caption = f"PDF only have {number_of_pages} pages 🤓\n\n"
        elif number_of_pages % 2 == 1:
            totalPgList = pglist[1:4] + \
                          [(number_of_pages//2), (number_of_pages//2)+1, (number_of_pages//2)+2] + \
                          pglist[-3:number_of_pages+1]
            caption = f"PDF pages: {totalPgList}\n\n"
        elif number_of_pages % 2 == 0:
            totalPgList = pglist[1:4] + \
                          [(number_of_pages//2)-1, (number_of_pages//2), (number_of_pages//2)+1, (number_of_pages//2)+2] + \
                          pglist[-3:number_of_pages+1]
            caption = f"PDF pages: {totalPgList}\n\n"
        await downloadMessage.edit(
                                  f"`Total pages: {len(totalPgList)}..` 🤌"
                                  )
        
        metaData = doc.metadata
        if metaData != None:
            for i in metaData:
                if metaData[i] != "":
                    caption += f"`{i}: {metaData[i]}`\n"
        
        zoom = 2
        mat = fitz.Matrix(
                         zoom, zoom
                         )
        os.mkdir(f'{message_id}/pgs')
        for pageNo in totalPgList:
            page = doc.loadPage(int(pageNo) - 1)
            pix = page.getPixmap(matrix = mat)
            # SAVING PREVIEW IMAGE
            with open(
                f'{message_id}/pgs/{pageNo}.jpg','wb'
            ):
                pix.writePNG(f'{message_id}/pgs/{pageNo}.jpg')
        try:
            await downloadMessage.edit(
                                      f"`Preparing an Album..` 🤹"
                                      )
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
                    picture.save(
                                file,
                                "JPEG",
                                optimize = True,
                                quality = qualityRate
                                )
                    qualityRate -= 5
                # ADDING TO GROUP MEDIA IF POSSIBLE
                else:
                    if len(media[chat_id]) == 1:
                        media[chat_id].append(
                                             InputMediaPhoto(
                                                            media = file,
                                                            caption = caption
                                                            )
                                             )
                    else:
                        media[chat_id].append(
                                             InputMediaPhoto(
                                                            media = file)
                                                            )
                    break
        await downloadMessage.edit(
                                  f"`Uploading: preview pages.. 🐬`"
                                  )
        await callbackQuery.message.reply_chat_action(
                                                     "upload_photo"
                                                     )
        await callbackQuery.message.reply_media_group(
                                                     media[chat_id], quote = True
                                                     )
        await downloadMessage.delete()
        doc.close; del media[chat_id]
        PROCESS.remove(chat_id)
        shutil.rmtree(f'{message_id}')
    except Exception as e:
        logger.exception(
                        "PREVIEW:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            PROCESS.remove(chat_id)
            await downloadMessage.edit(
                                      f"SOMETHING WENT WRONG"
                                      f"\n\nERROR: {e}")
            shutil.rmtree(f'{message_id}')
        except Exception: pass


#                                                                                                      Telegram: @nabilanavab
