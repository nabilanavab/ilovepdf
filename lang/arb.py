# copyright ©️ 2021 nabilanavab
file_name = "lang/arb.py"

from configs.config   import settings

#
RESTART = {
     "msg": "☠`بسبب التحميل الزائد ، يتم إعادة تشغيل الخادم \n \n لقد لاحظت أن عملك كان أيضًا في قائمة الانتظار \n\n هل يمكنك من فضلك المحاولة مرة أخرى ..! ",
     "btn": {"🚶 يغلق 🚶" : "close|mee"}
}

#
HOME = {
    "HomeA" : "مرحبًا {} .. !! \n مرحبًا بك في {}.! \n\n"
"باستخدام هذه الأداة ، يمكنك بسهولة تحويل الصور إلى PDF وضغط ملفات PDF وتقسيم ملفات PDF ودمجها وتشفيرها أو فك تشفيرها وتدوير صفحات PDF وغير ذلك الكثير. \n\n"
"ما عليك سوى إرسال ملف PDF / IMAGE لي وسيقوم بتنفيذ الإجراء المطلوب. للحصول على المساعدة ، حدد '⚠️ يساعد ⚠️' في أي وقت. برنامج PDF bot هنا لتسهيل حياتك .. \ n \ n"
"جربه الآن وشاهد كيف يمكن أن يساعدك في تلبية جميع احتياجات PDF الخاصة بك!",
    "HomeACB" : {
        "⚙️ إعدادات ⚙️" : "Home|B", "🌍 لغة 🌍" : "set|lang", "⚠️ يساعد ⚠️" : "Home|C",
        "📢 قناة 📢" : f"{str(settings.OWNED_CHANNEL)}", "🌟 مصدر الرمز 🌟" : f"{str(settings.SOURCE_CODE)}",
        "➕ أضف في المجموعة ➕" : "https://t.me/{}?startgroup=True"
    },
    "HomeAdminCB" : {
        "⚙️ إعدادات ⚙️" : "Home|B", "🌍 لغة 🌍" : "set|lang", "⚠️ يساعد ⚠️" : "Home|C",
        "📢 قناة 📢" : f"{str(settings.OWNED_CHANNEL)}", "🌟 مصدر الرمز 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 حالة 🗽" : f"status|home", "➕ أضف في المجموعة ➕" : "https://t.me/{}?startgroup=True", "🚶 يغلق 🚶" : "close|mee"
    },
    "HomeB" : "صفحة الإعدادات ⚙️\n\nاسم المستخدم   : {}\nمعرف المستخدم           : {}\nاسم المستخدم    : {}\nتاريخ الانضمام      : {}\n\Nلغة    : {}\n"
        "API                    : {}\nإبهام            : {}\nالتسمية التوضيحية        : {}\nاسم الملف      : {}""",
    "HomeBCB" : {
        "إبهام" : "set|thumb", "اسم" : "set|fname", "API" : "set|api", "التسمية التوضيحية" : "set|capt", "« العودة إلى المنزل «" : "Home|B2A"
    },
    "HomeC" : """**بعض الميزات الرئيسية هي:**
 
 ◍ ```قم بإنشاء ملف PDF من صورك: ما عليك سوى إرساله بتنسيق bot pms [png ، jpg ، jpeg]```
 ◍ ```استخراج النص من ملف PDF: يساعد في استخراج النص من ملف PDF وإرساله كرسالة منفصلة.```
 ◍ ```تحويل PDF إلى تنسيق ملف آخر: [الصور ، txt ، html ، json ، tar ، rar]```
 ◍ ```دمج ملفات PDF متعددة في ملف واحد: ملفات PDF متعددة لدمجها في ملف واحد```
 ◍ ```تقسيم ملف PDF إلى صفحات منفصلة: ملف PDF كبير لتقسيمه إلى صفحات منفصلة```
 ◍ ```استخراج الصور من ملف PDF: [all، range، pages] as image، doc، zip، rar```
 ◍ ```يساعد على تقليل الحجم عن طريق تحسين الصور. مفيد في إرسال الملف عبر البريد الإلكتروني عندما يكون كبيرًا جدًا```
 ◍ ```جلب البيانات الوصفية: عنوان الوثيقة ، المؤلف ، الموضوع ، الكلمات الأساسية المرتبطة بالمستند ، وتواريخ الإنشاء والتعديل```
 ◍ ```تشفير / فك تشفير ملفات PDF باستخدام كلمات المرور ومواقع الويب إلى ملف PDF وتدوير وإعادة تسمية وختم```
 ◍ ```WaterMark ، Combine ، Zoom ، Draw ، Add / Delete Pages ، Ocr pdf..```
 ◍ ```رسائل نصية إلى ملفات pdf ، وأكثر من ذلك بكثير 😎```""",
    "HomeCCB" : {
        "« العودة إلى المنزل «" : "Home|A",
        "⚠️ تعليمات ⚠️" : "Home|D"
    },
    "HomeD" : """كما تعلم ، هذه خدمة مجانية ، لا يمكنني ضمان المدة التي يمكنني خلالها الحفاظ على هذه الخدمة ..`😝
 
⚠️ تعليمات ⚠️:
  ◍ ``` يرجى ملاحظة أنه لا يتم التسامح مع البريد العشوائي بشكل عام ويمكن أن يؤدي إلى حظر المستخدم أو الروبوت من الخدمة```
  ◍ ``` انتظر حتى يقوم الروبوت بمعالجة الملف: سيقوم الروبوت بمعالجة ملف PDF وتنفيذ الإجراء المطلوب. قد يستغرق هذا بضع دقائق ، اعتمادًا على حجم الملف ومدى تعقيد الإجراء الذي يتم تنفيذه.```
  ◍ ``` بمجرد أن يكمل الروبوت الإجراء ، سيرسل لك النتائج. إذا كان الإجراء ناجحًا ، فستتلقى الإخراج. إذا لم ينجح الإجراء ، فسيخبرك الروبوت ويقدم لك أي رسائل خطأ ذات صلة. ```
  ◍ ``` سيتم حظر أي مستخدم يثبت أنه يقوم بتوزيع أو مشاركة محتوى إباحي على الروبوت بشكل دائم ```
** أرسل أي صورة لتبدأ: ** 😁 """,
    "HomeDCB" : { "⚠️ يساعد ⚠️" : "Home|C", "» العودة إلى المنزل »" : "Home|A" }
}

# GROUP WELCOME MESSAGE
HomeG = {
    "HomeA" : HOME['HomeA'],
    "HomeACB" : {
        "🌍 لغة 🌍" : "set|lang", "🛡️ يساعد 🛡️": "Home|C", "📢 قناة 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 مصدر الرمز 🌟": f"{settings.SOURCE_CODE}", "🚶 يغلق 🚶" : "close|mee",
    }
}

SETTINGS = {
    "lang" : "الآن حدد أي لغة..", "default" : ["تقصير ❌", "مخصص ✅"], "cant" : "لا يمكن استخدام هذه الميزة ❌",
    "wait" : { "منتظر.. 🥱" : "nabilanavab" }, "feedbtn" : { "أبلغ عن أي أخطاء تجدها!" : settings.REPORT },
    "chgLang" : {" إعدادات ⚙️ » تغيير اللغة 🌐" : "nabilanavab"}, "askApi" : "\n\n افتح الرابط ** أدناه ** وأرسل لي الرمز السري:",
    "waitApi" : { "Open link ✅" : "https://www.convertapi.com/a/signin" }, "error" : "Something went wrong while retrieving data from the database",
    "result" : ["Settings cannot be updated ❌", "Settings Updated Successfully ✅"],
    "back" : [{ "« BACK TO HOME «" : "Home|B2S" }, { "« BACK TO HOME «" : "Home|B2A" }],
    "feedback" : "Bug warning! If my texts sound weird, it's probably Google Translate's fault."
                 "\n\nReport a BUG in {} Lang:\n`• Specify Lang\n• Error Message\n• New Message`",
    "ask" : [
        "الآن أرسل لي..",
        "الآن ، أرسل لي .. 😅 \n\n سريع.! ليس لدي المزيد من الوقت لاستعراض النص .. 😏 \n\n/cancel إلغاء: "
    ],
    "thumb" : [
        {"إعدادات ⚙️» ظفري 📷 ":"nabilanavab"," ♻ يضيف ♻ ":"set|thumb+"," « العودة إلى المنزل « ":"Home|B"},
        {"إعدادات ⚙️» ظفري 📷 ":"nabilanavab"," ♻ يتغيرون ♻ ":"set|thumb+"," DELETE 🗑 ":"set|thumb-"," ««العودة إلى الصفحة الرئيسية« ":"Home|B2S"}
    ],
    "fname": [
        {"إعدادات ⚙️» اسم الملف 📷 ":"nabilanavab"," ♻ يضيف ♻ ":"set|fname+"," « العودة إلى المنزل « ":"Home|B2S"},
        {"إعدادات ⚙️» اسم الملف 📷 ":"nabilanavab"," ♻ يتغيرون ♻ ":"set|fname+"," DELETE 🗑 ":"set|fname-"," «العودة إلى الصفحة الرئيسية« ":"Home|B2S"}
    ] ,
    "api": [
        {"إعدادات ⚙️» API 📷 ​​":"nabilanavab"," ♻ يضيف ♻ ":"set|api+"," « العودة إلى المنزل « ":"Home|B2S"},
        {"إعدادات ⚙️» API 📷 ​​":"nabilanavab"," ♻ يتغيرون ♻ ":"set|api+"," 🗑 DELETE 🗑 ":"set|api-"," «العودة إلى الصفحة الرئيسية« ":"Home|B2S"}
    ] ,
    "capt": [
        {"الإعداد ⚙️» التسمية التوضيحية 📷":"nabilanavab"," ♻ يضيف ♻ ":"set|capt+","« العودة إلى المنزل «":"Home|B2S"},
        {"الإعداد ⚙️» التسمية التوضيحية 📷":"nabilanavab"," ♻ يتغيرون ♻ ":"set|capt+"," DELETE 🗑 ":"set|capt-","«العودة إلى الصفحة الرئيسية« ":"Home|B2S"}
    ]
}

BOT_COMMAND = {"start": "رسالة ترحيب ..", "txt2pdf": "إنشاء ملف PDF نصي"}

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

feedbackMsg = f"إذا كنت ❤ هذا الروبوت ، انضم إلى [تحديث القناة]({settings.OWNED_CHANNEL}) لتبقى على اطلاع. \n\n [اكتب تعليقًا 📋]({settings.FEEDBACK})"

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
    "Force" : """Wait [{}](tg://user?id={})..!!\n\nDue To The Huge Traffic Only **Channel Members** Can Use this Bot 🚶
\nThis Means That You Need To **Join** The Below Mentioned Channel for Using Me!\n\nHit on `"♻️retry♻️"` after joining.. 😅""",
    "ForceCB" : { "🌟 JOIN CHANNEL 🌟" : "{0}", "♻️ Refresh ♻️" : "refresh{1}" },
}

PDF_MESSAGE = {
    "pg" : "`Number of Pages: •{}•` 🌟", "pdf" : "`What should I do with this file.?`\n\nFile Name : `{}`\nFile Size : `{}`",
    "pdf_button" : {
        "⭐ META£ATA ⭐" : "pdf|meta", "🖼️ IMAGES 🖼️" : "pdf|img", "📑 TEXT 📑" : "pdf|txt", "🤸 ROTATE 🤸" : "pdf|rotate",
        "✂️ SPLIT/MERGE 🧬" : "pdf|trim", "🔐 ENCRY/DECRY 🔓" : "pdf|lock", "😗 FORMAT 😗" : "pdf|format",
        "💦 WATERMARK 💦" : "pdf|trade", "🗜 COMPRESS/OCR 🔎" : "pdf|comocr", "✏️ RENAME ✏️" : "#rename", "🔎 ZOOM 🔎" : "#zoom",
        "🔗 URL 🔗" : "link", "👻 FILTERS 👻" : "pdf|filter", "🟢 ADD/DLT 🔴" : "pdf|addlt", "🚶‍♂️ CLOSE 🚶‍♂️" : "close|all"
    },
    "error" : "__I can't do anything with this file.__ 😏\n\n🐉  `CODEC ERROR`  🐉",
    "errorCB" : { "❌ ERROR IN CODEC ❌" : "error", "🔸 CLOSE 🔸" : "close|all" },
    "encrypt" : "`FILE IS ENCRYPTED` 🔐\n\nFile Name: `{}`\nFile Size: `{}`",
    "encryptCB" : { "🔓 DECRYPT 🔓" : "#decrypt", "🚶‍♂️ CLOSE 🚶‍♂️" : "close|all" }
}

BUTTONS = {
    "meta" : { "❓ META£ATA:HELP ❓" : "nabilanavab|meta", "✔ ONLY METADATA ✔" : "#metadata", "✅ WITH PREVIEW ✅" : "#preview", "« BACK «" : "pdf" },
    "lock" : { "❓ ENCRYPT/DECRYPT:HELP ❓" : "nabilanavab|lock", "🔐 ENCRYPT 🔐" : "#encrypt", "🔓 DECRYPT 🔓" : "#decrypt", "« BACK «" : "pdf" },
    "trim" : { "❓ SPLIT/MERGE PDF:HELP ❓" : "nabilanavab|trim", "✂️ SPLIT ✂️" : "#split", "🧬 MERGE 🧬" : "#merge", "« BACK «" : "pdf" },
    "format" : { "❓ FORMAT:HELP ❓" : "nabilanavab|format", "☝️ SINGLE ☝️" : "#1-format", "✌ DOUBLE [HORIZ] ✌" : "#2-format-H",
                 "✌ DOUBLE [VERTI] ✌" : "#2-format-V", "🤟 TRIBLE [HORIZ] 🤟" : "#3-format-H", "🤟 TRIBLE [VERTI] 🤟" : "#3-format-V",
                 "😂 FOURBLE 😂" : "#4-format", "« BACK «" : "pdf" },
    "comocr" : { "❓ COMPRESS/OCR PDF:HELP ❓" : "nabilanavab|comocr", "🗜 COMPRESS 🗜" : "#compress", "📝 OCR 📝" : "#ocr", "« BACK «" : "pdf" },
    "trade" : { "❓ WATERMARK:HELP ❓" : "nabilanavab|trade", "💦 WATERMARK 💦" : "pdf|wa", "™️ STAMP ™️" : "pdf|stp", "« BACK «" : "pdf" },
    "filter" : { "❓ FILTER:HELP ❓" : "nabilanavab|format", "🎨 DRAW 🎨" : "#draw", "⚫ BLACK/WHITE ⚪" : "#baw", "🪐 SATURARE 🪐" : "#sat",
                "🖌 INVERT 🖌" : "#inv", "« BACK «" : "pdf" },
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
    "progress" : """\n**Done ✅ : **{0}/{1}\n**Speed 🚀:** {2}/s\n**Estimated Time ⏳:** {3}""", "upFileCB" : {"📤 .. UPLOADING.. 📤" : "nabilanavab"},
    "cbPRO_D" : ["📤 DOWNLOAD: {:.2f}% 📤", "🎯 CANCEL 🎯"], "cbPRO_U" : ["📤 UPLOADED: {:.2f}% 📤", "🎯 CANCEL 🎯"]
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
    "true" : "✅ TRUE ✅", "false" : "🔴 FALSE 🔴", "aio" : "Does the PDF file require a password to open.?🤔💭\n\nFile Name : `{}`\nFile Size : `{}`",
    "aio_button" : {"❓ INPUT FILE:HELP ❓":"nabilanavab|aioInput","✅ YES ✅":"aioInput|enc", "🔴 NO 🔴":"aioInput|dec","⏭ MOVE ⏭":"aioInput|dec" },
    "waitPASS" : "Now send me any text message.. 😪",
    "passMSG" : "`What should I do with this file.?`🤔💭\n\nInput:\n\tFile Name : `{}`\n\tFile Size   : `{}`\n\tPassword : ||•{}•||\n\n"
        "Output:\n\tFile Name   : `•{}•`\n\tWatermark : `•{}•`\n\tPassword    : ||•{}•||",
    "out_button" : { "⭐ META£ATA ⭐" : "nabilanavab|aio|met", "📸 PREVIEW 📸" : "nabilanavab|aio|pre","🗜 COMPRESS 🗜": "nabilanavab|aio|com",
        "📑 TEXT 📑" : "nabilanavab|aio|txt", "🤸 ROTATE 🤸" : "nabilanavab|aio|rot", "😗 FORMAT 😗" : "nabilanavab|aio|for",
        "🔐 ENCRYPT 🔐" : "nabilanavab|aio|enc", "💦 WATERMARK 💦" : "nabilanavab|aio|wat", "✏️ RENAME ✏️" : "nabilanavab|aio|rnm",
        "🚶‍♂️ BACK 🚶‍♂️" : "aio", "🆗 PROCESS 🆗" : "processAIO"
    },
    "out_values": ["aio|met|{F}", "aio|pre|{F}", "aio|com|{F}", "aio|txt|{F}", "aio|rot|{F}", "aio|for|{F}", "aio|enc|{F}", "aio|wat|{F}", "aio|rnm|{F}" ]
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
    "decrypt_error" : "Sorry, this password is invalid for decrypting the PDF file", "cantCompress" : "cant compress more 🙂",
    "completed" : "`Downloading Completed..` ✅\n\n```Started Processing\nIt might take some time..``` 🙇📝",
    "upload" : "`Started Uploading..` 📤", "encrypt_caption" : "__Page Number__: {}\n__key__ 🔐: ||{}||",
    "rename_caption" : "old name: `{}`\nnew name: `{}`", "exit" : "Your request is about to be canceled 😏", "compress_caption" : "Old File Size: `{}`\nNew File size: `{}`\nRatio: `{}`%",
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
    "aio" : "```{} work in progress..🔰\nwait it might take some time.. 💔```",
}

INLINE = {
    "search" : "️♻️ SEARCH ♻️", "openBot" : "😎 Open Bot 😎", 'query' : "{}  Results..",
    'lang_t' : "SET LANGUAGE ⚙️", "lang_d" : "help's to set your comfortable language 😇", "lang_b" : { "Now, Select Language 👇" : "nabilanavab" },
    'sear_t' : "SEARCH PDF 🔍", 'sear_d' : "You can now search through a vast library of PDF documents with ease and convenience. Using the inline search mode, you can simply type in the name of the document that you are looking for",
    'min' : '🔎 Type to searchPDF Files..', 'process' : '⚙️ Processing.. ', 'nothing' : '🤐 No results for "{}"', "select" : "✅ GET PDF ✅",
    'cbNotU' : BAN['cbNotU'], 'old' : "old queue..", 'inWork' : INDEX['inWork'], 'edit' : ["⚔ GET PDF ⚔", "🔎 SEARCH 🔎", "😇 open in bot 😇"],
    'noDB' : 'Admin Restricted 🏃', 'description' : "Author: {}\nVolume: {}   Year: {}  Pages: {}\nLanguage: {}  Extension: {}\nPublisher: {}",
    'caption' : "MD5: {}\nTitle: **{}.**\nAuthor: **{}.**\n\nVolume: {}\nYear: {}\nPages: {}\nLanguage: {}\nPublisher: {}"
}

HELP = {
    "meta" : "⭐ META£ATA ⭐\n\n✔ ONLY METADATA ✔ :\nFetch Metadata from a PDF file.\n\n✅ WITH PREVIEW ✅ :\nFetch 10 random images from PDF",
    "lock" : "🔐 ENCRY/DECRY 🔓/n/n🔐 ENCRYPT 🔐",
    "trim" : "-------------"
}
