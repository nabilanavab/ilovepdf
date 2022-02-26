# fileName : plugins/toKnown.py
# copyright ©️ 2021 nabilanavab




from pyrogram.types import Message
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`What shall i wanted to do with this file.?`

File Name : `{}`
File Size : `{}`

`Number of Pages: {}`✌️"""

#--------------->
#--------> EDIT CHECKPDF MESSAGE (IF PDF & NOT ENCRYPTED)
#------------------->

# convert unknown to known page number msgs
async def toKnown(callbackQuery, number_of_pages):
    try:
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            pdfInfoMsg.format(
                fileName, await gSF(fileSize), number_of_pages
            ),
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⭐ get page No & info ⭐",
                            callback_data=f"KpdfInfo|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "To Images 🖼️",
                            callback_data=f"KtoImage|{number_of_pages}"
                        ),
                        InlineKeyboardButton(
                            "To Text ✏️",
                            callback_data=f"KtoText|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Encrypt 🔐",
                            callback_data=f"Kencrypt|{number_of_pages}"
                        ),
                        InlineKeyboardButton(
                            "Decrypt 🔓",
                            callback_data=f"notEncrypted"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Compress 🗜️",
                            callback_data=f"Kcompress"
                        ),
                        InlineKeyboardButton(
                            "Rotate 🤸",
                            callback_data=f"Krotate|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                           "Split ✂️",
                            callback_data=f"Ksplit|{number_of_pages}"
                        ),
                        InlineKeyboardButton(
                            "Merge 🧬",
                            callback_data="merge"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Stamp ™️",
                            callback_data=f"Kstamp|{number_of_pages}"
                        ),
                        InlineKeyboardButton(
                            "Rename ✏️",
                            callback_data="rename"
                        )
                    ]
                ]
            )
        )
    except Exception as e:
        print(f"plugins/toKnown: {e}")


#                                                                                  Telegram: @nabilanavab
