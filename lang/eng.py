# LANG: ENGLISH LANG_CODE: ENG                                      >>  copyright ©️ 2021 nabilanavab  <<                                         fileName : lang/ENG.py
#                                        Thank: nabilanavab                                                   E-mail: nabilanavab@gmail.com

from configs.config import settings

# PM WELCOME MESSAGE (HOME A, B, C, D...)
HOME = {
    "HomeA" : """Hey [{}](tg://user?id={})..!!
This bot will help you to do many things with PDFs. 🥳

Some of the key features are:\n◍ `Convert images to PDF`
◍ `Convert PDF to images`\n◍ `Convert files to PDF`""",
    "HomeACB" : {
        "⚙️ SETTINGS ⚙️" : "Home|B", "⚠️ HELP ⚠️" : "Home|C",
        "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 SOURCE CODE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🚶 CLOSE 🚶" : "close|mee"
    },
    "HomeAdminCB" : {
        "⚙️ SETTINGS ⚙️" : "Home|B", "⚠️ HELP ⚠️" : "Home|C",
        "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 SOURCE CODE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 STATUS 🗽" : f"status|home", "🚶 CLOSE 🚶" : "close|mee"
    },
    "HomeB" : """SETTINGS PAGE ⚙️\n\nUSER NAME   : {}
USER ID           : {}\nUSERNAME    : {}\nJOIN DATE      : {}\n
LANGUAGE    : {}\nAPI                    : {}
THUMB            : {}\nCAPTION         : {}\nFILE NAME      : {}""",
    "HomeBCB" : {
        "🌍 LANG 🌍" : "set|lang", "📍 THUMB 📍" : "set|thumb",
        "📈 NAME 📈" : "set|fname", "💩 API 💩" : "set|api",
        "📅 CAPTION 📅" : "set|capt", "« BACK TO HOME «" : "Home|B2A"
    },
    "HomeC" : """🪂 **HELP MESSAGE** 🪂:

```Some of the main features are:
 ◍ Convert Images to PDF\n ◍ PDF Manupultions\n ◍ Many popular codecs to PDF
 
Modify the PDF file:
 ◍ PDF⥃IMAGES [all,range,pages]\n ◍ DOCS to PDF [png, jpg, jpeg]\n ◍ IMAGES⥃PDF\n ◍ PDF METADATA\n ◍ PDF⥃TEXT\n ◍ TEXT⥃PDF\n ◍ Compress pdf file
 ◍ SPLIT PDF [range, pages]\n ◍ MERGE PDF\n ◍ ADD STAMP\n ◍ RENAME PDF\n ◍ ROTATE PDF\n ◍ ENCRYPT/DECRYPT PDF\n ◍ PDF FORMATTER \n ◍ PDF⥃JSON/TXT FILE
 ◍ PDF⥃HTML [web view]\n ◍ URL⥃PDF\n ◍ PDF⥃ZIP/TAR/RAR [all, range, pages]\nAnd Much More.. ```""",
    "HomeCCB" : {"« BACK HOME «" : "Home|A", "🛈 INSTRUCTIONS 🛈" : "Home|D"},
    "HomeD" : """`As you know, this is a free service, I cannot guarantee how long I can maintain this service..`😝
 
⚠️ INSTRUCTIONS ⚠️:
🛈 __Please don't try to abuse Bot Admins__ 😒
🛈 __Don't spam here, may lead to a permanent ban 🎲__.
🛈 __Porn Contents too will gives you PERMANENT BAN 💯__

**Send any image to start:** 😁""",
    "HomeDCB" : {"⚠️ HELP ⚠️" : "Home|C", "» BACK HOME »" : "Home|A"}  
}

SETTINGS = {
    "default" : ["DEFAULT ❌", "CUSTOM ✅"], "chgLang" : {"SETTING ⚙️ » CHANGE LANG 🌐" : "nabilanavab"},
    "error" : "Something went wrong while retrieving data from the database", "lang" : "Now, Select any language..",
    "ask" : ["Now, Send me..", "Now, Send me.. 😅\n\nFast.! I have no more time to go over the text.. 😏\n\n/cancel: to cancel"],
    "askApi" : "\n\nOpen the **Below** link and Send me the secret code:", "waitApi" : {"Open link ✅" : "https://www.convertapi.com/a/signin"},
    "wait" : {"Waiting.. 🥱" : "nabilanavab"}, "back" : {"« BACK TO HOME «" : "Home|B2S"}, "errorCB" : {"« BACK TO HOME «" : "Home|B2A"},
    "result" : ["Settings cannot be updated ❌", "Settings Updated Successfully ✅"], "cant" : "This feature cannot be used ❌",
    "feedback" : "Reviews from Awesome Customers like you help Other.\n@nabilanavab"
                 "\n\nReport a BUG in {} Lang:\n`• Specify Lang\n• Error Message\n• New Message`",
    "feedbtn" : {"Report Lang Error" : settings.REPORT},
    "thumb" : [
        {"SETTING ⚙️ » THUMBNAIL 📷" : "nabilanavab", "♻ ADD ♻" : "set|thumb+", "« BACK TO HOME «" : "Home|B"},
        {"SETTING ⚙️ » THUMBNAIL 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|thumb+", "🗑 DELETE 🗑" : "set|thumb-", "« BACK TO HOME «" : "Home|B2S"}
    ],
    "fname" : [
        {"SETTING ⚙️ » FNAME 📷" : "nabilanavab", "♻ ADD ♻" : "set|fname+", "« BACK TO HOME «" : "Home|B2S"},
        {"SETTING ⚙️ » FNAME 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|fname+", "🗑 DELETE 🗑" : "set|fname-", "« BACK TO HOME «" : "Home|B2S"}
    ],
    "api" : [
        {"SETTING ⚙️ » API 📷" : "nabilanavab", "♻ ADD ♻" : "set|api+", "« BACK TO HOME «" : "Home|B2S"},
        {"SETTING ⚙️ » API 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|api+", "🗑 DELETE 🗑" : "set|api-", "« BACK TO HOME «" : "Home|B2S"}
    ],
    "capt" : [
        {"SETTING ⚙️ » CAPTION 📷" : "nabilanavab", "♻ ADD ♻" : "set|capt+", "« BACK TO HOME «" : "Home|B2S"},
        {"SETTING ⚙️ » CAPTION 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|capt+", "🗑 DELETE 🗑" : "set|capt-", "« BACK TO HOME «" : "Home|B2S"}
    ]
}

BOT_COMMAND = {"start" : "Welcome message..", "txt2pdf" : "Create text PDF's"}

HELP_CMD = {
    "userHELP" : """[USER COMMAND MESSAGES]:\n
/start: To check whether bot is alive or not\n/cancel: To cancel current work
/delete: Clear image to PDF **queue**\n/txt2pdf: Text to PDF""",
    "adminHelp" : """\n\n\n[ADMIN COMMAND MESSAGES]:\n
/send: To broadcast, PM message""",
    "footerHelp" : f"""\n\n\nSource-Code: [i 💜 PDF]({str(settings.SOURCE_CODE)})
Bot: @complete_pdf_bot 💎\n[Support Channel]({settings.OWNED_CHANNEL})""",
    "CB" : {"⚠️ CLOSE ⚠️" : "close|all"}
}

STATUS_MSG = {
    "HOME" : "`Now, select any option below to get current STATUS 💱.. `",
    "_HOME" : {
        "📊 ↓ SERVER ↓ 📊" : "nabilanavab", "📶 STORAGE 📶" : "status|server",
        "🥥 DATABASE 🥥" : "status|db", "🌝 ↓ GET LIST ↓ 🌝": "nabilanavab",
        "💎 ADMIN 💎" : "status|admin", "👤 USERS 👤" : "status|users",
        "« BACK «" : "Home|A"
    },
    "DB" : """📂 DATABASE :\n\n**◍ Database Users :** `{}` 📍\n**◍ Database Chats :** `{}` 📍""",
    "SERVER" : """**◍ Total Space     :** `{}`
**◍ Used Space     :** `{}({}%)`\n**◍ Free Space      :** `{}`
**◍ CPU Usage      :** `{}`%\n**◍ RAM Usage     :** `{}`%
**◍ Current Work  :** `{}`\n**◍ Message Id     :** `{}`""",
    "BACK" : {"« BACK «" : "status|home"}, "ADMIN" : "**Total ADMIN:** __{}__\n",
    "USERS" : "Users saved In DB Are:\n\n", "NO_DB" : "No dataBASE set Yet 💩"
}

feedbackMsg = f"[Write a FEEDBACK 📋]({settings.FEEDBACK})"

# GROUP WELCOME MESSAGE
HomeG = {
    "HomeA" : """Hello There.! 👋\nI'm new here {message.chat.title}\n
Let me introduce myself..\nMy Name is **iLovePDF,** and I can help you to do **many
things** with @telegram PDF files.\n\nThanks @nabilanavab for this AWESOME Bot 😅""",
    "HomeACB" : {
        "🤠 BOT OWNER 🤠": f"https://telegram.dog/{settings.OWNER_USERNAME}",
        "🛡️ UPDATE CHANNEL 🛡️": f"{settings.OWNED_CHANNEL}", "🌟 SOURCE CODE 🌟": f"{settings.SOURCE_CODE}"
    }
}

# BANNED USER UI
BAN = {
    "cbNotU" : "Message IS NOT for You.. 😏",
    "banCB" : {
        "Create your Own Bot": f"{settings.SOURCE_CODE}", "Tutorial": f"{settings.SOURCE_CODE}",
        "Update Channel": "https://telegram.dog/ilovepdf_bot"
    },
    "UCantUse" : """Hey {}\n\nFOR SOME REASON YOU CANT USE THIS BOT :(""",
    "UCantUseDB" : """Hey {}\n\nFOR SOME REASON YOU CANT USE THIS BOT :(\n\nREASON: {}""",
    "GroupCantUse" : """{} NEVER EXPECT A GOOD RESPONSE FROM ME\n
ADMINS RESTRICTED ME FROM WORKING HERE.. 🤭""",
    "GroupCantUseDB" : """{} NEVER EXPECT A GOOD RESPONSE FROM ME\n
ADMINS RESTRICTED ME FROM WORKING HERE.. 🤭\n\nREASON: {}""",
    "Force" : """Wait [{}](tg://user?id={})..!!\n
Due To The Huge Traffic Only **Channel Members** Can Use this Bot 🚶\n
This Means That You Need To **Join** The Below Mentioned Channel for Using Me!\n
Hit on `"♻️retry♻️"` after joining.. 😅""",
    "ForceCB" : {"🌟 JOIN CHANNEL 🌟" : "{}", "♻️ Refresh ♻️" : "refresh"},
    "Fool" : "വിളച്ചിലെടുക്കല്ലേ കേട്ടോ.. 🤭"
}

checkPdf = {
    "pg" : "`Number of Pages: •{}•` 🌟",
    "pdf" : """`What should I do with this file.?`\n\nFile Name : `{}`\nFile Size : `{}`""",
    "pdfCB" : {
        "⭐ META£ATA ⭐" : "metaData", "🗳️ PREVIEW 🗳️" : "preview",
        "🖼️ IMAGES 🖼️" : "pdf|img", "✏️ TEXT ✏️" : "pdf|txt",
        "🔐 ENCRYPT 🔐" : "work|encrypt", "🔒 DECRYPT 🔓" : "work|decrypt",
        "🗜️ COMPRESS 🗜️" : "work|compress", "🤸 ROTATE 🤸" : "pdf|rotate",
        "✂️ SPLIT ✂️" : "pdf|split", "🧬 MERGE 🧬" : "merge", "™️ STAMP ™️" : "pdf|stp",
        "✏️ RENAME ✏️" : "work|rename", "📝 OCR 📝" : "work|ocr",
         "🥷 A4 FORMAT 🥷" : "work|format", "🚫 CLOSE 🚫" : "close|all"
    },
    "error" : """__I can't do anything with this file.__ 😏\n\n🐉  `CODEC ERROR`  🐉""",
    "errorCB" : {"❌ ERROR IN CODEC ❌" : "error", "🔸 CLOSE 🔸" : "close|all"},
    "encrypt" : """`FILE IS ENCRYPTED` 🔐\n\nFile Name: `{}`\nFile Size: `{}`""",
    "encryptCB" : {"🔓 DECRYPT 🔓" : "work|decrypt"}
}

PROGRESS = {
    "progress" : """**\nDone ✅ : **{0}/{1}\n**Speed 🚀:** {2}/s\n**Estimated Time ⏳:** {3}""",
    "dlImage" : "`Downloading your Image..⏳`", "upFile" : "`Started Uploading..`📤",
    "dlFile" : "`Downloading your file..` 📥", "upFileCB" : {"📤 .. UPLOADING.. 📤" : "nabilanavab"},
    "workInP" : "WORK IN PROGRESS.. 🙇", "refresh" : {"♻️ Refresh ♻️" : "{}"},
    "takeTime" : """```⚙️ Work in Progress..`\n`It might take some time..```💛""",
    "cbPRO_D" : ["📤 DOWNLOAD: {:.2f}% 📤", "🎯 CANCEL 🎯"], "cbPRO_U" : ["📤 UPLOADED: {:.2f}% 📤", "🎯 CANCEL 🎯"]
}

GENERATE = {
    "deleteQueue" : "`Queue deleted Successfully..`🤧", "noQueue" : "`No Queue found..`😲",
    "noImages" : "No image found.!! 😒", "getFileNm" : "Now Send Me a File Name 😒: ",
    "geting" : "File Name: `{}`\nPages: `{}`", "getingCB" : {"📚 GENERATING PDF.." : "nabilanavab"},
    "currDL" : "Downloaded {} Images 🥱"
}

document = {
    "refresh" : PROGRESS['refresh'], "inWork" : PROGRESS['workInP'], "reply" : checkPdf['pdf'],
    "replyCB" : checkPdf['pdfCB'], "download" : PROGRESS['dlFile'], "process" : "⚙️ Processing..",
    "takeTime" : PROGRESS['takeTime'], "upFile" : PROGRESS['upFile'], "dlImage" : PROGRESS['dlImage'],
    "big" : """Due to Overload, Owner limits {}mb for pdf files 🙇
\n`please Send me a file less than {}mb Size` 🙃""",
    "bigCB" : {"💎 Create 2Gb Support Bot 💎" : "https://github.com/nabilanavab/ilovepdf"},
    "imageAdded" : """`Added {} pages to your PDF..`🤓\n\nfileName: `{}.pdf`""",
    "setHdImg" : """Now Image To PDF is in HD mode 😈""",
    "setDefault" : {"« Back to Default Quality «" : "close|hd"},
    "error" : """SOMETHING went WRONG.. 🐉\n\nERROR: `{}`""",
    "noAPI" : "`Please add convert API.. 💩\n\nstart » settings » api » add/change`",
    "useDOCKER" : "`File Not Supported, deploy bot using docker`",
    "fromFile" : "`Converted: {} to {}`", "unsupport" : "Unsupported file..🙄`",
    "generateRN" : {"GENERATE 📚" : "generate", "RENAME ✍️" : "generateREN"},
    "generate" : {"GENERATE 📚" : "generate"}, "cancelCB" : {"⟨ Cancel ⟩" : "close|me"}
}

noHelp = f"`No one gonna help you` 😏"

split = {
    "inWork" : PROGRESS['workInP'], "cancelCB" : document['cancelCB'],
    "download" : PROGRESS['dlFile'], "exit" : "`Process Cancelled..` 😏",
    "button" : {
        "⚙️ PDF » SPLIT ↓" : "nabilanavab", "With In Range 🦞" : "split|R",
        "Single Page 🐛" : "split|S", "« BACK «" : "pdf"
    },
    "work" : ["Range", "Single"], "over" : "`5 attempts over.. Process cancelled..`😏",
    "pyromodASK_1" : """__PDF Split » By Range\nNow, Enter the range (start:end) :__
\n/exit __to cancel__""",
    "completed" : "`Downloading Completed..` ✅",
    "error_1" : "`Syntax Error: justNeedStartAndEnd `🚶",
    "error_2" : "`Syntax Error: errorInEndingPageNumber `🚶",
    "error_3" : "`Syntax Error: errorInStartingPageNumber `🚶",
    "error_4" : "`Syntax Error: pageNumberMustBeADigit` 🧠",
    "error_5" : "`Syntax Error: noEndingPageNumber Or notADigit` 🚶",
    "error_6" : "`Can't find any number..`😏",
    "error_7" : "`Something went Wrong..`😅", "error_8" : "`Enter Numbers less than {}..`😏",
    "error_9" : "`1st Check Number of pages` 😏", "upload" : "⚙️ `Started Uploading..` 📤"
}

pdf2IMG = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "uploadfile" : split["upload"],
    "toImage" : {
        "⚙️ PDF » IMAGES ↓" : "nabilanavab", "🖼 IMG 🖼" : "pdf|img|img",
        "📂 DOC 📂" : "pdf|img|doc", "🤐 ZIP 🤐" : "pdf|img|zip",
        "🎯 TAR 🎯" : "pdf|img|tar","« BACK «" : "pdf" 
    },
    "imgRange" : {
        "⚙️ PDF » IMAGES » {} ↓" : "nabilanavab", "🙄 ALL 🙄" : "p2img|{}A",
        "🤧 RANGE 🤧" : "p2img|{}R", "🌝 PAGES 🌝" : "p2img|{}S", "« BACK «" : "pdf|img"
    },
    "over" : "`5 attempt over.. Process canceled..`😏",
    "pyromodASK_1" : """__Pdf - Img›Doc » Pages:\nNow, Enter the range (start:end) :__
\n/exit __to cancel__""",
    "pyromodASK_2" : """"__Pdf - Img›Doc » Pages:\nNow, Enter the Page Numbers seperated by__ (,) :
\n/exit __to cancel__""",
    "exit" : "`Process Canceled..` 😏",
    "error_1" : "`Syntax Error: justNeedStartAndEnd `🚶",
    "error_2" : "`Syntax Error: errorInEndingPageNumber `🚶",
    "error_3" : "`Syntax Error: errorInStartingPageNumber `🚶",
    "error_4" : "`Syntax Error: pageNumberMustBeADigit` 🧠",
    "error_5" : "`Syntax Error: noEndingPageNumber Or notADigit` 🚶",
    "error_6" : "`Can't find any number..`😏", "error_7" : "`Something went Wrong..`😅",
    "error_8" : "`PDF only have {} pages` 💩", "error_9" : "`1st Check Number of pages` 😏",
    "error_10" : "__Due to Some restrictions Bot Sends Only 50 pages as ZIP..__😅",
    "total" : "`Total pages: {}..⏳`", "upload" : "`Uploading: {}/{} pages.. 🐬`",
    "current" : "`Converted: {}/{} pages.. 🤞`", "complete" : "`Uploading Completed.. `🏌️",
    "canceledAT" : "`Canceled at {}/{} pages..` 🙄", "cbAns" : "⚙️ okDA, Canceling.. ",
    "cancelCB" : {"💤 CANCEL 💤" : "close|P2I"},     # EDITABLE: ❌
    "canceledCB" : {"🍄 CANCELLED 🍄" : "close|P2IDONE"},
    "completed" : {"😎 COMPLETED 😎" : "close|P2ICOMP"}
}

merge = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "upload" : PROGRESS['upFile'],
    "load" : "__Due to Overload you can only merge 5 PDFs at a time__",
    "sizeLoad" : "`Due to Overload Bot Only Support %sMb PDFs..", # removing %s show error
    "pyromodASK" : """__MERGE pdfs » Total PDFs in queue: {}__

/exit __to cancel__
/merge __to merge__""",
    "exit" : "`Process Cancelled..` 😏", "total" : "`Total PDFs : {} 💡",
    "current" : "__Started Downloading PDF : {} 📥__", "cancel" : "`Merging Process Cancelled.. 😏`",
    "started" : "__Merging Started.. __ 🪄", "caption" : "`Merged PDF 🙂`",
    "error" : "`May be File Encrypted..`\n\nReason: {}"
}

metaData = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "download" : PROGRESS['dlFile'],   # [❌]
    "read" : "Please read this message again.. 🥴"
}

preview = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "error" : document['error'],
    "download" : PROGRESS['dlFile'], "_" : "PDF only have {} pages 🤓\n\n",
    "__" : "PDF pages: {}\n\n", "total" : "`Total pages: {}..` 🤌",
    "album" : "`Preparing an Album..` 🤹", "upload" : f"`Uploading: preview pages.. 🐬`"
}

stamp = {
    "stamp" : {
        "⚙️ PDF » STAMP ↓" : "nabilanavab",
        "Not For Public Release 🤧" : "pdf|stp|10",
        "For Public Release 🥱" : "pdf|stp|8",
        "Confidential 🤫" : "pdf|stp|2", "Departmental 🤝" : "pdf|stp|3",
        "Experimental 🔬" : "pdf|stp|4", "Expired 🐀" : "pdf|stp|5",
        "Final 🔧" : "pdf|stp|6", "For Comment 🗯️" : "pdf|stp|7",
        "Not Approved 😒" : "pdf|stp|9", "Approved 🥳" : "pdf|stp|0",
        "Sold ✊" : "pdf|stp|11", "Top Secret 😷" : "pdf|stp|12",
        "Draft 👀" : "pdf|stp|13", "AsIs 🤏" : "pdf|stp|1",
        "« BACK «" : "pdf"
    },
    "stampA" : {
        "⚙️ PDF » STAMP » COLOR ↓" : "nabilanavab",
        "Red ❤️" : "spP|{}|r", "Blue 💙" : "spP|{}|b",
        "Green 💚" : "spP|{}|g", "Yellow 💛" : "spP|{}|c1",
        "Pink 💜" : "spP|{}|c2", "Hue 💚" : "spP|{}|c3",
        "White 🤍" : "spP|{}|c4", "Black 🖤" : "spP|{}|c5",
        "« Back «" : "pdf|stp"
    },
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "upload" : PROGRESS['upFile'],
    "stamping" : "`Started Stamping..` 💠", "caption" : """stamped pdf\ncolor : `{}`\nannot : `{}`"""
}

work = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "takeTime" : PROGRESS['takeTime'],
    "upload" : PROGRESS['upFile'], "button" : document['cancelCB'],
    "rot360" : "You have some **big problem..🙂**", "ocrError" : "Owner Restricted 😎🤏",
    "largeNo" : "Send a PDF file less than 5 pages.. 🙄",
    "pyromodASK_1" : """__PDF {} »\nNow, please enter the PASSWORD :__\n\n/exit __to cancel__""",
    "pyromodASK_2" : """__Rename PDF »\nNow, please enter the NEW NAME:__\n\n/exit __to cancel__""",
    "exit" : "`process canceled.. `😏", "ren_caption" : "__New Name:__ `{}`", 
    "notENCRYPTED" : "`File is Not Encrypted..` 👀",
    "compress" : "⚙️ `Started Compressing.. 🌡️\nIt might take some time..`💛",
    "decrypt" : "⚙️ `Started Decrypting.. 🔓\nIt might take some time..`💛",
    "encrypt" : "⚙️ `Started Encrypting.. 🔐\nIt might take some time..`💛",
    "ocr" : "⚙️ `Adding OCR Layer.. ✍️\nIt might take some time..`💛",
    "format" : "⚙️ `Started Formatting.. 🤘\nIt might take some time..`💛",
    "rename" : "⚙️ `Renameing PDf.. ✏️\nIt might take some time..`💛",
    "rot" : "⚙️ `Rotating PDf.. 🤸\nIt might take some time..`💛",
    "pdfTxt" : "⚙️ `Extracting Text.. 🐾\nIt might take some time..`💛",
    "fileNm" : "Old Filename: {}\nNew Filename: {}",
    "rotate" : {
        "⚙️ PDF » ROTATE ↓" : "nabilanavab", "90°" : "work|rot90", "180°" : "work|rot180",
        "270°" : "work|rot270", "360°" : "work|rot360", "« BACK «" : "pdf"
    },
    "txt" : {
        "⚙️ PDF » TXT ↓" : "nabilanavab", "📜 MESSAGE 📜" : "work|M", "🧾 TXT FILE 🧾" : "work|T",
        "🌐 HTML 🌐" : "work|H", "🎀 JSON 🎀" : "work|J", "« BACK «" : "pdf"
    }
}

PROCESS = {
    "ocr" : "OCR added", "decryptError" : "__Cannot Decrypt the file with__ `{}` 🕸️",
    "decrypted" : "__Decrypted File__", "encrypted" : "__Page Number__: {}\n__key__ 🔐: ||{}||",
    "compressed" : """`Original Size : {}\nCompressed Size : {}\n\nRatio : {:.2f} %`""",
    "cantCompress" : "File Can't be Compressed More..🤐",
    "pgNoError" : """__For Some Reason A4 FORMATTING Supports only for PDFs with less than 5 Pages__\n\nTotal Pages: {} ⭐""",
    "ocrError" : "`Already Have A Text Layer.. `😏",
    "90" : "__Rotated 90°__", "180" : "__Rotated 180°__", "270" : "__Rotated 270°__",
    "formatted" : "A4 Formatted File", "M" : "♻ Extracted {} Pages ♻",
    "H" : "HTML File", "T" : "TXT File", "J" : "JSON File"
}

pdf2TXT = {
    "upload" : PROGRESS["upFile"], "exit" : split['exit'], "nothing" : "Nothing to create.. 😏",
    "TEXT" : "`Create PDF From Text Messages »`", "start" : "Started Converting txt to Pdf..🎉",
    "font_btn" : {
        "TXT@PDF » SET FONT" : "nabilanavab", "Times" : "pdf|font|t", "Courier" : "pdf|font|c", "Helvetica (Default)" : "pdf|font|h",
        "Symbol" : "pdf|font|s", "Zapfdingbats" : "pdf|font|z", "🚫 CLOSE 🚫" : "close|me"
    },
    "size_btn" : { "TXT@PDF » {} » SET SCALE" : "nabilanavab", "Portarate" : "t2p|{}|p", "Landscape" : "t2p|{}|l", "« Back «": "pdf|T2P"},
    "askT" : "__TEXT TO PDF » Now, please enter a TITLE:__\n\n/exit __to cancel__\n/skip __to skip__",
    "askC" : "__TEXT TO PDF » Now, please enter paragraph {}:__\n\n/exit __to cancel__\n/create __to create__"
}

URL = {
    "get" : {"🧭 Get PDF File 🧭" : "getFile"}, "close" : HELP_CMD['CB'], "notPDF" : "`Not a PDF File",
    "error" : "🐉 SOMETHING WENT WRONG 🐉\n\nERROR: `{}`\n\nNB: In Groups, Bots Can Only fetch documents Send After Joining Group =)",
    "done" : "```Almost Done.. ✅\nNow, Started Uploading.. 📤```", "_error_" : "send me any url or direct telegram pdf links",
    "openCB" : {"Open In Browser" : "{}"}, "_error" : "`Some Thing Went Wrong =(`\n\n`{}`",
    "_get" : "[Open Chat]({})\n\n**ABOUT CHAT ↓**\nChat Type   : {}\nChat Name : {}\nChat Usr    : @{}\n"
             "Chat ID        : {}\nDate : {}\n\n**ABOUT MEDIA ↓**\nMedia       : {}\nFile Name : {}\nFile Size   : {}\n\nFile Type : {}"
}

getFILE = {
    "inWork" : PROGRESS['workInP'], "big" : "Send PDF url less than {}mb", "wait" : "Wait.. Let me.. 😜",
    "dl" : {"📥 ..DOWNLOADING.. 📥" : "nabilanavab"}, "up" : {"📤 ..UPLOADING..  📤" : "nabilanavab"},
    "complete" : {"😎 COMPLETED 😎" : f"{str(settings.SOURCE_CODE)}"}
}

cbAns = [
    "This feature is Under Development ⛷️", "Error annenn paranjille.. then what.. 😏",
    "Process Canceled.. 😏", "File Not Encrypted.. 👀", "Nothing Official About it.. 😅", "🎉 Completed.. 🏃"
]

inline_query = {
    "TOP" : { "Now, Select Language ⮷" : "nabilanavab" }, "capt" : "SET LANGUAGE ⚙️", "des" : "By: @nabilanavab ❤"
}

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
