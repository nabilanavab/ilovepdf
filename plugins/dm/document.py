# fileName : plugins/dm/document.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import fitz
import time
import shutil
import asyncio
import convertapi
from PIL import Image
from time import sleep
from pdf import PROCESS
from pyrogram import filters
from configs.dm import Config
from pdf import PDF, invite_link
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from pyrogram import Client as ILovePDF
from plugins.footer import footer, header
from plugins.fileSize import get_size_format as gSF
from plugins.progress import progress, uploadProgress
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from configs.images import WELCOME_PIC, BANNED_PIC, BIG_FILE, PDF_THUMBNAIL

#--------------->
#--------> convertAPI INSTANCE
#------------------->

if Config.CONVERT_API is not None:
    convertapi.api_secret = Config.CONVERT_API

#--------------->
#--------> MAXIMUM FILE SIZE (IF IN config var.)
#------------------->

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * (10 **6 )
else:
    MAX_FILE_SIZE = False

#--------------->
#--------> FILES TO PDF [SUPPORTED CODECS]
#------------------->

suprtedFile = [
    ".jpg", ".jpeg", ".png"
]                                       # Img to pdf file support

suprtedPdfFile = [
    ".epub", ".xps", ".oxps",
    ".cbz", ".fb2"
]                                      # files to pdf (zero limits)

suprtedPdfFile2 = [
    ".csv", ".doc", ".docx", ".dot",
    ".dotx", ".log", ".mpp", ".mpt",
    ".odt", ".pot", ".potx", ".pps",
    ".ppsx", ".ppt", ".pptx", ".pub",
    ".rtf", ".txt", ".vdx", ".vsd",
    ".vsdx", ".vst", ".vstx", ".wpd",
    ".wps", ".wri", ".xls", ".xlsb",
    ".xlsx", ".xlt", ".xltx", ".xml"
]                                       # file to pdf (ConvertAPI limit)

#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfReplyMsg = """`What shall i do with this file.?`

File Name : `{}`
File Size : `{}`"""

bigFileUnSupport = """Due to Overload, Owner limits {}mb for pdf files 🙇

`please Send me a file less than {}mb Size` 🙃"""

imageAdded = """`Added {} page/'s to your pdf..`🤓

fileName: `{}.pdf`"""

errorEditMsg = """Something went wrong..😐

ERROR: `{}`

For bot updates join @ilovepdf_bot"""

forceSubMsg = """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only Channel Members Can Use this Bot 🚶

This Means You Need To Join The Below Mentioned Channel for Using Me!

hit on "retry ♻️" after joining.. 😅"""

pdfReply = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⭐ META£ATA ⭐", callback_data="pdfInfo"),
            InlineKeyboardButton("🗳️ PREVIEW 🗳️", callback_data="preview")
        ],[
            InlineKeyboardButton("🖼️ IMAGES 🖼️", callback_data="toImage"),
            InlineKeyboardButton("✏️ TEXT ✏️", callback_data="toText")
        ],[
            InlineKeyboardButton("🔐 ENCRYPT 🔐", callback_data="encrypt"),
            InlineKeyboardButton("🔒 DECRYPT 🔓",callback_data="decrypt")
        ],[
            InlineKeyboardButton("🗜️ COMPRESS 🗜️", callback_data="compress"),
            InlineKeyboardButton("🤸 ROTATE 🤸", callback_data="rotate")
        ],[
            InlineKeyboardButton("✂️ SPLIT ✂️", callback_data="split"),
            InlineKeyboardButton("🧬 MERGE 🧬", callback_data="merge")
        ],[
            InlineKeyboardButton("™️ STAMP ™️", callback_data="stamp"),
            InlineKeyboardButton("✏️ RENAME ✏️", callback_data="rename")
        ],[
            InlineKeyboardButton("📝 OCR 📝", callback_data="ocr"),
            InlineKeyboardButton("🥷 A4 FORMAT 🥷", callback_data="format")
        ],[
            InlineKeyboardButton("🚫 CLOSE 🚫", callback_data="closeALL")
        ]]
    )

UPDATE_CHANNEL = Config.UPDATE_CHANNEL

#--------------->
#--------> REPLY TO DOCUMENTS/FILES
#------------------->

asNewDoc = filters.create(lambda _, __, query: query.data == "asnewDoc")

@ILovePDF.on_message(
                    ~filters.edited &
                    filters.private &
                    filters.incoming &
                    filters.document
                    )
async def documents(bot, message):
    try:
        global invite_link
        try: await message.reply_chat_action(
                                            "typing")
        except Exception: pass
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                userStatus = await bot.get_chat_member(
                                                      str(UPDATE_CHANNEL),
                                                      message.from_user.id
                                                      )
                # IF USER BANNED FROM CHANNEL
                if userStatus.status == 'banned':
                     await message.reply_photo(
                                         photo = BANNED_PIC,
                                         caption = "For Some Reason You Can't Use This Bot"
                                                  "\n\nContact Bot Owner 🤐",
                                         reply_markup = InlineKeyboardMarkup(
                                             [[InlineKeyboardButton("Owner 🎊",
                                              url = "https://t.me/nabilanavab")]]
                                         ))
                     return
            except Exception:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
                                         int(UPDATE_CHANNEL)
                                         )
                await message.reply_photo(
                                    photo = WELCOME_PIC, quote = True,
                                    caption = forceSubMsg.format(
                                                                message.from_user.first_name,
                                                                message.from_user.id
                                                                ),
                                    reply_markup = InlineKeyboardMarkup(
                                         [[
                                               InlineKeyboardButton("🌟 JOIN CHANNEL 🌟",
                                                             url=invite_link.invite_link)
                                         ],[
                                               InlineKeyboardButton("Refresh ♻️",
                                                      callback_data="refreshDoc")
                                         ]]
                                    ))
                return
        
        if message.from_user.id in PROCESS:
            return await message.reply(
                                      "WORK IN PROGRESS 🙇", quote = True,
                                      reply_markup = InlineKeyboardMarkup(
                                          [[
                                              InlineKeyboardButton("♻️ Try Again ♻️",
                                                            callback_data="asnewDoc")
                                          ]]
                                      ))
        isPdfOrImg = message.document.file_name        # file name
        fileSize = message.document.file_size          # file size
        fileNm, fileExt = os.path.splitext(isPdfOrImg) # seperate name & extension
        
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            await message.reply_photo(
                                photo = BIG_FILE,
                                caption = bigFileUnSupport.format(
                                        MAX_FILE_SIZE, MAX_FILE_SIZE
                                ),
                                reply_markup = InlineKeyboardMarkup(
                                     [[
                                          InlineKeyboardButton("💎 Create 2Gb Support Bot 💎",
                                                url="https://github.com/nabilanavab/ilovepdf")
                                     ]]
                                ))
            return
        
        # IMAGE AS FILES (ADDS TO PDF FILE)
        elif fileExt.lower() in suprtedFile:
            try:
                imageDocReply = await message.reply_text(
                                                        "`Downloading your Image..⏳`",
                                                        quote = True
                                                        )
                if not isinstance(PDF.get(message.from_user.id), list):
                    PDF[message.from_user.id] = []
                await message.download(
                      f"{message.from_user.id}/{message.from_user.id}.jpg"
                      )
                img = Image.open(
                                f"{message.from_user.id}/{message.from_user.id}.jpg"
                ).convert("RGB")
                PDF[message.from_user.id].append(img)
                await imageDocReply.edit(
                                        imageAdded.format(
                                                         len(PDF[message.from_user.id]),
                                                         message.from_user.id
                                                         ),
                                        reply_markup = InlineKeyboardMarkup(
                                                                           [[
                                                                               InlineKeyboardButton(
                                                                                                   "GENERATE 📚",
                                                                                                   callback_data="generate"
                                                                                                   ),
                                                                               InlineKeyboardButton(
                                                                                                   "RENAME ✍️",
                                                                                                   callback_data="generateREN"
                                                                                                   )
                                                                           ]]
                                                       )
                                        )
            except Exception as e:
                await imageDocReply.edit(
                                        errorEditMsg.format(e)
                                        )
        
        # REPLY TO .PDF FILE EXTENSION
        elif fileExt.lower() == ".pdf":
            pdfMsgId = await message.reply_text(
                                               "⚙️ Processing.",
                                               quote = True
                                               )
            await asyncio.sleep(0.5)
            await pdfMsgId.edit("⚙️ Processing..")
            await asyncio.sleep(0.5)
            await pdfMsgId.edit(
                               text = pdfReplyMsg.format(
                                                        isPdfOrImg,
                                                        await gSF(fileSize)
                               ),
                               reply_markup = pdfReply
                               )
            await footer(message, message)
        
        # FILES TO PDF (PYMUPDF/FITZ)
        elif fileExt.lower() in suprtedPdfFile:
            try:
                PROCESS.append(message.from_user.id)
                pdfMsgId = await message.reply_text(
                                                   "`Downloading your file..` 📥",
                                                   quote = True
                                                   )
                input_file = f"{message.message_id}/{isPdfOrImg}"
                # DOWNLOAD PROGRESS
                c_time = time.time()
                downloadLoc = await bot.download_media(
                                                      message = message.document.file_id,
                                                      file_name = input_file,
                                                      progress = progress,
                                                      progress_args = (
                                                                      message.document.file_size,
                                                                      pdfMsgId,
                                                                      c_time
                                                                      )
                                                      )
                # CHECKS PDF DOWNLOADED OR NOT
                if downloadLoc is None:
                    PROCESS.remove(chat_id)
                    return
                
                await pdfMsgId.edit(
                                   "`Work in Progress..`\nIt might take some time.. 💛`"
                                   )
                Document = fitz.open(input_file)
                b = Document.convert_to_pdf()
                pdf = fitz.open("pdf", b)
                pdf.save(
                        f"{message.message_id}/{fileNm}.pdf",
                        garbage = 4,
                        deflate = True,
                        )
                pdf.close()
                
                # Getting thumbnail
                thumbnail, fileName = await thumbName(message, isPdfOrImg)
                if PDF_THUMBNAIL != thumbnail:
                    await bot.download_media(
                                            message = thumbnail,
                                            file_name = f"{message.message_id}/thumbnail.jpeg"
                                            )
                    thumbnail = await formatThumb(f"{message.message_id}/thumbnail.jpeg")
                
                await pdfMsgId.edit(
                                   "`Started Uploading..`📤"
                                   )
                await message.reply_chat_action(
                                               "upload_document"
                                               )
                c_time = time.time()
                logFile = await message.reply_document(
                                            file_name = f"{fileName}.pdf",
                                            document = open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                                            thumb = thumbnail,
                                            caption = f"`Converted: {fileExt} to pdf`",
                                            quote = True,
                                            progress = uploadProgress,
                                            progress_args = (
                                                            pdfMsgId,
                                                            c_time
                                                            )
                                            )
                await pdfMsgId.delete()
                await footer(message, logFile)
                PROCESS.remove(message.from_user.id)
                shutil.rmtree(f"{message.message_id}")
            except Exception as e:
                logger.exception(
                        "AS_NEW_DOC:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
                try:
                    shutil.rmtree(f"{message.message_id}")
                    PROCESS.remove(message.from_user.id)
                    await pdfMsgId.edit(
                                       errorEditMsg.format(e)
                                       )
                except Exception:
                    pass
        
        # FILES TO PDF (CONVERTAPI)
        elif fileExt.lower() in suprtedPdfFile2:
            if not Config.CONVERT_API:
                pdfMsgId = await message.reply_text(
                                                   "`Owner Forgot to add ConvertAPI.. contact Owner 😒`",
                                                   quote = True
                                                   )
                return 
            else:
                try:
                    PROCESS.append(message.from_user.id)
                    input_file = f"{message.message_id}/{isPdfOrImg}"
                    
                    pdfMsgId = await message.reply_text(
                                                       "`Downloading your file..` 📥",
                                                       quote = True
                                                       )
                    # DOWNLOAD PROGRESS
                    c_time = time.time()
                    downloadLoc = await bot.download_media(
                                                          message = message.document.file_id,
                                                          file_name = input_file,
                                                          progress = progress,
                                                          progress_args = (
                                                                          message.document.file_size,
                                                                          pdfMsgId,
                                                                          c_time
                                                                          )
                                                          )
                    # CHECKS PDF DOWNLOADED OR NOT
                    if downloadLoc is None:
                        PROCESS.remove(chat_id)
                        return
                    
                    await pdfMsgId.edit(
                                       "`Work in Progress..`\n`It might take some time..`💛"
                                       )
                    try:
                        convertapi.convert(
                                          "pdf",
                                              {
                                                  "File": f"{message.message_id}/{isPdfOrImg}"
                                              },
                                              from_format=fileExt[1:],
                                          ).save_files(
                                              f"{message.message_id}/{fileNm}.pdf"
                                          )
                    except Exception:
                        try:
                            await pdfMsgId.edit(
                                               "ConvertAPI limit reaches.. contact Owner"
                                               )
                            shutil.rmtree(f"{message.message_id}")
                            PROCESS.remove(message.from_user.id)
                            return
                        except Exception: pass
                    
                    # Getting thumbnail
                    thumbnail, fileName = await thumbName(message, isPdfOrImg)
                    if PDF_THUMBNAIL != thumbnail:
                        await bot.download_media(
                                                message = thumbnail,
                                                file_name = f"{message.message_id}/thumbnail.jpeg"
                                                )
                        thumbnail = await formatThumb(f"{message.message_id}/thumbnail.jpeg")
                    await pdfMsgId.edit(
                                       "`Started Uploading..`📤"
                                       )
                    await message.reply_chat_action(
                                                   "upload_document"
                                                   )
                    logFile = await message.reply_document(
                                                file_name = f"{fileNm}.pdf",
                                                document = open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                                                thumb = thumbnail,
                                                caption = f"`Converted: {fileExt} to pdf`",
                                                quote = True
                                                )
                    await pdfMsgId.delete();
                    await footer(message, logFile)
                    PROCESS.remove(message.from_user.id)
                    shutil.rmtree(f"{message.message_id}")
                except Exception:
                    PROCESS.remove(message.from_user.id)
        
        # UNSUPPORTED FILES
        else:
            try:
                await message.reply_text(
                                        "`unsupported file..🙄`",
                                        quote = True
                                        )
            except Exception:
                pass
    except Exception as e:
        logger.exception(
                        "DOCUMENTS:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(asNewDoc)
async def _asNewDoc(bot, callbackQuery):
    try:
        if callbackQuery.from_user.id in PROCESS:
            return await callbackQuery.answer(
                                             "WORK IN PROGRESS..🙇"
                                             )
        await callbackQuery.answer(
                                  "⚙️ PROCESSING.."
                                  )
        if await header(bot, callbackQuery):
            return
        await callbackQuery.message.delete()
        await documents(
                       bot, callbackQuery.message.reply_to_message
                       )
    except Exception as e:
        logger.exception(
                        "AS_NEW_DOC:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
