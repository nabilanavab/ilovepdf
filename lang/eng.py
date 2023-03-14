# copyright ©️ 2021 nabilanavab
file_name = "lang/eng.py"


from configs.config   import settings

# REPLY MESSAGE FOR BROKEN WORKS
RESTART = {
    "msg" : """☠ `𝐎𝐕𝐄𝐑𝐋𝐎𝐀𝐃 𝐃𝐄𝐂𝐓𝐄𝐂𝐓𝐄𝐃`☠:\n__pǝʇɹɐʇsǝɹ ɹǝʌɹǝs__ \n
I noticed that your work was also in queue

Can you please try again..!""",
    "btn" : { "🚶 CLOSE 🚶" : "close|mee" }
}

# PM WELCOME MESSAGE (HOME A, B, C, D...)
HOME = {
    "HomeA" : "Hey {}..!!\n"
"Welcome to {}.!\n\n"

"With this tool, you can easily convert images to PDF, compress PDF files, split , merge, encrypt or decrypt PDFs, rotate PDF pages, and much more.\n\n"






"Simply send me a PDF/IMAGE and it will perform the requested action. for help select '⚠️ HELP ⚠️' at any time.the PDF bot is here to make your life easier..\n\n"


"Try it out now and see how it can help you with all of your PDF needs!",
    "HomeACB" : {
        "⚙️ SETTINGS ⚙️" : "Home|B",
        "🌍 LANGUAGE 🌍" : "set|lang",
        "⚠️ HELP ⚠️" : "Home|C",
        "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 SOURCE CODE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "➕ ADD IN GROUP ➕" : "https://t.me/{}?startgroup=True"
    },
    "HomeAdminCB" : {
        "⚙️ SETTINGS ⚙️" : "Home|B",
        "🌍 LANGUAGE 🌍" : "set|lang",
        "⚠️ HELP ⚠️" : "Home|C",
        "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 SOURCE CODE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 STATUS 🗽" : f"status|home",
        "➕ ADD IN GROUP ➕" : "https://t.me/{}?startgroup=True",
        "🚶 CLOSE 🚶" : "close|mee"
    },
    "HomeB" : """SETTINGS PAGE ⚙️

USER NAME   : {}
USER ID           : {}
USERNAME    : {}
JOIN DATE      : {}

LANGUAGE    : {}
API                    : {}
THUMB            : {}
CAPTION         : {}
FILE NAME      : {}""",
    "HomeBCB" : {
        "📍 THUMB 📍" : "set|thumb",
        "📈 NAME 📈" : "set|fname",
        "💩 API 💩" : "set|api",
        "📅 CAPTION 📅" : "set|capt",
        "« BACK TO HOME «" : "Home|B2A"
    },
    "HomeC" : """**Some of the main features are:**
 
 ◍ ```Create a PDF from your images: simply send it in bot pms [png, jpg, jpeg]```
 ◍ ```Extract the text from the PDF: Helps to extract the text from the PDF file and send as separate message.```
 ◍ ```Convert the PDF to another file format: [images, txt, html, json, tar, rar]```
 ◍ ```Merge multiple PDFs into one: Multiple PDF files to combine into a single file```
 ◍ ```Split a PDF into separate pages: Large PDF file to split it into separate ones```
 ◍ ```Extract images from the PDF: [all,range,pages] as image, doc, zip, rar```
 ◍ ```Helps to reduce size by optimizing the images. Useful in sending file via email when it's too large```
 ◍ ```Fetches Metadata: title of the document, the author, the subject, the keywords associated with the document, and the creation and modification dates```
 ◍ ```Encrypt/Decrypt Pdfs Using passwords, Websites to Pdf, Rotate, Rename, stamb..```
 ◍ ```WaterMark, Combine, Zoom, Draw, Add/Delete pages, Ocr pdf..```
 ◍ ```text messages to pdf files, and Much More.. 😎```""",
    "HomeCCB" : {
        "« BACK HOME «" : "Home|A",
        "🛈 INSTRUCTIONS 🛈" : "Home|D"
    },
    "HomeD" : """`As you know, this is a free service, I cannot guarantee how long I can maintain this service..`😝
 
⚠️ INSTRUCTIONS ⚠️:
 ◍ ```Please note that spamming is generally not tolerated and can result in the user or bot being banned from the service```
 ◍ ```Wait for the bot to process the file: The bot will process the PDF file and perform the requested action. This may take a few minutes, depending on the size of the file and the complexity of the action being performed.```
 ◍ ```Once the bot has completed the action, it will send you the results. If the action was successful, you will receive the output. If the action was not successful, the bot will let you know and provide any relevant error messages.```
 ◍ ```Any user found to be distributing or sharing pornographic content on the bot will be permanently banned```
**Send any image to start:** 😁""",
    "HomeDCB" : {
        "⚠️ HELP ⚠️" : "Home|C",
        "» BACK HOME »" : "Home|A"
    }  
}

# GROUP WELCOME MESSAGE
HomeG = {
    "HomeA" : HOME['HomeA'],
    "HomeACB" : {
        "🌍 LANGUAGE 🌍" : "set|lang",
        "🛡️ HELP 🛡️": "Home|C",
        "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 SOURCE CODE 🌟": f"{settings.SOURCE_CODE}",
        "🚶 CLOSE 🚶" : "close|mee",
    }
}

SETTINGS = {
    "lang" : "Now, Select any language..",
    "default" : ["DEFAULT ❌", "CUSTOM ✅"],
    "cant" : "This feature cannot be used ❌",
    "wait" : { "Waiting.. 🥱" : "nabilanavab" },
    "feedbtn" : { "Report any bugs you find!" : settings.REPORT },
    "chgLang" : {"SETTING ⚙️ » CHANGE LANG 🌐" : "nabilanavab"},
    "askApi" : "\n\nOpen the **Below** link and Send me the secret code:",
    "waitApi" : { "Open link ✅" : "https://www.convertapi.com/a/signin" },
    "error" : "Something went wrong while retrieving data from the database",
    "result" : ["Settings cannot be updated ❌", "Settings Updated Successfully ✅"],
    "back" : [{ "« BACK TO HOME «" : "Home|B2S" }, { "« BACK TO HOME «" : "Home|B2A" }],
    "feedback" : "Bug warning! If my texts sound weird, it's probably Google Translate's fault."
                 "\n\nReport a BUG in {} Lang:\n`• Specify Lang\n• Error Message\n• New Message`",
    "ask" : [
        "Now, Send me..",
        "Now, Send me.. 😅\n\nFast.! I have no more time to go over the text.. 😏\n\n/cancel: to cancel"
    ],
    "thumb" : [
        {
            "SETTING ⚙️ » THUMBNAIL 📷" : "nabilanavab",
            "♻ ADD ♻" : "set|thumb+",
            "« BACK TO HOME «" : "Home|B"
        },
        {
            "SETTING ⚙️ » THUMBNAIL 📷" : "nabilanavab",
            "♻ CHANGE ♻" : "set|thumb+",
            "🗑 DELETE 🗑" : "set|thumb-",
            "« BACK TO HOME «" : "Home|B2S"
        }
    ],
    "fname" : [
        {
            "SETTING ⚙️ » FNAME 📷" : "nabilanavab",
            "♻ ADD ♻" : "set|fname+",
            "« BACK TO HOME «" : "Home|B2S"
        },
        {
            "SETTING ⚙️ » FNAME 📷" : "nabilanavab",
            "♻ CHANGE ♻" : "set|fname+",
            "🗑 DELETE 🗑" : "set|fname-",
            "« BACK TO HOME «" : "Home|B2S"
        }
    ],
    "api" : [
        {
            "SETTING ⚙️ » API 📷" : "nabilanavab",
            "♻ ADD ♻" : "set|api+",
            "« BACK TO HOME «" : "Home|B2S"
        },
        {
            "SETTING ⚙️ » API 📷" : "nabilanavab",
            "♻ CHANGE ♻" : "set|api+",
            "🗑 DELETE 🗑" : "set|api-",
            "« BACK TO HOME «" : "Home|B2S"
        }
    ],
    "capt" : [
        {
            "SETTING ⚙️ » CAPTION 📷" : "nabilanavab",
            "♻ ADD ♻" : "set|capt+",
            "« BACK TO HOME «" : "Home|B2S"
        },
        {
            "SETTING ⚙️ » CAPTION 📷" : "nabilanavab",
            "♻ CHANGE ♻" : "set|capt+",
            "🗑 DELETE 🗑" : "set|capt-",
            "« BACK TO HOME «" : "Home|B2S"
        }
    ]
}

BOT_COMMAND = {
    "start" : "Welcome message..",
    "txt2pdf" : "Create text PDF's"
}

STATUS_MSG = {
    "_HOME" : {
        "📊 ↓ SERVER ↓ 📊" : "nabilanavab",
        "📶 STORAGE 📶" : "status|server",
        "🥥 DATABASE 🥥" : "status|db",
        "🌝 ↓ GET LIST ↓ 🌝": "nabilanavab",
        "💎 ADMIN 💎" : "status|admin",
        "👤 USERS 👤" : "status|users",
        "« BACK «" : "Home|A"
    },
    "DB" : """📂 DATABASE :

**◍ Database Users :** `{}` 📍
**◍ Database Chats :** `{}` 📍""",
    "SERVER" : """**◍ Total Space     :** `{}`
**◍ Used Space     :** `{}({}%)`
**◍ Free Space      :** `{}`
**◍ CPU Usage      :** `{}`%
**◍ RAM Usage     :** `{}`%
**◍ Current Work  :** `{}`
**◍ Message Id     :** `{}`""",
    "USERS" : "Users in Database are.",
    "NO_DB" : "No dataBASE set Yet 💩",
    "ADMIN" : "**Total ADMIN:** __{}__\n",
    "BACK" : { "« BACK «" : "status|home" },
    "HOME" : "`Now, select any option below to get current STATUS 💱.. `",
}

feedbackMsg = f"IF YOU ❤ THIS BOT, JOIN OUR [UPDATE CHANNEL]({settings.OWNED_CHANNEL}) TO STAY INFORMED.\n\n[Write a FEEDBACK 📋]({settings.FEEDBACK})"

# BANNED USER UI
BAN = {
    "UCantUse" : """Hey {}

FOR SOME REASON YOU CANT USE THIS BOT :(""",
    "UCantUseDB" : """Hey {}

FOR SOME REASON YOU CANT USE THIS BOT :(

REASON: {}""",
    "GroupCantUse" : """{} NEVER EXPECT A GOOD RESPONSE FROM ME

ADMINS RESTRICTED ME FROM WORKING HERE.. 🤭""",
    "GroupCantUseDB" : """{} NEVER EXPECT A GOOD RESPONSE FROM ME

ADMINS RESTRICTED ME FROM WORKING HERE.. 🤭

REASON: {}""",
    "cbNotU" : "Oops, Sorry to break your heart, this message is not for you 💔.\n\nBetter luck next time! 😏",
    "Fool" : "Please don't try to fool me.. 🤭",
    "banCB" : {
        "Create your Own Bot": f"{settings.SOURCE_CODE}",
        "Tutorial": f"{settings.SOURCE_CODE}",
        "Update Channel": "https://telegram.dog/ilovepdf_bot"
    },
    "Force" : """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only **Channel Members** Can Use this Bot 🚶

This Means That You Need To **Join** The Below Mentioned Channel for Using Me!

Hit on `"♻️retry♻️"` after joining.. 😅""",
    "ForceCB" : {
        "🌟 JOIN CHANNEL 🌟" : "{0}",
        "♻️ Refresh ♻️" : "refresh{1}"
    },
}

checkPdf = {
    "pg" : "`Number of Pages: •{}•` 🌟",
    "pdf" : """`What should I do with this file.?`

File Name : `{}`
File Size : `{}`""",
    "pdfCB1" : {
        "⭐ META£ATA ⭐" : "metaData",
        "🗳️ PREVIEW 🗳️" : "preview",
        "🖼️ IMAGES 🖼️" : "pdf|img",
        "✏️ TEXT ✏️" : "pdf|txt",
        "🔐 ENCRYPT 🔐" : "work|encrypt",
        "🔒 DECRYPT 🔓" : "work|decrypt",
        "🗜️ COMPRESS 🗜️" : "close|dev",
        "🤸 ROTATE 🤸" : "pdf|rotate",
        "✂️ SPLIT ✂️" : "pdf|split",
        "🧬 MERGE 🧬" : "merge",
        "™️ STAMP ™️" : "pdf|stp",
        "✏️ RENAME ✏️" : "work|rename",
        "🔗 URL 🔗" : "link",
        "» 🏴‍☠️ MORE 🏴‍☠️ »" : "pdf2",
        "🚫 CLOSE 🚫" : "close|all"
    },
    "pdfCB2" : {
        " ↓ SECOND PAGE  ↓ " : "nabilanavab",
        "📝 OCR 📝" : "work|ocr",
        "🥷 A4 FORMAT 🥷" : "work|format", 
        "🖤 BLACK/WHITE 🤍" : "baw",
        "🍴 SATUTATION 🍴" : "sat",
        "📎 COMBINE PDF 📎" : "comb",
        "🔎 ZOOM PDF 🔎" : "zoom",
        "➖ DELETE PAGES ➖": "close|dev",
        "➕ ADD PAGES ➕" : "close|dev",
        "🎨 DRAW PDF 🎨" : "draw",
        "😈 CODEC 😈" : "close|dev",
        "💦 WATERMARK 💦" : "pdf|wa",
        "« 🏴‍☠️ BACK 🏴‍☠️ «" : "pdf1",
        "🚫 CLOSE 🚫" : "close|all"
    },
    "error" : """__I can't do anything with this file.__ 😏

🐉  `CODEC ERROR`  🐉""",
    "errorCB" : {
        "❌ ERROR IN CODEC ❌" : "error",
        "🔸 CLOSE 🔸" : "close|all"
    },
    "encrypt" : """`FILE IS ENCRYPTED` 🔐

File Name: `{}`
File Size: `{}`""",
    "encryptCB" : {"🔓 DECRYPT 🔓" : "work|decrypt"}
}

PROGRESS = {
    "progress" : """\n**Done ✅ : **{0}/{1}
**Speed 🚀:** {2}/s
**Estimated Time ⏳:** {3}""",
    "workInP" : "WORK IN PROGRESS.. 🙇",
    "upFile" : "`Started Uploading..`📤",
    "refresh" : { "♻️ Refresh ♻️" : "{}" },
    "dlFile" : "`Downloading your file..` 📥",
    "dlImage" : "`Downloading your Image..⏳`",
    "upFileCB" : {"📤 .. UPLOADING.. 📤" : "nabilanavab"},
    "takeTime" : """```⚙️ Work in Progress..`
`It might take some time..```💛""",
    "cbPRO_D" : ["📤 DOWNLOAD: {:.2f}% 📤", "🎯 CANCEL 🎯"],
    "cbPRO_U" : ["📤 UPLOADED: {:.2f}% 📤", "🎯 CANCEL 🎯"]
}

GENERATE = {
    "noQueue" : "`No Queue found..`😲",
    "noImages" : "No image found.!! 😒",
    "currDL" : "Downloaded {} Images 🥱",
    "geting" : "File Name: `{}`\nPages: `{}`",
    "getFileNm" : "Now Send Me a File Name 😒: ",
    "deleteQueue" : "`Queue deleted Successfully..`🤧",
    "getingCB" : {"📚 GENERATING PDF.." : "nabilanavab"},
}

document = {
    "reply" : checkPdf['pdf'],
    "upFile" : PROGRESS['upFile'],
    "process" : "⚙️ Processing..",
    "replyCB" : checkPdf['pdfCB1'],
    "inWork" : PROGRESS['workInP'],
    "download" : PROGRESS['dlFile'],
    "refresh" : PROGRESS['refresh'],
    "dlImage" : PROGRESS['dlImage'],
    "takeTime" : PROGRESS['takeTime'],
    "fromFile" : "`Converted: {} to {}`",
    "unsupport" : "Unsupported file..🙄`",
    "cancelCB" : { "⟨ Cancel ⟩" : "close|me" },
    "generate" : { "GENERATE 📚" : "generate" },
    "generateRN" : {
        "GENERATE 📚" : "generate",
        "RENAME ✍️" : "generateREN"
    },
    "noAPI" : """`Please add convert API.. 💩

start » settings » api » add/change`""",
    "error" : """SOMETHING went WRONG.. 🐉

ERROR: `{}`""",
    "setHdImg" : """Now Image To PDF is in HD mode 😈""",
    "setDefault" : { "« Back to Default Quality «" : "close|hd" },
    "useDOCKER" : "`File Not Supported, deploy bot using docker`",
    "big" : """Due to Overload, Owner limits {}mb for pdf files 🙇

`please Send me a file less than {}mb Size` 🙃""",
    "bigCB" : {
        "💎 Create 2Gb Support Bot 💎" : "https://github.com/nabilanavab/ilovepdf"
    },
    "imageAdded" : """`Added {} pages to your PDF..`🤓

fileName: `{}.pdf`"""
}

gDocument = {
    "admin" : """Due to Some Telegram Limits..

I can only work as an admin
__Please promote me as admin__ ☺️""",
    "notDOC" : "Broh Please Reply to a Document or an Image..🤧",
    "Gadmin" : """Only Group Admins Can Use This Bot
Else Come to my Pm 😋""",
    "adminO" : """`Only admins can do it..`

Or try on your pdfs(__reply to your message__)"""
}
gDocument.update(document)

noHelp = f"`No one gonna help you` 😏"

split = {
    "work" : ["Range", "Single"],
    "inWork" : PROGRESS['workInP'],
    "download" : PROGRESS['dlFile'],
    "cancelCB" : document['cancelCB'],
    "exit" : "`Process Cancelled..` 😏",
    "button" : {
        "⚙️ PDF » SPLIT ↓" : "nabilanavab",
        "With In Range 🦞" : "split|R",
        "Single Page 🐛" : "split|S",
        "« BACK «" : "pdf1"
    },
    "over" : "`5 attempts over.. Process cancelled..`😏",
    "pyromodASK_1" : """__PDF Split » By Range
Now, Enter the range (start:end) :__

/exit __to cancel__""",
    "completed" : "`Downloading Completed..` ✅",
    "error_1" : "`Syntax Error: justNeedStartAndEnd `🚶",
    "error_2" : "`Syntax Error: errorInEndingPageNumber `🚶",
    "error_3" : "`Syntax Error: errorInStartingPageNumber `🚶",
    "error_4" : "`Syntax Error: pageNumberMustBeADigit` 🧠",
    "error_5" : "`Syntax Error: noEndingPageNumber Or notADigit` 🚶",
    "error_6" : "`Can't find any number..`😏",
    "error_7" : "`Something went Wrong..`😅",
    "error_8" : "`Enter Numbers less than {}..`😏",
    "error_9" : "`1st Check Number of pages` 😏",
    "upload" : "⚙️ `Started Uploading..` 📤"
}

pdf2IMG = {
    "uploadfile" : split["upload"],
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "download" : PROGRESS['dlFile'],
    "toImage" : {
        "⚙️ PDF » IMAGES ↓" : "nabilanavab",
        "🖼 IMG 🖼" : "pdf|img|img",
        "📂 DOC 📂" : "pdf|img|doc",
        "🤐 ZIP 🤐" : "pdf|img|zip",
        "🎯 TAR 🎯" : "pdf|img|tar",
        "« BACK «" : "pdf1" 
    },
    "imgRange" : {
        "⚙️ PDF » IMAGES » {} ↓" : "nabilanavab",
        "🙄 ALL 🙄" : "p2img|{}A",
        "🤧 RANGE 🤧" : "p2img|{}R",
        "🌝 PAGES 🌝" : "p2img|{}S",
        "« BACK «" : "pdf|img"
    },
    "over" : "`5 attempt over.. Process canceled..`😏",
    "pyromodASK_1" : """__Pdf - Img›Doc » Pages:
Now, Enter the range (start:end) :__

/exit __to cancel__""",
    "pyromodASK_2" : """"__Pdf - Img›Doc » Pages:
Now, Enter the Page Numbers seperated by__ (,) :

/exit __to cancel__""",
    "exit" : "`Process Canceled..` 😏",
    "error_1" : "`Syntax Error: justNeedStartAndEnd `🚶",
    "error_2" : "`Syntax Error: errorInEndingPageNumber `🚶",
    "error_3" : "`Syntax Error: errorInStartingPageNumber `🚶",
    "error_4" : "`Syntax Error: pageNumberMustBeADigit` 🧠",
    "error_5" : "`Syntax Error: noEndingPageNumber Or notADigit` 🚶",
    "error_6" : "`Can't find any number..`😏",
    "error_7" : "`Something went Wrong..`😅",
    "error_8" : "`PDF only have {} pages` 💩",
    "error_9" : "`1st Check Number of pages` 😏",
    "error_10" : "__Due to Some restrictions Bot Sends Only 50 pages as ZIP..__😅",
    "total" : "`Total pages: {}..⏳`",
    "upload" : "`Uploading: {}/{} pages.. 🐬`",
    "current" : "`Converted: {}/{} pages.. 🤞`",
    "complete" : "`Uploading Completed.. `🏌️",
    "canceledAT" : "`Canceled at {}/{} pages..` 🙄",
    "cbAns" : "⚙️ okDA, Canceling.. ",
    "cancelCB" : {"💤 CANCEL 💤" : "close|P2I"},     # EDITABLE: ❌
    "canceledCB" : {"🍄 CANCELLED 🍄" : "close|P2IDONE"},
    "completed" : {"😎 COMPLETED 😎" : "close|P2ICOMP"}
}

merge = {
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "upload" : PROGRESS['upFile'],
    "load" : "__Due to Overload you can only merge 5 PDFs at a time__",
    "sizeLoad" : "`Due to Overload Bot Only Support %sMb PDFs..", # removing %s show error
    "pyromodASK" : """__MERGE pdfs » Total PDFs in queue: {}__

/exit __to cancel__
/merge __to merge__""",
    "exit" : "`Process Cancelled..` 😏",
    "total" : "`Total PDFs : {} 💡",
    "current" : "__Started Downloading PDF : {} 📥__",
    "cancel" : "`Merging Process Cancelled.. 😏`",
    "started" : "__Merging Started.. __ 🪄",
    "caption" : "`Merged PDF 🙂`",
    "error" : """`May be File Encrypted..`

Reason: {}"""
}

metaData = {
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "download" : PROGRESS['dlFile'],   # [❌]
    "read" : "Please read this message again.. 🥴"
}

preview = {
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "error" : document['error'],
    "download" : PROGRESS['dlFile'],
    "_" : "PDF only have {} pages 🤓\n\n",
    "__" : "PDF pages: {}\n\n",
    "total" : "`Total pages: {}..` 🤌",
    "album" : "`Preparing an Album..` 🤹",
    "upload" : f"`Uploading: preview pages.. 🐬`"
}

stamp = {
    "stamp" : {
        "⚙️ PDF » STAMP ↓" : "nabilanavab",
        "Not For Public Release 🤧" : "pdf|stp|10",
        "For Public Release 🥱" : "pdf|stp|8",
        "Confidential 🤫" : "pdf|stp|2",
        "Departmental 🤝" : "pdf|stp|3",
        "Experimental 🔬" : "pdf|stp|4",
        "Expired 🐀" : "pdf|stp|5",
        "Final 🔧" : "pdf|stp|6",
        "For Comment 🗯️" : "pdf|stp|7",
        "Not Approved 😒" : "pdf|stp|9",
        "Approved 🥳" : "pdf|stp|0",
        "Sold ✊" : "pdf|stp|11",
        "Top Secret 😷" : "pdf|stp|12",
        "Draft 👀" : "pdf|stp|13",
        "AsIs 🤏" : "pdf|stp|1",
        "« BACK «" : "pdf1"
    },
    "stampA" : {
        "⚙️ PDF » STAMP » COLOR ↓" : "nabilanavab",
        "Red ❤️" : "spP|{}|r",
        "Blue 💙" : "spP|{}|b",
        "Green 💚" : "spP|{}|g",
        "Yellow 💛" : "spP|{}|c1",
        "Pink 💜" : "spP|{}|c2",
        "Hue 💚" : "spP|{}|c3",
        "White 🤍" : "spP|{}|c4",
        "Black 🖤" : "spP|{}|c5",
        "« Back «" : "pdf|stp"
    },
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "download" : PROGRESS['dlFile'],
    "upload" : PROGRESS['upFile'],
    "stamping" : "`Started Stamping..` 💠",
    "caption" : """stamped pdf\ncolor : `{}`
annot : `{}`"""
}

work = {
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "download" : PROGRESS['dlFile'],
    "takeTime" : PROGRESS['takeTime'],
    "upload" : PROGRESS['upFile'],
    "button" : document['cancelCB'],
    "rot360" : "You have some **big problem..🙂**",
    "ocrError" : "Owner Restricted 😎🤏",
    "largeNo" : "Send a PDF file less than 5 pages.. 🙄",
    "pyromodASK_1" : """__PDF {} »
Now, please enter the PASSWORD :__

/exit __to cancel__""",
    "pyromodASK_2" : """__Rename PDF »
Now, please enter the NEW NAME:__

/exit __to cancel__""",
    "exit" : "`process canceled.. `😏",
    "ren_caption" : "__New Name:__ `{}`", 
    "notENCRYPTED" : "`File is Not Encrypted..` 👀",
    "compress" : """⚙️ ```Started Compressing.. 🌡️
It might take some time..```💛""",
    "decrypt" : """⚙️ ```Started Decrypting.. 🔓
It might take some time..```💛""",
    "encrypt" : """⚙️ ```Started Encrypting.. 🔐
It might take some time..```💛""",
    "ocr" : """⚙️ ```Adding OCR Layer.. ✍️
It might take some time..```💛""",
    "format" : """⚙️ ```Started Formatting.. 🤘
It might take some time..```💛""",
    "rename" : """⚙️ ```Renameing PDf.. ✏️
It might take some time..```💛""",
    "rot" : """⚙️ ```Rotating PDf.. 🤸
It might take some time..```💛""",
    "pdfTxt" : """⚙️ ```Extracting Text.. 🐾
It might take some time..```💛""",
    "fileNm" : """Old Filename: {}
New Filename: {}""",
    "rotate" : {
        "⚙️ PDF » ROTATE ↓" : "nabilanavab",
        "90°" : "work|rot90",
        "180°" : "work|rot180",
        "270°" : "work|rot270",
        "360°" : "work|rot360",
        "« BACK «" : "pdf1"
    },
    "txt" : {
        "⚙️ PDF » TXT ↓" : "nabilanavab",
        "📜 MESSAGE 📜" : "work|M",
        "🧾 TXT FILE 🧾" : "work|T",
        "🌐 HTML 🌐" : "work|H",
        "🎀 JSON 🎀" : "work|J",
        "« BACK «" : "pdf1"
    }
}

PROCESS = {
    "ocr" : "OCR added",
    "decryptError" : "__Cannot Decrypt the file with__ `{}` 🕸️",
    "decrypted" : "__Decrypted File__",
    "encrypted" : "__Page Number__: {}\n__key__ 🔐: ||{}||",
    "compressed" : """`Original Size : {}
Compressed Size : {}

Ratio : {:.2f} %`""",
    "cantCompress" : "File Can't be Compressed More..🤐",
    "pgNoError" : """__For Some Reason A4 FORMATTING Supports only for PDFs with less than 5 Pages__

Total Pages: {} ⭐""",
    "ocrError" : "`Already Have A Text Layer.. `😏",
    "90" : "__Rotated 90°__",
    "180" : "__Rotated 180°__",
    "270" : "__Rotated 270°__",
    "formatted" : "A4 Formatted File",
    "M" : "♻ Extracted {} Pages ♻",
    "H" : "HTML File",
    "T" : "TXT File",
    "J" : "JSON File"
}

pdf2TXT = {
    "upload" : PROGRESS["upFile"],
    "exit" : split['exit'],
    "nothing" : "Nothing to create.. 😏",
    "TEXT" : "`Create PDF From Text Messages »`",
    "start" : "Started Converting txt to Pdf..🎉",
    "font_btn" : {
        "TXT@PDF » SET FONT" : "nabilanavab",
        "Times" : "pdf|font|t",
        "Courier" : "pdf|font|c",
        "Helvetica (Default)" : "pdf|font|h",
        "Symbol" : "pdf|font|s",
        "Zapfdingbats" : "pdf|font|z",
        "🚫 CLOSE 🚫" : "close|me"
    },
    "size_btn" : {
        "TXT@PDF » {} » SET SCALE" : "nabilanavab",
        "Portarate" : "t2p|{}|p",
        "Landscape" : "t2p|{}|l",
        "« Back «": "pdf|T2P"
    },
    "askT" : """__TEXT TO PDF » Now, please enter a TITLE:__

/exit __to cancel__\n/skip __to skip__""",
    "askC" : """__TEXT TO PDF » Now, please enter paragraph {}:__

/exit __to cancel__\n/create __to create__"""
}

URL = {
    "notPDF" : "`Not a PDF File",
    "close" : { "close" : "close|all" },
    "get" : {"🧭 Get PDF File 🧭" : "getFile"},
    "error" : """🐉 SOMETHING WENT WRONG 🐉,

ERROR: `{}`

NB: In Groups, Bots Can Only fetch documents Send After Joining Group =)""",
    "done" : "```Almost Done.. ✅\nNow, Started Uploading.. 📤```",
    "_error_" : "send me any url or direct telegram pdf links",
    "openCB" : {"Open In Browser" : "{}"},
    "_error" : "`Some Thing Went Wrong =(`\n\n`{}`",
    "_get" : """[Open Chat]({})

**ABOUT CHAT ↓**
Chat Type   : {}
Chat Name : {}
Chat Usr    : @{}
Chat ID        : {}
Date : {}

**ABOUT MEDIA ↓**
Media       : {}
File Name : {}
File Size   : {}
File Type : {}"""
}

getFILE = {
    "wait" : "Wait.. Let me.. 😜",
    "inWork" : PROGRESS['workInP'],
    "big" : "Send PDF url less than {}mb",
    "dl" : {"📥 ..DOWNLOADING.. 📥" : "nabilanavab"},
    "up" : {"📤 ..UPLOADING..  📤" : "nabilanavab"},
    "complete" : {"😎 COMPLETED 😎" : f"{str(settings.SOURCE_CODE)}"}
}

cbAns = [
    "This feature is Under Development ⛷️",
    "Error annenn paranjille.. then what.. 😏",
    "Process Canceled.. 😏",
    "File Not Encrypted.. 👀",
    "Nothing Official About it.. 😅",
    "🎉 Completed.. 🏃"
]

wa = {
    "exit" : split["exit"],
    "over" : pdf2IMG['over'],
    "upFile" : PROGRESS['upFile'],
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "download" : PROGRESS['dlFile'],
    "error" : "Something went Wrong 🙂",
    "cancelCB" : {"⟨ Cancel ⟩" : "close|me"},
    "add" : "Adding watermark to PDF File 💩",
    "waDL" : "__Getting watermark File..__ 🙄",
    "type" : {
        "⚙️ PDF » WATERMARK ↓" : "nabilanavab",
        "💬 TEXT 💬" : "pdf|wa|txt",
        "🖼 IMAGE 🖼" : "close|dev",
        "📎 PDF 📎" : "close|dev",
        "« BACK «" : "pdf2"
    },
    "op" : {
        "⚙️ PDF » WATERMARK » {} » OPCACiTY ↓" : "nabilanavab",
        "𝟙𝟘" : "pdf|wa|{}|o01",
        "𝟚𝟘" : "pdf|wa|{}|o02",
        "𝟛𝟘" : "pdf|wa|{}|o03",
        "𝟜𝟘" : "pdf|wa|{}|o04",
        "𝟝𝟘" : "pdf|wa|{}|o05",
        "𝟞𝟘" : "pdf|wa|{}|o06",
        "𝟟𝟘" : "pdf|wa|{}|o07",
        "𝟠𝟘" : "pdf|wa|{}|o08",
        "𝟡𝟘" : "pdf|wa|{}|o09",
        "𝟙𝟘𝟘" : "pdf|wa|{}|o10",
        "« BACK «" : "pdf|wa"
    },
    "po" : {
        "⚙️ PDF » WATERMARK » POSiTiON ↓" : "nabilanavab",
        "⬆️ ToP ⬆️" : "wa|{0}|{1}|pT",
        "↔️ MiDDLE ↔️" : "wa|{0}|{1}|pM",
        "⬇️ BoTToM ⬇️" : "wa|{0}|{1}|pB",
        "« BACK «" : "pdf|wa|{0}"
    },
    "poTXT" : {
        "⚙️ PDF » WATERMARK » POSiTiON ↓" : "nabilanavab",
        "⬆️ ToP ⬆️" : "pdf|wa|{0}|{1}|pT",
        "↔️ MiDDLE ↔️" : "pdf|wa|{0}|{1}|pM",
        "⬇️ BoTToM ⬇️" : "pdf|wa|{0}|{1}|pB",
        "« BACK «" : "pdf|wa|{0}"
    },
    "color" : {
        "⚙️ PDF » WATERMARK » CoLoR ↓" : "nabilanavab",
        "᠎᠎᠎⚪️" : "wa|{0}|{1}|{2}|W",
        "᠎⚫️" : "wa|{0}|{1}|{2}|B",
        "᠎᠎🟤" : "wa|{0}|{1}|{2}|C",
        "᠎🔴" : "wa|{0}|{1}|{2}|R",
        "᠎᠎🟢" : "wa|{0}|{1}|{2}|G",
        "🔵" : "wa|{0}|{1}|{2}|N",
        "᠎᠎🟡" : "wa|{0}|{1}|{2}|Y",
        "᠎᠎🟠" : "wa|{0}|{1}|{2}|O",
        "🟣" : "wa|{0}|{1}|{2}|V",
        "« BACK «" : "pdf|wa|{0}|{1}"
    }, 
    "txt" : """__Now, Send me any Text Message__

/exit : to cancel""", 
    "pdf" : """__Send me the watermark pdf.__

/exit : to cancel""",
    "img" : """__Send me the watermark Image as file.__
__ Supported Files [png, jpeg, jpg]__

/exit : to cancel""",
}

comb = {
    "upFile" : PROGRESS['upFile'],
    "inWork" : PROGRESS['workInP'],
    "process" : document['process'],
    "process" : document['process'],
    "download" : PROGRESS['dlFile'],
    "cancelCB" : {"⟨ Cancel ⟩" : "close|me"},
}

inline_query = {
    "capt" : "SET LANGUAGE ⚙️",
    "des" : "By: @nabilanavab ❤",
    "TOP" : { "Now, Select Language ⮷" : "nabilanavab" },
}

LINK = {
    "gen" : "`🔗 Generating..`",
    "_gen" : """```🔗 Generating..
We're working on it!

Please allow a moment for the processing to complete.```""",
    "no" : "Unfortunately, we encountered an error 😓",
    "type" : """`🔗 Generating..`

**Public** 📢:
__The file accessed via this link will be publicly available, allowing anyone to save and forward it__.


**Protect** 🔐:
__Ensures the confidentiality of the message by preventing its forwarding and saving__.""",
    "notify" : "Get Notify when a someone fetch this pdf",
    "notify_pvt" : {
        "🔔 NOTIFY 🔔" : "link-pvt-ntf",
        "🔕 MUTE 🔕" : "link-pvt-mut"
    },
    "notify_pub" : {
        "🔔 NOTIFY 🔔" : "link-pbc-ntf",
        "🔕 MUTE 🔕" : "link-pbc-mut"
    },
    "typeBTN" : {
        "📢 PUBLIC 📢" : "link-pub",
        "🔐 PRIVATE 🔐" : "link-pvt"
    },
    "link" : "**Here it is! This is what you were searching for..**",
    "error" : "Oops, it looks like something went wrong. Please try again later.\n\n`ERROR:` {}"
}

DELETE = {
    "button" : {
        "⚙️ PDF » SPLIT ↓" : "nabilanavab",
        "With In Range 🦞" : "split|dR",
        "Single Page 🐛" : "split|dS",
        "« BACK «" : "pdf1"
    },
}
