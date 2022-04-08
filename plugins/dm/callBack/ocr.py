# fileName : plugins/dm/callBack/ocr.py
# copyright ©️ 2021 nabilanavab

import os
import time
import fitz
import shutil
try:
    nabilanavab=False
    import ocrmypdf
except Exception:
    nabilanavab=True
from time import sleep
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram import Client as ILovePDF

#--------------->
#--------> LOCAL VARIABLES
#------------------->

PDF_THUMBNAIL=Config.PDF_THUMBNAIL

#--------------->
#--------> OCR PDF
#------------------->

ocrs=["ocr", "Kocr|"]
ocr=filters.create(lambda _, __, query: query.data.startswith(tuple(ocrs)))

@ILovePDF.on_callback_query(ocr)
async def _ocr(bot, callbackQuery):
    try:
        print('entered ocr')
        # CHECKS IF BOT DOING ANY WORK
        if nabilanavab==True:
            await callbackQuery.answer("Owner Restricted 😎🤏")
            return
        await callbackQuery.answer("Just add text layer to pdf😎🤏")
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer("Work in progress.. 🙇")
            return
        # CALLBACK DATA
        data=callbackQuery.data
        # ONLY SUPPORTS 5 IMAGES(DUE TO SERVER RESTRICTIONS)
        if data[0]=="K":
            _, number_of_pages=callbackQuery.data.split("|")
            if int(number_of_pages)>=5:
                await callbackQuery.answer("send a pdf file less than 5 pages` 🙄")
                return
        # ADD TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # DOWNLOAD MESSSAGE
        downloadMessage=await callbackQuery.message.reply_text(
            "`Downloding your pdf..` ⏳", quote=True
        )
        input_file=f"{callbackQuery.message.message_id}/inPut.pdf"
        file_id=callbackQuery.message.reply_to_message.document.file_id
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        fileNm=callbackQuery.message.reply_to_message.document.file_name
        fileNm, fileExt=os.path.splitext(fileNm)   # seperates name & extension
        
        # STARTED DOWNLOADING
        c_time=time.time()
        downloadLoc=await bot.download_media(
            message=file_id, file_name=input_file, progress=progress,
            progress_args=( fileSize, downloadMessage, c_time )
        )
        # CHECKS PDF DOWNLOADED OR NOT
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit("`Adding OCR layer..`🤌")
        # CHECK PDF OR NOT(HERE compressed, SO PG UNKNOWN)
        if data=="ocr":
            checked=await checkPdf(input_file, callbackQuery)
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
        else:
            with fitz.open(input_file) as ocrPdf:
                number_of_pages=ocrPdf.pageCount
                if int(number_of_pages)>5:
                    await downloadMessage.edit("__Send me a file less than 5 images__ 😅")
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f"{callbackQuery.message.message_id}")
                    return
        output_file=f"{callbackQuery.message.message_id}/ocr.pdf"
        try:
            ocrmypdf.ocr(
                input_file=open(
                    input_file, "rb"
                ),
                output_file=open(
                    output_file, "wb"
                ),
                deskew=True
            )
        except Exception as e:
            print(f"callback/ocr: {e}")
            await downloadMessage.edit("`Already Have A Text Layer.. `😏")
            shutil.rmtree(f"{callbackQuery.message.message_id}")
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await bot.send_chat_action(
            callbackQuery.message.chat.id, "upload_document"
        )
        await downloadMessage.edit("`Started Uploading..` 🏋️")
        await callbackQuery.message.reply_document(
            file_name=f"{fileNm}.pdf", quote=True,
            document=open(output_file, "rb"), thumb=PDF_THUMBNAIL,
            caption="`OCR PDF`"
        )
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("ocr: " , e)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
            PROCESS.remove(callbackQuery.message.chat.id)
        except Exception:
            pass

#                                                             Telegram: @nabilanavab
