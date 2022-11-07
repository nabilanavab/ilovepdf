# LANG: HINDI [UZBEKISTAN 🇺🇿] LANG CODE: HND                       >>  copyright ©️ 2021 nabilanavab  <<                                         fileName : lang/uzb.py
#                                              Thank: nabilanavab                                           E-mail: nabilanavab@gmail.com

from configs.config import settings

# PM WELCOME MESSAGE (HOME A, B, C, D...)
HOME = {
    "HomeA" : """Salom [{}](tg://user?id={})..!!
Ushbu bot sizga PDFar bilan ko'p narsalarni qilishda yordam beradi 🥳

Asosiy xususiyatlardan ba'zilari:\n◍ `Rasmlarni PDFga aylantirish`
◍ `PDFni rasmlarga o'tkazish`\n◍ `Ofis fayllarini PDFga aylantirish`""",
    "HomeACB" : {
        "⚙️ SOZLAMALAR ⚙️" : "Home|B", "⚠️ YORDAM ⚠️" : "Home|C",
        "📢 KANAL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 MANBA KODI 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🚶 YOPISH 🚶" : "close|mee"
    },
    "HomeAdminCB" : {
        "⚙️ SOZLAMALAR ⚙️" : "Home|B", "⚠️ YORDAM ⚠️" : "Home|C",
        "📢 KANAL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 MANBA KODI 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 STATUSI 🗽" : f"status|home", "🚶 YOPISH 🚶" : "close|mee"
    },
    "HomeB" : """SOZLAMALAR ⚙️\n\nFOYDALANUVCHI NOMI   : {}
FOYDALANUVCHI ID           : {}\nUSERNAME    : {}\nQO'SHILGAN SANASI      : {}\n
LANGUAGE    : {}\nAPI                    : {}
ESKIZ            : {}\nMAXSUS NOM         : {}\nFAYL NOMI      : {}""",
    "HomeBCB" : {
        "🌍 TIL 🌍" : "set|lang", "📍 ESKIZ 📍" : "set|thumb",
        "📈 NOMI 📈" : "set|fname", "💩 API 💩" : "set|api",
        "📅 MAXSUS NOM 📅" : "set|capt", "« BOSH SAHIFA «" : "Home|B2A"
    },
    "HomeC" : """🪂 **Yordam XABAR** 🪂:
```
Asosiy xususiyatlardan ba'zilari:
 ◍ Tasvirlarni PDF ga oʻzgartiring\n ◍ PDF qoʻllanmalari\n ◍ Koʻplab mashhur kodeklarni pdf ga aylantiring
 
Pdf faylini o'zgartirish:
 ◍ PDF⥃TASIRLAR [barcha, diapazon, sahifalar]\n ◍ xujjatlardan PDFgacha [png, jpg, jpeg]\n ◍ TASVIRLAR⥃PDF\n ◍ PDF METAMAʼLOV\n ◍ PDF⥃TEXT\n ◍ MATN⥃PDF\n ◍ Pdf faylni siqish
 ◍ PDF NI BOʻLASH [diapazon, sahifalar]\n ◍ PDF-NI BIRGA OLISH\n ◍ SHTAMP QOʻSHING\n ◍ PDF NOMNI Oʻzgartiring\n ◍ PDF-NI AYLANTIRISH\n ◍ PDF FORMATTERI \n ◍ PDF⥃FIJSON/TXT
 ◍ PDF⥃HTML [veb koʻrinishi]\n ◍ URL⥃PDF\n ◍ PDF⥃ZIP/TAR/RAR [barcha, diapazon, sahifalar]\nVa yana koʻp.. ```""",
    "HomeCCB" : {"« BOSH SAHIFA «" : "Home|A", "⚠️ QO'LLANMA ⚠️" : "Home|D"},
    "HomeD" : """`Bu bepul xizmat bo'lgani uchun men bu xizmatni qancha vaqt saqlab turishimga kafolat bera olmayman..`😝
 
⚠️ Ko'rsatmalar ⚠️:
🛈 __Iltimos, bot adminlarini suiiste'mol qilishga urinmang__ 😒
🛈 __Bu yerda spam yubormang, doimiy ravishda taqiqlanishi mumkin 🎲__.
🛈 __ Porno kontent ham sizga DOIMIY BAN beradi 💯__

**Boshlash uchun istalgan rasmni yuboring:** 😁""",
    "HomeDCB" : {"⚠️ YORDAM ⚠️" : "Home|C", "» BOSH SAHIFA »" : "Home|A"}  
}

SETTINGS = {
    "default" : ["STANDART ❌", "MAXSUS ✅"], "chgLang" : {"SOZLAMALAR ⚙️ » TILNI O'ZGARTIRISH 🌐" : "nabilanavab"},
    "error" : "Maʼlumotlar bazasidan maʼlumotlarni olishda nimadir xato ketdi", "lang" : "Endi, xohlagan tilni tanlang...",
    "ask" : ["Endi, Menga yuboring..", "Endi, Menga yuboring... 😅\n\nTez.! Matnni ko'rib chiqishga vaqtim yo'q.. 😏\n\n/bekor qilish: bekor qilish"],
     "askApi" : "\n\nQuyidagi havolani oching va menga maxfiy kodni yuboring:", "waitApi" : {"Havolani ochish ✅" : "https://www.convertapi.com/a/signin"},
    "wait" : {"Kutilmoqda.. 🥱" : "nabilanavab"}, "back" : {"« BOSH SAHIFA «" : "Home|B2S"}, "errorCB" : {"« BOSH SAHIFA «" : "Home|B2A"},
    "result" : ["Sozlamalarni yangilab bo'lmadi ❌", "Sozlamalar muvaffaqqiyatli yangilandi ✅"], "cant" : "Ushbu funksiyadan foydalanib bo'lmaydi ❌",
    "feedback" : "Sizga oʻxshagan Ajoyib mijozlar sharhlari boshqalarga yordam beradi.\n@azik_developer"
                 "\n\nXatolikni xabar berish {} til:\n`• Maxsus til\n• Xato xabar\n• Yangi xabar`",
    "feedbtn" : {"Til xatosi haqida xabar berish" : settings.REPORT},
    "thumb" : [
        {"SOZLAMA ⚙️ » ESKIZ 📷" : "nabilanavab", "♻ QO'SHISH ♻" : "set|thumb+", "« BOSH SAHIFA «" : "Home|B"},
        {"SOZLAMA ⚙️ » ESKIZ 📷" : "nabilanavab", "♻ ALMASHTIRISH ♻" : "set|thumb+", "🗑 O'CHIRISH 🗑" : "set|thumb-", "« BOSH SAHIFA «" : "Home|B2S"}
    ],
    "fname" : [
        {"SOZLAMA ⚙️ » FNAME 📷" : "nabilanavab", "♻ QO'SHISH ♻" : "set|fname+", "« BOSH SAHIFA «" : "Home|B2S"},
        {"SOZLAMA ⚙️ » FNAME 📷" : "nabilanavab", "♻ ALMASHTIRISH ♻" : "set|fname+", "🗑 O'CHIRISH 🗑" : "set|fname-", "« BOSH SAHIFA «" : "Home|B2S"}
    ],
    "api" : [
        {"SOZLAMA ⚙️ » API 📷" : "nabilanavab", "♻ QO'SHISH ♻" : "set|api+", "« BOSH SAHIFA «" : "Home|B2S"},
        {"SOZLAMA ⚙️ » API 📷" : "nabilanavab", "♻ ALMASHTIRISH ♻" : "set|api+", "🗑 O'CHIRISH 🗑" : "set|api-", "« BOSH SAHIFA «" : "Home|B2S"}
    ],
    "capt" : [
        {"SOZLAMA ⚙️ » MAXSUS NOM 📷" : "nabilanavab", "♻ QO'SHISH ♻" : "set|capt+", "« BOSH SAHIFA «" : "Home|B2S"},
        {"SOZLAMA ⚙️ » MAXSUS NOM 📷" : "nabilanavab", "♻ ALMASHTIRISH ♻" : "set|capt+", "🗑 O'CHIRISH 🗑" : "set|capt-", "« BOSH SAHIFA «" : "Home|B2S"}
    ]
}

BOT_COMMAND = {"start" : "Xush kelibsiz xabari..", "txt2pdf" : "Matndan PDF yaratish"}

HELP_CMD = {
    "userHELP" : """[FOYDALANUVCHI BUYRUQLARI XABARI]:\n
/start: Botni ishga tushirish\n/cancel: joriy ishni bekor qilish
/delete: PDF qilayotga\n/txt2pdf: Matndan PDF yaratish""",
    "adminHelp" : """\n\n\n[ADMIN BUYRUQLARI XABARI]:\n
/send: foydalanuvchiga shaxsiy xabar yuborish uchun""",
    "footerHelp" : f"""\n\n\nManba-kodi: [i 💜 PDF]({str(settings.SOURCE_CODE)})
Bot: @azik_pdfbot 💎\n[Qo'llab quvvatlash]({settings.OWNED_CHANNEL})""",
    "CB" : {"⚠️ YOPISH ⚠️" : "close|all"}
}

STATUS_MSG = {
    "HOME" : "`Endi hozirgi holatni olish uchun pastdan istalgan variantni tanlang 💱.. `",
    "_HOME" : {
        "📊 ↓ SERVER ↓ 📊" : "nabilanavab", "📶 XOTIRA 📶" : "status|server",
        "🥥 MA'LUMOTLAR BAZASI 🥥" : "status|db", "🌝 ↓ VRO'YXATNI OLISH ↓ 🌝": "nabilanavab",
        "💎 ADMIN 💎" : "status|admin", "👤 FOYDALANUVCHILAR 👤" : "status|users",
        "« ORQAGA «" : "Home|A"
    },
    "DB" : """📂 MA'LUMOTLAR BAZASI :\n\n**◍ Ma'lumotlar bazasi foydalanuvchilari :** `{}`ta 📍\n**◍ Ma'lumotlar bazasi guruhlari :** `{}`ta 📍""",
    "SERVER" : """**◍ Umumiy xotira     :** `{}`
**◍ Foydalanilgan xotira     :** `{}({}%)`\n**◍ Bo'sh xotira      :** `{}`
**◍ CPU foydalanishi      :** `{}`%\n**◍ RAM foydalanishi     :** `{}`%
**◍ Hozirgi ishlar  :** `{}`ta\n**◍ Xabar IDsi     :** `{}`""",
    "BACK" : {"« ORQAGA «" : "status|home"}, "ADMIN" : "**Total ADMIN:** __{}__\n",
    "USERS" : "Maʼlumotlar bazasida saqlangan foydalanuvchilar:\n\n", "NO_DB" : "Hozircha maʼlumotlar bazasi oʻrnatilmagan 💩"
}

feedbackMsg = f"[Taklif va shikoyat yozish 📋]({settings.FEEDBACK})"

# GROUP WELCOME MESSAGE
HomeG = {
    "HomeA" : """Salom guruhdagilar.! 🖐️\nMen bu yerda yangiman {message.chat.title}\n
O'zimni tanishtirishga ijozat bering..\nMening ismim iLovePDF, men sizga ko'p narsalarni qilishga yordam bera olaman
@Telegram PDF fayllaridagi narsalar\n\nUshbu ajoyib bot uchun @azik_developer ga rahmat 😅""",
    "HomeACB" : {
        "🤠 BOT YARATUVCHISI 🤠": f"https://telegram.dog/{settings.OWNER_USERNAME}",
        "🛡️ YANGILANISH KANALI 🛡": f"{settings.OWNED_CHANNEL}", "🌟 MANBA KODI 🌟": f"{settings.SOURCE_CODE}"
    }
}

# BANNED USER UI
BAN = {
    "cbNotU" : "Xabar siz uchun emas.. 😏",
    "banCB" : {
        "O'z botingizni yarating": f"{settings.SOURCE_CODE}", "Qo'llanma": f"{settings.SOURCE_CODE}",
        "Yangilanish kanali": "https://telegram.dog/azik_projectss"
    },
    "UCantUse" : """Hey {}\n\nBA'ZI SABABLARGA KO'RA SIZ BU BOTDAN FOYDALANA OLMAYSIZ :(""",
    "UCantUseDB" : """Hey {}\n\nBA'ZI SABABLARGA KO'RA SIZ BU BOTDAN FOYDALANA OLMAYSIZ :(\n\nSABABI: {}""",
    "GroupCantUse" : """{} HECH QACHON MENDAN YAXSHI JAVOB KUTMANG\n
ADMINLAR BU YERDA ISHLASHIMNI CHEKLASHDI.. 🤭""",
    "GroupCantUseDB" : """{} HECH QACHON MENDAN YAXSHI JAVOB KUTMANG\n
ADMINLAR BU YERDA ISHLASHIMNI CHEKLASHDI.. 🤭\n\nSABABI: {}""",
    "Force" : """Kuting [{}](tg://user?id={})..!!\n
Katta yuk tufayli bu botdan faqat kanal a'zolari foydalanishi mumkin 🚶\n
Bu Mendan foydalanish uchun quyida ko'rsatilgan kanalga qo'shilishingiz kerakligini bildiradi!\n
Qo‘shilgandan so‘ng “♻️ Qayta urinish♻️” tugmasini bosing.. 😅""",
    "ForceCB" : {"🌟 KANALGA ULANISH 🌟" : "{}", "♻️ Qayta urinish ♻️" : "refresh"},
    "Fool" : "Chiroqni olmangടോ.. 🤭"
}

checkPdf = {
    "pg" : "`Sahifalar soni: •{}•`ta 🌟",
    "pdf" : """`Ushbu faylni nima qilmoqchisiz.?`\n\nFayl Nomi : `{}`\nFayl Hajmi : `{}`""",
    "pdfCB" : {
        "⭐ METADATA ⭐" : "metaData", "🗳️ KO'RIB CHIQISH 🗳️" : "preview",
        "🖼️ RASMGA O'TKAZISH 🖼️" : "pdf|img", "✏️ MATNGA O'TKAZISH ✏️" : "pdf|txt",
        "🔐 SHIFRLAR 🔐" : "work|encrypt", "🔒 SHIFRDAN OCHISH 🔓" : "work|decrypt",
        "🗜️ SIQISH 🗜️" : "work|compress", "🤸 AYLANTIRISH 🤸" : "pdf|rotate",
        "✂️ KESISH ✂️" : "pdf|split", "🧬 BIRLASHTIRISH 🧬" : "merge", "™️ STAMP ™️" : "pdf|stp",
        "✏️ QAYTA NOMLASH ✏️" : "work|rename", "📝 OCR 📝" : "work|ocr",
         "🥷 A4 FORMATGA O'TKAZISH 🥷" : "work|format", "🚫 YOPISH 🚫" : "close|all"
    },
    "error" : """__Men bu fayl bilan hech narsa qilmayman__ 😏\n\n🐉  `KODEK XATOLIGI`  🐉""",
    "errorCB" : {"❌ KODEKDA XATOLIK ❌" : "error", "🔸 YOPISH 🔸" : "close|all"},
    "encrypt" : """`FAYL SHIFRLANGAN` 🔐\n\nFayl Nomi: `{}`\nFayl Hajmi: `{}`""",
    "encryptCB" : {"🔓 SHIFRDAN OCHISH 🔓" : "work|decrypt"}
}

PROGRESS = {
    "progress" : """**\nTugalllandi ✅ : **{0}/{1}\n**Tezligi 🚀:** {2}/s\n**Qolgan vaqt ⏳:** {3}""",
    "dlImage" : "`Rasmingiz yuklab olinmoqda..⏳`", "upFile" : "`Sizga yuborilmoqda..`📤",
    "dlFile" : "`Faylingiz yuklab olinmoqda..` 📥", "upFileCB" : {"📤 .. YUBORILMOQDA.. 📤" : "nabilanavab"},
    "workInP" : "ISHLAB CHIQILMOQDA.. 🙇", "refresh" : {"♻️ Qayta urinish ♻️" : "{}"},
    "takeTime" : """```⚙️ Ish davom etmoqda..`\n`Bu biroz vaqt olishi mumkin..```💛""",
    "cbPRO_D" : ["📤 Yuklab olinmoqda: {:.2f}% 📤", "🎯 BEKOR QILISH 🎯"], "cbPRO_U" : ["📤 YUKLANDI: {:.2f}% 📤", "🎯 BEKOR QILISH 🎯"]
}

GENERATE = {
    "deleteQueue" : "`Navbat muvaffaqqiyatli o'chirildi..`🤧", "noQueue" : "`Navbat topilmadi..`😲",
    "noImages" : "Rasm topilmadi.!! 😒", "getFileNm" : "Endi menga fayl nomini yuboring 😒: ",
    "geting" : "Fayl Nomi: `{}`\nSahifalar: `{}`ta", "getingCB" : {"📚 PDF YARATILMOQDA.." : "nabilanavab"},
    "currDL" : "Yuklab olingan {} rasm 🥱"
}

document = {
    "refresh" : PROGRESS['refresh'], "inWork" : PROGRESS['workInP'], "reply" : checkPdf['pdf'],
    "replyCB" : checkPdf['pdfCB'], "download" : PROGRESS['dlFile'], "process" : "⚙️ Qayta ishlanmoqda..",
    "takeTime" : PROGRESS['takeTime'], "upFile" : PROGRESS['upFile'], "dlImage" : PROGRESS['dlImage'],
    "big" : """Haddan tashqari yuk tufayli, admin pdf fayllar uchun {}mb ni cheklaydi 🙇
\n`Iltimos, menga {}mb hajmidan kichikroq fayl yuboring` 🙃""",
    "bigCB" : {"💎 2 Gb qo'llab-quvvatlash botini yarating 💎" : "https://github.com/nabilanavab/ilovepdf"},
    "imageAdded" : """`Qo'shildi {} sahifa sizning PDFingizga..`🤓\n\nFaylNomi: `{}.pdf`""",
    "setHdImg" : """Endi PDF formatiga tasvir HD rejimida 😈""",
    "setDefault" : {"« Standart sifatga qaytish «" : "close|hd"},
    "error" : """NIMADIR XATO KETDI.. 🐉\n\nXATOLIK: `{}`""",
    "noAPI" : "`Iltimos, aylantirish API'sini qo'shing.. 💩\n\nboshlash » sozlamalar » api » qo'shish/o'zgartirish`",
    "useDOCKER" : "`Fayl qo'llab-quvvatlanmaydi, docker yordamida botni o'rnating`",
    "fromFile" : "`Konvertatsiya qilindi: {} dan {}`ga", "unsupport" : "`Qo'llab quvvatlanmaydigan fayl..🙄`",
    "generateRN" : {"YARATISH 📚" : "generate", "NOM O'ZGARTIRIB YARATISH ✍️" : "generateREN"},
    "generate" : {"YARATISH 📚" : "generate"}, "cancelCB" : {"⟨ Bekor qilish ⟩" : "close|me"}
}

noHelp = f"`hech kim sizga yordam bermaydi` 😏"

split = {
    "inWork" : PROGRESS['workInP'], "cancelCB" : document['cancelCB'],
    "download" : PROGRESS['dlFile'], "exit" : "`Jarayon bekor qilindi..` 😏",
    "button" : {
        "⚙️ PDF » KESISH ↓" : "nabilanavab", "Sahifalar soni bilan 🦞" : "split|R",
        "Yakka sahifalar 🐛" : "split|S", "« ORQAGA «" : "pdf"
    },
    "work" : ["Range", "Single"], "over" : "`5 marta urinish.. Jarayon bekor qilindi..`😏",
    "pyromodASK_1" : """__Pdf kesish » Oraliqda\nEndi, oraliqni kiriting (boshlanish:oxiri) :__
\n/exit __bekor qilish uchun__""",
    "completed" : "`Downloading Completed..` ✅",
    "error_1" : "`Syntaksis Xatolik: FaqatBoshlangichvaoxirgisahifa `🚶",
    "error_2" : "`Syntaksis Xatolik: oxirgiRaqamtogrikiritng `🚶",
    "error_3" : "`Syntaksis Xatolik: birinchiraqamtogrikiriting `🚶",
    "error_4" : "`Syntaksis Xatolik: sahifasoniraqambolishikerak` 🧠",
    "error_5" : "`Syntaksis Xatolik: tushashRaqamiYoq yoki Sonmas` 🚶",
    "error_6" : "`Hech qanday raqam topib bo'lmadi..`😏",
    "error_7" : "`Nimadir xato ketdi..`😅", "error_8" : "`Ushbu {} sondan kichik raqamlar kiriting..`😏",
    "error_9" : "`Birinchi sahifalar sonini tekshiring` 😏", "upload" : "⚙️ `Sizga yuborilmoqda..` 📤"
}

pdf2IMG = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "uploadfile" : split["upload"],
    "toImage" : {
        "⚙️ PDF » RASMGA O'TKAZISH ↓" : "nabilanavab", "🖼 RASM SHAKLDA 🖼" : "pdf|img|img",
        "📂 FAYL SHAKLDA 📂" : "pdf|img|doc", "🤐 ZIP SHAKLDA 🤐" : "pdf|img|zip",
        "🎯 TAR SHAKLDA 🎯" : "pdf|img|tar","« ORQAGA «" : "pdf" 
    },
    "imgRange" : {
        "⚙️ PDF » RASMGA O'TKAZISH » {} ↓" : "nabilanavab", "🙄 HAMMASINI 🙄" : "p2img|{}A",
        "🤧 ORALIQ BILAN 🤧" : "p2img|{}R", "🌝 SAHIFALAR BILAN 🌝" : "p2img|{}S", "« ORQAGA «" : "pdf|img"
    },
    "over" : "`5 marta urinish.. Jarayon bekor qilindi..`😏",
    "pyromodASK_1" : """__Pdf - Rasm›Fayl sifatida » Sahifalar:\nEndi, oraliqni kiriting (boshlanish:oxiri) :__
\n/exit __bekor qilish uchun__""",
    "pyromodASK_2" : """__Pdf - Rasm›Fayl sifatida » Pages:\nEndi, sonlarni vergul bilan kiriting (1,3,5) :__
\n/exit __bekor qilish uchun__""",
    "exit" : "`Process Canceled..` 😏",
    "error_1" : "`Syntaksis Xatolik: FaqatBoshlangichvaoxirgisahifa `🚶",
    "error_2" : "`Syntaksis Xatolik: oxirgiRaqamtogrikiritng `🚶",
    "error_3" : "`Syntaksis Xatolik: birinchiraqamtogrikiriting `🚶",
    "error_4" : "`Syntaksis Xatolik: sahifasoniraqambolishikerak` 🧠",
    "error_5" : "`Syntaksis Xatolik: tushashRaqamiYoq yoki Sonmas` 🚶",
    "error_6" : "`Hech qanday raqam topilmadi..`😏", "error_7" : "`Nimadir xato ketdi..`😅",
    "error_8" : "`PDF da faqatgina {} sahifa mavjud` 💩", "error_9" : "`birinchi sahifalar sonini tekshiring` 😏",
    "error_10" : "__Ba'zi cheklovlar tufayli Bot faqat 50 sahifani ZIP sifatida yuboradi..__😅",
    "total" : "`Umumiy sahifalar: {}..⏳`", "upload" : "`Yuborilmoqda: {}/{} sahifalar.. 🐬`",
    "current" : "`Tugallandi: {}/{} sahifalar.. 🤞`", "complete" : "`Yuborish tugallandi.. `🏌️",
    "canceledAT" : "`Bekor qilindi {}/{} sahifalarda..` 🙄", "cbAns" : "⚙️ Okey, Bekor qilinmoqda.. ",
    "cancelCB" : {"💤 BEKOR QILISH 💤" : "close|P2I"},     # EDITABLE: ❌
    "canceledCB" : {"🍄 BEKOR QILINDI 🍄" : "close|P2IDONE"},
    "completed" : {"😎 TUGALLANDI 😎" : "close|P2ICOMP"}
}

merge = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "upload" : PROGRESS['upFile'],
    "load" : "__Haddan tashqari yuklanish tufayli siz bir vaqtning o'zida faqat 5 ta pdf faylni birlashtira olasiz__",
    "sizeLoad" : "`Haddan tashqari yuk tufayli Bot Faqat %sMb pdf fayllarni qo'llab-quvvatlaydi..", # removing %s show error
    "pyromodASK" : """__BIRLASHITIRISH pdflarni » Umuumiy navbatdagi pdflar: {}__

/exit __bekor qilish uchun__
/merge __birlashitirsh uchun__""",
    "exit" : "`Jarayon bekor qilindi..` 😏", "total" : "`Umumiy PDFlar : {} 💡",
    "current" : "__PDFni yuklab olish boshlanmoqda : {} 📥__", "cancel" : "`birlashtirish jarayoni tugallandi.. 😏`",
    "started" : "__Birlshtirish boshlandi.. __ 🪄", "caption" : "`Birlashtirigan pdf 🙂`",
    "error" : "`balki PDF himoyalangan..`\n\nSababi: {}"
}

metaData = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "download" : PROGRESS['dlFile'],   # [❌]
    "read" : "Ilitmos ushbu xabarni qayta o'qing.. 🥴"
}

preview = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "error" : document['error'],
    "download" : PROGRESS['dlFile'], "_" : "PDFda atigi {} sahifa mavjud 🤓\n\n",
    "__" : "PDF safifalar: {}\n\n", "total" : "`Umumiy sahifalar: {}..` 🤌",
    "album" : "`Albom tayyorlanmoqda..` 🤹", "upload" : f"`Yuborilmqoda: oldindan ko;rish rasmlari.. 🐬`"
}

stamp = {
    "stamp" : {
        "⚙️ PDF » PECHAT ↓" : "nabilanavab",
        "Not For Public Release 🤧" : "pdf|stp|10",
        "For Public Release 🥱" : "pdf|stp|8",
        "Confidential 🤫" : "pdf|stp|2", "Departmental 🤝" : "pdf|stp|3",
        "Experimental 🔬" : "pdf|stp|4", "Expired 🐀" : "pdf|stp|5",
        "Final 🔧" : "pdf|stp|6", "For Comment 🗯️" : "pdf|stp|7",
        "Not Approved 😒" : "pdf|stp|9", "Approved 🥳" : "pdf|stp|0",
        "Sold ✊" : "pdf|stp|11", "Top Secret 😷" : "pdf|stp|12",
        "Draft 👀" : "pdf|stp|13", "AsIs 🤏" : "pdf|stp|1",
        "« ORQAGA «" : "pdf"
    },
    "stampA" : {
        "⚙️ PDF » PECHAT » RANGI ↓" : "nabilanavab",
        "Qizil ❤️" : "spP|{}|r", "Ko'k 💙" : "spP|{}|b",
        "Yashil 💚" : "spP|{}|g", "Sariq 💛" : "spP|{}|c1",
        "Pushti 💜" : "spP|{}|c2", "Havorang 💚" : "spP|{}|c3",
        "Oq 🤍" : "spP|{}|c4", "Qora 🖤" : "spP|{}|c5",
        "« Orqaga «" : "pdf|stp"
    },
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "upload" : PROGRESS['upFile'],
    "stamping" : "`Pechatlash boshlanmoqda..` 💠", "caption" : """Pechatlangan pdf\nrangi : `{}`\nannot : `{}`"""
}

work = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "takeTime" : PROGRESS['takeTime'],
    "upload" : PROGRESS['upFile'], "button" : document['cancelCB'],
    "rot360" : "Sizda katta muammo bor..🙂", "ocrError" : "Admin cheklagan 😎🤏",
    "largeNo" : "menga 5 sahifadan kam pdf yuboring.. 🙄",
    "pyromodASK_1" : """__PDF {} »\nEndi, ilimtos parolni kiriting :__\n\n/exit __bekor qilish uchun__""",
    "pyromodASK_2" : """__Qayta nomlash PDF »\nEndi, Iltimos yangi nomni  kiriting:__\n\n/exit __bekor qilish uchun__""",
    "exit" : "`Jarayon bekor qilindi.. `😏", "ren_caption" : "__Yangi nomi:__ `{}`", 
    "notENCRYPTED" : "`Fayl himoyalanmagan..` 👀",
    "compress" : "⚙️ `Siqish boshlanmoqda.. 🌡️\nBu biroz vaqt olishi mumkin..`💛",
    "decrypt" : "⚙️ `Paroldan ochish boshlanmoqda.. 🔓\nBu biroz vaqt olishi mumkin..`💛",
    "encrypt" : "⚙️ `Shifrlash boshlanmoqda.. 🔐\nBu biroz vaqt olishi mumkin..`💛",
    "ocr" : "⚙️ `OCr qatlam qo'shilmoqda.. ✍️\nBu biroz vaqt olishi mumkin..`💛",
    "format" : "⚙️ `Formatlash boshlandi.. 🤘\nBu biroz vaqt olishi mumkin..`💛",
    "rename" : "⚙️ `Qayta nomlash boshlanmoqda.. ✏️\nBu biroz vaqt olishi mumkin..`💛",
    "rot" : "⚙️ `Aylantirish boshlanmoqda.. 🤸\nBu biroz vaqt olishi mumkin..`💛",
    "pdfTxt" : "⚙️ `Matn chiqarib olinmoqda.. 🐾\nBu biroz vaqt olishi mumkin..`💛",
    "fileNm" : "Eski fayl nomi: {}\nYangi fayl nomi: {}",
    "rotate" : {
        "⚙️ PDF » AYLANTIRISH ↓" : "nabilanavab", "90°" : "work|rot90", "180°" : "work|rot180",
        "270°" : "work|rot270", "360°" : "work|rot360", "« ORQAGA «" : "pdf"
    },
    "txt" : {
        "⚙️ PDF » MATN QILISH ↓" : "nabilanavab", "📜 XABAR 📜" : "work|M", "🧾 TXT FAYL 🧾" : "work|T",
        "🌐 HTML 🌐" : "work|H", "🎀 JSON 🎀" : "work|J", "« ORQAGA «" : "pdf"
    }
}

PROCESS = {
    "ocr" : "OCR QOSHILDI  ", "decryptError" : "__Faylni ushbu parol bilan himoyalab bo'lmadi__ `{}` 🕸️",
    "decrypted" : "__Himoyalangan fayl__", "encrypted" : "__Sahida raqami__: {}\n__Parol__ 🔐: ||{}||",
    "compressed" : """`Haqiqiy hajmi : {}\nSiqilgan hajmi : {}\n\nNisbati : {:.2f} %`""",
    "cantCompress" : "Faylni bundab ortiq siqib bo'lmaydi..🤐",
    "pgNoError" : """__Bazi sabablarga kora A4 FORMATLASH 5 sahifadan kam bo'lgan pdf fayllarni qo'llab-quvvatlaydi__\n\nJami sahifalar: {} ⭐""",
    "ocrError" : "`Allaqachon matn qatlami mavjud.. `😏",
    "90" : "__90° aylantirilgan__", "180" : "__180° aylantirilgan__", "270" : "__270° aylantirilgan__",
    "formatted" : "A4 Formatlangan fayl", "M" : "♻ Chiqarili {} sahifalar ♻",
    "H" : "HTML Fayl", "T" : "TXT Fayl", "J" : "JSON Fayl"
}

pdf2TXT = {
    "upload" : PROGRESS["upFile"], "exit" : split['exit'], "nothing" : "Yaratishga hech nima yoq.. 😏",
    "TEXT" : "`Matndan PDF yaratish »`", "start" : "txt faylini Pdf ga aylantirish boshlandi..🎉",
    "font_btn" : {
        "TXT@PDF » SHRIFTNI TANLASH" : "nabilanavab", "Times" : "pdf|font|t", "Courier" : "pdf|font|c", "Helvetica (Default)" : "pdf|font|h",
        "Symbol" : "pdf|font|s", "Zapfdingbats" : "pdf|font|z", "🚫 YOPISH 🚫" : "close|me"
    },
    "size_btn" : { "TXT@PDF » {} » jOYLASHISH TANLANG" : "nabilanavab", "To'gri" : "t2p|{}|p", "O'nggag burilgan" : "t2p|{}|l", "« Orqaga «": "pdf|T2P"},
    "askT" : "__MATNNI PDF QILISH » Endi, iltimos sarlavha kiritng:__\n\n/exit __bekor qilish uchun__\n/skip __o'tkazib yuborish__",
    "askC" : "__MATNNI PDF QILISH » Now, Iltimos, paragrafni kiriting {}:__\n\n/exit __bekor qilish uchunl__\n/create __yaratish uchun__"
}

URL = {
     "get" : {"🧭 PDF faylni oling 🧭" : "getFile"}, "close" : HELP_CMD['CB'], "notPDF" : "`PDF fayl emas",
     "error" : "🐉 Nimadir xato ketdi 🐉\n\nXATO: `{}`\n\nNB: Guruhlarda botlar faqat guruhga qoʻshilgandan keyin yuboriladigan hujjatlarni olishi mumkin =)",
     "done" : "```Deyarli tugadi.. ✅\nEndi, Yuklash boshlandi.. 📤```", "_error_" : "menga istalgan url yoki bevosita telegram pdf havolalarini yuboring",
     "openCB" : {"Brauzerda ochish" : "{}"}, "_error" : "`Biror narsa noto'g'ri ketdi =(`\n\n`{}`",
     "_get" : "[Chatni ochish]({})\n\n**CHAT HAQIDA ↓**\nChat turi: {}\nChat nomi: {}\nChat Usr: @{}\n"
              "Chat ID : {}\nSana : {}\n\n**MEDIYA HAQIDA ↓**\nMedia: {}\nFayl nomi: {}\nFayl hajmi: {}\n\nFayl turi: {}"
}

getFILE = {
    "inWork" : PROGRESS['workInP'], "big" : "pdf urlni {}mb dan kamroq yuborish", "wait" : "Kutib turing.. Menga ruxsat bering.. 😜",
    "dl" : {"📥 ..YUKLASH.. 📥" : "nabilanavab"}, "up" : {"📤 ..YUKLASH.. 📤" : "nabilanavab"},
    "complete" : {"😎 COMPLETED 😎" : f"{str(settings.SOURCE_CODE)}"}
}

cbAns = [
    "Bu xususiyat ishlab chiqilmoqda ⛷️", "Annenn paranjille xatosi.. keyin nima.. 😏",
    "Jarayon bekor qilindi.. 😏", "Fayl shifrlanmagan.. 👀", "Bu haqda hech qanday rasmiy narsa yo'q.. 😅", "🎉 Bajarildi.. 🏃"
]

inline_query = {
    "TOP" : { "Endi tilni Tanlang" : "nabilanavab" }, "capt" : "TILI SOZLASH ⚙️", "des" : "By: @nabilanavab ❤"
}
