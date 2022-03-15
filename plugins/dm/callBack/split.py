# fileName : plugins/dm/callBack/split.py
# copyright ©️ 2021 nabilanavab

import time
import shutil
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from PyPDF2 import PdfFileWriter, PdfFileReader
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

pdfInfoMsg = """`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️
"""

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

# ----- ----- ----- ----- ----- ----- ----- CALLBACK SPLITTING PDF ----- ----- ----- ----- ----- ----- -----

split = filters.create(lambda _, __, query: query.data == "split")
Ksplit = filters.create(lambda _, __, query: query.data.startswith("Ksplit|"))

splitR = filters.create(lambda _, __, query: query.data == "splitR")
splitS = filters.create(lambda _, __, query: query.data == "splitS")

KsplitR = filters.create(lambda _, __, query: query.data.startswith("KsplitR|"))
KsplitS = filters.create(lambda _, __, query: query.data.startswith("KsplitS|"))



# Split pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(split)
async def _split(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Split pdf » Pages:            \n\nTotal Page Number(s):__ `unknown`",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("With In Range 🦞", callback_data="splitR")
                    ],[
                        InlineKeyboardButton("Single Page 🐛", callback_data="splitS")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="BTPM")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Split pgNo (with known pdf page number)
@ILovePDF.on_callback_query(Ksplit)
async def _Ksplit(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"Split pdf » Pages:          \n\nTotal Page Number(s): {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("With In Range 🦞", callback_data=f"KsplitR|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("Single Page 🐛", callback_data=f"KsplitS|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(splitR)
async def _splitROrS(bot, callbackQuery):
    try:
        # CHECKS IF USER IN PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        # ADD TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # PYROMOD (ADD-ON)
        nabilanavab = True; i = 0
        while(nabilanavab):
            # REQUEST FOR PG NUMBER (MAX. LIMIT 5)
            if i >= 5:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 attempt over.. Process canceled..`😏"
                )
                break
            i += 1
            needPages = await bot.ask(
                text="__Pdf Split » By Range\nNow, Enter the range (start:end) :__\n\n/exit __to cancel__",
                chat_id=callbackQuery.message.chat.id,
                reply_to_message_id=callbackQuery.message.message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            # IF /exit PROCESS CANCEL
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Process Cancelled..` 😏"
                )
                break
            pageStartAndEnd=list(needPages.text.replace('-',':').split(':'))
            if len(pageStartAndEnd) > 2:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: justNeedStartAndEnd `🚶"
                )
            elif len(pageStartAndEnd) == 2:
                start = pageStartAndEnd[0]
                end = pageStartAndEnd[1]
                if start.isdigit() and end.isdigit():
                    if (1 <= int(pageStartAndEnd[0])):
                        if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                            nabilanavab = False
                            break
                        else:
                            await bot.send_message(
                                callbackQuery.message.chat.id,
                                "`Syntax Error: errorInEndingPageNumber `🚶"
                            )
                    else:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`Syntax Error: errorInStartingPageNumber `🚶"
                        )
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`Syntax Error: pageNumberMustBeADigit` 🧠"
                    )
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: noEndingPageNumber Or notADigit` 🚶"
                )
        # nabilanavab=True iff AN ERROR OCCURS
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        if nabilanavab == False:
            downloadMessage = await callback_data.message.reply_text(
                text="`Downloding your pdf..` ⏳", quote=True
            )
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc = await bot.download_media(
                message=file_id,
                file_name=f"{callbackQuery.message.message_id}/pdf.pdf",
                progress=progress,
                progress_args=(
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            await downloadMessage.edit(
                "`Downloading Completed..🤞`"
            )
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            splitInputPdf = PdfFileReader(f"{callbackQuery.message.message_id}/pdf.pdf")
            number_of_pages = splitInputPdf.getNumPages()
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`1st Check Number of pages` 😏"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                return
            splitOutput = PdfFileWriter()
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            file_path=f"{callbackQuery.message.message_id}/split.pdf"
            with open(file_path, "wb") as output_stream:
                splitOutput.write(output_stream)
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name="SPLITED.pdf", thumb=PDF_THUMBNAIL, quote=True,
                document=f"{callbackQuery.message.message_id}/split.pdf",
                caption=f"from `{pageStartAndEnd[0]}` to `{pageStartAndEnd[1]}`"
            )
            await downloadMessage.delete()
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("SplitR: ",e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass

# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(splitS)
async def _splitS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        PROCESS.append(callbackQuery.message.chat.id)
        newList = []
        nabilanavab = True; i = 0
        while(nabilanavab):
            if i >= 5:
                bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 attempt over.. Process canceled..`😏"
                )
                break
            i += 1
            needPages = await bot.ask(
                text="__Pdf Split » By Pages\nNow, Enter Page Numbers seperate by__ (,) :\n\n/exit __to cancel__",
                chat_id=callbackQuery.message.chat.id,
                reply_to_message_id=callbackQuery.message.message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            singlePages = list(needPages.text.replace(',',':').split(':'))
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Process Cancelled..` 😏"
                )
                break
            elif 1 <= len(singlePages) <= 100:
                try:
                    for i in singlePages:
                        if i.isdigit():
                            newList.append(i)
                    if newList != []:
                        nabilanavab = False
                        break
                    elif newList == []:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`Cant find any number..`😏"
                        )
                        continue
                except Exception:
                    pass
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Something went Wrong..`😅"
                )
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        if nabilanavab == False:
            downloadMessage = await callbackQuery.message.reply_text(
                text="`Downloding your pdf..`⏳", quote=True
            )
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc = await bot.download_media(
                message=file_id,
                file_name=f"{callbackQuery.message.message_id}/pdf.pdf",
                progress=progress,
                progress_args=(
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            await downloadMessage.edit(
                "`Downloading Completed..🤞`"
            )
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
            splitInputPdf=PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages=splitInputPdf.getNumPages()
            splitOutput=PdfFileWriter()
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            with open(
                f"{callbackQuery.message.message_id}/split.pdf", "wb"
            ) as output_stream:
                splitOutput.write(output_stream)
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name="SPLITED.pdf", thumb=PDF_THUMBNAIL,
                document=f"{callbackQuery.message.message_id}/split.pdf",
                caption=f"Pages : `{newList}`", quote=True
            )
            await downloadMessage.delete()
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("splitS ;", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass

# Split (with known pdf page number)
@ILovePDF.on_callback_query(KsplitR)
async def _KsplitR(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        PROCESS.append(callbackQuery.message.chat.id)
        _, number_of_pages=callbackQuery.data.split("|")
        number_of_pages=int(number_of_pages)
        nabilanavab = True; i = 0
        while(nabilanavab):
            if i >= 5:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 attempt over.. Process canceled..`😏"
                )
                break
            i += 1
            needPages = await bot.ask(
                text=f"__Pdf Split » By Range\nNow, Enter the range (start:end) :\nTotal Pages : __`{number_of_pages}` 🌟\n\n/exit __to cancel__",
                chat_id=callbackQuery.message.chat.id,
                reply_to_message_id=callbackQuery.message.message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Process Cancelled..` 😏"
                )
                break
            pageStartAndEnd=list(needPages.text.replace('-',':').split(':'))
            if len(pageStartAndEnd) > 2:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: justNeedStartAndEnd `🚶"
                )
            elif len(pageStartAndEnd) == 2:
                start = pageStartAndEnd[0]
                end = pageStartAndEnd[1]
                if start.isdigit() and end.isdigit():
                    if (int(1) <= int(start) and int(start) < number_of_pages):
                        if (int(start) < int(end) and int(end) <= number_of_pages):
                            nabilanavab = False
                            break
                        else:
                            await bot.send_message(
                                callbackQuery.message.chat.id,
                                "`Syntax Error: errorInEndingPageNumber `🚶"
                            )
                    else:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            "`Syntax Error: errorInStartingPageNumber `🚶"
                        )
                else:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "`Syntax Error: pageNumberMustBeADigit` 🚶"
                    )
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Syntax Error: noSuchPageNumbers` 🚶"
                )
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        if nabilanavab == False:
            downloadMessage = await callbackQuery.message.reply_text(
                text="`Downloding your pdf..` ⏳", quote=True
            )
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc = await bot.download_media(
                message=file_id,
                file_name=f"{callbackQuery.message.message_id}/pdf.pdf",
                progress=progress,
                progress_args=(
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            await downloadMessage.edit(
                "`Downloading Completed..🤞`"
            )
            splitInputPdf = PdfFileReader(f"{callbackQuery.message.message_id}/pdf.pdf")
            number_of_pages = splitInputPdf.getNumPages()
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`1st Check the Number of pages` 😏"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                return
            splitOutput = PdfFileWriter()
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            file_path=f"{callbackQuery.message.message_id}/split.pdf"
            with open(file_path, "wb") as output_stream:
                splitOutput.write(output_stream)
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name="SPLITED.pdf", thumb=PDF_THUMBNAIL, quote=True,
                document=f"{callbackQuery.message.message_id}/split.pdf",
                caption=f"from `{pageStartAndEnd[0]}` to `{pageStartAndEnd[1]}`"
            )
            await downloadMessage.delete()
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("KsplitR :", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass

# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(KsplitS)
async def _KsplitS(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        PROCESS.append(callbackQuery.message.chat.id)
        _, number_of_pages = callbackQuery.data.split("|")
        newList = []
        nabilanavab = True; i = 0
        while(nabilanavab):
            if i >= 5:
                bot.send_message(
                    callbackQuery.message.chat.id,
                    "`5 attempt over.. Process canceled..`😏"
                )
                break
            i += 1
            needPages = await bot.ask(
                text=f"__Pdf Split » By Pages\nEnter Page Numbers seperate by__ (,) :\n__Total Pages : __`{number_of_pages}` 🌟\n\n/exit __to cancel__",
                chat_id=callbackQuery.message.chat.id,
                reply_to_message_id=callbackQuery.message.message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            singlePages = list(needPages.text.replace(',',':').split(':'))
            if needPages.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Process Cancelled..` 😏"
                )
                break
            elif 1 <= int(len(singlePages)) and int(len(singlePages)) <= 100:
                try:
                    for i in singlePages:
                        if (i.isdigit() and int(i) <= int(number_of_pages)):
                            newList.append(i)
                    if newList == []:
                        await bot.send_message(
                             callbackQuery.message.chat.id,
                            f"`Enter Numbers less than {number_of_pages}..`😏"
                        )
                        continue
                    else:
                        nabilanavab = False
                        break
                except Exception:
                    pass
            else:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`Something went Wrong..`😅"
                )
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
        if nabilanavab == False:
            downloadMessage = await callbackQuery.message.reply_text(
                text="`Downloding your pdf..`⏳", quote=True
            )
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc = await bot.download_media(
                message=file_id,
                file_name=f"{callbackQuery.message.message_id}/pdf.pdf",
                progress=progress,
                progress_args=(
                    fileSize,
                    downloadMessage,
                    c_time
                )
            )
            if downloadLoc is None:
                PROCESS.remove(callbackQuery.message.chat.id)
                return
            await downloadMessage.edit(
                "`Downloading Completed..🤞`"
            )
            splitInputPdf = PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
            number_of_pages = splitInputPdf.getNumPages()
            splitOutput = PdfFileWriter()
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            with open(
                f"{callbackQuery.message.message_id}/split.pdf", "wb"
            ) as output_stream:
                splitOutput.write(output_stream)
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name="SPLITED.pdf", thumb=PDF_THUMBNAIL,
                document=f"{callbackQuery.message.message_id}/split.pdf",
                caption=f"Pages : `{newList}`", quote=True
            )
            await downloadMessage.delete()
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("Ksplits: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass

#                                                                                                                                    Telegram: @nabilanavab
