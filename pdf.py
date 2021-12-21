# !/usr/bin/python
# -*- coding: utf-8 -*-

# ABOUT DEV. & SOURCE CODE
#    nabilanavab, india, kerala
#    Telegram: @nabilanavab
#    Email: nabilanavab@gmail.com
#    copyright ©️ 2021 nabilanavab
#    Released Under Apache License


import os
import fitz
import shutil
import logging
import convertapi
from PIL import Image
from time import sleep
from configs import Config, Msgs
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from PyPDF2 import PdfFileWriter, PdfFileReader
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# LOGGING INFO
# logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


# PYROGRAM INSTANCE
bot = Client(
    "pyroPdf",
    parse_mode = "markdown",
    api_id = Config.API_ID,
    api_hash = Config.API_HASH,
    bot_token = Config.API_TOKEN
)


# GLOBAL VARIABLES
PDF = {}            # save images for generating pdf
media = {}          # sending group images(pdf 2 img)
PDF2IMG = {}        # save fileId of each user(later uses)
PROCESS = []        # to check current process
mediaDoc = {}       # sending group document(pdf 2 img)
PAGENOINFO = {}     # saves no.of pages that user send last
PDF2IMGPGNO = {}    # more info about pdf file(for extraction)


# SUPPORTED FILES
suprtedFile = [
    ".jpg", ".jpeg", ".png"
]                                       # Img to pdf file support
suprtedPdfFile = [
    ".epub", ".xps", ".oxps",
    ".cbz", ".fb2"
]                                       # files to pdf (zero limits)
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


# CREATING ConvertAPI INSTANCE
if Config.CONVERT_API is not None:
    convertapi.api_secret = os.getenv("CONVERT_API")

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * 10000


# FORCE SUBSCRIPTION
async def forceSub(chatId):
    
    try:
        await bot.get_chat_member(
            str(Config.UPDATE_CHANNEL), chatId
        )
        return "subscribed"
        
    except Exception:
        
        try:
            invite_link = await bot.create_chat_invite_link(
                int(Config.UPDATE_CHANNEL)
            )
            
            await bot.send_message(
                chatId,
                Msgs.forceSubMsg.format(
                    chatId.from_user.first_name, chatId
                ),
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🌟 JOIN CHANNEL 🌟",
                                url = invite_link.invite_link
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Refresh ♻️",
                                callback_data = "refresh"
                            )
                        ]
                    ]
                )
            )
            return "notSubscribed"
        
        except Exception:
            pass


# REPLY TO /start COMMAND
@bot.on_message(filters.command(["start"]))
async def start(bot, message):
    
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        
        if Config.UPDATE_CHANNEL:
        
            try:
                await bot.get_chat_member(
                    str(Config.UPDATE_CHANNEL), message.chat.id
                )
            
            except Exception:
                invite_link = await bot.create_chat_invite_link(
                    int(Config.UPDATE_CHANNEL)
                )
                
                await bot.send_message(
                    message.chat.id,
                    Msgs.forceSubMsg.format(
                        message.from_user.first_name, message.chat.id
                    ),
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🌟 JOIN CHANNEL 🌟",
                                    url = invite_link.invite_link
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Refresh ♻️",
                                    callback_data = "refresh"
                                )
                            ]
                        ]
                    )
                )
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                return
        
        await bot.send_message(
            message.chat.id,
            Msgs.welcomeMsg.format(
                message.from_user.first_name, message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Source Code ❤️",
                            callback_data = "strtDevEdt"
                        ),
                        InlineKeyboardButton(
                            "Explore Bot 🎊",
                            callback_data = "imgsToPdfEdit"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Close",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        await bot.delete_messages(
            chat_id = message.chat.id,
            message_ids = message.message_id
        )
        
    except Exception:
        pass


# if message is a /id
@bot.on_message(filters.command(["id"]))
async def userId(bot, message):
    
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        await bot.send_message(
            message.chat.id, f'Your Id: `{message.chat.id}`'
        )
        
    except Exception:
        pass


# if message is a /feedback
@bot.on_message(filters.command(["feedback"]))
async def feedback(bot, message):
    
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        await bot.send_message(
            message.chat.id, Msgs.feedbackMsg,
            disable_web_page_preview = True
        )
        
    except Exception:
        pass


# /deletes : Deletes current Images to pdf Queue
@bot.on_message(filters.command(["delete"]))
async def cancelI2P(bot, message):
    
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        del PDF[message.chat.id]
        await bot.send_message(
            message.chat.id, "`Queue deleted Successfully..`🤧",
            reply_to_message_id = message.message_id
        )
        shutil.rmtree(f"{message.chat.id}")
        
    except Exception:
        await bot.send_message(
            message.chat.id, "`No Queue founded..`😲",
            reply_to_message_id = message.message_id
        )


# cancel current pdf to image Queue
@bot.on_message(filters.command(["cancel"]))
async def cancelP2I(bot, message):
    
    try:
        PROCESS.remove(message.chat.id)
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        await bot.send_message(
            message.chat.id, '`Canceled current work..`🤧'
        )
    
    except Exception:
        await bot.send_message(
            message.chat.id, '`Nothing to cancel..`🏃'
        )


# if message is an image
@bot.on_message(filters.private & filters.photo)
async def images(bot, message):
    
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        
        if Config.UPDATE_CHANNEL:
            check = await forceSub(message.chat.id)
            
            if check == "notSubscribed":
                return
        
        imageReply = await bot.send_message(
            message.chat.id,
            "`Downloading your Image..⏳`",
            reply_to_message_id = message.message_id
        )
        
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id] = []
        
        await message.download(
            f"{message.chat.id}/{message.chat.id}.jpg"
        )
        
        img = Image.open(
            f"{message.chat.id}/{message.chat.id}.jpg"
        ).convert("RGB")
        
        PDF[message.chat.id].append(img)
        await imageReply.edit(
            Msgs.imageAdded.format(len(PDF[message.chat.id]))
        )
        
    except Exception:
        pass


# if message is a document/file
@bot.on_message(filters.private & filters.document)
async def documents(bot, message):
    
    try:
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        
        if Config.UPDATE_CHANNEL:
            check = await forceSub(message.chat.id)
            
            if check == "notSubscribed":
                return
        
        isPdfOrImg = message.document.file_name
        fileSize = message.document.file_size
        fileNm, fileExt = os.path.splitext(isPdfOrImg)
        
        if Config.MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            
            try:
                bigFileUnSupport = await bot.send_message(
                    message.chat.id,
                    Msgs.bigFileUnSupport.format(Config.MAX_FILE_SIZE, Config.MAX_FILE_SIZE)
                )
                
                sleep(5)
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = bigFileUnSupport.message_id
                )
                
            except Exception:
                pass
        
        elif fileExt.lower() in suprtedFile:
            
            try:
                imageDocReply = await bot.send_message(
                    message.chat.id,
                    "`Downloading your Image..⏳`",
                    reply_to_message_id = message.message_id
                )
                
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id] = []
                
                await message.download(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                )
                
                img = Image.open(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                ).convert("RGB")
                
                PDF[message.chat.id].append(img)
                await imageDocReply.edit(
                    Msgs.imageAdded.format(len(PDF[message.chat.id]))
                )
            
            except Exception as e:
                
                await imageDocReply.edit(
                    Msgs.errorEditMsg.format(e)
                )
                
                sleep(5)
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = imageDocReply.message_id
                )
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
        
        elif fileExt.lower() == ".pdf":
            
            try:
                if message.chat.id in PROCESS:
                    
                    await message.reply_text(
                        '`Doing Some other Work.. 🥵`'
                    )
                    return
                
                pdfMsgId = await bot.send_message(
                    message.chat.id,
                    "`Processing.. 🚶`"
                )
                
                await message.download(
                    f"{message.message_id}/pdftoimage.pdf"
                )
                
                doc = fitz.open(f'{message.message_id}/pdftoimage.pdf')
                noOfPages = doc.pageCount
                
                PDF2IMG[message.chat.id] = message.document.file_id
                PDF2IMGPGNO[message.chat.id] = noOfPages
                
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = pdfMsgId.message_id
                )
                
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                
                pdfMsgId = await message.reply_text(
                    Msgs.pdfReplyMsg.format(noOfPages),
                    reply_markup = ForceReply(),
                    parse_mode = "md"
                )
                
                doc.close()
                shutil.rmtree(f'{message.message_id}')
            
            except Exception as e:
                
                try:
                    PROCESS.remove(message.chat.id)
                    doc.close()
                    shutil.rmtree(f'{message.message_id}')
                    
                    await pdfMsgId.edit(
                        Msgs.errorEditMsg.format(e)
                    )
                    sleep(15)
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = pdfMsgId.message_id
                    )
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = message.message_id
                    )
                
                except Exception:
                    pass
        
        elif fileExt.lower() in suprtedPdfFile:
            
            try:
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                pdfMsgId = await message.reply_text(
                    "`Downloading your file..⏳`",
                )
                
                await message.download(
                    f"{message.message_id}/{isPdfOrImg}"
                )
                
                await pdfMsgId.edit(
                    "`Creating pdf..`💛"
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
                
                await pdfMsgId.edit(
                    "`Started Uploading..`🏋️"
                )
                
                sendfile = open(
                    f"{message.message_id}/{fileNm}.pdf", "rb"
                )
                
                await bot.send_document(
                    chat_id = message.chat.id,
                    document = sendfile,
                    thumb = Config.PDF_THUMBNAIL,
                    caption = f"`Converted: {fileExt} to pdf`"
                )
                await pdfMsgId.edit(
                    "`Uploading Completed..❤️`"
                )
                
                shutil.rmtree(f"{message.message_id}")
                
                sleep(5)
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                await bot.send_message(
                    message.chat.id, Msgs.feedbackMsg,
                    disable_web_page_preview = True
                )
            
            except Exception as e:
                
                try:
                    shutil.rmtree(f"{message.message_id}")
                    await pdfMsgId.edit(
                        Msgs.errorEditMsg.format(e)
                    )
                    sleep(15)
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = pdfMsgId.message_id
                    )
                    await bot.delete_messages(
                        chat_id = message.chat.id,
                        message_ids = message.message_id
                    )
                    
                except Exception:
                    pass
        
        elif fileExt.lower() in suprtedPdfFile2:
            
            if os.getenv("CONVERT_API") is None:
                
                pdfMsgId = await message.reply_text(
                    "`Owner Forgot to add ConvertAPI.. contact Owner 😒`",
                )
                sleep(15)
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = pdfMsgId.message_id
                )
            
            else:
                
                try:
                    await bot.send_chat_action(
                        message.chat.id, "typing"
                    )
                    pdfMsgId = await message.reply_text(
                        "`Downloading your file..⏳`",
                    )
                    
                    await message.download(
                        f"{message.message_id}/{isPdfOrImg}"
                    )
                    
                    await pdfMsgId.edit(
                        "`Creating pdf..`💛"
                    )
                    
                    try:
                        await convertapi.convert(
                            "pdf",
                            {
                                "File": f"{message.message_id}/{isPdfOrImg}"
                            },
                            from_format = fileExt[1:],
                        ).save_files(
                            f"{message.message_id}/{fileNm}.pdf"
                        )
                        
                    except Exception:
                        
                        try:
                            shutil.rmtree(f"{message.message_id}")
                            await pdfMsgId.edit(
                                "ConvertAPI limit reaches.. contact Owner"
                            )
                            
                        except Exception:
                            pass
                    
                    sendfile = open(
                        f"{message.message_id}/{fileNm}.pdf", "rb"
                    )
                    await bot.send_document(
                        chat_id = message.chat.id,
                        Document = sendfile,
                        thumb = Config.PDF_THUMBNAIL,
                        caption = f"`Converted: {fileExt} to pdf`",
                    )
                    
                    await pdfMsgId.edit(
                        "`Uploading Completed..`🏌️"
                    )
                    
                    shutil.rmtree(f"{message.message_id}")
                    
                    sleep(5)
                    await bot.send_chat_action(
                        message.chat.id, "typing"
                    )
                    await bot.send_message(
                        message.chat.id, Msgs.feedbackMsg,
                        disable_web_page_preview = True
                    )
                
                except Exception:
                    pass
        
        else:
            
            try:
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                unSuprtd = await bot.send_message(
                    message.chat.id, "`unsupported file..🙄`"
                )
                sleep(15)
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = unSuprtd.message_id
                )
                
            except Exception:
                pass
            
    except Exception:
        pass


# if message is /extract
@bot.on_message(filters.command(["extract"]))
async def extract(bot, message):
    
    try:
        if message.chat.id in PROCESS:
            
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await message.reply_text("`Doing Some Work..🥵`", quote=True)
            return
        
        needPages = message.text.replace('/extract ', '')
        
        if message.chat.id not in PDF2IMG:
            
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await bot.send_message(
                message.chat.id,
                "`send me a pdf first..🤥`"
            )
            return
        
        else:
            pageStartAndEnd = list(needPages.replace('-',':').split(':'))
            
            if len(pageStartAndEnd) > 2:
                
                await bot.send_message(
                    message.chat.id,
                    "`I just asked you starting & ending 😅`"
                )
                return
            
            elif len(pageStartAndEnd) == 2:
                try:
                    
                    if (1 <= int(pageStartAndEnd[0]) <= PDF2IMGPGNO[message.chat.id]):
                        
                        if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1]) <= PDF2IMGPGNO[message.chat.id]):
                            PAGENOINFO[message.chat.id] = [False, int(pageStartAndEnd[0]), int(pageStartAndEnd[1]), None]    #elmnts in list (is singlePage, start, end, if single pg number)
                            
                        else:
                            await bot.send_message(
                                message.chat.id,
                                "`Syntax Error: errorInEndingPageNumber 😅`"
                            )
                            return
                        
                    else:
                        await bot.send_message(
                            message.chat.id,
                            "`Syntax Error: errorInStartingPageNumber 😅`"
                        )
                        return
                    
                except:
                    
                    await bot.send_message(
                        message.chat.id,
                        "`Syntax Error: noSuchPageNumbers 🤭`"
                    )
                    return
            
            elif len(pageStartAndEnd) == 1:
                
                if pageStartAndEnd[0] == "/extract":
                    
                    if (PDF2IMGPGNO[message.chat.id]) == 1:
                        PAGENOINFO[message.chat.id] = [True, None, None, 1]
                        #elmnts in list (is singlePage, start, end, if single pg number)
                    
                    else:
                        PAGENOINFO[message.chat.id] = [False, 1, PDF2IMGPGNO[message.chat.id], None]
                        #elmnts in list (is singlePage, start, end, if single pg number)
                    
                elif 0 < int(pageStartAndEnd[0]) <= PDF2IMGPGNO[message.chat.id]:
                    PAGENOINFO[message.chat.id] = [True, None, None, pageStartAndEnd[0]]
                
                else:
                    await bot.send_message(
                        message.chat.id,
                        '`Syntax Error: noSuchPageNumber 🥴`'
                    )
                    return
            
            else:
                await bot.send_message(
                    message.chat.id,
                    "`Syntax Error: pageNumberMustBeAnIntiger 🧠`"
                )
                return
            
            if PAGENOINFO[message.chat.id][0] == False:
                
                if pageStartAndEnd[0] == "/extract":
                    await bot.send_message(
                        message.chat.id,
                        text = f"Extract images from `{PAGENOINFO[message.chat.id][1]}` to `{PAGENOINFO[message.chat.id][2]}` As:",
                        disable_web_page_preview = True,
                        reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Images 🖼️️",
                                        callback_data = "multipleImgAsImages"
                                    ),
                                    InlineKeyboardButton(
                                        "Document 📁 ",
                                        callback_data = "multipleImgAsDocument"
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "PDF 🎭",
                                        callback_data = "multipleImgAsPdfError"
                                    )
                                ]
                            ]
                        )
                    )
                
                else:
                    await bot.send_message(
                        message.chat.id,
                        text = f"Extract images from `{PAGENOINFO[message.chat.id][1]}` to `{PAGENOINFO[message.chat.id][2]}` As:",
                        disable_web_page_preview = True,
                        reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Images 🖼️️",
                                        callback_data = "multipleImgAsImages"
                                    ),
                                    InlineKeyboardButton(
                                        "Document 📁 ",
                                        callback_data = "multipleImgAsDocument"
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "PDF 🎭",
                                        callback_data = "multipleImgAsPdf"
                                    )
                                ]
                            ]
                        )
                    )
                
            if PAGENOINFO[message.chat.id][0] == True:
                
                await bot.send_message(
                    message.chat.id,
                    text = f"Extract page number: `{PAGENOINFO[message.chat.id][3]}` As:",
                    disable_web_page_preview = True,
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Images 🖼️️",
                                    callback_data = "asImages"
                                ),
                                InlineKeyboardButton(
                                    "Document 📁 ",
                                    callback_data = "asDocument"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "PDF 🎭",
                                    callback_data = "asPdf"
                                )
                            ]
                        ]
                    )
                )
                
    except Exception:
        
        try:
            del PAGENOINFO[message.chat.id]
            PROCESS.remove(message.chat.id)
            
        except Exception:
            pass


# If message is /text
@bot.on_message(filters.command(["text"]))
async def textCommand(bot, message):
    
    try:
        if message.chat.id in PROCESS:
            
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await message.reply_text(
                "`Doing Some Work..🥵`"
            )
            return
        
        if message.chat.id not in PDF2IMG:
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await bot.send_message(
                message.chat.id,
                "`send me a pdf first..🤥`"
            )
            return
        
        else:
            await bot.send_message(
                message.chat.id,
                text = f"Send Extracted Text As:",
                disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Text ✍️",
                                callback_data = "txtMsg"
                            ),
                            InlineKeyboardButton(
                                "Txt File 🗂️",
                                callback_data = "txtFile"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Html 🌐",
                                callback_data = "txtHtml"
                            ),
                            InlineKeyboardButton(
                                "Json 🔖",
                                callback_data = "txtJson"
                            )
                        ]
                    ]
                )
            )
            
    except Exception:
        
        try:
            del PAGENOINFO[message.chat.id]
            PROCESS.remove(message.chat.id)
            
        except Exception:
            pass


# If message is /encrypt
@bot.on_message(filters.command(["encrypt"]))
async def encrypt(bot, message):
    try:
        
        if message.chat.id in PROCESS:
            
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await message.reply_text(
                "`Doing Some Work..🥵`"
            )
            return
        
        if message.chat.id not in PDF2IMG:
            
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            await bot.send_message(
                message.chat.id,
                "`send me a pdf first..🤥`"
            )
            return
        
        password = message.text.replace('/encrypt ', '')
        
        if password == '/encrypt':
            
            await bot.send_message(
                message.chat.id,
                "`can't find a password..`🐹"
            )
            return
        
        PROCESS.append(message.chat.id)
        
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        pdfMsgId = await bot.send_message(
            message.chat.id,
            "`Downloading your pdf..`🕐"
        )
        
        await bot.download_media(
            PDF2IMG[message.chat.id],
            f"{message.message_id}/pdf.pdf"
        )
        
        await pdfMsgId.edit(
            "`Encrypting pdf.. `🔐"
        )
                
        outputFileObj = PdfFileWriter()
        inputFile = PdfFileReader(
            f"{message.message_id}/pdf.pdf"
        )
        pgNmbr = inputFile.numPages
        
        if pgNmbr > 150:
            await bot.send_message(
                message.chat.id,
                f"send me a pdf less than 150pgs..👀"
            )
            return
        
        for i in range(pgNmbr):
            
            if pgNmbr >= 50:
                if i % 10 == 0:
                    await pdfMsgId.edit(
                        f"`Encrypted {i}/{pgNmbr} pages..`🔑",
                    )
            
            page = inputFile.getPage(i)
            outputFileObj.addPage(page)
            
        outputFileObj.encrypt(password)
        
        await pdfMsgId.edit(
            text = "`Started Uploading..`🏋️",
        )
        
        with open(
            f"{message.message_id}/Encrypted.pdf", "wb"
        ) as f:
            outputFileObj.write(f)
        
        if message.chat.id not in PROCESS:
            try:
                shutil.rmtree(f'{message.message_id}')
                return
            
            except Exception:
                return
        
        await bot.send_chat_action(
            message.chat.id, "upload_document"
        )
        
        with open(
            f"{message.message_id}/Encrypted.pdf", "rb"
        ) as sendfile:
            
            await bot.send_document(
                chat_id = message.chat.id,
                document = sendfile,
                thumb = Config.PDF_THUMBNAIL,
                caption = Msgs.encryptedFileCaption.format(
                    pgNmbr, password
                )
            )
        
        await pdfMsgId.edit(
            "`Uploading Completed..`🏌️",
        )
        
        shutil.rmtree(f"{message.message_id}")
        
        del PDF2IMG[message.chat.id]
        PROCESS.remove(message.chat.id)
        
        sleep(5)
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        await bot.send_message(
            message.chat.id, Msgs.feedbackMsg,
            disable_web_page_preview=True
        )

    except Exception as e:
        
        try:
            await pdfMsgId.edit(
                Msgs.errorEditMsg.format(e)
            )
            PROCESS.remove(message.chat.id)
            shutil.rmtree(f"{message.message_id}")
            
            await pdfMsgId.edit(
                Msgs.errorEditMsg.format(e),
            )
            
        except Exception:
            pass


# If message is /generate
@bot.on_message(filters.command(["generate"]))
async def generate(bot, message):
    
    try:
        newName = str(message.text.replace("/generate", ""))
        images = PDF.get(message.chat.id)
        
        if isinstance(images, list):
            pgnmbr = len(PDF[message.chat.id])
            del PDF[message.chat.id]
        
        if not images:
            await bot.send_chat_action(
                message.chat.id, "typing"
            )
            imagesNotFounded = await message.reply_text(
                "`No image founded.!!`😒"
            )
            sleep(5)
            await message.delete()
            await bot.delete_messages(
                chat_id = message.chat.id,
                message_ids = imagesNotFounded.message_id
            )
            return
        
        gnrtMsgId = await bot.send_message(
            message.chat.id, f"`Generating pdf..`💚"
        )
        
        if newName == " name":
            fileName = f"{message.from_user.first_name}" + ".pdf"
        
        elif len(newName) > 1 and len(newName) <= 15:
            fileName = f"{newName}" + ".pdf"
        
        elif len(newName) > 15:
            fileName = f"{message.from_user.first_name}" + ".pdf"
        
        else:
            fileName = f"{message.chat.id}" + ".pdf"
        
        images[0].save(fileName, save_all = True, append_images = images[1:])
        
        await gnrtMsgId.edit(
            "`Uploading pdf.. `🏋️",
        )
        await bot.send_chat_action(
            message.chat.id, "upload_document"
        )
        
        with open(fileName, "rb") as sendfile:
            
            await bot.send_document(
                chat_id = message.chat.id,
                document = sendfile,
                thumb = Config.PDF_THUMBNAIL,
                caption = f"file Name: `{fileName}`\n\n`Total pg's: {pgnmbr}`",
            )
        
        await gnrtMsgId.edit(
            "`Successfully Uploaded.. `🤫",
        )
        
        os.remove(fileName)
        shutil.rmtree(f"{message.chat.id}")
        
        sleep(5)
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        await bot.send_message(
            message.chat.id, Msgs.feedbackMsg,
            disable_web_page_preview = True
        )
        
    except Exception as e:
        os.remove(fileName)
        shutil.rmtree(f"{message.chat.id}")
        print(e)


# delete spam messages
@bot.on_message(filters.private)
async def spam(bot, message):
    
    try:
        spamMsgId = await bot.send_message(
            message.chat.id, f"`unsupported media..😪`"
        )
        sleep(5)
        await message.delete()
        await bot.delete_messages(
            chat_id = message.chat.id,
            message_ids = spamMsgId.message_id
        )
    
    except Exception:
        pass


@bot.on_callback_query()
async def answer(client, callbackQuery):
    
    edit = callbackQuery.data
    
    if edit == "strtDevEdt":
        
        try:
            await callbackQuery.edit_message_text(
                Msgs.aboutDev, disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Source Codes",
                                url = "https://github.com/nabilanavab/ilovepdf"
                            ),
                            InlineKeyboardButton(
                                "🔙 Home 🏡",
                                callback_data = "back"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Close 🚶",
                                callback_data = "close"
                            )
                        ]
                    ]
                )
            )
            return
        
        except Exception:
            pass
        
    elif edit == "imgsToPdfEdit":
        
        try:
            await callbackQuery.edit_message_text(
                Msgs.I2PMsg, disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🔙 Home 🏡",
                                callback_data = "back"
                            ),
                            InlineKeyboardButton(
                                "PDF to images ➡️",
                                callback_data = "pdfToImgsEdit"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Close 🚶",
                                callback_data = "close"
                            )
                        ]
                    ]
                )
            )
            return
        
        except Exception:
            pass
        
    elif edit == "pdfToImgsEdit":
        
        try:
            await callbackQuery.edit_message_text(
                Msgs.P2IMsg, disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🔙 Imgs To Pdf",
                                callback_data = "imgsToPdfEdit"
                            ),
                            InlineKeyboardButton(
                                "Home 🏡",
                                callback_data = "back"
                            ),
                            InlineKeyboardButton(
                                "file to Pdf ➡️",
                                callback_data = "filsToPdfEdit"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Close 🚶",
                                callback_data = "close"
                            )
                        ]
                    ]
                )
            )
            return
        
        except Exception:
            pass
        
    elif edit == "filsToPdfEdit":
        
        try:
            await callbackQuery.edit_message_text(
                Msgs.F2PMsg, disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🔙 PDF to imgs",
                                callback_data = "pdfToImgsEdit"
                            ),
                            InlineKeyboardButton(
                                "Home 🏡",
                                callback_data = "back"
                            ),
                            InlineKeyboardButton(
                                "WARNING ⚠️",
                                callback_data = "warningEdit"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Close 🚶",
                                callback_data = "close"
                            )
                        ]
                    ]
                )
            )
            return
        
        except Exception:
            pass
        
    elif edit == "warningEdit":
        
        try:
            await callbackQuery.edit_message_text(
                Msgs.warningMessage, disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "WARNING ⚠️",
                                callback_data = "warningEdit"
                            ),
                            InlineKeyboardButton(
                                "Home 🏡",
                                callback_data = "back"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Close 🚶",
                                callback_data = "close"
                            )
                        ]
                    ]
                )
            )
            return
        
        except Exception:
            pass
        
    elif edit == "back":
        
        try:
            await callbackQuery.edit_message_text(
                Msgs.back2Start, disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Source Code ♥️",
                                callback_data = "strtDevEdt"
                            ),
                            InlineKeyboardButton(
                                "Explore More 🎊",
                                callback_data = "imgsToPdfEdit"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Close 🚶",
                                callback_data = "close"
                            )
                        ]
                    ]
                )
            )
            return
        
        except Exception:
            pass
    
    elif edit == "close":
        
        try:
            await bot.delete_messages(
                chat_id = callbackQuery.message.chat.id,
                message_ids = callbackQuery.message.message_id
            )
            return
        
        except Exception:
            pass
        
    elif edit in ["multipleImgAsImages", "multipleImgAsDocument", "asImages", "asDocument"]:
        
        try:
            if (callbackQuery.message.chat.id in PROCESS) or (callbackQuery.message.chat.id not in PDF2IMG):
                
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = "Same work done before..🏃"
                )
                return
            
            PROCESS.append(callbackQuery.message.chat.id)
            
            await bot.edit_message_text(
                chat_id = callbackQuery.message.chat.id,
                message_id = callbackQuery.message.message_id,
                text = "`Downloading your pdf..⏳`"
            )
            
            await bot.download_media(
                PDF2IMG[callbackQuery.message.chat.id],
                f'{callbackQuery.message.message_id}/pdf.pdf'
            )
            
            del PDF2IMG[callbackQuery.message.chat.id]
            del PDF2IMGPGNO[callbackQuery.message.chat.id]
            
            doc = fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf')
            zoom = 1
            mat = fitz.Matrix(zoom, zoom)
            
            if edit == "multipleImgAsImages" or edit == "multipleImgAsDocument":
                
                if int(int(PAGENOINFO[callbackQuery.message.chat.id][2])+1 - int(PAGENOINFO[callbackQuery.message.chat.id][1])) >= 11:
                    await bot.pin_chat_message(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = callbackQuery.message.message_id,
                        disable_notification = True,
                        both_sides = True
                    )
                
                percNo = 0
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = f"`Total pages: {int(PAGENOINFO[callbackQuery.message.chat.id][2])+1 - int(PAGENOINFO[callbackQuery.message.chat.id][1])}..⏳`"
                )
                totalPgList = range(int(PAGENOINFO[callbackQuery.message.chat.id][1]), int(PAGENOINFO[callbackQuery.message.chat.id][2] + 1))
                
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'{callbackQuery.message.message_id}/pgs')
                    
                    for pageNo in pgList:
                        page = doc.loadPage(pageNo-1)
                        pix = page.getPixmap(matrix = mat)
                        cnvrtpg += 1
                        
                        await bot.edit_message_text(
                            chat_id = callbackQuery.message.chat.id,
                            message_id = callbackQuery.message.message_id,
                            text = f"`Converted: {cnvrtpg}/{int((PAGENOINFO[callbackQuery.message.chat.id][2])+1 - int(PAGENOINFO[callbackQuery.message.chat.id][1]))} pages.. 🤞`"
                        )
                        
                        if callbackQuery.message.chat.id not in PROCESS:
                            
                            try:
                                await bot.edit_message_text(
                                    chat_id = callbackQuery.message.chat.id,
                                    message_id = callbackQuery.message.message_id,
                                    text = f"`Canceled at {cnvrtpg}/{int((PAGENOINFO[callbackQuery.message.chat.id][2])+1 - int(PAGENOINFO[callbackQuery.message.chat.id][1]))} pages.. 🙄`"
                                )
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            
                            except Exception:
                                return
                        
                        with open(
                            f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg','wb'
                        ):
                            pix.writePNG(f'{callbackQuery.message.message_id}/pgs/{pageNo}.jpg')
                        
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = callbackQuery.message.message_id,
                        text = f"`Started Uploading: {cnvrtpg}'th pg \n\nThis might take some Time :(.. 🤞`"
                    )
                    
                    directory = f'{callbackQuery.message.message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key=os.path.getctime)
                    
                    percNo = percNo + len(imag)
                    media[callbackQuery.message.chat.id] = []
                    mediaDoc[callbackQuery.message.chat.id] = []
                    LrgFileNo = 1
                    
                    for file in imag:
                        if os.path.getsize(file) >= 1000000:
                            
                            picture = Image.open(file)
                            CmpImg = f'{callbackQuery.message.message_id}/pgs/temp{LrgFileNo}.jpeg'
                            picture.save(CmpImg, "JPEG", optimize=True, quality = 50) 
                            
                            LrgFileNo += 1
                            
                            if os.path.getsize(CmpImg) >= 1000000:
                                continue
                            
                            else:
                                media[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaPhoto(media = file)
                                )
                                mediaDoc[
                                    callbackQuery.message.chat.id
                                ].append(
                                    InputMediaDocument(media = file)
                                )
                                continue
                        
                        media[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaPhoto(media = file)
                        )
                        mediaDoc[
                            callbackQuery.message.chat.id
                        ].append(
                            InputMediaDocument(media = file)
                        )
                    
                    if edit == "multipleImgAsImages":
                        
                        if callbackQuery.message.chat.id not in PROCESS:
                            
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            
                            except Exception:
                                return
                        
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_photo"
                        )
                        
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                media[callbackQuery.message.chat.id]
                            )
                            
                        except Exception:
                            del media[callbackQuery.message.chat.id]
                            del mediaDoc[callbackQuery.message.chat.id]
                        
                    if edit == "multipleImgAsDocument":
                        
                        if callbackQuery.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'{callbackQuery.message.message_id}')
                                doc.close()
                                return
                            
                            except Exception:
                                return
                        
                        await bot.send_chat_action(
                            callbackQuery.message.chat.id, "upload_document"
                        )
                        
                        try:
                            await bot.send_media_group(
                                callbackQuery.message.chat.id,
                                mediaDoc[callbackQuery.message.chat.id]
                            )
                        except Exception:
                            del mediaDoc[callbackQuery.message.chat.id]
                            del media[callbackQuery.message.chat.id]
                        
                    shutil.rmtree(f'{callbackQuery.message.message_id}/pgs')
                
                PROCESS.remove(callbackQuery.message.chat.id)
                del PAGENOINFO[callbackQuery.message.chat.id]
                doc.close()
                
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = f'`Uploading Completed.. `🏌️'
                )
                shutil.rmtree(f'{callbackQuery.message.message_id}')
                
                sleep(5)
                await bot.send_chat_action(
                    callbackQuery.message.chat.id, "typing"
                )
                await bot.send_message(
                    callbackQuery.message.chat.id, Msgs.feedbackMsg,
                    disable_web_page_preview=True
                )
            
            if edit == "asImages" or edit == "asDocument":
                
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = f"`Fetching page Number:{PAGENOINFO[callbackQuery.message.chat.id][3]} 🤧`"
                )
                
                page = doc.loadPage(int(PAGENOINFO[callbackQuery.message.chat.id][3])-1)
                pix = page.getPixmap(matrix = mat)
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = f"`Successfully Converted your page..✌️`"
                )
                
                os.mkdir(f'{callbackQuery.message.message_id}/pgs')
                
                with open(
                    f'{callbackQuery.message.message_id}/pgs/{PAGENOINFO[callbackQuery.message.chat.id][3]}.jpg','wb'
                ):
                    pix.writePNG(f'{callbackQuery.message.message_id}/pgs/{PAGENOINFO[callbackQuery.message.chat.id][3]}.jpg')
                
                file = f'{callbackQuery.message.message_id}/pgs/{PAGENOINFO[callbackQuery.message.chat.id][3]}.jpg'
                    
                if os.path.getsize(file) >= 1000000:
                    picture = Image.open(file)
                    CmpImg = f'{callbackQuery.message.message_id}/pgs/temp{PAGENOINFO[callbackQuery.message.chat.id][3]}.jpeg'
                    
                    picture.save(
                        CmpImg,
                        "JPEG",
                        optimize = True,
                        quality = 50
                    )
                    file = CmpImg
                    
                    if os.path.getsize(CmpImg) >= 1000000:
                        await bot.send_message(
                            callbackQuery.message.chat.id,
                            '`too high resolution.. 🙄`'
                        )
                        return
                    
                if edit == "asImages":
                    await bot.send_chat_action(
                        callbackQuery.message.chat.id, "upload_photo"
                    )
                    sendfile = open(file,'rb')
                    await bot.send_photo(
                        callbackQuery.message.chat.id,
                        sendfile
                    )
                    
                if edit == "asDocument":
                    await bot.send_chat_action(
                        callbackQuery.message.chat.id, "upload_document"
                    )
                    sendfile = open(file,'rb')
                    await bot.send_document(
                        callbackQuery.message.chat.id,
                        thumb = Config.PDF_THUMBNAIL,
                        document = sendfile
                    )
                    
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = f'`Uploading Completed.. `🏌️'
                )
                
                PROCESS.remove(callbackQuery.message.chat.id)
                del PAGENOINFO[callbackQuery.message.chat.id]
                doc.close()
                
                shutil.rmtree(f'{callbackQuery.message.message_id}')
                
                sleep(5)
                await bot.send_chat_action(
                    callbackQuery.message.chat.id, "typing"
                )
                await bot.send_message(
                    callbackQuery.message.chat.id, Msgs.feedbackMsg,
                    disable_web_page_preview = True
                )
                
        except Exception as e:
            
            try:
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = Msgs.errorEditMsg.format(e)
                )
                shutil.rmtree(f'{callbackQuery.message.message_id}')
                PROCESS.remove(callbackQuery.message.chat.id)
                doc.close()
            
            except Exception:
                pass
            
    elif edit == "multipleImgAsPdfError":
        
        try:
            await bot.answer_callback_query(
                callbackQuery.id,
                text = Msgs.fullPdfSplit,
                show_alert = True,
                cache_time = 0
            )
            
        except Exception:
            pass
        
    elif edit in ["multipleImgAsPdf", "asPdf"]:
        
        try:
            if (callbackQuery.message.chat.id in PROCESS) or (callbackQuery.message.chat.id not in PDF2IMG):
                
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = "Same work done before..🏃"
                )
                return
            
            PROCESS.append(callbackQuery.message.chat.id)
            
            await bot.edit_message_text(
                chat_id = callbackQuery.message.chat.id,
                message_id = callbackQuery.message.message_id,
                text = "`Downloading your pdf..⏳`"
            )
            
            await bot.download_media(
                PDF2IMG[callbackQuery.message.chat.id],
                f'{callbackQuery.message.message_id}/pdf.pdf'
            )
            
            del PDF2IMG[callbackQuery.message.chat.id]
            del PDF2IMGPGNO[callbackQuery.message.chat.id]
            
            try:
                if edit == "multipleImgAsPdf":
                    
                    splitInputPdf = PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
                    splitOutput = PdfFileWriter()
                    
                    for i in range(int(PAGENOINFO[callbackQuery.message.chat.id][1])-1, int(PAGENOINFO[callbackQuery.message.chat.id][2])):
                        splitOutput.addPage(
                            splitInputPdf.getPage(i)
                        )
                        
                    file_path = f"{callbackQuery.message.message_id}/split.pdf"
                    with open(file_path, "wb") as output_stream:
                        splitOutput.write(output_stream)
                        
                    await bot.send_document(
                        chat_id = callbackQuery.message.chat.id,
                        thumb = Config.PDF_THUMBNAIL,
                        document = f"{callbackQuery.message.message_id}/split.pdf"
                    )
                
                if edit == "asPdf":
                    
                    splitInputPdf = PdfFileReader(f'{callbackQuery.message.message_id}/pdf.pdf')
                    splitOutput = PdfFileWriter()
                    
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(PAGENOINFO[callbackQuery.message.chat.id][3])-1
                        )
                    )
                    
                    with open(f"{callbackQuery.message.message_id}/split.pdf", "wb") as output_stream:
                        splitOutput.write(output_stream)
                        
                    await bot.send_document(
                        chat_id = callbackQuery.message.chat.id,
                        thumb = Config.PDF_THUMBNAIL,
                        document = f"{callbackQuery.message.message_id}/split.pdf"
                    )
                
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                PROCESS.remove(callbackQuery.message.chat.id)
                del PAGENOINFO[callbackQuery.message.chat.id]
                
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = "`Uploading Completed..🤞`"
                )
            
            except Exception as e:
                
                try:
                    await bot.edit_message_text(
                        chat_id = callbackQuery.message.chat.id,
                        message_id = callbackQuery.message.message_id,
                        text = Msgs.errorEditMsg.format(e)
                    )
                    shutil.rmtree(f"{callbackQuery.message.message_id}")
                    PROCESS.remove(callbackQuery.message.chat.id)
                    del PAGENOINFO[callbackQuery.message.chat.id]
                
                except Exception:
                    pass
        
        except Exception as e:
            
            try:
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = Msgs.errorEditMsg.format(e)
                )
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                PROCESS.remove(callbackQuery.message.chat.id)
                del PAGENOINFO[callbackQuery.message.chat.id]
                
            except Exception:
                pass
        
    elif edit in ["txtFile", "txtMsg", "txtHtml", "txtJson"]:
        
        try:
            if (callbackQuery.message.chat.id in PROCESS) or (callbackQuery.message.chat.id not in PDF2IMG):
                
                await bot.edit_message_text(
                    chat_id = callbackQuery.message.chat.id,
                    message_id = callbackQuery.message.message_id,
                    text = "Same work done before..🏃"
                )
                return
                
            PROCESS.append(callbackQuery.message.chat.id)
            
            await bot.edit_message_text(
                chat_id = callbackQuery.message.chat.id,
                message_id = callbackQuery.message.message_id,
                text = "`Downloading your pdf..⏳`"
            )
            
            await bot.download_media(
                PDF2IMG[callbackQuery.message.chat.id],
                f'{callbackQuery.message.message_id}/pdf.pdf'
            )
            
            del PDF2IMG[callbackQuery.message.chat.id]
            del PDF2IMGPGNO[callbackQuery.message.chat.id]
            
            doc = fitz.open(f'{callbackQuery.message.message_id}/pdf.pdf') # open document
            
            if edit == "txtFile":
                
                out = open(f'{callbackQuery.message.message_id}/pdf.txt', "wb") # open text output
                for page in doc:                               # iterate the document pages
                    text = page.get_text().encode("utf8")      # get plain text (is in UTF-8)
                    out.write(text)                            # write text of page()
                    out.write(bytes((12,)))                    # write page delimiter (form feed 0x0C)
                out.close()
                
                await bot.send_chat_action(
                    callbackQuery.message.chat.id, "upload_document"
                )
                
                sendfile = open(f"{callbackQuery.message.message_id}/pdf.txt",'rb')
                await bot.send_document(
                    chat_id = callbackQuery.message.chat.id,
                    thumb = Config.PDF_THUMBNAIL,
                    document = sendfile
                )
                
                sendfile.close()
            
            if edit == "txtMsg":
                
                for page in doc:                                     # iterate the document pages
                    pdfText = page.get_text().encode("utf8")            # get plain text (is in UTF-8)
                    if 1 <= len(pdfText) <= 1048:
                        
                        if callbackQuery.message.chat.id not in PROCESS:
                            
                            try:
                                await bot.send_chat_action(
                                    callbackQuery.message.chat.id, "typing"
                                )
                                await bot.send_message(
                                    callbackQuery.message.chat.id, pdfText
                                )
                                
                            except Exception:
                                return
            
            if edit == "txtHtml":
                
                out = open(f'{callbackQuery.message.message_id}/pdf.html', "wb") # open text output
                
                for page in doc:                                     # iterate the document pages
                    text = page.get_text("html").encode("utf8")      # get plain text as html(is in UTF-8)
                    out.write(text)                                  # write text of page()
                    out.write(bytes((12,)))                          # write page delimiter (form feed 0x0C)
                out.close()
                
                await bot.send_chat_action(
                    callbackQuery.message.chat.id, "upload_document"
                )
                
                sendfile = open(f"{callbackQuery.message.message_id}/pdf.html",'rb')
                
                await bot.send_document(
                    chat_id = callbackQuery.message.chat.id,
                    thumb = Config.PDF_THUMBNAIL,
                    document = sendfile
                )
                
                sendfile.close()
            
            if edit == "txtJson":
                
                out = open(f'{callbackQuery.message.message_id}/pdf.json', "wb") # open text output
                
                for page in doc:                                    # iterate the document pages
                    text = page.get_text("json").encode("utf8")     # get plain text as html(is in UTF-8)
                    out.write(text)                                 # write text of page()
                    out.write(bytes((12,)))                         # write page delimiter (form feed 0x0C)
                out.close()
                
                await bot.send_chat_action(
                    callbackQuery.message.chat.id, "upload_document"
                )
                
                sendfile = open(f"{callbackQuery.message.message_id}/pdf.json", 'rb')
                await bot.send_document(
                    chat_id = callbackQuery.message.chat.id,
                    thumb = Config.PDF_THUMBNAIL,
                    document = sendfile
                )
                
                sendfile.close()
            
            await bot.edit_message_text(
                chat_id = callbackQuery.message.chat.id,
                message_id = callbackQuery.message.message_id,
                text = "`Completed my task..😉`"
            )
            
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f'{callbackQuery.message.message_id}')
            
        except Exception as e:
            
            try:
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    Msgs.errorEditMsg.format(e)
                )
                shutil.rmtree(f'{callbackQuery.message.message_id}')
                PROCESS.remove(callbackQuery.message.chat.id)
                doc.close()
            
            except Exception:
                pass
           
    elif edit == "refresh":
        
        try:
            await bot.get_chat_member(
                str(Config.UPDATE_CHANNEL),
                callbackQuery.message.chat.id
            )
            
            await bot.edit_message_text(
                chat_id = callbackQuery.message.chat.id,
                message_id = callbackQuery.message.message_id,
                text = Msgs.welcomeMsg.format(
                    callbackQuery.from_user.first_name,
                    callbackQuery.message.chat.id
                ),
                disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Source Code ❤️",
                                callback_data = "strtDevEdt"
                            ),
                            InlineKeyboardButton(
                                "Explore Bot 🎊",
                                callback_data = "imgsToPdfEdit"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Close",
                                callback_data = "close"
                            )
                        ]
                    ]
                )
            )
            
        except Exception:
            
            try:
                await bot.answer_callback_query(
                    callbackQuery.id,
                    text = Msgs.foolRefresh,
                    show_alert = True,
                    cache_time = 0
                )
                
            except Exception:
                pass
        
bot.run()
