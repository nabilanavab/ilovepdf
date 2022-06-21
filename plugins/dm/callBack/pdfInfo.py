# fileName : plugins/dm/Callback/pdfInfo.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import fitz
import time
import shutil
from pdf import PROCESS
from pyrogram import filters
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from plugins.footer import footer, header
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`What shall do with this file.?`

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️"""

encryptedMsg = """`FILE IS ENCRYPTED` 🔐

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️"""

#--------------->
#--------> PDF META DATA
#------------------->

pdfInfo = filters.create(lambda _, __, query: query.data == "pdfInfo")

@ILovePDF.on_callback_query(pdfInfo)
async def _pdfInfo(bot, callbackQuery):
    try:
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.message_id
        
        # CB MESSAGE DELETES IF USER DELETED PDF
        if await header(bot, callbackQuery):
            return
        
        # CHECKS PROCESS
        if chat_id in PROCESS:
            return await callbackQuery.answer(
                                             "WORK IN PROGRESS.. 🙇"
                                             )
        
        # ADD TO PROCESS
        PROCESS.append(chat_id)
        
        # DOWNLOADING STARTED
        downloadMessage = await callbackQuery.edit_message_text(
                                                               "`Downloding your pdf..` 📥", 
                                                               )
        pdf_path = f"{message_id}/pdfInfo.pdf"
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
        c_time = time.time()
        downloadLoc = await bot.download_media(
                                              message = file_id,
                                              file_name = pdf_path,
                                              progress = progress,
                                              progress_args = (
                                                              fileSize,
                                                              downloadMessage,
                                                              c_time
                                                              )
                                              )
        # CHECKS IS DOWNLOADING COMPLETED OR PROCESS CANCELED
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        
        # OPEN FILE WITH FITZ
        with fitz.open(pdf_path) as pdf:
            isPdf = pdf.is_pdf
            metaData = pdf.metadata
            isEncrypted = pdf.is_encrypted
            number_of_pages = pdf.pageCount
            # CHECKS IF FILE ENCRYPTED
            if isPdf and isEncrypted:
                pdfMetaData = f"\nFile Encrypted 🔐\n"
            if isPdf and not(isEncrypted):
                pdfMetaData = "\n"
            # ADD META DATA TO pdfMetaData STRING
            if metaData != None:
                for i in metaData:
                    if metaData[i] != "":
                        pdfMetaData += f"`{i}: {metaData[i]}`\n"
            fileName = callbackQuery.message.reply_to_message.document.file_name
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            if isPdf and not(isEncrypted):
                editedPdfReplyCb = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⭐ META£ATA ⭐",
                                 callback_data=f"KpdfInfo|{number_of_pages}"),
                            InlineKeyboardButton("🗳️ PREVIEW 🗳️",
                                                   callback_data=f"Kpreview"),
                        ],[
                            InlineKeyboardButton("🖼️ toIMAGES 🖼️",
                                 callback_data=f"KtoImage|{number_of_pages}"),
                            InlineKeyboardButton("✏️ toTEXT ✏️",
                                  callback_data=f"KtoText|{number_of_pages}")
                        ],[
                            InlineKeyboardButton("🔐 ENCRYPT 🔐",
                                 callback_data=f"Kencrypt|{number_of_pages}"),
                            InlineKeyboardButton("🔒 DECRYPT 🔓",
                                               callback_data=f"notEncrypted")
                        ],[
                            InlineKeyboardButton("🗜️ COMPRESS 🗜️",
                                                  callback_data=f"Kcompress"),
                            InlineKeyboardButton("🤸 ROTATE 🤸",
                                  callback_data=f"Krotate|{number_of_pages}")
                        ],[
                            InlineKeyboardButton("✂️ SPLIT ✂️",
                                   callback_data=f"Ksplit|{number_of_pages}"),
                            InlineKeyboardButton("🧬 MERGE 🧬",
                                                       callback_data="merge")
                        ],[
                            InlineKeyboardButton("™️ STAMP ™️",
                                   callback_data=f"Kstamp|{number_of_pages}"),
                            InlineKeyboardButton("✏️ RENAME ✏️",
                                                      callback_data="rename")
                        ],[
                            InlineKeyboardButton("📝 OCR 📝",
                                     callback_data=f"Kocr|{number_of_pages}"),
                            InlineKeyboardButton("🥷 A4 FORMAT 🥷",
                                  callback_data=f"Kformat|{number_of_pages}")
                        ],[
                            InlineKeyboardButton("🚫 CLOSE 🚫",
                                                    callback_data="closeALL")
                        ]
                    ]
                )
                await callbackQuery.edit_message_text(
                                                     pdfInfoMsg.format(
                                                                      fileName,
                                                                      await gSF(fileSize),
                                                                      number_of_pages
                                                                      ) + pdfMetaData,
                                                     reply_markup = editedPdfReplyCb
                                                     )
            elif isPdf and isEncrypted:
                await callbackQuery.edit_message_text(
                                                     encryptedMsg.format(
                                                                        fileName,
                                                                        await gSF(fileSize),
                                                                        number_of_pages
                                                                        ) + pdfMetaData,
                                                     reply_markup=InlineKeyboardMarkup(
                                                           [[
                                                                 InlineKeyboardButton("🔓 DECRYPT 🔓",
                                                                              callback_data="decrypt")
                                                           ],[
                                                                 InlineKeyboardButton("🚫 CLOSE 🚫",
                                                                           callback_data="closeALL")
                                                           ]]
                                                     ))
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
            await footer(callbackQuery.message, False)
    
    # EXCEPTION DURING FILE OPENING
    except Exception as e:
        logger.exception(
                        "METADATA[PDF_INFO]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            await callbackQuery.edit_message_text(
                                                 f"SOMETHING went WRONG.. 🐉"
                                                 f"\n\nERROR: {e}",
                                                 reply_markup = InlineKeyboardMarkup(
                                                       [[
                                                             InlineKeyboardButton("❌ Error in file ❌",
                                                                                 callback_data=f"error")
                                                       ],[
                                                             InlineKeyboardButton("🚫 CLOSE 🚫",
                                                                       callback_data="closeALL")
                                                       ]]
                                                  ))
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
        except Exception:
            pass

#                                                                                              Telegram: @nabilanavab
