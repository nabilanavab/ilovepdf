# fileName : plugins/dm/callBack/images.py
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
from PIL import Image
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from pyrogram.errors import FloodWait
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from plugins.footer import footer, header
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

mediaDoc = {}
media = {}

cancel = InlineKeyboardMarkup(
                             [[InlineKeyboardButton("💤 CANCEL 💤",
                                     callback_data = "cancelP2I")]]
                             )
canceled = InlineKeyboardMarkup(
                               [[InlineKeyboardButton("🍄 CANCELED 🍄",
                                            callback_data="canceled")]]
                               )
completed = InlineKeyboardMarkup(
                                [[InlineKeyboardButton("😎 COMPLETED 😎",
                                             callback_data="completed")]]
                                )

#--------------->
#--------> CHECKS IF USER CANCEL PROCESS
#------------------->

async def notInPROCESS(chat_id, message, current, total, deleteID):
    if chat_id in PROCESS:
        return False
    else:
        await message.edit(
                          text = f"`Canceled at {current}/{total} pages..` 🙄",
                          reply_markup = canceled
                          )
        shutil.rmtree(f'{deleteID}')
        doc.close()
        return True

#--------------->
#--------> PDF TO IMAGES
#------------------->

KcbExtract = ["KIA|", "KIR|", "KDA|", "KDR|", "KIS|", "KDS|"]
EXTRACT = filters.create(lambda _, __, query: query.data in ["IA", "DA", "IR", "DR", "IS", "DS"])
KEXTRACT = filters.create(lambda _, __, query: query.data.startswith(tuple(KcbExtract)))


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(EXTRACT)
async def _EXTRACT(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.from_user.id
        message_id = callbackQuery.message.message_id
        
        if chat_id in PROCESS:
            await callbackQuery.answer(
                                      "Work in progress.. 🙇"
                                      )
            return
        
        # ↓ ADD TO PROCESS       ↓ CALLBACK DATA
        PROCESS.append(chat_id); data = callbackQuery.data
        await callbackQuery.answer(
                                  "⚙️ Processing.."
                                  )
        
        # ACCEPTING PAGE NUMBER
        if data in ["IA", "DA"]:
            nabilanavab = False
        # RANGE (START:END)
        elif data in ["IR", "DR"]:
            nabilanavab = True
            i = 0
            # 5 EXCEPTION, BREAK MERGE PROCESS
            while(nabilanavab):
                if i >= 5:
                    await callbackQuery.message.reply_text(
                                                          "`5 attempt over.. Process canceled..`😏"
                                                          )
                    break
                i += 1
                # PYROMOD ADD-ON (PG NO REQUEST)
                needPages = await bot.ask(
                                         text = "__Pdf - Img›Doc » Pages:\n"
                                                "Now, Enter the range (start:end) :__\n\n"
                                                "/exit __to cancel__",
                                         chat_id = chat_id,
                                         reply_to_message_id = message_id,
                                         filters = filters.text,
                                         reply_markup = ForceReply(True)
                )
                # EXIT PROCESS
                if needPages.text == "/exit":
                    await needPages.reply_text(
                                              "`Process Canceled..` 😏",
                                              quote = True
                                              )
                    break
                # SPLIT STRING TO START & END
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                # IF STRING HAVE MORE THAN 2 LIMITS
                if len(pageStartAndEnd) > 2:
                    await callbackQuery.message.reply_text(
                                                          "`Syntax Error: justNeedStartAndEnd `🚶"
                                                          )
                # CORRECT FORMAT
                elif len(pageStartAndEnd) == 2:
                    start = pageStartAndEnd[0]
                    end = pageStartAndEnd[1]
                    if start.isdigit() and end.isdigit():
                        if (1 <= int(pageStartAndEnd[0])):
                            if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                                nabilanavab = False
                                break
                            else:
                                await callbackQuery.message.reply_text(
                                                                      "`Syntax Error: errorInEndingPageNumber `🚶"
                                                                      )
                        else:
                            await callbackQuery.message.reply_text(
                                                                  "`Syntax Error: errorInStartingPageNumber `🚶"
                                                                  )
                    else:
                        await callbackQuery.message.reply_text(
                                                              "`Syntax Error: pageNumberMustBeADigit` 🧠"
                                                              )
                else:
                    await callbackQuery.message.reply_text(
                                                          "`Syntax Error: noEndingPageNumber Or notADigit` 🚶"
                                                          )
        # SINGLE PAGES
        else:
            newList = []
            nabilanavab = True
            i = 0
            # 5 REQUEST LIMIT
            while(nabilanavab):
                if i >= 5:
                    await callbackQuery.message.reply_text(
                                                          "`5 attempt over.. Process canceled..`😏"
                                                          )
                    break
                i += 1
                # PYROMOD ADD-ON
                needPages = await bot.ask(
                                         text = "__Pdf - Img›Doc » Pages:\n"
                                                "Now, Enter the Page Numbers seperated by__ (,) :\n\n"
                                                "/exit __to cancel__",
                                         chat_id = chat_id,
                                         reply_to_message_id = message_id,
                                         filters = filters.text,
                                         reply_markup = ForceReply(True)
                                         )
                # SPLIT PAGE NUMBERS (,)
                singlePages = list(needPages.text.replace(',',':').split(':'))
                # PROCESS CANCEL
                if needPages.text == "/exit":
                    await needPages.reply(
                                         "`Process Canceled..` 😏",
                                         quote = True
                                         )
                    break
                # PAGE NUMBER LESS THAN 100
                elif 1 <= len(singlePages) <= 100:
                    # CHECK IS PAGE NUMBER A DIGIT(IF ADD TO A NEW LIST)
                    for i in singlePages:
                        if i.isdigit():
                            newList.append(i)
                    if newList != []:
                        nabilanavab = False
                        break
                    # AFTER SORTING (IF NO DIGIT PAGES RETURN)
                    elif newList == []:
                        await callbackQuery.message.reply(
                                                         "`Cant find any number..`😏"
                                                         )
                        continue
                else:
                    await callbackQuery.message.reply(
                                                     "`Something went Wrong..`😅"
                                                     )
        if nabilanavab == True:
            PROCESS.remove(chat_id)
            return
        
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        if nabilanavab == False:
            # DOWNLOAD MESSAGE
            downloadMessage = await callbackQuery.message.reply(
                                                               text = "`Downloding your pdf..` 📥", 
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
            # CHECK DOWNLOAD COMPLETED/CANCELED
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            # CHECK PDF CODEC, ENCRYPTION..
            checked, nabilanavab = await checkPdf(
                                                 input_file,
                                                 callbackQuery
                                                 )
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            # OPEN PDF WITH FITZ
            doc = fitz.open(input_file)
            number_of_pages = doc.pageCount
            if data in ["IA", "DA"]:
                pageStartAndEnd = [1, int(number_of_pages)]
            if data in ["IR", "DR"]:
                if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                    await downloadMessage.edit(
                                              f"`PDF only have {number_of_pages} pages` 💩"
                                              )
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f"{message_id}")
                    return
            zoom = 2; mat = fitz.Matrix(zoom, zoom)
            if data in ["IA", "DA", "IR", "DR"]:
                if int(int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])) >= 11:
                    await downloadMessage.pin(
                                             disable_notification = True,
                                             both_sides = True
                                             )
                await downloadMessage.edit(
                                          text = f"`Total pages: {int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])}..⏳`",
                                          reply_markup = cancel
                                          )
                totalPgList = range(int(pageStartAndEnd[0]), int(pageStartAndEnd[1])+1)
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{message_id}/pgs')
                    for pageNo in pgList:
                        page = doc.load_page(pageNo-1)
                        pix = page.get_pixmap(matrix = mat)
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            if await notInPROCESS(
                                                 chat_id,
                                                 downloadMessage,
                                                 cnvrtpg,
                                                 pageStartAndEnd[1],
                                                 message_id
                                                 ):
                                return
                            await downloadMessage.edit(
                                                      text = f"`Converted: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} pages.. 🤞`",
                                                      reply_markup = cancel
                                                      )
                        with open(
                            f'{message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.save(f'{message_id}/pgs/{pageNo}.jpg')
                    if await notInPROCESS(
                                         chat_id,
                                         downloadMessage,
                                         cnvrtpg,
                                         pageStartAndEnd[1],
                                         message_id
                                         ):
                        return
                    await downloadMessage.edit(
                                              text = f"`Preparing an Album..` 🤹",
                                              reply_markup = cancel
                                              )
                    directory = f'{message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key = os.path.getctime)
                    if data in ["IA", "IR"]:
                        media[chat_id] = []
                    else:
                        mediaDoc[chat_id] = []
                    for file in imag:
                        qualityRate = 95
                        for i in range(200):
                            if os.path.getsize(file) >= 1000000:
                                picture = Image.open(file)
                                picture.save(
                                            file,
                                            "JPEG",
                                            optimize = True,
                                            quality = qualityRate
                                            )
                                qualityRate -= 5; asyncio.sleep(1)
                            else:
                                if data in ["IA", "IR"]:
                                    media[chat_id].append(
                                                         InputMediaPhoto(media = file)
                                                         )
                                else:
                                    mediaDoc[chat_id].append(
                                                            InputMediaDocument(media = file)
                                                            )
                                break
                    if await notInPROCESS(
                                         chat_id,
                                         downloadMessage,
                                         cnvrtpg,
                                         pageStartAndEnd[1],
                                         message_id
                                         ):
                        return
                    if chat_id in PROCESS:
                        await downloadMessage.edit(
                                                  text = f"`Uploading: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} pages.. 🐬`",
                                                  reply_markup = cancel
                                                  )
                    else:
                        shutil.rmtree(f'{message_id}')
                        doc.close()
                        return
                    if data in ["IA", "IR"]:
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}'); doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_photo"
                                                                     )
                        for i in range(1,100):
                            try:
                                await callbackQuery.message.reply_media_group(
                                                           media[chat_id]
                                                           )
                                break
                            except FloodWait as e:
                                await asyncio.sleep(e.x)
                                await callbackQuery.message.reply_media_group(
                                                               media[chat_id]
                                                               )
                    
                    if data in ["DA", "DR"]:
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_document"
                                                                     )
                        try:
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                    shutil.rmtree(f'{message_id}/pgs')
                PROCESS.remove(chat_id); doc.close()
                await downloadMessage.edit(
                                          text = f'`Uploading Completed.. `🏌️',
                                          reply_markup = completed
                                          )
                shutil.rmtree(f'{message_id}')
            if data in ["IS", "DS"]:
                if int(len(newList)) >= 11:
                    await downloadMessage.pin(
                                             disable_notification = True,
                                             both_sides = True
                                             )
                totalPgList = []
                for i in newList:
                    if 1 <= int(i) <= number_of_pages:
                        totalPgList.append(i)
                if len(totalPgList) < 1:
                    await downloadMessage.edit(
                                              f"`PDF Only have {number_of_pages} page(s) `😏"
                                              )
                    PROCESS.remove(chat_id); shutil.rmtree(f'{message_id}'); doc.close()
                    return
                await downloadMessage.edit(
                                          text = f"`Total pages: {len(totalPgList)}..⏳`",
                                          reply_markup = cancel
                                          )
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{message_id}/pgs')
                    for pageNo in pgList:
                        if int(pageNo) <= int(number_of_pages):
                            page = doc.load_page(int(pageNo)-1)
                            pix = page.get_pixmap(matrix=mat)
                        else:
                            continue
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await downloadMessage.edit(
                                                      text = f"`Converted: {cnvrtpg}/{len(totalPgList)} pages.. 🤞`",
                                                      reply_markup = cancel
                                                      )
                            if await notInPROCESS(
                                                 chat_id,
                                                 callbackQuery,
                                                 cnvrtpg,
                                                 totalPgList,
                                                 message_id
                                                 ):
                                return
                        with open(
                            f'{message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.save(f'{message_id}/pgs/{pageNo}.jpg')
                    if await notInPROCESS(
                                         chat_id,
                                         downloadMessage,
                                         cnvrtpg,
                                         totalPgList,
                                         message_id
                                         ):
                        return
                    await downloadMessage.edit(
                                              text = f"`Preparing an Album..` 🤹",
                                              reply_markup = cancel
                                              )
                    directory = f'{message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key = os.path.getctime)
                    if data == "IS":
                        media[chat_id] = []
                    else:
                        mediaDoc[chat_id] = []
                    for file in imag:
                        qualityRate = 95
                        for i in range(200):
                            if os.path.getsize(file) >= 1000000:
                                picture = Image.open(file)
                                picture.save(
                                            file,
                                            "JPEG",
                                            optimize = True,
                                            quality = qualityRate
                                            )
                                qualityRate -= 5; asyncio.sleep(1)
                            else:
                                if data == "IS":
                                    media[chat_id].append(InputMediaPhoto(media = file))
                                else:
                                    mediaDoc[chat_id].append(InputMediaDocument(media = file))
                                break
                    if await notInPROCESS(
                                         chat_id,
                                         downloadMessage,
                                         cnvrtpg,
                                         totalPgList,
                                         message_id
                                         ):
                        return
                    await downloadMessage.edit(
                                              text = f"`Uploading: {cnvrtpg}/{len(totalPgList)} pages.. 🐬`",
                                              reply_markup = cancel
                                              )
                    if data == "IS":
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}'); doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_photo"
                                                                     )
                        try:
                            await callbackQuery.message.reply_media_group(
                                                            media[chat_id]
                                                            )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await callbackQuery.message.reply_media_group(
                                                            media[chat_id]
                                                            )
                    if data == "DS":
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}'); doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_document"
                                                                     )
                        try:
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                    shutil.rmtree(f'{message_id}/pgs')
                PROCESS.remove(chat_id); doc.close()
                await downloadMessage.edit(
                                          text = f'`Uploading Completed.. `🏌️',
                                          reply_markup = completed
                                          )
                shutil.rmtree(f'{message_id}')
                await footer(callbackQuery.message.reply_to_message, False)
    except Exception as e:
        logger.exception(
                        "PDF2IMAGES:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            PROCESS.remove(chat_id)
            shutil.rmtree(f'{message_id}')
        except Exception:
            pass

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KEXTRACT)
async def _KEXTRACT(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.from_user.id
        message_id = callbackQuery.message.message_id
        
        if chat_id in PROCESS:
            await callbackQuery.answer(
                                      "Work in progress.. 🙇"
                                      )
            return
        await callbackQuery.answer(
                                  "⚙️ Processing.."
                                  )
        data = callbackQuery.data[:3]
        _, number_of_pages = callbackQuery.data.split("|")
        PROCESS.append(chat_id)
        if data in ["KIA", "KDA"]:
            nabilanavab = False
        elif data in ["KIR", "KDR"]:
            nabilanavab = True
            i = 0
            while(nabilanavab):
                if i >= 5:
                    await callbackQuery.message.reply_text(
                                                          "`5 attempt over.. Process canceled..`😏"
                                                          )
                    break
                i += 1
                needPages = await bot.ask(
                                         text = "__Pdf - Img›Doc » Pages:\n"
                                                "Now, Enter the range (start:end) :__\n\n"
                                                "/exit __to cancel__",
                                         chat_id = chat_id,
                                         reply_to_message_id = message_id,
                                         filters = filters.text,
                                         reply_markup = ForceReply(True)
                                         )
                if needPages.text == "/exit":
                    await callbackQuery.message.reply_text(
                                                          "`Process Canceled..` 😏",
                                                          quote = True
                                                          )
                    break
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                if len(pageStartAndEnd) > 2:
                    await callbackQuery.message.reply_text(
                                                          "`Syntax Error: justNeedStartAndEnd `🚶"
                                                          )
                elif len(pageStartAndEnd) == 2:
                    start = pageStartAndEnd[0]
                    end = pageStartAndEnd[1]
                    if start.isdigit() and end.isdigit():
                        if (1 <= int(pageStartAndEnd[0])):
                            if int(pageStartAndEnd[0]) < int(pageStartAndEnd[1]) and int(pageStartAndEnd[1]) <= int(number_of_pages):
                                nabilanavab = False
                                break
                            else:
                                await callbackQuery.message.reply_text(
                                                                      "`Syntax Error: errorInEndingPageNumber `🚶"
                                                                      )
                        else:
                            await callbackQuery.message.reply_text(
                                                                  "`Syntax Error: errorInStartingPageNumber `🚶"
                                                                  )
                    else:
                        await callbackQuery.message.reply_text(
                                                              "`Syntax Error: pageNumberMustBeADigit` 🧠"
                                                              )
                else:
                    await callbackQuery.message.reply_text(
                                                          "`Syntax Error: noEndingPageNumber Or notADigit` 🚶"
                                                          )
        elif data in ["KIS", "KDS"]:
            newList = []
            nabilanavab = True
            i = 0
            while(nabilanavab):
                if i >= 5:
                    await callbackQuery.message.reply_text(
                                                          "`5 attempt over.. Process canceled..`😏"
                                                          )
                    break
                i += 1
                needPages = await bot.ask(
                                         text = "__Pdf - Img›Doc » Pages:\n"
                                                "Now, Enter the Page Numbers seperated by__ (,) :\n\n"
                                                "/exit __to cancel__",
                                         chat_id = chat_id,
                                         reply_to_message_id = message_id,
                                         filters = filters.text,
                                         reply_markup = ForceReply(True)
                                         )
                singlePages = list(needPages.text.replace(',',':').split(':'))
                if needPages.text == "/exit":
                    await needPages.reply_text(
                                              "`Process Canceled..` 😏",
                                              quote = True
                                              )
                    break
                elif 1 <= len(singlePages) <= 100:
                    for i in singlePages:
                        if i.isdigit() and int(i) <= int(number_of_pages):
                            newList.append(i)
                    if newList != []:
                        nabilanavab = False
                        break
                    elif newList == []:
                        await callbackQuery.message.reply_text(
                                                              "`Cant find any number..`😏"
                                                              )
                        continue
                else:
                    await callbackQuery.message.reply_text(
                                                          "`100 page is enough..`😅"
                                                          )
        if nabilanavab == True:
            PROCESS.remove(chat_id)
            return
        
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        if nabilanavab == False:
            downloadMessage = await callbackQuery.message.reply_text(
                                                                    text = "`Downloding your pdf..` 📥",
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
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            checked, number_of_pages = await checkPdf(
                                                     input_file,
                                                     callbackQuery 
                                                     )
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
            doc = fitz.open(input_file)
            number_of_pages = doc.pageCount
            if data in ["KIA", "KDA"]:
                pageStartAndEnd = [1, int(number_of_pages)]
            if data in ["KIR", "KDR"]:
                if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                    await downloadMessage.edit(
                                              text = f"`PDF only have {number_of_pages} pages` 💩"
                                              )
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f"{message_id}")
                    return
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            if data in ["KIA", "KDA", "KIR", "KDR"]:
                if int(int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])) >= 11:
                    await downloadMessage.pin(
                                             disable_notification = True,
                                             both_sides = True
                                             )
                await downloadMessage.edit(
                                          text = f"`Total pages: {int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])}..⏳`",
                                          reply_markup = cancel
                                          )
                totalPgList = range(int(pageStartAndEnd[0]), int(pageStartAndEnd[1])+1)
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{message_id}/pgs')
                    for pageNo in pgList:
                        page = doc.load_page(pageNo-1)
                        pix = page.get_pixmap(matrix=mat)
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await downloadMessage.edit(
                                                      text = f"`Converted: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} pages.. 🤞`",
                                                      reply_markup = cancel
                                                      )
                        if chat_id not in PROCESS:
                            try:
                                await downloadMessage.edit(
                                                          text = f"`Canceled at {cnvrtpg}/{int(int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0]))} pages.. 🙄`",
                                                          reply_markup = canceled
                                                          )
                                shutil.rmtree(f'{message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        with open(
                            f'{message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.save(f'{message_id}/pgs/{pageNo}.jpg')
                    try:
                        await downloadMessage.edit(
                                                  text = f"`Preparing an Album..` 🤹",
                                                  reply_markup = cancel 
                                                  )
                    except Exception:
                        pass
                    directory = f'{message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key = os.path.getctime)
                    if data in ["KIA", "KIR"]:
                        media[chat_id] = []
                    else:
                        mediaDoc[chat_id] = []
                    for file in imag:
                        qualityRate = 95
                        for i in range(200):
                            if os.path.getsize(file) >= 1000000:
                                picture = Image.open(file)
                                picture.save(
                                            file,
                                            "JPEG",
                                            optimize = True,
                                            quality = qualityRate 
                                            )
                                qualityRate -= 5
                                asyncio.sleep(1)
                            else:
                                if data in ["KIA", "KIR"]:
                                    media[chat_id].append(
                                                         InputMediaPhoto(media = file)
                                                         )
                                else:
                                    mediaDoc[chat_id].append(
                                                            InputMediaDocument(media = file)
                                                            )
                                break
                    await downloadMessage.edit(
                                              text = f"`Uploading: {cnvrtpg}/{int(pageStartAndEnd[1])+1 - int(pageStartAndEnd[0])} pages.. 🐬`",
                                              reply_markup = cancel
                                              )
                    if data in ["KIA", "KIR"]:
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_photo"
                                                                     )
                        try:
                            await callbackQuery.message.reply_media_group(
                                                            media[chat_id]
                                                            )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await callbackQuery.message.reply_media_group(
                                                            media[chat_id]
                                                            )
                    if data in ["KDA", "KDR"]:
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_document"
                                                                     )
                        try:
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                    shutil.rmtree(f'{message_id}/pgs')
                PROCESS.remove(chat_id)
                doc.close()
                await downloadMessage.edit(
                                          text = f'`Uploading Completed.. `🏌️',
                                          reply_markup = completed
                                          )
                shutil.rmtree(f'{message_id}')
            if data in ["KIS", "KDS"]:
                if int(len(newList)) >= 11:
                    await downloadMessage.pin(
                                             disable_notification = True,
                                             both_sides = True
                                             )
                totalPgList = []
                for i in newList:
                    if 1 <= int(i) <= number_of_pages:
                        totalPgList.append(i)
                if len(totalPgList) < 1:
                    await downloadMessage.edit(
                                              text = f"`PDF Only have {number_of_pages} page(s) `😏"
                                              )
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f'{message_id}')
                    doc.close()
                    return
                await downloadMessage.edit(
                                          text=f"`Total pages: {len(totalPgList)}..⏳`", 
                                          reply_markup = cancel
                                          )
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{message_id}/pgs')
                    for pageNo in pgList:
                        if int(pageNo) <= int(number_of_pages):
                            page = doc.load_page(int(pageNo)-1)
                            pix = page.get_pixmap(matrix = mat)
                        else:
                            continue
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await downloadMessage.edit(
                                                      text = f"`Converted: {cnvrtpg}/{len(totalPgList)} pages.. 🤞`",
                                                      reply_markup = cancel
                                                      )
                        if chat_id not in PROCESS:
                            try:
                                await downloadMessage.edit(
                                                          text = f"`Canceled at {cnvrtpg}/{len(totalPgList)} pages.. 🙄`",
                                                          reply_markup = canceled
                                                          )
                                shutil.rmtree(f'{message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        with open(
                            f'{message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.save(f'{message_id}/pgs/{pageNo}.jpg')
                    try:
                        await downloadMessage.edit(
                                                  text=f"`Preparing an Album..` 🤹",
                                                  reply_markup = cancel
                                                  )
                    except Exception:
                        pass
                    directory = f'{message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key = os.path.getctime)
                    if data == "KIS":
                        media[chat_id] = []
                    else:
                        mediaDoc[chat_id] = []
                    for file in imag:
                        qualityRate = 95
                        for i in range(200):
                            if os.path.getsize(file) >= 1000000:
                                picture = Image.open(file)
                                picture.save(
                                            file,
                                            "JPEG",
                                            optimize = True,
                                            quality = qualityRate 
                                            )
                                qualityRate -= 5
                                asyncio.sleep(1)
                            else:
                                if data == "KIS":
                                    media[chat_id].append(
                                                         InputMediaPhoto(media = file)
                                                         )
                                else:
                                    mediaDoc[chat_id].append(
                                                            InputMediaDocument(media=file)
                                                            )
                                break
                    await downloadMessage.edit(
                                              text = f"`Uploading: {cnvrtpg}/{len(totalPgList)} pages.. 🐬`",
                                              reply_markup = cancel
                                              )
                    if data== "KIS":
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_photo"
                                                                     )
                        try:
                            await callbackQuery.message.reply_media_group(
                                                            media[chat_id]
                                                            )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await callbackQuery.message.reply_media_group(
                                                            media[chat_id]
                                                            )
                    if data == "KDS":
                        if chat_id not in PROCESS:
                            try:
                                shutil.rmtree(f'{message_id}')
                                doc.close()
                                return
                            except Exception:
                                return
                        await callbackQuery.message.reply_chat_action(
                                                                     "upload_document"
                                                                     )
                        try:
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await callbackQuery.message.reply_media_group(
                                                         mediaDoc[chat_id]
                                                         )
                    shutil.rmtree(f'{message_id}/pgs')
                PROCESS.remove(chat_id)
                doc.close()
                await downloadMessage.edit(
                                          text = f'`Uploading Completed.. `🏌️',
                                          reply_markup = completed
                                          )
                shutil.rmtree(f'{message_id}')
                await footer(callbackQuery.message.reply_to_message, False)
    except Exception as e:
        logger.exception(
                        "PDF2IMAGES:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            PROCESS.remove(chat_id)
            shutil.rmtree(f'{message_id}')
        except Exception:
            pass

#                                                                                                                                            Telegram: @nabilanavab
