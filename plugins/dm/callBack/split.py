# fileName : plugins/dm/callBack/split.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import time
import shutil
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from plugins.checkPdf import checkPdf
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from plugins.footer import footer, header
from PyPDF2 import PdfFileWriter, PdfFileReader
from plugins.fileSize import get_size_format as gSF
from plugins.progress import progress, uploadProgress
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


split = filters.create(lambda _, __, query: query.data == "split")
Ksplit = filters.create(lambda _, __, query: query.data.startswith("Ksplit|"))

splitProcess = filters.create(lambda _, __, query: query.data.startswith(tuple(["splitR", "splitS", "KsplitR|", "KsplitS"])))

@ILovePDF.on_callback_query(split)
async def _split(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
                                             "__Split pdf » Pages:"
                                             "\n\nTotal Page Number(s):__ `unknown`",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("With In Range 🦞",
                                                                            callback_data = "splitR")
                                                 ],[
                                                     InlineKeyboardButton("Single Page 🐛",
                                                                            callback_data = "splitS")
                                                 ],[
                                                     InlineKeyboardButton("« Back «",
                                                                              callback_data = "BTPM")
                                                 ]]
                                             ))
    except Exception: pass

# Split pgNo (with known pdf page number)
@ILovePDF.on_callback_query(Ksplit)
async def _Ksplit(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
                                             f"Split pdf » Pages:"
                                             f"\n\nTotal Page Number(s): {number_of_pages}__ 🌟",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("With In Range 🦞",
                                                            callback_data = f"KsplitR|{number_of_pages}")
                                                 ],[
                                                     InlineKeyboardButton("Single Page 🐛",
                                                            callback_data = f"KsplitS|{number_of_pages}")
                                                 ],[
                                                     InlineKeyboardButton("« Back «",
                                                              callback_data = f"KBTPM|{number_of_pages}")
                                                 ]]
                                             ))
    except Exception: pass

@ILovePDF.on_callback_query(splitProcess)
async def _splitProcess(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.message_id
        
        # CHECKS IF USER IN PROCESS
        if chat_id in PROCESS:
            await callbackQuery.answer(
                                      "Work in progress..🙇"
                                      )
            return
        await callbackQuery.answer()
        data = callbackQuery.data
        if data.startswith(tuple(["splitR", "KsplitR|"])):
            process = "Range"
        else:
            process = "Single"
        
        if data.startswith("K"):
            _, number_of_pages = callbackQuery.data.split("|")
        
        # ADD TO PROCESS
        PROCESS.append(chat_id)
        nabilanavab = True; i = 0
        while(nabilanavab):
            # REQUEST FOR PG NUMBER (MAX. LIMIT 5)
            if i >= 5:
                await callbackQuery.message.reply(
                                                 "`5 attempt over.. Process canceled..`😏"
                                                 )
                break
            i += 1
            needPages = await bot.ask(
                                     text = "__Pdf Split » By Range\n"
                                            "Now, Enter the range (start:end) :__\n\n"
                                            "/exit __to cancel__",
                                     chat_id = chat_id,
                                     reply_to_message_id = message_id,
                                     filters = filters.text,
                                     reply_markup = ForceReply(True)
                                     )
            # IF /exit PROCESS CANCEL
            if needPages.text == "/exit":
                await needPages.reply(
                                     "`Process Cancelled..` 😏",
                                     quote = True
                                     )
                break
            if data == "splitR":
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                if len(pageStartAndEnd) > 2:
                    await callbackQuery.message.reply(
                                                     "`Syntax Error: justNeedStartAndEnd `🚶"
                                                     )
                elif len(pageStartAndEnd) == 2:
                    start = pageStartAndEnd[0]; end = pageStartAndEnd[1]
                    if start.isdigit() and end.isdigit():
                        if (1 <= int(pageStartAndEnd[0])):
                            if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                                nabilanavab = False
                                break
                            else:
                                await callbackQuery.message.reply(
                                                                 "`Syntax Error: errorInEndingPageNumber `🚶"
                                                                 )
                        else:
                            await callbackQuery.message.reply(
                                                             "`Syntax Error: errorInStartingPageNumber `🚶"
                                                             )
                    else:
                        await callbackQuery.message.reply(
                                                         "`Syntax Error: pageNumberMustBeADigit` 🧠"
                                                         )
                else:
                    await callbackQuery.message.reply(
                                                     "`Syntax Error: noEndingPageNumber Or notADigit` 🚶"
                                                     )
            if data == "splitS":
                newList = []
                singlePages = list(needPages.text.replace(',',':').split(':'))
                if 1 <= len(singlePages) <= 100:
                    try:
                        for i in singlePages:
                            if i.isdigit():
                                newList.append(i)
                        if newList != []:
                            nabilanavab = False
                            break
                        elif newList == []:
                            await callbackQuery.message.reply(
                                                             "`Cant find any number..`😏"
                                                             )
                            continue
                    except Exception: pass
                else:
                    await callbackQuery.message.reply(
                                                     "`Something went Wrong..`😅"
                                                     )
            if data.startswith("KsplitR|"):
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                if len(pageStartAndEnd)>2:
                    await callbackQuery.message.reply(
                                                     "`Syntax Error: justNeedStartAndEnd `🚶"
                                                     )
                elif len(pageStartAndEnd) == 2:
                    start = pageStartAndEnd[0]; end = pageStartAndEnd[1]
                    if start.isdigit() and end.isdigit():
                        if (int(1) <= int(start) and int(start) < int(number_of_pages)):
                            if (int(start) < int(end) and int(end) <= int(number_of_pages)):
                                nabilanavab = False
                                break
                            else:
                                await callbackQuery.message.reply(
                                                                 "`Syntax Error: errorInEndingPageNumber `🚶"
                                                                 )
                        else:
                            await callbackQuery.message.reply(
                                                             "`Syntax Error: errorInStartingPageNumber `🚶"
                                                             )
                    else:
                        await callbackQuery.message.reply(
                                                         "`Syntax Error: pageNumberMustBeADigit` 🚶"
                                                         )
                else:
                    await callbackQuery.message.reply(
                                                     "`Syntax Error: noSuchPageNumbers` 🚶"
                                                     )
            if data.startswith("KsplitS|"):
                newList = []
                singlePages = list(needPages.text.replace(',',':').split(':'))
                if 1 <= int(len(singlePages)) and int(len(singlePages)) <= 100:
                    try:
                        for i in singlePages:
                            if (i.isdigit() and int(i) <= int(number_of_pages)):
                                newList.append(i)
                        if newList == []:
                            await callbackQuery.message.reply(
                                                             f"`Enter Numbers less than {number_of_pages}..`😏"
                                                             )
                            continue
                        else:
                            nabilanavab = False
                            break
                    except Exception: pass
                else:
                    await callbackQuery.message.reply(
                                                     "`Something went Wrong..`😅"
                                                     )
        
        # nabilanavab == False [No Error]
        if nabilanavab == True:
            PROCESS.remove(chat_id)
        if nabilanavab == False:
            input_file = f"{message_id}/inPut.pdf"
            output_file = f"{message_id}/outPut.pdf"
            
            downloadMessage = await callbackQuery.message.reply(
                                                               "`Downloding your pdf..` 📥", 
                                                               quote = True
                                                               )
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            c_time = time.time()
            downloadLoc = await bot.download_media(
                                                  message = file_id,
                                                  file_name = input_file,
                                                  progress = progress,
                                                  progress_args = (
                                                                  fileSize,
                                                                  downloadMessage,
                                                                  c_time
                                                  ))
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            await downloadMessage.edit(
                                      "`Downloading Completed..` ✅"
                                      )
            if not data.startswith("K"):
                checked, number_of_pages = await checkPdf(input_file, callbackQuery)
                if not(checked == "pass"):
                    await downloadMessage.delete()
                    return
            splitInputPdf = PdfFileReader(input_file)
            number_of_pages = splitInputPdf.getNumPages()
            
            if data == "splitR":
                if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                    await callbackQuery.message.reply(
                                                     "`1st Check Number of pages` 😏"
                                                     )
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f"{message_id}")
                    return
            
            splitOutput = PdfFileWriter()
            
            if data == "splitR":
                for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                    splitOutput.addPage(
                        splitInputPdf.getPage(i)
                    )
            elif data == "splitS":
                for i in newList:
                    if int(i) <= int(number_of_pages):
                        splitOutput.addPage(
                            splitInputPdf.getPage(
                                int(i)-1
                            )
                        )
            elif data.startswith("KsplitR"):
                for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                    splitOutput.addPage(
                        splitInputPdf.getPage(i)
                    )
            elif data.startswith("KsplitS"):
                for i in newList:
                    if int(i) <= int(number_of_pages):
                        splitOutput.addPage(
                            splitInputPdf.getPage(
                                int(i)-1
                            )
                        )
            
            with open(output_file, "wb") as output_stream:
                splitOutput.write(output_stream)
            
            fileNm = callbackQuery.message.reply_to_message.document.file_name
            thumbnail, fileName = await thumbName(callbackQuery.message, fileNm)
            if PDF_THUMBNAIL != thumbnail:
                location = await bot.download_media(
                                                   message = thumbnail,
                                                   file_name = f"{callbackQuery.message.message_id}.jpeg"
                                                   )
                thumbnail = await formatThumb(location)
            
            await downloadMessage.edit(
                                      "⚙️ `Started Uploading..` 📤"
                                      )
            await callbackQuery.message.reply_chat_action(
                                                         "upload_document"
                                                         )
            if data.startswith(tuple(["splitS", "KsplitS"])):
                caption = f"{newList}"
            else:
                caption = f"from `{pageStartAndEnd[0]}` to `{pageStartAndEnd[1]}`"
            c_time = time.time()
            await callbackQuery.message.reply_document(
                                                      file_name = fileName,
                                                      thumb = thumbnail,
                                                      quote = True,
                                                      document = output_file,
                                                      caption = caption,
                                                      progress = uploadProgress,
                                                      progress_args = (
                                                                      downloadMessage,
                                                                      c_time
                                                                      )
                                                      )
            
            await downloadMessage.delete()
            PROCESS.remove(chat_id)
            try:
                os.remove(location)
            except Exception: pass
            shutil.rmtree(f"{message_id}")
            await footer(callbackQuery.message, False)
    except Exception:
        logger.exception(
                        "SPLIT:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
        except Exception: pass

#                                                                                                     Telegram : @nabilanavab
