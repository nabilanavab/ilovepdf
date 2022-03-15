# fileName : plugins/dm/callBack/compress.py
# copyright ©️ 2021 nabilanavab

import os
import time
import shutil
from time import sleep
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet

#--------------->
#--------> LOCAL VARIABLES
#------------------->

compressedCaption = """`Original Size : {}
Compressed Size : {}

Ratio : {:.2f} %`"""

PDF_THUMBNAIL=Config.PDF_THUMBNAIL

#--------------->
#--------> PDF COMPRESSION
#------------------->

compress = filters.create(lambda _, __, query: query.data in ["compress", "Kcompress"])

@ILovePDF.on_callback_query(compress)
async def _compress(bot, callbackQuery):
    try:
        # CHECKS IF BOT DOING ANY WORK
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress.. 🙇"
            )
            return
        # ADD TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # CALLBACK DATA
        data = callbackQuery.data
        # DOWNLOAD MESSSAGE
        downloadMessage = await callbackQuery.message.reply_text(
            "`Downloding your pdf..` ⏳", quote=True
        )
        input_file=f"{callbackQuery.message.message_id}/inCompress.pdf"
        output_file = f"{callbackQuery.message.message_id}/compressed.pdf"
        file_id=callbackQuery.message.reply_to_message.document.file_id
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        fileNm=callbackQuery.message.reply_to_message.document.file_name
        fileNm, fileExt=os.path.splitext(fileNm)        # seperates name & extension
        
        # STARTED DOWNLOADING
        c_time=time.time()
        downloadLoc=await bot.download_media(
            message=file_id,
            file_name=input_file,
            progress=progress,
            progress_args=(
                fileSize,
                downloadMessage,
                c_time
            )
        )
        # CHECKS PDF DOWNLOADED OR NOT
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit(
            "`Started Compressing..` 🗜️"
        )
        # CHECK PDF OR NOT(HERE compressed, SO PG UNKNOWN)
        if data == "compress":
            checked=await checkPdf(input_file, callbackQuery)
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
        # Initialize the library
        PDFNet.Initialize()
        doc = PDFDoc(input_file)
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and
        # compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(
            output_file, SDFDoc.e_linearized
        )
        doc.Close()
        
        # FILE SIZE COMPARISON (RATIO)
        initialSize=os.path.getsize(input_file)
        compressedSize=os.path.getsize(output_file)
        ratio=(1 - (compressedSize/initialSize)) * 100
        await bot.send_chat_action(
            callbackQuery.message.chat.id, "upload_document"
        )
        await downloadMessage.edit(
            "`Started Uploading..` 🏋️"
        )
        await callbackQuery.message.reply_document(
            file_name=f"{fileNm}.pdf", quote=True,
            document=open(output_file, "rb"),
            thumb=PDF_THUMBNAIL,
            caption=compressedCaption.format(
                await gSF(initialSize), await gSF(compressedSize), ratio
            )
        )
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("Compress: " , e)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
            PROCESS.remove(callbackQuery.message.chat.id)
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
