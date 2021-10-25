# copyright ©️ 2021 nabilanavab
# !/usr/bin/python
# -*- coding: utf-8 -*-

# packages Used:
# pip install pyTelegramBotAPI
# pip install pillow
# pip install pyMuPdf
# pip install convertapi

import os
import telebot
from telebot import types
from telebot.types import InputMediaPhoto, InputMediaDocument
from PIL import Image
import shutil
from time import sleep
import fitz
import convertapi

#Creating an instance (telebot)
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")

#Creating an instance (convertapi)
if os.getenv("CONVERT_API") is not None:
    convertapi.api_secret = os.getenv("CONVERT_API")


#message replies
strtMsg = f"""Hey ..!! This bot will helps you to do many things with pdf's 🥳

Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert PDF to images`
◍ `Convert files to pdf`

Update Channel: @ilovepdf\_bot 🤩

[Source Code 🏆](https://github.com/nabilanavab/ilovepdf)
[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


aboutDev = """About Dev:

OwNeD By: @nabilanavab 😜
Update Channel: @ilovepdf\_bot 😇

Lang Used: Python🐍
[Source Code](https://github.com/nabilanavab/ilovepdf)

Join @ilovepdf\_bot, if you ❤ this

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


expMsg1 = """
Images to pdf :

        Just Send/forward me some images. When you are finished; use /generate to get your pdf..😉

 ◍ Image Sequence will be considered 🤓
 ◍ For better quality pdfs(send images without Compression) 🤧
 
 ◍ `/delete` - Delete's the current Queue 😒
 ◍ `/id` - to get your telegram ID 🤫
 
 ◍ RENAME YOUR PDF:
 
    - By default, your telegram ID will be treated as your pdf name..🙂
    - `/generate fileName` - to change pdf name to fileName🤞
    - `/generate name` - to get pdf with your telegram name

For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


expMsg2 = """
PDF to images:

        Just Send/forward me a pdf file.

 ◍ I will Convert it to images ✌️
 ◍ if Multiple pages in pdf(send as albums) 😌
 ◍ Page numbers are sequentially ordered 😬
 ◍ Send images faster than anyother bots 😋
 ◍ /cancel : to cancel a pdf to image work

1st bot on telegram wich send images without converting entire pdf to images

For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


expMsg3 = """
Files to PDF:

        Just Send/forward me a Supported file.. I will convert it to pdf and send it to you..😎

◍ Supported files(.epub, .xps, .oxps, .cbz, .fb2) 😁
◍ No need to specify your telegram file extension 🙄
◍ Only Images & ASCII characters Supported 😪
◍ added 30+ new file formats that can be converted to pdf..
API LIMITS..😕

For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


expMsg4 = """
WARNING MESSAGE ⚠️:

◍ This bot is completely free to use so please dont spam here 🙏

◍ Please don't try to spread 18+ contents 😒

IF THERE IS ANY KIND OF REPORTING, BUGS, REQUESTS, AND SUGGESTIONS PLEASE CONTACT @nabilanavab

For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


strtMsgCb = """
Hey..!! This bot will helps you to do many things with pdf's 🥳

Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert PDF to images`
◍ `Convert files to pdf`

For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


feedbackMsg = f"""
For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"""


#global Variables
PDF = {}   # for generating pdf
media = {}    # for sending group images(pdf 2 img)
PDF2IMG = {}    # saves file id of each use for later uses
PROCESS = []    # to check current process
mediaDoc = {}    # for sending group document(pdf 2 img)
PAGENOINFO = {}    # saves no.of pages that the user send last
PDF2IMGPGNO = {}    # more info about pdf file(for extraction)


# start message handler
@bot.message_handler(commands=["start"])
def strt(message):
    
    try:
        bot.send_chat_action(message.chat.id, "typing")
        
        key = types.InlineKeyboardMarkup()
        key.add(
            types.InlineKeyboardButton("Source Code ❤️", callback_data="strtDevEdt"),
            types.InlineKeyboardButton("Explore More 🥳", callback_data="imgsToPdfEdit"),
        )
        bot.send_message(
            message.chat.id,
            strtMsg, 
            disable_web_page_preview=True,
            reply_markup=key
        )
        
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        
    except Exception:
        pass


# /id : Get telegram id
@bot.message_handler(commands=["id"])
def UsrId(message):
    
    try:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, f"Your ID - `{message.chat.id}`")
    
    except Exception:
        pass


# /feedback Message
@bot.message_handler(commands=["feedback"])
def feedback(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(
            message.chat.id,
            feedbackMsg,
            disable_web_page_preview=True
        )
        
    except Exception:
        pass


# Deletes the current Images to pdf Queue
@bot.message_handler(commands=["delete"])
def delQueue(message):

    try:
        bot.send_chat_action(message.chat.id, "typing")
        shutil.rmtree(f"./{message.chat.id}")
        bot.reply_to(message, "`Queue deleted Successfully..`🤧")
        
        try:
            del PDF[message.chat.id]
        except Exception:
            pass

    except Exception:
        bot.reply_to(message, "`No Queue founded..`😲")


# cancel current pdf to image Queue
@bot.message_handler(commands=["cancel"])
def cancelP2I(message):
    
    try:
        PROCESS.remove(message.chat.id)
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, '`Canceled current work..`🤧')
    
    except Exception:
        bot.send_message(message.chat.id, '`Nothing to cancel..`🏃')


# Reply to images
@bot.message_handler(content_types=["photo"])
def pic(message):
    
    try:
        bot.send_chat_action(message.chat.id, "typing")
        picMsgId = bot.reply_to(
            message,
            "`Downloading your Image..⏳`",
        )
        
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id] = []
        
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        try:
            os.makedirs(f"./{message.chat.id}/imgs")
        
        except Exception:
            pass
        
        with open(f"./{message.chat.id}/imgs/{message.chat.id}.jpg", "wb") as new_file:
            new_file.write(downloaded_file)
        
        img = Image.open(
            f"./{message.chat.id}/imgs/{message.chat.id}.jpg"
        ).convert("RGB")
        
        PDF[message.chat.id].append(img)
        bot.edit_message_text(
            chat_id=message.chat.id,
            text=f"""`Added {len(PDF[message.chat.id])} page/'s to your pdf..`🤓

/generate to generate PDF 🤞""",
            message_id=picMsgId.message_id,
        )
    
    except Exception:
        pass


@bot.message_handler(content_types=["document"])
def fls(message):
    
    try:
        bot.send_chat_action(message.chat.id, "typing")
        isPdfOrImg = message.document.file_name
        fileSize = message.document.file_size
        
        fileNm, fileExt = os.path.splitext(isPdfOrImg)
        suprtedFile = [".jpg", ".jpeg", ".png"]
        suprtedPdfFile = [".epub", ".xps", ".oxps", ".cbz", ".fb2"]
        suprtedPdfFile2 = [
            ".csv",
            ".doc",
            ".docx",
            ".dot",
            ".dotx",
            ".log",
            ".mpp",
            ".mpt",
            ".odt",
            ".pot",
            ".potx",
            ".pps",
            ".ppsx",
            ".ppt",
            ".pptx",
            ".pub",
            ".rtf",
            ".txt",
            ".vdx",
            ".vsd",
            ".vsdx",
            ".vst",
            ".vstx",
            ".wpd",
            ".wps",
            ".wri",
            ".xls",
            ".xlsb",
            ".xlsx",
            ".xlt",
            ".xltx",
            ".xml",
        ]
        
        if fileSize >= 20000000:
            
            try:
                bot.send_chat_action(message.chat.id, "typing")
                unSuprtd = bot.send_message(
                    message.chat.id,
                    """
Due to Overload, bot supports only 20mb files

`please Send me a file less than 20mb Size`😪
""",
                )
                sleep(15)
                bot.delete_message(
                    chat_id=message.chat.id, message_id=message.message_id
                )
                bot.delete_message(
                    chat_id=message.chat.id, message_id=unSuprtd.message_id
                )
            except Exception:
                pass
        
        elif fileExt.lower() in suprtedFile:
            
            try:
                picMsgId = bot.reply_to(
                    message,
                    "`Downloading your Image..⏳`",
                )
                
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id] = []
                
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                
                try:
                    os.makedirs(f"./{message.chat.id}/imgs")
                
                except Exception:
                    pass
                
                with open(
                    f"./{message.chat.id}/imgs/{message.chat.id}{isPdfOrImg}", "wb"
                ) as new_file:
                    new_file.write(downloaded_file)
                
                img = Image.open(
                    f"./{message.chat.id}/imgs/{message.chat.id}{isPdfOrImg}"
                ).convert("RGB")
                
                PDF[message.chat.id].append(img)
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    text=f"""`Added {len(PDF[message.chat.id])} page/'s to your pdf..`🤓

/generate to generate PDF 🤞""",
                    message_id=picMsgId.message_id,
                )
            
            except Exception as e:
                
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    text=f"""Something went wrong..😐

`ERROR: {e}`

For bot updates join @ilovepdf\_bot 💎""",
                    message_id=picMsgId.message_id,
                )
                sleep(5)
                bot.delete_message(
                    chat_id=message.chat.id, message_id=picMsgId.message_id
                )
                bot.delete_message(
                    chat_id=message.chat.id, message_id=message.message_id
                )
        
        elif fileExt.lower() == ".pdf":
            
            try:
                if message.chat.id in PROCESS:
                    bot.send_chat_action(message.chat.id, "typing")
                    bot.reply_to(
                        message,
                        f'`Doing Some other Work.. 🥵`'
                    )
                    return
                
                bot.send_chat_action(message.chat.id, "typing")
                pdfMsgId = bot.send_message(
                    message.chat.id,
                    "`Processing.. 🚶`"
                )
                
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                
                os.mkdir(f"./{message.message_id}")
                with open(
                    f"./{message.message_id}/pdf.pdf", "wb"
                ) as new_file:
                    new_file.write(downloaded_file)
                
                doc = fitz.open(f'./{message.message_id}/pdf.pdf')
                noOfPages = doc.pageCount
                
                PDF2IMG[message.chat.id] = message.document.file_id
                PDF2IMGPGNO[message.chat.id] = noOfPages
                
                bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=pdfMsgId.message_id
                )
                
                bot.send_chat_action(message.chat.id, "typing")
                markup = types.ForceReply(selective=False)
                pdfMsgId = bot.reply_to(
                    message,
                    f"""`Total pages: {noOfPages}pgs`

_Unlike all other bots, this bot start sending images without converting the entire PDF to pages_ 😉

reply:
/extract - _to get entire pages_
/extract `pgNo` - _go get a specific page_
/extract `start:end` - _go get all the images b/w_

Join Update Channel @ilovepdf\_bot, More features soon 🔥""",
                    reply_markup=markup)
                
                doc.close()
                shutil.rmtree(f'./{message.message_id}')
            
            except Exception as e:
                
                try:
                    bot.send_message(
                        message.chat.id,
                        f"{e}"
                    )
                    PROCESS.remove(message.chat.id)
                    doc.close()
                    shutil.rmtree(f'./{message.message_id}')
                
                except Exception:
                    pass
        
        elif fileExt.lower() in suprtedPdfFile:
            
            try:
                
                bot.send_chat_action(message.chat.id, "typing")
                pdfMsgId = bot.reply_to(
                    message,
                    "`Downloading your file..⏳`",
                )
                
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                
                os.mkdir(f"./{message.message_id}pdf{message.chat.id}")
                with open(
                    f"./{message.message_id}pdf{message.chat.id}/{isPdfOrImg}", "wb"
                ) as new_file:
                    new_file.write(downloaded_file)
                
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    text="`Creating pdf..`💛",
                    message_id=pdfMsgId.message_id,
                )
                
                Document = fitz.open(
                    f"./{message.message_id}pdf{message.chat.id}/{isPdfOrImg}"
                )
                b = Document.convert_to_pdf()
                
                pdf = fitz.open("pdf", b)
                pdf.save(
                    f"./{message.message_id}pdf{message.chat.id}/{fileNm}.pdf",
                    garbage=4,
                    deflate=True,
                )
                
                pdf.close()
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    text="`Started Uploading..`💚",
                    message_id=pdfMsgId.message_id,
                )
                
                sendfile = open(
                    f"./{message.message_id}pdf{message.chat.id}/{fileNm}.pdf", "rb"
                )
                bot.send_document(
                    message.chat.id, sendfile, caption=f"` Converted: {fileExt} to pdf`"
                )
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    text="`Uploading Completed..❤️`",
                    message_id=pdfMsgId.message_id,
                )
                
                shutil.rmtree(f"./{message.message_id}pdf{message.chat.id}")
                
                sleep(10)
                bot.send_chat_action(message.chat.id, "typing")
                feedbackMsg = """
For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
                bot.send_message(
                    message.chat.id, feedbackMsg, disable_web_page_preview=True
                )

            except Exception as e:
                
                try:
                    shutil.rmtree(f"./{message.message_id}pdf{message.chat.id}")
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        text=f"""Something went wrong..😐

`ERROR: {e}`

For bot updates join @ilovepdf\_bot 💎
""",
                        message_id=pdfMsgId.message_id,
                    )
                    
                    sleep(15)
                    bot.delete_message(
                        chat_id=message.chat.id, message_id=pdfMsgId.message_id
                    )
                    bot.delete_message(
                        chat_id=message.chat.id, message_id=message.message_id
                    )
                    
                except Exception:
                    pass
        
        elif fileExt.lower() in suprtedPdfFile2:
            
            if os.getenv("CONVERT_API") is None:
                
                pdfMsgId = bot.reply_to(
                    message,
                    "`Owner Forgot to add ConvertAPI.. contact Owner 😒`",
                )
                sleep(15)
                bot.delete_message(
                    chat_id=message.chat.id, message_id=pdfMsgId.message_id
                )
            
            else:
                
                try:
                    
                    bot.send_chat_action(message.chat.id, "typing")
                    pdfMsgId = bot.reply_to(
                        message,
                        "`Downloading your file..⏳`",
                    )
                    
                    file_info = bot.get_file(message.document.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    
                    os.mkdir(f"./{message.message_id}pdf{message.chat.id}")
                    with open(
                        f"./{message.message_id}pdf{message.chat.id}/{isPdfOrImg}", "wb"
                    ) as new_file:
                        new_file.write(downloaded_file)
                    
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        text="`Creating pdf..`💛",
                        message_id=pdfMsgId.message_id,
                    )
                    convertapi.convert(
                        "pdf",
                        {
                            "File": f"./{message.message_id}pdf{message.chat.id}/{isPdfOrImg}"
                        },
                        from_format=fileExt[1:],
                    ).save_files(
                        f"./{message.message_id}pdf{message.chat.id}/{fileNm}.pdf"
                    )
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        text="`Uploading Completed..`❤️",
                        message_id=pdfMsgId.message_id,
                    )
                    sendfile = open(
                        f"./{message.message_id}pdf{message.chat.id}/{fileNm}.pdf", "rb"
                    )
                    bot.send_document(
                        message.chat.id,
                        sendfile,
                        caption=f"`Converted: {fileExt} to pdf`",
                    )
                    
                    shutil.rmtree(f"./{message.message_id}pdf{message.chat.id}")
                    
                    sleep(10)
                    bot.send_chat_action(message.chat.id, "typing")
                    feedbackMsg = """
For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
                    bot.send_message(
                        message.chat.id, feedbackMsg, disable_web_page_preview=True
                    )
                
                except Exception:
                    
                    try:
                        shutil.rmtree(f"./{message.message_id}pdf{message.chat.id}")
                        bot.edit_message_text(
                            chat_id=message.chat.id,
                            text="""ConvertAPI limit reaches.. contact Owner""",
                            message_id=pdfMsgId.message_id,
                        )
                        
                    except Exception:
                        pass
        
        else:
            
            try:
                bot.send_chat_action(message.chat.id, "typing")
                unSuprtd = bot.send_message(
                    message.chat.id, """`unsupported file..🙄`"""
                )
                sleep(15)
                bot.delete_message(
                    chat_id=message.chat.id, message_id=message.message_id
                )
                bot.delete_message(
                    chat_id=message.chat.id, message_id=unSuprtd.message_id
                )
            except Exception:
                pass
            
    except Exception:
        pass


# Reply to /extract 
@bot.message_handler(commands=["extract"])
def extract(message):
    try:
        
        if message.chat.id in PROCESS:
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(
                message,
                "`Doing Some Work..🥵`"
            )
            return
        
        needPages = message.text.replace('/extract ', '')
        
        if message.chat.id not in PDF2IMG:
            bot.send_chat_action(message.chat.id, "typing")
            bot.send_message(
                message.chat.id,
                "`send me a pdf first..🤥`"
            )
            return
        
        else:
            pageStartAndEnd = list(needPages.replace('-',':').split(':'))
            
            if len(pageStartAndEnd) > 2:
                bot.send_message(
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
                            bot.send_message(
                                message.chat.id,
                                "`Syntax Error: errorInEndingPageNumber 😅`"
                            )
                            return
                    else:
                        bot.send_message(
                            message.chat.id,
                            "`Syntax Error: errorInStartingPageNumber 😅`"
                        )
                        return
                    
                except:
                    bot.send_message(
                        message.chat.id,
                        "`Syntax Error: noSuchPageNumbers 🤭`"
                    )
                    return
            
            elif len(pageStartAndEnd) == 1:
                
                if pageStartAndEnd[0] == "/extract":
                    
                    if (PDF2IMGPGNO[message.chat.id]) == 1:
                        PAGENOINFO[message.chat.id] = [True, None, None, 1]    #elmnts in list (is singlePage, start, end, if single pg number)
                    
                    else:
                        PAGENOINFO[message.chat.id] = [False, 1, PDF2IMGPGNO[message.chat.id], None]    #elmnts in list (is singlePage, start, end, if single pg number)
                    
                elif 0 < int(pageStartAndEnd[0]) <= PDF2IMGPGNO[message.chat.id]:
                    PAGENOINFO[message.chat.id] = [True, None, None, pageStartAndEnd[0]]
                
                else:
                    bot.send_message(
                        message.chat.id,
                        '`Syntax Error: noSuchPageNumber 🥴`'
                    )
                    return
                
            else:
                bot.send_message(
                    message.chat.id,
                    "`Syntax Error: pageNumberMustBeAnIntiger 🧠`"
                )
                return
            
            if PAGENOINFO[message.chat.id][0] == False:
                key = types.InlineKeyboardMarkup()
                key.add(
                    types.InlineKeyboardButton(
                        "Images 🖼️", callback_data="multipleImgAsImages"
                    ),
                    types.InlineKeyboardButton(
                        "Document 📁 ", callback_data="multipleImgAsDocument"
                    )
                )
                
                question = f"Extract images from `{PAGENOINFO[message.chat.id][1]}` to `{PAGENOINFO[message.chat.id][2]}` As:"
                bot.send_message(
                    message.chat.id,
                    question,
                    reply_markup=key
                )
                
            if PAGENOINFO[message.chat.id][0] == True:
                key = types.InlineKeyboardMarkup()
                key.add(
                    types.InlineKeyboardButton(
                        "Images 🖼️", callback_data="asImages"
                    ),
                    types.InlineKeyboardButton(
                        "Document 📂", callback_data="asDocument"
                    )
                )
                
                question = f"Extract page number: `{PAGENOINFO[message.chat.id][3]}` As:"
                bot.send_message(
                    message.chat.id,
                    question,
                    reply_markup=key
                )
                
    except Exception:
        
        try:
            del PAGENOINFO[message.chat.id]
            PROCESS.remove(message.chat.id)
            del media[message.chat.id]
            del mediaDoc[message.chat.id]
            
        except Exception:
            pass


# callback
@bot.callback_query_handler(func=lambda call: call.data)
def strtMsgEdt(call):
    edit = call.data

    if edit == "strtDevEdt":

        try:
            
            key = types.InlineKeyboardMarkup()
            key.add(
                types.InlineKeyboardButton("🔙 Home 🏡", callback_data="back")
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=aboutDev,
                disable_web_page_preview=True,
                reply_markup=key,
            )
        
        except Exception:
            pass
        
    elif edit == "imgsToPdfEdit":
    
        try:
            key = types.InlineKeyboardMarkup()
            key.add(
                types.InlineKeyboardButton(
                    "🔙 Home 🏡", callback_data="back"
                ),
                types.InlineKeyboardButton(
                    "PDF to images ➡️", callback_data="pdfToImgsEdit"
                ),
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=expMsg1,
                disable_web_page_preview=True,
                reply_markup=key,
            )
        
        except Exception:
            pass
        
    elif edit == "pdfToImgsEdit":
        
        try:
            
            key = types.InlineKeyboardMarkup()
            key.add(
                types.InlineKeyboardButton(
                    "🔙 Imgs To Pdf", callback_data="imgsToPdfEdit"
                ),
                types.InlineKeyboardButton("Home 🏡", callback_data="back"),
                types.InlineKeyboardButton(
                    "file to Pdf ➡️", callback_data="filsToPdfEdit"
                ),
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=expMsg2,
                disable_web_page_preview=True,
                reply_markup=key,
            )
        
        except Exception:
            pass
    
    elif edit == "filsToPdfEdit":
    
        try:
            key = types.InlineKeyboardMarkup()
            key.add(
                types.InlineKeyboardButton(
                    "🔙 PDF to imgs", callback_data="imgsToPdfEdit"
                ),
                types.InlineKeyboardButton("Home 🏡", callback_data="back"),
                types.InlineKeyboardButton(
                    "WARNING ⚠️", callback_data="warningEdit"
                ),
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=expMsg3,
                disable_web_page_preview=True,
                reply_markup=key,
            )
        
        except Exception:
            pass
    
    elif edit == "warningEdit":
    
        try:
            key = types.InlineKeyboardMarkup()
            key.add(
                types.InlineKeyboardButton(
                    "🔙 WARNING ⚠️", callback_data="warningEdit"
                ),
                types.InlineKeyboardButton("Home 🏡", callback_data="back"),
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=expMsg4,
                disable_web_page_preview=True,
                reply_markup=key,
            )
        
        except Exception:
            pass
    
    elif edit == "back":
    
        try:
            key = types.InlineKeyboardMarkup()
            key.add(
                types.InlineKeyboardButton(
                    "Source Code ❤️", callback_data="strtDevEdt"
                ),
                types.InlineKeyboardButton(
                    "Explore More 🥳", callback_data="imgsToPdfEdit"
                ),
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=strtMsg,
                disable_web_page_preview=True,
                reply_markup=key,
            )
        
        except Exception:
            pass
    
    elif edit in ["multipleImgAsImages", "multipleImgAsDocument", "asImages", "asDocument"]:
        
        try:
            if (call.message.chat.id in PROCESS) or (call.message.chat.id not in PDF2IMG):
                
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = "Same work done before..🏃"
                )
                return
                
            PROCESS.append(call.message.chat.id)
            
            if edit == "multipleImgAsImages" or edit == "multipleImgAsDocument":
                
                bot.send_chat_action(call.message.chat.id, "typing")
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = "`Downloading your pdf..⏳`"
                )
            
                if int(int(PAGENOINFO[call.message.chat.id][2])+1 - int(PAGENOINFO[call.message.chat.id][1])) >= 11:
                    bot.pin_chat_message(
                        chat_id = call.message.chat.id,
                        message_id = call.message.message_id,
                        disable_notification = True
                    )
                
                file_info = bot.get_file(PDF2IMG[call.message.chat.id])
                downloaded_file = bot.download_file(file_info.file_path)
                
                os.mkdir(f'./{call.message.message_id}')
                with open(
                    f'./{call.message.message_id}/pdf.pdf', 'wb'
                ) as new_file:
                    new_file.write(downloaded_file)
                
                del PDF2IMG[call.message.chat.id]
                del PDF2IMGPGNO[call.message.chat.id]
                
                doc = fitz.open(f'./{call.message.message_id}/pdf.pdf')
                zoom = 1
                mat = fitz.Matrix(zoom, zoom)
                noOfPages = doc.pageCount
                percNo = 0
                
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = f"`Total pages: {int(PAGENOINFO[call.message.chat.id][2])+1 - int(PAGENOINFO[call.message.chat.id][1])}..⏳`"
                )
                totalPgList = range(int(PAGENOINFO[call.message.chat.id][1]), int(PAGENOINFO[call.message.chat.id][2] + 1))
                
                cnvrtpg = 0
                for i in range(0, len(totalPgList), 10):
                    
                    pgList = totalPgList[i:i+10]
                    os.mkdir(f'./{call.message.message_id}/pgs')
                    
                    for pageNo in pgList:
                        page = doc.loadPage(pageNo-1)
                        pix = page.getPixmap(matrix = mat)
                        cnvrtpg += 1
                        
                        bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text = f"`Converted: {cnvrtpg}/{int((PAGENOINFO[call.message.chat.id][2])+1 - int(PAGENOINFO[call.message.chat.id][1]))} pages.. 🤞`"
                        )
                        
                        if call.message.chat.id not in PROCESS:
                            try:
                                
                                bot.edit_message_text(
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text = f"`Canceled at {cnvrtpg}/{int((PAGENOINFO[call.message.chat.id][2])+1 - int(PAGENOINFO[call.message.chat.id][1]))} pages.. 🙄`"
                                )
                                shutil.rmtree(f'./{call.message.message_id}')
                                doc.close()
                                return
                            
                            except Exception:
                                return
                        
                        with open(
                            f'./{call.message.message_id}/pgs/{pageNo}.jpg','wb'
                        ) as f:
                            pix.writePNG(f'./{call.message.message_id}/pgs/{pageNo}.jpg')
                        
                    directory = f'./{call.message.message_id}/pgs'
                    imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                    imag.sort(key=os.path.getctime)
                    
                    percNo = percNo + len(imag)
                    media[call.message.chat.id] = []
                    mediaDoc[call.message.chat.id] = []
                    LrgFileNo = 1
                    
                    for file in imag:
                        if os.path.getsize(file) >= 1000000:
                            
                            picture = Image.open(file)
                            CmpImg = f'./{call.message.message_id}/pgs/temp{LrgFileNo}.jpeg'
                            picture.save(CmpImg, "JPEG", optimize=True, quality=50) 
                            
                            LrgFileNo += 1
                            
                            if os.path.getsize(CmpImg) >= 1000000:
                                continue
                            
                            else:
                                fi = open(CmpImg, "rb")
                                media[call.message.chat.id].append(InputMediaPhoto (fi))
                                mediaDoc[call.message.chat.id].append(InputMediaDocument (fi))
                                continue
                        
                        fi = open(file, "rb")
                        media[call.message.chat.id].append(InputMediaPhoto (fi))
                        mediaDoc[call.message.chat.id].append(InputMediaDocument (fi))
                        
                    shutil.rmtree(f'./{call.message.message_id}/pgs')
                    sleep(3)
                    
                    if edit == "multipleImgAsImages":
                        
                        if call.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'./{call.message.message_id}')
                                doc.close()
                                return
                            
                            except Exception:
                                return
                        
                        bot.send_chat_action(call.message.chat.id, "upload_photo")
                        
                        try:
                            bot.send_media_group(
                                call.message.chat.id,
                                media[call.message.chat.id]
                            )
                        except Exception:
                            del media[call.message.chat.id]
                            pass
                        
                    if edit == "multipleImgAsDocument":
                        
                        if call.message.chat.id not in PROCESS:
                            try:
                                shutil.rmtree(f'./{call.message.message_id}')
                                doc.close()
                                return
                            
                            except Exception:
                                return
                        
                        bot.send_chat_action(call.message.chat.id, "upload_document")
                        
                        try:
                            bot.send_media_group(
                                call.message.chat.id,
                                mediaDoc[call.message.chat.id]
                            )
                        except Exception:
                            del mediaDoc[call.message.chat.id]
                            pass
                    
                PROCESS.remove(call.message.chat.id)
                
                del media[call.message.chat.id]
                del mediaDoc[call.message.chat.id]
                del PAGENOINFO[call.message.chat.id]
                doc.close()
                
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = f'`Uploading Completed.. 🤫`'
                )
                shutil.rmtree(f'./{call.message.message_id}')
                
                sleep(10)
                bot.send_chat_action(call.message.chat.id, "typing")
                feedbackMsg = f'''
Join Update Channel @ilovepdf\_bot, More features soon 🔥

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
'''
                bot.send_message(call.message.chat.id, feedbackMsg, disable_web_page_preview=True)
            
            if edit == "asImages" or edit == "asDocument":
                
                bot.send_chat_action(call.message.chat.id, "typing")
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = "`Downloading your pdf..⏳`"
                )
                
                file_info = bot.get_file(PDF2IMG[call.message.chat.id])
                downloaded_file = bot.download_file(file_info.file_path)
                
                os.mkdir(f'./{call.message.message_id}')
                with open(
                    f'./{call.message.message_id}/pdf.pdf', 'wb'
                ) as new_file:
                    new_file.write(downloaded_file)
                
                del PDF2IMG[call.message.chat.id]
                del PDF2IMGPGNO[call.message.chat.id]
                
                doc = fitz.open(f'./{call.message.message_id}/pdf.pdf')
                zoom = 1
                mat = fitz.Matrix(zoom, zoom)
                noOfPages = doc.pageCount
                        
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = f"`Fetching page Number:{PAGENOINFO[call.message.chat.id][3]} 🤧`"
                )
                
                page = doc.loadPage(int(PAGENOINFO[call.message.chat.id][3])-1)
                pix = page.getPixmap(matrix = mat)
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = f"`Successfully Converted your page..✌️`"
                )
                
                os.mkdir(f'./{call.message.message_id}/pgs')
                
                with open(
                    f'./{call.message.message_id}/pgs/{PAGENOINFO[call.message.chat.id][3]}.jpg','wb'
                ) as f:
                    pix.writePNG(f'./{call.message.message_id}/pgs/{PAGENOINFO[call.message.chat.id][3]}.jpg')
                
                file = f'./{call.message.message_id}/pgs/{PAGENOINFO[call.message.chat.id][3]}.jpg'
                    
                if os.path.getsize(file) >= 1000000:
                    picture = Image.open(file)
                    CmpImg = f'./{call.message.message_id}/pgs/temp{PAGENOINFO[call.message.chat.id][3]}.jpeg'
                    
                    picture.save(
                        CmpImg,
                        "JPEG",
                        optimize=True,
                        quality=50
                    )
                    file = CmpImg
                    
                    if os.path.getsize(CmpImg) >= 1000000:
                        bot.send_message(
                            call.message.chat.id,
                            '`too high resolution.. 🙄`'
                        )
                        return
                    
                if edit == "asImages":
                    bot.send_chat_action(call.message.chat.id, "upload_photo")
                    sendfile = open(file,'rb')
                    bot.send_photo(
                        call.message.chat.id,
                        sendfile
                    )
                    
                if edit == "asDocument":
                    bot.send_chat_action(call.message.chat.id, "upload_document")
                    sendfile = open(file,'rb')
                    bot.send_document(
                        call.message.chat.id,
                        sendfile
                    )
                    
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text = f'`Uploading Completed.. 🤫`'
                )
                
                PROCESS.remove(call.message.chat.id)
                del PAGENOINFO[call.message.chat.id]
                doc.close()
                
                shutil.rmtree(f'./{call.message.message_id}')
                sleep(10)
                bot.send_chat_action(call.message.chat.id, "typing")
                feedbackMsg = f'''
Join Update Channel @ilovepdf\_bot, More features soon 🔥

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
'''
                bot.send_message(
                    call.message.chat.id,
                    feedbackMsg,
                    disable_web_page_preview=True
                )
                
        except Exception as e:
            
            try:
                bot.send_message(call.message.chat.id, f'{e}')
                shutil.rmtree(f'./{call.message.message_id}')
                PROCESS.remove(call.message.chat.id)
                doc.close()
            
            except Exception:
                pass


# Reply to /generate 
@bot.message_handler(commands=["generate"])
def generate(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        newName = message.text.replace("/generate", "")
        images = PDF.get(message.chat.id)
        
        if isinstance(images, list):
            pgnmbr = len(PDF[message.chat.id])
            del PDF[message.chat.id]
        
        if not images:
            ntFnded = bot.reply_to(message, "`No image founded.!!`😒")
            sleep(5)
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.delete_message(chat_id=message.chat.id, message_id=ntFnded.message_id)
            return
        
        gnrtMsgId = bot.send_message(message.chat.id, f"`Generating pdf..`💚")
        
        if newName == " name":
            fileName = f"{message.from_user.first_name}" + ".pdf"
        
        elif len(newName) > 1 and len(newName) <= 15:
            fileName = f"{newName}" + ".pdf"
        
        elif len(newName) > 15:
            fileName = f"{message.from_user.first_name}" + ".pdf"
        
        else:
            fileName = f"{message.chat.id}" + ".pdf"
        
        path = os.path.join(f"./{message.chat.id}", fileName)
        images[0].save(path, save_all=True, append_images=images[1:])
        bot.edit_message_text(
            chat_id=message.chat.id,
            text="`Uploading pdf... `♥️",
            message_id=gnrtMsgId.message_id,
        )
        bot.send_chat_action(message.chat.id, "upload_document")
        
        sendfile = open(path, "rb")
        bot.send_document(
            message.chat.id,
            sendfile,
            caption=f"file Name: `{fileName}`\n\n`Total pg's: {pgnmbr}`",
        )
        bot.edit_message_text(
            chat_id=message.chat.id,
            text="`Successfully Uploaded.. `🤫",
            message_id=gnrtMsgId.message_id,
        )
        
        shutil.rmtree(f"./{message.chat.id}")
        
        sleep(10)
        bot.send_chat_action(message.chat.id, "typing")
        feedbackMsg = """
For bot updates join @ilovepdf\_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
        bot.send_message(
            message.chat.id,
            feedbackMsg,
            disable_web_page_preview=True
        )
        
    except Exception:
        pass


# delete spam messages
@bot.message_handler(
    content_types=[
        "text",
        "audio",
        "sticker",
        "video",
        "video_note",
        "voice",
        "location",
        "contact",
    ]
)
def unSuprtd(message):

    try:
        bot.send_chat_action(message.chat.id, "typing")
        unSuprtd = bot.send_message(
            message.chat.id,
            "`unsupported file..`🏌️"
        )
        sleep(5)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=unSuprtd.message_id)

    except Exception:
        pass

bot.infinity_polling(timeout=10, long_polling_timeout = 5)
