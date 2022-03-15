# fileName : plugins/dm/callBack/stamp.py
# copyright ©️ 2021 nabilanavab




import os
import time
import fitz
import shutil
from time import sleep
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

"""
____VARIABLES____

stmp = Stamp CB

STAMP ANNOTATIONS: [pymuPdf/fituz](annot)
0 : STAMP_Approved
1 : STAMP_AsIs
2 : STAMP_Confidential
3 : STAMP_Departmental
4 : STAMP_Experimental
5 : STAMP_Expired
6 : STAMP_Final
7 : STAMP_ForComment
8 : STAMP_ForPublicRelease
9 : STAMP_NotApproved
10: STAMP_NotForPublicRelease
11: STAMP_Sold
12: STAMP_TopSecret
13: STAMP_Draft


COLOR: [RGB]
r = red, g = green, b = blue
"""


PDF_THUMBNAIL = Config.PDF_THUMBNAIL

#--------------->
#--------> PDF COMPRESSION
#------------------->

# pdfMessage to stamp --> "stamp"(stampselect)
stamp = filters.create(lambda _, __, query: query.data == "stamp")
Kstamp = filters.create(lambda _, __, query: query.data.startswith("Kstamp"))

# stampSelect to color --> "stmp"(stampcolor)
stmp = filters.create(lambda _, __, query: query.data.startswith("stmp"))
Kstmp = filters.create(lambda _, __, query: query.data.startswith("Kstmp"))

# color --> stamping process
colors = ["color", "Kcolor"]
color = filters.create(lambda _, __, query: query.data.startswith(tuple(colors)))



# stamp selet message(with unknown pdf page number)
@ILovePDF.on_callback_query(stamp)
async def _stamp(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Add Stamp » Select Stamp:         \nTotal pages: unknown__ 😐",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Not For Public Release 🤧", callback_data="stmp|10")
                    ],[
                        InlineKeyboardButton("For Public Release 🥱", callback_data="stmp|8")
                    ],[
                        InlineKeyboardButton("Confidential 🤫", callback_data="stmp|2"),
                        InlineKeyboardButton("Departmental 🤝", callback_data="stmp|3")
                    ],[
                        InlineKeyboardButton("Experimental 🔬", callback_data="stmp|4"),
                        InlineKeyboardButton("Expired 🐀",callback_data="stmp|5")
                    ],[
                        InlineKeyboardButton("Final 🔧", callback_data="stmp|6"),
                        InlineKeyboardButton("For Comment 🗯️",callback_data="stmp|7")
                    ],[
                        InlineKeyboardButton("Not Approved 😒",callback_data="stmp|9"),
                        InlineKeyboardButton("Approved 🥳", callback_data="stmp|0")
                    ],[
                        InlineKeyboardButton("Sold ✊",callback_data="stmp|11"),
                        InlineKeyboardButton("Top Secret 😷", callback_data="stmp|12"),
                    ],[
                        InlineKeyboardButton("Draft 👀",callback_data="stmp|13"),
                        InlineKeyboardButton("AsIs 🤏", callback_data="stmp|1")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="BTPM")
                    ]
                ]
            )
        )
    except Exception:
        pass


# Stamp select message (with known pdf page number)
@ILovePDF.on_callback_query(Kstamp)
async def _Kstamp(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Add Stamp » Select Stamp:         \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Not For Public Release 🤧", callback_data=f"Kstmp|{number_of_pages}|10")
                    ],[
                        InlineKeyboardButton("For Public Release 🥱", callback_data=f"Kstmp|{number_of_pages}|8")
                    ],[
                        InlineKeyboardButton("Confidential 🤫", callback_data=f"Kstmp|{number_of_pages}|2"),
                        InlineKeyboardButton("Departmental 🤝", callback_data=f"Kstmp|{number_of_pages}|3")
                    ],[
                        InlineKeyboardButton("Experimental 🔬", callback_data=f"Kstmp|{number_of_pages}|4"),
                        InlineKeyboardButton("Expired 🐀",callback_data=f"Kstmp|{number_of_pages}|5")
                    ],[
                        InlineKeyboardButton("Final 🔧", callback_data=f"Kstmp|{number_of_pages}|6"),
                        InlineKeyboardButton("For Comment 🗯️",callback_data=f"Kstmp|{number_of_pages}|7")
                    ],[
                        InlineKeyboardButton("Not Approved 😒",callback_data=f"Kstmp|{number_of_pages}|9"),
                        InlineKeyboardButton("Approved 🥳", callback_data=f"Kstmp|{number_of_pages}|0")
                    ],[
                        InlineKeyboardButton("Sold ✊",callback_data=f"Kstmp|{number_of_pages}|11"),
                        InlineKeyboardButton("Top Secret 😷", callback_data=f"Kstmp|{number_of_pages}|12"),
                    ],[
                        InlineKeyboardButton("Draft 👀",callback_data=f"Kstmp|{number_of_pages}|13"),
                        InlineKeyboardButton("AsIs 🤏", callback_data=f"Kstmp|{number_of_pages}|1")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass


# Stamp color message (with unknown pdf page number)
@ILovePDF.on_callback_query(stmp)
async def _stmp(bot, callbackQuery):
    try:
        _, annot = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            "__Add Stamp » Select Color:         \nTotal pages: unknown__ 😐",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Red ❤️", callback_data=f"color|{annot}|r"),
                        InlineKeyboardButton("Blue 💙", callback_data=f"color|{annot}|b")
                    ],[
                        InlineKeyboardButton("Green 💚", callback_data=f"color|{annot}|g"),
                        InlineKeyboardButton("Yellow 💛", callback_data=f"color|{annot}|c1")
                    ],[
                        InlineKeyboardButton("Pink 💜", callback_data=f"color|{annot}|c2"),
                        InlineKeyboardButton("Hue 💚", callback_data=f"color|{annot}|c3")
                    ],[
                        InlineKeyboardButton("White 🤍", callback_data=f"color|{annot}|c4"),
                        InlineKeyboardButton("Black 🖤", callback_data=f"color|{annot}|c5")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"stamp")
                    ]
                ]
            )
        )
    except Exception:
        pass


# Stamp color message (with known pdf page number)
@ILovePDF.on_callback_query(Kstmp)
async def _Kstmp(bot, callbackQuery):
    try:
        _, number_of_pages, annot = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Add Stamp » Select Color:         \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Red ❤️", callback_data=f"Kcolor|{annot}|r"),
                        InlineKeyboardButton("Blue 💙", callback_data=f"Kcolor|{annot}|b")
                    ],[
                        InlineKeyboardButton("Green 💚", callback_data=f"Kcolor|{annot}|g"),
                        InlineKeyboardButton("Yellow 💛", callback_data=f"Kcolor|{annot}|c1")
                    ],[
                        InlineKeyboardButton("Pink 💜", callback_data=f"Kcolor|{annot}|c2"),
                        InlineKeyboardButton("Hue 💚", callback_data=f"Kcolor|{annot}|c3")
                    ],[
                        InlineKeyboardButton("White 🤍", callback_data=f"Kcolor|{annot}|c4"),
                        InlineKeyboardButton("Black 🖤", callback_data=f"Kcolor|{annot}|c5")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"Kstamp|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass


@ILovePDF.on_callback_query(color)
async def _color(bot, callbackQuery):
    try:
        # CHECK IF USER IN PROCESS
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress.. 🙇"
            )
            return
        
        _, annot, colr = callbackQuery.data.split("|")
        # ADD USER TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        data = callbackQuery.data
        # STARTED DOWNLOADING
        downloadMessage=await callbackQuery.message.reply_text(
            "`Downloding your pdf..` ⏳", quote=True
        )
        input_file=f"{callbackQuery.message.message_id}/pdf.pdf"
        file_id=callbackQuery.message.reply_to_message.document.file_id
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        fileNm = callbackQuery.message.reply_to_message.document.file_name
        fileNm, fileExt = os.path.splitext(fileNm)        # seperates name & extension
        # DOWNLOAD PROGRESS
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
        
        # COLOR CODE
        if colr == "r":
            color = (1, 0, 0)
        elif colr == "b":
            color = (0, 0, 1)
        elif colr == "g":
            color = (0, 1, 0)
        elif colr == "c1":
            color = (1, 1, 0)
        elif colr == "c2":
            color = (1, 0, 1)
        elif colr == "c3":
            color = (0, 1, 1)
        elif colr == "c4":
            color = (1, 1, 1)
        elif colr == "c5":
            color = (0, 0, 0)
        
        # CHECK DOWNLOAD COMPLETED OR CANCELED
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        #STAMPING STARTED
        await downloadMessage.edit(
            "`Started Stamping..` 💠"
        )
        if data.startswith("color"):
            checked = await checkPdf(input_file, callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
        output_file=f"{callbackQuery.message.message_id}/stamped.pdf"
        r = fitz.Rect(72, 72, 440, 200)
        with fitz.open(input_file) as doc:
            page=doc.load_page(0)
            annot=page.add_stamp_annot(r, stamp=int(f"{annot}"))
            annot.set_colors(stroke=color)
            annot.set_opacity(0.5)
            annot.update()
            doc.save(output_file)
        # STARTED UPLOADING
        await bot.send_chat_action(
            callbackQuery.message.chat.id,
            "upload_document"
        )
        await downloadMessage.edit(
            "`Started Uploading..` 🏋️"
        )
        # SEND DOCUMENT
        await callbackQuery.message.reply_document(
            file_name=f"{fileNm}.pdf",
            document=open(output_file, "rb"),
            thumb=PDF_THUMBNAIL, quote=True,
            caption="stamped pdf"
        )
        # DELETE DOWNLOAD MESSAGE
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    
    except Exception as e:
        try:
            print("Stamp: ",e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
            await downloadMessage.delete()
        except Exception:
            pass


#                                                                                  Telegram: @nabilanavab
