# fileName : plugins/dm/callBack/asImgOrDoc.py
# copyright ©️ 2021 nabilanavab

from pyrogram import filters
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfReply = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⭐ META£ATA ⭐", callback_data="pdfInfo"),
                InlineKeyboardButton("🗳️ PREVIEW 🗳️", callback_data="preview")
            ],[
                InlineKeyboardButton("🖼️ toIMAGES 🖼️", callback_data="toImage"),
                InlineKeyboardButton("✏️ toTEXT ✏️", callback_data="toText")
            ],[
                InlineKeyboardButton("🔐 ENCRYPT 🔐", callback_data="encrypt"),
                InlineKeyboardButton("🔓 DECRYPT 🔓", callback_data="decrypt")
            ],[
                InlineKeyboardButton("🗜 COMPRESS 🗜️", callback_data="compress"),
                InlineKeyboardButton("🤸 ROTATE 🤸", callback_data="rotate")
            ],[
                InlineKeyboardButton("✂️ SPLIT ✂️", callback_data="split"),
                InlineKeyboardButton("🧬 MERGE 🧬", callback_data="merge")
            ],[
                InlineKeyboardButton("™️ STAMP ™️", callback_data="stamp"),
                InlineKeyboardButton("✏️ RENAME ✏️", callback_data="rename")
            ],[
                InlineKeyboardButton("🚫 CLOSE 🚫",callback_data="closeALL")
            ]
        ]
    )

BTPMcb = """`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`"""

KBTPMcb = """`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️"""

#--------------->
#--------> LOCAL VARIABLES
#------------------->

"""
______VARIABLES______

I : as image
D : as document
K : pgNo known
A : Extract All
R : Extract Range
S : Extract Single page
BTPM : back to pdf message
KBTPM : back to pdf message (known pages)

"""

#--------------->
#--------> PDF TO IMAGES (CB/BUTTON)
#------------------->


BTPM = filters.create(lambda _, __, query: query.data == "BTPM")
toImage = filters.create(lambda _, __, query: query.data == "toImage")
KBTPM = filters.create(lambda _, __, query: query.data.startswith("KBTPM|"))
KtoImage = filters.create(lambda _, __, query: query.data.startswith("KtoImage|"))

I = filters.create(lambda _, __, query: query.data == "I")
D = filters.create(lambda _, __, query: query.data == "D")
KI = filters.create(lambda _, __, query: query.data.startswith("KI|"))
KD = filters.create(lambda _, __, query: query.data.startswith("KD|"))


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(I)
async def _I(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » as Img » Pages:           \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data="IA")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data="IR")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data="IS")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="toImage")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(D)
async def _D(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » as Doc » Pages:           \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data="DA")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data="DR")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data="DS")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="toImage")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KI)
async def _KI(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » as Img » Pages:           \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data=f"KIA|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data=f"KIR|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data=f"KIS|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KtoImage|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KD)
async def _KD(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » as Doc » Pages:           \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data=f"KDA|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data=f"KDR|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data=f"KDS|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KtoImage|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toImage)
async def _toImage(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Send pdf Images as:           \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Images 🖼️", callback_data="I")
                    ],[
                        InlineKeyboardButton("Documents 📂", callback_data="D")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="BTPM")
                    ]
                ]
            )
        )
    except Exception:
        pass

# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoImage)
async def _KtoImage(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Send pdf Images as:           \nTotal pages: {number_of_pages}__ 😐",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Images 🖼️", callback_data=f"KI|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("Documents 📂", callback_data=f"KD|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# back to pdf message (unknown page number)
@ILovePDF.on_callback_query(BTPM)
async def _BTPM(bot, callbackQuery):
    try:
        fileName=callbackQuery.message.reply_to_message.document.file_name
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            BTPMcb.format(
                fileName, await gSF(fileSize)
            ),
            reply_markup = pdfReply
        )
    except Exception:
        pass

# back to pdf message (with known page Number)
@ILovePDF.on_callback_query(KBTPM)
async def _KBTPM(bot, callbackQuery):
    try:
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            KBTPMcb.format(
                fileName, await gSF(fileSize), number_of_pages
            ),
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⭐ META£ATA ⭐", callback_data=f"KpdfInfo|{number_of_pages}"),
                        InlineKeyboardButton("🗳️ PREVIEW 🗳️", callback_data="Kpreview")
                    ],[
                        InlineKeyboardButton("🖼️ toIMAGES 🖼️", callback_data=f"KtoImage|{number_of_pages}"),
                        InlineKeyboardButton("✏️ ToTEXT ✏️", callback_data=f"KtoText|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🔐 ENCRYPT 🔐", callback_data=f"Kencrypt|{number_of_pages}"),
                        InlineKeyboardButton("🔓 DECRYPT 🔓", callback_data=f"notEncrypted")
                    ],[
                        InlineKeyboardButton("🗜️ COMPRESS 🗜️", callback_data=f"Kcompress"),
                        InlineKeyboardButton("🤸 ROTATE 🤸", callback_data=f"Krotate|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("✂️ SPLIT ✂️", callback_data=f"Ksplit|{number_of_pages}"),
                        InlineKeyboardButton("🧬 MERGE 🧬", callback_data="merge")
                    ],[
                        InlineKeyboardButton("™️ STAMP ™️", callback_data=f"Kstamp|{number_of_pages}"),
                        InlineKeyboardButton("✏️ RENAME ✏️", callback_data="rename")
                    ],[
                        InlineKeyboardButton("🚫 CLOSE 🚫", callback_data="closeALL")
                    ]
                ]
            )
        )
    except Exception:
        pass

#                                                                                             Telegram: @nabilanavab
