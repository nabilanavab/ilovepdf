# copyright ©️ 2021 nabilanavab
file_name = "lang/eng.py"


from configs.config   import settings

# REPLY MESSAGE FOR BROKEN WORKS
RESTART = {
    "msg" : """☠ `𝐎𝐕𝐄𝐑𝐋𝐎𝐀𝐃 𝐃𝐄𝐂𝐓𝐄𝐂𝐓𝐄𝐃`☠:\n__𝐬𝐞𝐫𝐯𝐞𝐫 𝐫𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝__ \n\nI noticed that your work was also in queue\n\nCan you please try again..!""",
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
        "⚙️ SETTINGS ⚙️" : "Home|B", "🌍 LANGUAGE 🌍" : "set|lang", "⚠️ HELP ⚠️" : "Home|C",
        "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}", "🌟 SOURCE CODE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "➕ ADD IN GROUP ➕" : "https://t.me/{}?startgroup=True"
    },
    "HomeAdminCB" : {
        "⚙️ SETTINGS ⚙️" : "Home|B", "🌍 LANGUAGE 🌍" : "set|lang", "⚠️ HELP ⚠️" : "Home|C",
        "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}", "🌟 SOURCE CODE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 STATUS 🗽" : f"status|home", "➕ ADD IN GROUP ➕" : "https://t.me/{}?startgroup=True", "🚶 CLOSE 🚶" : "close|mee"
    },
    "HomeB" : "SETTINGS PAGE ⚙️\n\nUSER NAME   : {}\nUSER ID           : {}\nUSERNAME    : {}\nJOIN DATE      : {}\n\nLANGUAGE    : {}\n"
        "API                    : {}\nTHUMB            : {}\nCAPTION         : {}\nFILE NAME      : {}""",
    "HomeBCB" : {
        "📍 THUMB 📍" : "set|thumb", "📈 NAME 📈" : "set|fname", "💩 API 💩" : "set|api", "📅 CAPTION 📅" : "set|capt", "« BACK TO HOME «" : "Home|B2A"
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
    "HomeDCB" : { "⚠️ HELP ⚠️" : "Home|C", "» BACK HOME »" : "Home|A" }
}

# GROUP WELCOME MESSAGE
HomeG = {
    "HomeA" : HOME['HomeA'],
    "HomeACB" : {
        "🌍 LANGUAGE 🌍" : "set|lang", "🛡️ HELP 🛡️": "Home|C", "📢 CHANNEL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 SOURCE CODE 🌟": f"{settings.SOURCE_CODE}", "🚶 CLOSE 🚶" : "close|mee",
    }
}

SETTINGS = {
    "lang" : "Now, Select any language..", "default" : ["DEFAULT ❌", "CUSTOM ✅"], "cant" : "This feature cannot be used ❌",
    "wait" : { "Waiting.. 🥱" : "nabilanavab" }, "feedbtn" : { "Report any bugs you find!" : settings.REPORT },
    "chgLang" : {"SETTING ⚙️ » CHANGE LANG 🌐" : "nabilanavab"}, "askApi" : "\n\nOpen the **Below** link and Send me the secret code:",
    "waitApi" : { "Open link ✅" : "https://www.convertapi.com/a/signin" }, "error" : "Something went wrong while retrieving data from the database",
    "result" : ["Settings cannot be updated ❌", "Settings Updated Successfully ✅"],
    "back" : [{ "« BACK TO HOME «" : "Home|B2S" }, { "« BACK TO HOME «" : "Home|B2A" }],
    "feedback" : "Bug warning! If my texts sound weird, it's probably Google Translate's fault."
                 "\n\nReport a BUG in {} Lang:\n`• Specify Lang\n• Error Message\n• New Message`",
    "ask" : [
        "Now, Send me..",
        "Now, Send me.. 😅\n\nFast.! I have no more time to go over the text.. 😏\n\n/cancel: to cancel"
    ],
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

BOT_COMMAND = { "start" : "Welcome message..", "txt2pdf" : "Create text PDF's" }

STATUS_MSG = {
    "_HOME" : {
        "📊 ↓ SERVER ↓ 📊" : "nabilanavab", "📶 STORAGE 📶" : "status|server", "🥥 DATABASE 🥥" : "status|db",
        "🌝 ↓ GET LIST ↓ 🌝": "nabilanavab", "💎 ADMIN 💎" : "status|admin", "👤 USERS 👤" : "status|users", "« BACK «" : "Home|A"
    },
    "DB" : """📂 DATABASE :\n\n**◍ Database Users :** `{}` 📍\n**◍ Database Chats :** `{}` 📍""",
    "SERVER" : "**◍ Total Space     :** `{}`\n**◍ Used Space     :** `{}({}%)`\n**◍ Free Space      :** `{}`\n**◍ CPU Usage      :** `{}`%"
               "**◍ RAM Usage     :** `{}`%\n**◍ Current Work  :** `{}`\n**◍ Message Id     :** `{}`",
    "USERS" : "Users in Database are.", "NO_DB" : "No dataBASE set Yet 💩", "ADMIN" : "**Total ADMIN:** __{}__\n",
    "BACK" : { "« BACK «" : "status|home" }, "HOME" : "`Now, select any option below to get current STATUS 💱.. `",
}

feedbackMsg = f"IF YOU ❤ THIS BOT, JOIN OUR [UPDATE CHANNEL]({settings.OWNED_CHANNEL}) TO STAY INFORMED.\n\n[Write a FEEDBACK 📋]({settings.FEEDBACK})"

# BANNED USER UI
BAN = {
    "UCantUse" : """Hey {}\n\nFOR SOME REASON YOU CANT USE THIS BOT :(""",
    "UCantUseDB" : """Hey {}\n\nFOR SOME REASON YOU CANT USE THIS BOT :(\n\nREASON: {}""",
    "GroupCantUse" : """{} NEVER EXPECT A GOOD RESPONSE FROM ME\n\nADMINS RESTRICTED ME FROM WORKING HERE.. 🤭""",
    "GroupCantUseDB" : """{} NEVER EXPECT A GOOD RESPONSE FROM ME\n\nADMINS RESTRICTED ME FROM WORKING HERE.. 🤭\n\nREASON: {}""",
    "cbNotU" : "Oops, Sorry to break your heart, this message is not for you 💔.\n\nBetter luck next time! 😏",
    "Fool" : "Please don't try to fool me.. 🤭",
    "banCB" : {
        "Create your Own Bot": f"{settings.SOURCE_CODE}", "Tutorial": f"{settings.SOURCE_CODE}", "Update Channel": "https://telegram.dog/ilovepdf_bot"
    },
    "Force" : """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only **Channel Members** Can Use this Bot 🚶

This Means That You Need To **Join** The Below Mentioned Channel for Using Me!

Hit on `"♻️retry♻️"` after joining.. 😅""",
    "ForceCB" : { "🌟 JOIN CHANNEL 🌟" : "{0}", "♻️ Refresh ♻️" : "refresh{1}" },
}

PDF_MESSAGE = {
    "pg" : "`Number of Pages: •{}•` 🌟", "pdf" : "`What should I do with this file.?`\n\nFile Name : `{}`\nFile Size : `{}`",
    "pdf_button" : {
        "⭐ META£ATA ⭐" : "pdf|meta", "🖼️ IMAGES 🖼️" : "pdf|img", "📑 TEXT 📑" : "pdf|txt", "🤸 ROTATE 🤸" : "pdf|rotate",
        "✂️ SPLIT/MERGE 🧬" : "pdf|trim", "🔐 ENCRY\DECRY 🔓" : "pdf|lock", "😗 FORMAT 😗" : "pdf|format",
        "💦 WATERMARK 💦" : "pdf|trade", "🗜 COMPRESS\OCR 🗜" : "pdf|comocr", "✏️ RENAME ✏️" : "#rename", "🔎 ZOOM 🔎" : "#zoom",
        "🔗 URL 🔗" : "link", "👻 FILTER 👻" : "pdf|filter", "🟢 ADD/DLT 🔴" : "pdf|addlt", "🚫 CLOSE 🚫" : "close|all"
    },
    "error" : "__I can't do anything with this file.__ 😏\n\n🐉  `CODEC ERROR`  🐉",
    "errorCB" : { "❌ ERROR IN CODEC ❌" : "error", "🔸 CLOSE 🔸" : "close|all" },
    "encrypt" : "`FILE IS ENCRYPTED` 🔐\n\nFile Name: `{}`\nFile Size: `{}`",
    "encryptCB" : { "🔓 DECRYPT 🔓" : "#decrypt", "🚫 CLOSE 🚫" : "close|all" }
}

BUTTONS = {
    "meta" : { "❓ META£ATA:HELP ❓" : "nabilanavab|meta", "✔ ONLY METADATA ✔" : "#metadata", "✅ Fetch 10 Random Images ✅" : "#preview", "« BACK «" : "pdf" },
    "lock" : { "❓ ENCRYPT/DECRYPT:HELP ❓" : "nabilanavab|lock", "🔐 ENCRYPT 🔐" : "#encrypt", "🔓 DECRYPT 🔓" : "#decrypt", "« BACK «" : "pdf" },
    "trim" : { "❓ SPLIT/MERGE PDF:HELP ❓" : "nabilanavab|trim", "✂️ SPLIT ✂️" : "#split", "🧬 MERGE 🧬" : "#merge", "« BACK «" : "pdf" },
    "format" : { "❓ FORMAT:HELP ❓" : "nabilanavab|format", "☝️ SINGLE ☝️" : "#1-format", "✌ DOUBLE [HORIZ] ✌" : "#2-format-H",
                 "✌ DOUBLE [VERTI] ✌" : "#2-format-V", "🤟 TRIBLE [HORIZ] 🤟" : "#3-format-H", "🤟 TRIBLE [VERTI] 🤟" : "#3-format-V",
                "😂 FOURBLE 😂" : "#4-format", "« BACK «" : "pdf" },
    "comocr" : { "❓ COMPRESS/OCR PDF:HELP ❓" : "nabilanavab|comocr", "🗜 COMPRESS 🗜" : "#compress", "📝 OCR 📝" : "#ocr", "« BACK «" : "pdf" },
    "trade" : { "❓ WATERMARK:HELP ❓" : "nabilanavab|trade", "💦 WATERMARK 💦" : "pdf|wa", "™️ STAMP ™️" : "pdf|stp", "« BACK «" : "pdf" },
    "filter" : { "❓ FILTER:HELP ❓" : "nabilanavab|format", "🎨 DRAW 🎨" : "#draw", "⚫ BLACK/WHITE ⚪" : "#baw", "🪐 SATURARE 🪐" : "#sat", "« BACK «" : "pdf" },
    "addlt" : { "❓ ADD/DELETE PAGES:HELP ❓" : "nabilanavab|format", "🟢 ADD PAGES 🟢" : "close|dev", "🔴 DELETE PAGES 🔴" : "#deletePg", "« BACK «" : "pdf" },
    "toImage" : { "⚙️ PDF » IMAGES ↓" : "nabilanavab", "🖼 IMG 🖼" : "pdf|img|img", "📂 DOC 📂" : "pdf|img|doc",
        "🤐 ZIP 🤐" : "pdf|img|zip", "🎯 TAR 🎯" : "pdf|img|tar", "« BACK «" : "pdf" },
    "imgRange" : { "⚙️ PDF » IMAGES » {} ↓" : "nabilanavab", "🙄 ALL 🙄" : "#p2img|{}A", "🤧 CUSTOM 🤧" : "#p2img|{}C", "« BACK «" : "pdf|img" },
    "rotate" : { "⚙️ PDF » ROTATE ↓" : "nabilanavab", "90°" : "#rot90", "180°" : "#rot180", "270°" : "#rot270", "360°" : "#rot360", "« BACK «" : "pdf" },
    "txt" : { "⚙️ PDF » TXT ↓" : "nabilanavab", "📜 MESSAGE 📜" : "#textM", "🧾 TXT FILE 🧾" : "#textT",
        "🌐 HTML 🌐" : "#textH", "🎀 JSON 🎀" : "#textJ", "« BACK «" : "pdf" },
    "type" : { "⚙️ PDF » WATERMARK ↓" : "nabilanavab", "💬 TEXT 💬" : "pdf|wa|txt", "🖼 IMAGE 🖼" : "pdf|wa|img",
              "📎 PDF 📎" : "pdf|wa|pdf", "« BACK «" : "pdf|trade" },
    "op" : {
        "⚙️ PDF » WATERMARK » {} » OPCACiTY ↓" : "nabilanavab",
        "𝟙𝟘" : "pdf|wa|{}|o01", "𝟚𝟘" : "pdf|wa|{}|o02", "𝟛𝟘" : "pdf|wa|{}|o03", "𝟜𝟘" : "pdf|wa|{}|o04", "𝟝𝟘" : "pdf|wa|{}|o05",
        "𝟞𝟘" : "pdf|wa|{}|o06", "𝟟𝟘" : "pdf|wa|{}|o07", "𝟠𝟘" : "pdf|wa|{}|o08", "𝟡𝟘" : "pdf|wa|{}|o09", "𝟙𝟘𝟘" : "pdf|wa|{}|o10", "« BACK «" : "pdf|wa"
    },
    "po" : {
        "⚙️ PDF » WATERMARK » POSiTiON ↓" : "nabilanavab",
        "⬆️ ToP ⬆️" : "wa|{0}|{1}|pT", "↔️ MiDDLE ↔️" : "wa|{0}|{1}|pM", "⬇️ BoTToM ⬇️" : "wa|{0}|{1}|pB", "« BACK «" : "pdf|wa|{0}"
    },
    "poTXT" : {
        "⚙️ PDF » WATERMARK » POSiTiON ↓" : "nabilanavab",
        "⬆️ ToP ⬆️" : "pdf|wa|{0}|{1}|pT", "↔️ MiDDLE ↔️" : "pdf|wa|{0}|{1}|pM", "⬇️ BoTToM ⬇️" : "pdf|wa|{0}|{1}|pB", "« BACK «" : "pdf|wa|{0}"
    },
    "color" : {
        "⚙️ PDF » WATERMARK » CoLoR ↓" : "nabilanavab",
        "᠎᠎᠎⚪️" : "#wa|{0}|{1}|{2}|W", "᠎⚫️" : "#wa|{0}|{1}|{2}|B", "᠎᠎🟤" : "#wa|{0}|{1}|{2}|C",  "᠎🔴" : "#wa|{0}|{1}|{2}|R", "᠎᠎🟢" : "#wa|{0}|{1}|{2}|G",
        "🔵" : "#wa|{0}|{1}|{2}|N", "᠎᠎🟡" : "#wa|{0}|{1}|{2}|Y", "᠎᠎🟠" : "#wa|{0}|{1}|{2}|O", "🟣" : "#wa|{0}|{1}|{2}|V", "« BACK «" : "pdf|wa|{0}|{1}"
    },
    "stamp" : {
        "⚙️ PDF » STAMP ↓" : "nabilanavab", "Not For Public Release 🤧" : "pdf|stp|10", "For Public Release 🥱" : "pdf|stp|8",
        "Confidential 🤫" : "pdf|stp|2", "Departmental 🤝" : "pdf|stp|3", "Experimental 🔬" : "pdf|stp|4", "Expired 🐀" : "pdf|stp|5",
        "Final 🔧" : "pdf|stp|6", "For Comment 🗯️" : "pdf|stp|7", "Not Approved 😒" : "pdf|stp|9", "Approved 🥳" : "pdf|stp|0",
        "Sold ✊" : "pdf|stp|11", "Top Secret 😷" : "pdf|stp|12", "Draft 👀" : "pdf|stp|13", "AsIs 🤏" : "pdf|stp|1", "« BACK «" : "pdf|trade"
    },
    "stampA" : {
        "⚙️ PDF » STAMP » COLOR ↓" : "nabilanavab", "Red ❤️" : "#spP|{}|r", "Blue 💙" : "#spP|{}|b", "Green 💚" : "#spP|{}|g", "Yellow 💛" : "#spP|{}|c1",
        "Pink 💜" : "#spP|{}|c2", "Hue 💚" : "#spP|{}|c3", "White 🤍" : "#spP|{}|c4", "Black 🖤" : "#spP|{}|c5", "« Back «" : "pdf|stp"
    }
}

PROGRESS = {
    "progress" : """\n**Done ✅ : **{0}/{1}\n**Speed 🚀:** {2}/s\n**Estimated Time ⏳:** {3}""",
    "upFileCB" : {"📤 .. UPLOADING.. 📤" : "nabilanavab"},
    "cbPRO_D" : ["📤 DOWNLOAD: {:.2f}% 📤", "🎯 CANCEL 🎯"],
    "cbPRO_U" : ["📤 UPLOADED: {:.2f}% 📤", "🎯 CANCEL 🎯"]
}

GENERATE = {
    "noQueue" : "`No Queue found..`😲", "noImages" : "No image found.!! 😒", "currDL" : "Downloaded {} Images 🥱", "geting" : "File Name: `{}`\nPages: `{}`",
    "getFileNm" : "Now Send Me a File Name 😒: ", "deleteQueue" : "`Queue deleted Successfully..`🤧", "getingCB" : {"📚 GENERATING PDF.." : "nabilanavab"},
}

DOCUMENT = {
    "replyCB" : { "😏 ALL IN ONE 😏" : "aio" , "😎 SINGLE USE 😎" : "pdf", "🚶‍♂️ CLOSE 🚶‍♂️" : "close|all" }, "_replyCB" : PDF_MESSAGE['pdf_button'],
    "reply" : PDF_MESSAGE['pdf'], "upFile" : "`Started Uploading..`📤", "process" : "⚙️ Processing..", "inWork" : "WORK IN PROGRESS.. 🙇",
    "download" : "`Downloading your file..` 📥", "refresh" : { "♻️ Refresh ♻️" : "{}" }, "dlImage" : "`Downloading your Image..⏳`",
    "takeTime" : """```⚙️ Work in Progress..\nIt might take some time..```💛""", "fromFile" : "`Converted: {} to {}`",
    "unsupport" : "Unsupported file..🙄`", "cancelCB" : { "⟨ Cancel ⟩" : "close|me" }, "generate" : { "GENERATE 📚" : "generate" },
    "generateRN" : { "GENERATE 📚" : "generate", "RENAME ✍️" : "generateREN" }, "setHdImg" : """Now Image To PDF is in HD mode 😈""",
    "noAPI" : """`Please add convert API.. 💩\n\nstart » settings » api » add/change`""", "error" : """SOMETHING went WRONG.. 🐉\n\nERROR: `{}`""",
    "setDefault" : { "« Back to Default Quality «" : "close|hd" }, "useDOCKER" : "`File Not Supported, deploy bot using docker`",
    "big" : """Due to Overload, Owner limits {}mb for pdf files 🙇\n\n`please Send me a file less than {}mb Size` 🙃""",
    "bigCB" : { "💎 Create 2Gb Support Bot 💎" : "https://github.com/nabilanavab/ilovepdf" },
    "imageAdded" : """`Added {} pages to your PDF..`🤓\n\nfileName: `{}.pdf`"""
}

AIO = {
    "aio" : "Does the PDF file require a password to open ?🤔💭\n\nFile Name : `{}`\nFile Size : `{}`",
    "aio_button" : {"❓ INPUT FILE:HELP ❓":"nabilanavab|aioInput","🔐 ENCRYPTED 🔐":"aioInput|enc","🔓 DECRYPTED 🔓":"aioInput|dec","⏭ MOVE ⏭":"aioInput|dec" }
    "waitPASS" : { "Now send Password.. 😪" : "nabilanavab|aioInput" },
    "passMSG" : "Does the PDF file require a password to open ?🤔💭\n\nFile Name : `{}`\nFile Size : `{}`\n\nPassword: ||{}||",
    "out_button" : {"efc" : "fvdc", "cefre" : "Fdcdfv", "ERfcer" : "FVDFV"}
}

gDOCUMENT = {
    "admin" : """Due to Some Telegram Limits..\n\nI can only work as an admin\n__Please promote me as admin__ ☺️""",
    "notDOC" : "Broh Please Reply to a Document or an Image..🤧",
    "Gadmin" : """Only Group Admins Can Use This Bot\nElse Come to my Pm 😋""",
    "adminO" : """`Only admins can do it..`\n\nOr try on your pdfs(__reply to your message__)"""
}
gDOCUMENT.update(DOCUMENT)

noHelp = f"`No one gonna help you` 😏"

pdf2TXT = {
    "upload" : DOCUMENT['upFile'], "exit" : "`Process Cancelled..` 😏", "nothing" : "Nothing to create.. 😏", "TEXT" : "`Create PDF From Text Messages »`",
    "start" : "Started Converting txt to Pdf..🎉",
    "font_btn" : {
        "TXT@PDF » SET FONT" : "nabilanavab", "Times" : "pdf|font|t", "Courier" : "pdf|font|c", "Helvetica (Default)" : "pdf|font|h",
        "Symbol" : "pdf|font|s", "Zapfdingbats" : "pdf|font|z", "🚫 CLOSE 🚫" : "close|me"
    },
    "size_btn" : {
        "TXT@PDF » {} » SET SCALE" : "nabilanavab", "Portarate" : "t2p|{}|p", "Landscape" : "t2p|{}|l", "« Back «": "pdf|T2P"
    },
    "askT" : """__TEXT TO PDF » Now, please enter a TITLE:__\n\n/exit __to cancel__\n/skip __to skip__""",
    "askC" : """__TEXT TO PDF » Now, please enter paragraph {}:__\n\n/exit __to cancel__\n/create __to create__"""
}

URL = {
    "notPDF" : "`Not a PDF File", "close" : { "close" : "close|all" }, "get" : {"🧭 Get PDF File 🧭" : "getFile"},
    "error" : """🐉 SOMETHING WENT WRONG 🐉,\n\nERROR: `{}`\n\nNB: In Groups, Bots Can Only fetch documents Send After Joining Group =)""",
    "done" : "```Almost Done.. ✅\nNow, Started Uploading.. 📤```", "_error_" : "send me any url or direct telegram pdf links",
    "openCB" : {"Open In Browser" : "{}"}, "_error" : "`Some Thing Went Wrong =(`\n\n`{}`",
    "_get" : """[Open Chat]({})\n\n**ABOUT CHAT ↓**\nChat Type   : {}\nChat Name : {}\nChat Usr    : @{}\nChat ID        : {}\nDate : {}
\n**ABOUT MEDIA ↓**\nMedia       : {}\nFile Name : {}\nFile Size   : {}\nFile Type : {}"""
}

getFILE = {
    "wait" : "Wait.. Let me.. 😜", "inWork" : DOCUMENT['inWork'], "big" : "Send PDF url less than {}mb", "dl" : {"📥 ..DOWNLOADING.. 📥" : "nabilanavab"},
    "up" : {"📤 ..UPLOADING..  📤" : "nabilanavab"}, "complete" : {"😎 COMPLETED 😎" : f"{str(settings.SOURCE_CODE)}"}
}

cbAns = [
    "This feature is Under Development ⛷️", "Error annenn paranjille.. then what.. 😏", "Process Canceled.. 😏",
    "File Not Encrypted.. 👀", "Nothing Official About it.. 😅", "🎉 Completed.. 🏃"
]

inline_query = {"capt" : "SET LANGUAGE ⚙️", "des" : "By: @nabilanavab ❤", "TOP" : { "Now, Select Language ⮷" : "nabilanavab" } }

LINK = {
    "gen" : "`🔗 Generating..`", "no" : "Unfortunately, we encountered an error 😓", "notify" : "Get Notify when a someone fetch this pdf",
    "_gen" : """```🔗 Generating..\nWe're working on it!\n\nPlease allow a moment for the processing to complete.```""",
    "type" : """`🔗 Generating..`\n\n**Public** 📢:\n__The file accessed via this link will be publicly available, allowing anyone to save and forward it__.
\n\n**Protect** 🔐:\n__Ensures the confidentiality of the message by preventing its forwarding and saving__.""",
    "notify_pvt" : { "🔔 NOTIFY 🔔" : "link-pvt-ntf", "🔕 MUTE 🔕" : "link-pvt-mut"},
    "notify_pub" : { "🔔 NOTIFY 🔔" : "link-pbc-ntf", "🔕 MUTE 🔕" : "link-pbc-mut"},
    "typeBTN" : { "📢 PUBLIC 📢" : "link-pub", "🔐 PRIVATE 🔐" : "link-pvt" },
    "link" : "**Here it is! This is what you were searching for..**", "error" : "Oops, it looks like something went wrong. Please try again later.\n\n`ERROR:` {}"
}

INDEX = {
    "rot360" : "You have some big problem..🙂", "ocrError" : "Owner Restricted 😎🤏", "notEncrypt": "File Not Encrypted.. 👀",
    "largeNo" : "It contains too many pages, send me a pdf fewer than 5 pages 😐", "inWork" : "WORK IN PROGRESS.. 🙇", "process" : "🚨 processing..",
    "pyromodASK_1" : "_PDF {} »\nNow, please enter the PASSWORD :__\n\n/exit __to cancel__",   # encrypt, decrypt
    "pyromodASK_2" : "Enter PDF new Name:\n\n/exit to cancel", "pyromodASK_3" : "__MERGE pdfs » Total PDFs in queue: {}\n\n/exit to cancel\n/merge to merge__",
    "download" : "`Downloading your file..` 📥", "button" : { "⟨ Cancel ⟩" : "close|me" }, "error" : "error: {} ",
    "decrypt_error" : "Sorry, this password is invalid for decrypting the PDF file",
    "completed" : "`Downloading Completed..` ✅\n\n```Started Processing\nIt might take some time..``` 🙇📝",
    "upload" : "`Started Uploading..` 📤", "encrypt_caption" : "__Page Number__: {}\n__key__ 🔐: ||{}||",
    "rename_caption" : "old name: `{}`\new name: `{}`", "exit" : "Your request is about to be canceled 😏",
    "askImage" : "Please enter the PDF page syntax that you would like to use,\n\nSyntax:\n\t"
                 "Range of page: `[start, end]`,\n\tSpecific page: `separated by commas`.\n\nExample: `1,3,5,12:19`",
    "pdfToImgError" : "`Invalid syntax for page number`\n`NB: Pdf only have {} pages` ⭐."
                      "\n\nPlease enter a valid syntax for the page number,\nsuch as `[start:end]` or `[page_numbers]`.",
    "_total" : "`Total pages: {}..⏳`", "_canceledAT" : "`Canceled at {}/{} pages..` 🙄", "_upload" : "`Uploading: {}/{} pages.. 🐬`",
    "_cancelCB" : {"💤 CANCEL 💤" : "close|P2I"}, "_canceledCB" : {"🍄 CANCELLED 🍄" : "close|P2IDONE"}, "_completed" : {"😎 COMPLETED 😎" : "close|P2ICOMP"},
    "finished" : "Your current task has been completed successfully. 😎", "cancelCB" : "⚙️ okDA, Canceling.. ",
    "sizeLoad" : "`Due to Overload Bot Only Support %sMb PDFs..", "mergeDl" : "`Downloadeding {}`", "merge" : "`started merging {} pdfs`",
    "watermark_txt" : "__Now, Send me a Text Message__\n\n/exit : to cancel", "watermark_pdf" : "__Send me the watermark pdf.__\n\n/exit : to cancel",
    "watermark_img" : "__Send me the watermark Image as file__\n__ Supported Files [png, jpeg, jpg]__\n\n/exit : to cancel",
    "adding_wa" : "Adding Watermark to PDF File 😎", "readAgain" : "please read this message again.. 🥴😲", "zipTAR" : "`converted {}/{}` 😎",
}

HELP = {
    "meta" : "⭐ META£ATA ⭐\n\n✔ ONLY METADATA ✔ : will help you fetch metadata from a PDF file.\n\n✅ Fetch 10 Random Images ✅ : will allow you to extract 10 random images from the PDF file if they exist.",
    
}
