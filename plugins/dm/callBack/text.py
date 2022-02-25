# fileName : plugins/dm/callBack/text.py
# copyright ©️ 2021 nabilanavab




import time
import fitz
import shutil
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️
"""

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

#--------------->
#--------> VARIABLES
#------------------->

"""
______VARIABLES______

M = text message
T = text file
H = html file
J = Json file

'K' for pg no known pdfs
"""

#--------------->
#--------> PDF TO TEXT
#------------------->


M = filters.create(lambda _, __, query: query.data in ["M", "KM"])
T = filters.create(lambda _, __, query: query.data in ["T", "KT"])
J = filters.create(lambda _, __, query: query.data in ["J", "KJ"])
H = filters.create(lambda _, __, query: query.data in ["H", "KH"])

toText = filters.create(lambda _, __, query: query.data == "toText")
KtoText = filters.create(lambda _, __, query: query.data.startswith("KtoText|"))


# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toText)
async def _toText(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf » Text\nTotal Pages: unknown 😐         \nNow, Specify the format:__",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Messages 📜",
                            callback_data="M"
                        ),
                        InlineKeyboardButton(
                            "Txt file 🧾",
                            callback_data="T"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Html 🌐",
                            callback_data="H"
                        ),
                        InlineKeyboardButton(
                            "Json 🎀",
                            callback_data="J"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« Back «",
                            callback_data="BTPM"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoText)
async def _KtoText(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf » Text\nTotal pages: {number_of_pages} 🌟         \nNow, Specify the format:__",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Messages 📜",
                            callback_data="KM"
                        ),
                        InlineKeyboardButton(
                            "Txt file 🧾",
                            callback_data="KT"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Html 🌐",
                            callback_data="KH"
                        ),
                        InlineKeyboardButton(
                            "Json 🎀",
                            callback_data="KJ"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« Back «",
                            callback_data=f"KBTPM|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# to Text file (with unknown pdf page number)
@ILovePDF.on_callback_query(T)
async def _T(bot, callbackQuery):
    try:
        # CHECH USER PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        # ADD TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        data = callbackQuery.data
        # DOWNLOAD MESSAGE
        downloadMessage = await callbackQuery.message.reply_text(
            "`Downloding your pdf..` ⏳", quote=True
        )
        # DOWNLOAD PROGRESS
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        c_time = time.time()
        downloadLoc = await bot.download_media(
            message = file_id,
            file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
            progress = progress,
            progress_args = (
                fileSize,
                downloadMessage,
                c_time
            )
        )
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit(
            "`Downloading Completed..` 🥱"
        )
        if data == "T":
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await bot.delete_messages(
                    chat_id = callbackQuery.message.chat.id,
                    message_ids = downloadMessage.message.message_id
                )
                return
        with fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf') as doc:
            number_of_pages = doc.pageCount
            with open(f'{callbackQuery.message.message_id}/pdf.txt', "wb") as out: # open text output
                for page in doc:                               # iterate the document pages
                    text = page.get_text().encode("utf8")      # get plain text (is in UTF-8)
                    out.write(text)                            # write text of page()
                    out.write(bytes((12,)))                    # write page delimiter (form feed 0x0C)
        await bot.send_chat_action(
            callbackQuery.message.chat.id,
            "upload_document"
        )
        await bot.send_document(
            chat_id = callbackQuery.message.chat.id,
            reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
            thumb = PDF_THUMBNAIL,
            document = f"{callbackQuery.message.message_id}/pdf.txt",
            caption = "__Txt file__"
        )
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("Text/T: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# to Text message (with unknown pdf page number)
@ILovePDF.on_callback_query(M)
async def _M(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        PROCESS.append(callbackQuery.message.chat.id)
        data = callbackQuery.data
        downloadMessage = await bot.send_message(
            chat_id = callbackQuery.message.chat.id,
            reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
            text = "`Downloding your pdf..` ⏳"
        )
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        c_time = time.time()
        downloadLoc = await bot.download_media(
            message = file_id,
            file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
            progress = progress,
            progress_args = (
                fileSize,
                downloadMessage,
                c_time
            )
        )
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit(
            "`Downloading Completed..` 🥱"
        )
        if data == "M":
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await bot.delete_messages(
                    chat_id = callbackQuery.message.chat.id,
                    message_ids = downloadMessage.message.message_id
                )
                return
        with fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf') as doc:
            number_of_pages = doc.pageCount
            for page in doc:                               # iterate the document pages
                pdfText = page.get_text().encode("utf8")            # get plain text (is in UTF-8)
                if 1 <= len(pdfText) <= 1048:
                    await bot.send_chat_action(
                        callbackQuery.message.chat.id, "typing"
                    )
                    await bot.send_message(
                        callbackQuery.message.chat.id, pdfText
                    )
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("Text/M: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# to Html file (with unknown pdf page number)
@ILovePDF.on_callback_query(H)
async def _H(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        PROCESS.append(callbackQuery.message.chat.id)
        data = callbackQuery.data
        downloadMessage = await bot.send_message(
            chat_id = callbackQuery.message.chat.id,
            reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
            text = "`Downloding your pdf..` ⏳"
        )
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        c_time = time.time()
        downloadLoc = await bot.download_media(
            message = file_id,
            file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
            progress = progress,
            progress_args = (
                fileSize,
                downloadMessage,
                c_time
            )
        )
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit(
            "`Downloading Completed..` 🥱"
        )
        if data == "H":
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await bot.delete_messages(
                    chat_id = callbackQuery.message.chat.id,
                    message_ids = downloadMessage.message.message_id
                )
                return
        with fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf') as doc:
            number_of_pages = doc.pageCount
            with open(f'{callbackQuery.message.message_id}/pdf.html', "wb") as out: # open text output
                for page in doc:                                # iterate the document pages
                    text = page.get_text("html").encode("utf8") # get plain text (is in UTF-8)
                    out.write(text)                             # write text of page()
                    out.write(bytes((12,)))                     # write page delimiter (form feed 0x0C)
        await bot.send_chat_action(
            callbackQuery.message.chat.id,
            "upload_document"
        )
        await bot.send_document(
            chat_id = callbackQuery.message.chat.id,
            reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
            thumb = PDF_THUMBNAIL,
            document = f"{callbackQuery.message.message_id}/pdf.html",
            caption = "__Html file : helps to view pdf on any browser..__ 😉"
        )
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception:
        try:
            print("Text/H: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


# to Text file (with unknown pdf page number)
@ILovePDF.on_callback_query(J)
async def _J(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress..🙇"
            )
            return
        PROCESS.append(callbackQuery.message.chat.id)
        data = callbackQuery.data
        downloadMessage = await bot.send_message(
            chat_id = callbackQuery.message.chat.id,
            reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
            text = "`Downloding your pdf..` ⏳"
        )
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        c_time = time.time()
        downloadLoc = await bot.download_media(
            message = file_id,
            file_name = f"{callbackQuery.message.message_id}/pdf.pdf",
            progress = progress,
            progress_args = (
                fileSize,
                downloadMessage,
                c_time
            )
        )
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit(
            "`Downloading Completed..` 🥱"
        )
        if data == "J":
            checked = await checkPdf(f'{callbackQuery.message.message_id}/pdf.pdf', callbackQuery)
            if not(checked == "pass"):
                await bot.delete_messages(
                    chat_id = callbackQuery.message.chat.id,
                    message_ids = downloadMessage.message.message_id
                )
                return
        with fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf') as doc:
            number_of_pages = doc.pageCount
            with open(f'{callbackQuery.message.message_id}/pdf.json', "wb") as out: # open text output
                for page in doc:                                # iterate the document pages
                    text = page.get_text("json").encode("utf8") # get plain text (is in UTF-8)
                    out.write(text)                             # write text of page()
                    out.write(bytes((12,)))                     # write page delimiter (form feed 0x0C)
        await bot.send_chat_action(
            callbackQuery.message.chat.id,
            "upload_document"
        )
        await bot.send_document(
            chat_id = callbackQuery.message.chat.id,
            reply_to_message_id = callbackQuery.message.reply_to_message.message_id,
            thumb = PDF_THUMBNAIL,
            document = f"{callbackQuery.message.message_id}/pdf.json",
            caption = "__Json File__"
        )
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception:
        try:
            print("Text/J: ", e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass


#                                                                                  Telegram: @nabilanavab
