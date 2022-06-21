# fileName : plugins/group/doc.py
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
import shutil
import asyncio
import convertapi
from pdf import myID
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
from configs.group import groupConfig
from pyrogram import Client as ILovePDF
from plugins.footer import footer, header
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from configs.images import WELCOME_PIC, BANNED_PIC, BIG_FILE, PDF_THUMBNAIL

if Config.CONVERT_API is not None:
    convertapi.api_secret = Config.CONVERT_API

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

/generate to generate PDF 🤞"""

errorEditMsg = """Something went wrong..😐

ERROR: `{}`

For bot updates join @ilovepdf_bot"""

forceSubMsg = """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only Channel Members Can Use this Bot 🚶

This Means You Need To Join The Below Mentioned Channel for Using Me!

hit on "retry ♻️" after joining.. 😅"""

foolRefresh = "വിളച്ചിലെടുക്കല്ലേ കേട്ടോ 😐"

#--------------->
#--------> PDF REPLY BUTTON
#------------------->

pdfReply = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⭐ META£ATA ⭐", 
                             callback_data="pdfInfo"),
            InlineKeyboardButton("🗳️ PREVIEW 🗳️",
                             callback_data="preview")
        ],[
            InlineKeyboardButton("🖼️ IMAGES 🖼️",
                             callback_data="toImage"),
            InlineKeyboardButton("✏️ TEXT ✏️",
                              callback_data="toText")
        ],[
            InlineKeyboardButton("🔐 ENCRYPT 🔐",
                             callback_data="encrypt"),
            InlineKeyboardButton("🔒 DECRYPT 🔓",
                             callback_data="decrypt")
        ],[
            InlineKeyboardButton("🗜️ COMPRESS 🗜️",
                            callback_data="compress"),
            InlineKeyboardButton("🤸 ROTATE 🤸",
                              callback_data="rotate")
        ],[
            InlineKeyboardButton("✂️ SPLIT ✂️",
                               callback_data="split"),
            InlineKeyboardButton("🧬 MERGE 🧬",
                               callback_data="underDev")
        ],[
            InlineKeyboardButton("™️ STAMP ™️",
                               callback_data="stamp"),
            InlineKeyboardButton("✏️ RENAME ✏️",
                              callback_data="rename")
        ],[
            InlineKeyboardButton("📝 OCR 📝",
                                 callback_data="ocr"),
            InlineKeyboardButton("🥷 A4 FORMAT 🥷",
                              callback_data="format")
        ],[
            InlineKeyboardButton("🚫 CLOSE 🚫",
                            callback_data="closeALL")
        ]]
    )

UPDATE_CHANNEL = Config.UPDATE_CHANNEL

ONLY_GROUP_ADMIN = groupConfig.ONLY_GROUP_ADMIN

#--------------->
#--------> REPLY TO group DOCUMENTS/FILES/IMAGES
#------------------->

@ILovePDF.on_message(
                    filters.group &
                    ~filters.edited &
                    filters.incoming &
                    filters.command(
                          ["analyse", "check",
                             "nabilanavab"]
                                   )
                    )
async def documents(bot, message):
    try:
        global invite_link, myID
        if not myID:
            myID = await bot.get_me()
        await message.reply_chat_action(
                                       "typing"
                                       )
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                userStatus = await bot.get_chat_member(
                                                      str(UPDATE_CHANNEL),
                                                      message.from_user.id
                                                      )
                # IF USER BANNED FROM CHANNEL
                if userStatus.status == 'banned':
                     return await message.reply_photo(
                                              photo = BANNED_PIC,
                                              caption = "For Some Reason You Can't Use This Bot"
                                                        "\n\nContact Bot Owner 🤐",
                                              reply_markup = InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("Owner 🎊",
                                                      url="https://t.me/nabilanavab")]]
                                              ))
            except Exception:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
                                                                   int(UPDATE_CHANNEL)
                                                                   )
                return await message.reply_photo(
                                    photo = WELCOME_PIC,
                                    caption = forceSubMsg.format(
                                            message.from_user.first_name, message.from_user.id
                                    ),
                                    reply_markup = InlineKeyboardMarkup(
                                         [[
                                               InlineKeyboardButton("🌟 JOIN CHANNEL 🌟",
                                                           url = invite_link.invite_link)
                                         ],[
                                               InlineKeyboardButton("Refresh ♻️",
                                                    callback_data = "refreshAnalyse")
                                         ]]
                                    ))
        
        if message.from_user.id in PROCESS:
            return await message.reply_to_message.reply(
                                                       "WORK IN PROGRESS.. 🙇"
                                                       "\nTry Again Later.. 😉"
                                                       "\n\nRequest from: {}".format(message.from_user.mention),
                                                       quote = True,
                                                       reply_markup = InlineKeyboardMarkup(
                                                             [[
                                                                 InlineKeyboardButton(
                                                                          "♻️ Try Again ♻️",
                                                                 callback_data = "newGrupDoc")
                                                             ]]
                                                       ))
        
        status = await bot.get_chat_member(
                                           message.chat.id,
                                           myID.id
                                           )
        if status.status not in ["administrator", "creator"]:
            return await message.reply(
                                      "Due to Some Telegram Limits.."
                                      "I can only work as an admin\n\n"
                                      "__Please promote me as admin__ ☺️",
                                      quote = True
                                      )
        
        if (not message.reply_to_message) or not(message.reply_to_message.document or message.reply_to_message.photo):
            return await message.reply(
                                      "Broh Please Reply to a Document or an Image..🤧",
                                      quote = True
                                      )
        
        if message.from_user.id in Config.ADMINS:
            pass
        else:
            isAdmin = await bot.get_chat_member(
                                         message.chat.id,
                                         message.from_user.id
                                         )
            if ONLY_GROUP_ADMIN and isAdmin.status not in ["administrator", "creator"]:
                return await message.reply(
                                          "Only Group Admins Can Use This Bot\n"
                                          "Else Come to my Pm 😋", quote = True
                                          )
            elif isAdmin.status not in ["administrator", "creator"]:
                if message.from_user.id != message.reply_to_message.from_user.id:
                    return await message.reply(
                                              "Please Reply to Your Message.. 🙂"
                                              )
        
        if message.reply_to_message.photo:
            imageReply = await message.reply_to_message.reply_text(
                                             "`Downloading your Image..` 📥",
                                             quote = True
                                             )
            if not isinstance(PDF.get(message.chat.id), list):
                PDF[message.chat.id] = []
            await message.reply_to_message.download(
                                     f"{message.chat.id}/{message.chat.id}.jpg"
                                     )
            img = Image.open(
                f"{message.chat.id}/{message.chat.id}.jpg"
            ).convert("RGB")
            PDF[message.chat.id].append(img)
            return await imageReply.edit(
                                 imageAdded.format(
                                                  len(PDF[message.chat.id])
                                                  )
                                 )
        
        isPdfOrImg = message.reply_to_message.document.file_name        # file name
        fileSize = message.reply_to_message.document.file_size          # file size
        fileNm, fileExt = os.path.splitext(isPdfOrImg) # seperate name & extension
        
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            await message.reply_to_message.reply_photo(
                                     photo = BIG_FILE,
                                     caption = bigFileUnSupport.format(
                                             MAX_FILE_SIZE, MAX_FILE_SIZE
                                     ),
                                     reply_markup = InlineKeyboardMarkup(
                                          [[
                                               InlineKeyboardButton("💎 Create 2Gb Support Bot 💎",
                                                     url = "https://github.com/nabilanavab/ilovepdf")
                                           ]]
                                    ))
            return
        
        # IMAGE AS FILES (ADDS TO PDF FILE)
        elif fileExt.lower() in suprtedFile:
            try:
                imageDocReply = await message.reply_to_message.reply_text(
                                                        "`Downloading your Image.. 📥`",
                                                        quote = True
                                                        )
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id] = []
                await message.reply_to_message.download(
                                      f"{message.chat.id}/{message.chat.id}.jpg"
                                      )
                img = Image.open(
                                f"{message.chat.id}/{message.chat.id}.jpg"
                                ).convert("RGB")
                PDF[message.chat.id].append(img)
                await imageDocReply.edit(
                                        imageAdded.format(
                                                         len(PDF[message.chat.id])
                                                         )
                                        )
            except Exception as e:
                await imageDocReply.edit(
                                        errorEditMsg.format(e)
                                        )
        
        # REPLY TO .PDF FILE EXTENSION
        elif fileExt.lower() == ".pdf":
            pdfMsgId = await message.reply_to_message.reply_text(
                                                                "⚙️ PROCESSING.",
                                                                quote = True
                                                                )
            await asyncio.sleep(0.5)
            await pdfMsgId.edit("⚙️ PROCESSING..")
            await asyncio.sleep(0.5)
            await pdfMsgId.edit("⚙️ PROCESSING...")
            await asyncio.sleep(0.5)
            await pdfMsgId.edit(
                               text = pdfReplyMsg.format(
                                                        isPdfOrImg,
                                                        await gSF(fileSize)
                               ),
                               reply_markup = pdfReply
                               )
            await footer(message, message.reply_to_message)
        
        # FILES TO PDF (PYMUPDF/FITZ)
        elif fileExt.lower() in suprtedPdfFile:
            try:
                PROCESS.append(message.from_user.id)
                pdfMsgId = await message.reply_to_message.reply_text(
                                                   "`Downloading your file.. 📥`",
                                                   quote = True
                                                   )
                await message.reply_to_message.download(
                                      f"{message.message_id}/{isPdfOrImg}"
                                      )
                await pdfMsgId.edit(
                                   "`Work in Progress.. It might take some time.. 💛`"
                                   )
                Document = fitz.open(
                                    f"{message.message_id}/{isPdfOrImg}"
                                    )
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
                                   "`Started Uploading..` 📤"
                                   )
                await message.reply_chat_action(
                                               "upload_document"
                                               )
                logFile = await message.reply_to_message.reply_document(
                                            file_name = f"{fileName}.pdf",
                                            document = open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                                            thumb = thumbnail,
                                            caption = f"`Converted: {fileExt} to pdf`",
                                            quote = True
                                            )
                await pdfMsgId.delete(); PROCESS.remove(message.from_user.id)
                shutil.rmtree(f"{message.message_id}")
                await footer(message, logFile)
            except Exception as e:
                try:
                    await pdfMsgId.edit(
                                       errorEditMsg.format(e)
                                       )
                    shutil.rmtree(f"{message.message_id}")
                    PROCESS.remove(message.from_user.id)
                except Exception:
                    pass
        
        # FILES TO PDF (CONVERTAPI)
        elif fileExt.lower() in suprtedPdfFile2:
            if Config.CONVERT_API is None:
                pdfMsgId = await message.reply_text(
                                                   "`Owner Forgot to add ConvertAPI.. contact Owner 😒`",
                                                   quote = True
                                                   )
                return 
            else:
                try:
                    PROCESS.append(message.from_user.id)
                    pdfMsgId = await message.reply_to_message.reply_text(
                                                       "`Downloading your file.. 📥`",
                                                       quote = True
                                                       )
                    await message.reply_to_message.download(
                                          f"{message.message_id}/{isPdfOrImg}"
                                          )
                    await pdfMsgId.edit(
                                       "`Work in Progress.. It might take some time..`💛"
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
                            shutil.rmtree(f"{message.message_id}")
                            await pdfMsgId.edit(
                                               "ConvertAPI limit reaches.. contact Owner"
                                               )
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
                                       "`Started Uploading..` 📤"
                                       )
                    await message.reply_chat_action(
                                                   "upload_document"
                                                   )
                    logFile = await message.reply_to_message.reply_document(
                                                file_name = f"{fileNm}.pdf",
                                                document = open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                                                thumb = PDF_THUMBNAIL,
                                                caption = f"`Converted: {fileExt} to pdf`",
                                                quote = True
                                                )
                    await pdfMsgId.delete(); PROCESS.remove(message.from_user.id)
                    shutil.rmtree(f"{message.message_id}")
                    await footer(message, logFile)
                except Exception:
                    PROCESS.remove(message.from_user.id)
                    pass
        
        # UNSUPPORTED FILES
        else:
            try:
                await message.reply_to_message.reply_text(
                                        "`unsupported file..🙄`",
                                        quote = True
                                        )
            except Exception:
                pass
    except Exception as e:
        logger.exception(
                        "»»GROUP:DOC:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

newGrupDoc = filters.create(lambda _, __, query: query.data == "newGrupDoc")
refreshAnalyse = filters.create(lambda _, __, query: query.data == "refreshAnalyse")

@ILovePDF.on_callback_query(refreshAnalyse)
async def _refreshGrup(bot, callbackQuery):
    try:
        if callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id:
            return await callbackQuery.answer("Message Not For You.. 😏")
        
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        userStatus = await bot.get_chat_member(
                                              str(UPDATE_CHANNEL),
                                              callbackQuery.from_user.id
                                              )
        await callbackQuery.answer()
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        if callbackQuery.data == "refreshAnalyse":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return await analyse(bot, messageId)
    except Exception as e:
        try:
            logger.exception(
                        "»»GROUP:DOCUMENTS:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                                           callbackQuery.id,
                                           text = foolRefresh,
                                           show_alert = True,
                                           cache_time = 0
                                           )
        except Exception: pass

@ILovePDF.on_callback_query(newGrupDoc)
async def _asDoc(bot, callbackQuery):
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
    except Exception:
        logger.exception(
                        "»»GROUP:DOC:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
