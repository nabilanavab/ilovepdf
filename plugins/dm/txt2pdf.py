# fileName : Plugins/dm/txt2pdf.py
# copyright ©️ 2021 nabilanavab

import os
from fpdf import FPDF
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup

#--------------->
#--------> config vars
#------------------->

PDF_THUMBNAIL=Config.PDF_THUMBNAIL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> LOCAL VARIABLES
#------------------->

TXT = {}

UCantUse = "For Some Reason You Can't Use This Bot 🛑"

button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "😉 قناة البوت 😉",
                    url="https://t.me/engineering_electrical9"
                )
            ]
       ]
    )

#--------------->
#--------> REPLY TO /txt2pdf
#------------------->

@ILovePDF.on_message(filters.private & filters.command(["txt2pdf"]) & ~filters.edited)
async def feedback(bot, message):
    try:
        await message.reply_chat_action("typing")
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse, reply_markup=button, quote=True
            )
            return
        await message.reply_text(
            text="__ الان, يرجى تحديد نمط الخط »__",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Times", callback_data="font|t"),
                        InlineKeyboardButton("Courier", callback_data="font|c")
                    ],[
                        InlineKeyboardButton("Helvetica (Default)", callback_data="font|h")
                    ],[
                        InlineKeyboardButton("Symbol", callback_data="font|s"),
                        InlineKeyboardButton("Zapfdingbats", callback_data="font|z")
                    ],[
                        InlineKeyboardButton("🚫 اغلق ", callback_data="closeme")
                    ]
                ]
            )
        )
        await message.delete()
    except Exception as e:
        print(e)

txt2pdf = filters.create(lambda _, __, query: query.data.startswith("font"))

@ILovePDF.on_callback_query(txt2pdf)
async def _txt2pdf(bot, callbackQuery):
    try:
        _, font = callbackQuery.data.split("|")
        await callbackQuery.message.edit(
            text=f"نص إلى ملف PDF» الآن حدد حجم الصفحة »",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("حمل", callback_data=f"pgSize|{font}|p")
                    ],[
                        InlineKeyboardButton("منظر جمالي 🖼", callback_data=f"pgSize|{font}|l")
                    ],[
                        InlineKeyboardButton("« عودة 🔙 «", callback_data=f"txt2pdfBack")
                    ]
                ]
            )
        )
    except Exception as e:
        print(e)

txt2pdfBack = filters.create(lambda _, __, query: query.data == "txt2pdfBack")

@ILovePDF.on_callback_query(txt2pdfBack)
async def _txt2pdfBack(bot, callbackQuery):
    try:
        await callbackQuery.message.edit(
            text="__الآن , يرجى تحديد نمط الخط »__",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Times", callback_data="font|t"),
                        InlineKeyboardButton("Courier", callback_data="font|c")
                    ],[
                        InlineKeyboardButton("Helvetica", callback_data="font|h")
                    ],[
                        InlineKeyboardButton("Symbol", callback_data="font|s"),
                        InlineKeyboardButton("Zapfdingbats", callback_data="font|z")
                    ],[
                        InlineKeyboardButton("🚫 أغلق ", callback_data="closeme")
                    ]
                ]
            ),
            disable_web_page_preview=True
        )
    except Exception as e:
        print(e)

pgSize = filters.create(lambda _, __, query: query.data.startswith("pgSize"))

@ILovePDF.on_callback_query(pgSize)
async def _pgSize(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل .. 🙇"
            )
            return
        bla, _, __ = callbackQuery.data.split("|")
        PROCESS.append(callbackQuery.message.chat.id)
        TXT[callbackQuery.message.chat.id] = []
        nabilanavab=True
        while(nabilanavab):
            # 1st value will be pdf title
            askPDF = await bot.ask(
                text="__النص  الى  pdf»الآن ، الرجاء إدخال عنوان :__\n\n/exit __ لالغاء__\n/skip __لتخطي__",
                chat_id=callbackQuery.message.chat.id,
                reply_to_message_id=callbackQuery.message.message_id,
                filters=None
            )
            if askPDF.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`تم إلغاء العملية ..` 😏"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                del TXT[callbackQuery.message.chat.id]
                break
            elif askPDF.text == "/skip":
                TXT[callbackQuery.message.chat.id].append(None)
                nabilanavab=False
            elif askPDF.text:
                TXT[callbackQuery.message.chat.id].append(f"{askPDF.text}")
                nabilanavab=False
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
            TXT.remove(callbackQuery.message.chat.id)
            return
        nabilanavab=True
        while(nabilanavab):
            # other value will be pdf para
            askPDF = await bot.ask(
                text=f"__النص الى pdf » الآن ، الرجاء إدخال فقرة {len(TXT[callbackQuery.message.chat.id])-1}:__"
                      "\n\n/exit __لإلغاء__\n/create __لأنشاء__",
                chat_id=callbackQuery.message.chat.id,
                reply_to_message_id=callbackQuery.message.message_id,
                filters=None
            )
            if askPDF.text == "/exit":
                await bot.send_message(
                    callbackQuery.message.chat.id,
                    "`تم إلغاء العملية ..` 😏"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                del TXT[callbackQuery.message.chat.id]
                break
            elif askPDF.text == "/create":
                if TXT[callbackQuery.message.chat.id][0]==None and len(TXT[callbackQuery.message.chat.id])==1:
                    await bot.send_message(
                        callbackQuery.message.chat.id,
                        "لا شي لأنشاء.. 😏"
                    )
                else:
                    processMessage = await callbackQuery.message.reply_text(
                        "بدأ في تحويل txt إلى Pdf..", quote=True
                    )
                    nabilanavab=False
            elif askPDF.text:
                TXT[callbackQuery.message.chat.id].append(f"{askPDF.text}")
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            PROCESS.remove(callbackQuery.message.chat.id)
            TXT.remove(callbackQuery.message.chat.id)
            return
        
        # Started Creating PDF
        if _ == "t":
            font="Times"
        elif _ == "c":
            font="Courier"
        elif _ == "h":
            font="Helvetica"
        elif _ == "s":
            font="Symbol"
        elif _ == "z":
            font="ZapfDingbats"
        
        pdf = FPDF()
        pdf.add_page(orientation=__)
        pdf.set_font(font, "B", size=20)
        if TXT[callbackQuery.message.chat.id][0] != None:
            pdf.cell(200, 20, txt=TXT[callbackQuery.message.chat.id][0], ln=1, align="C")
        pdf.set_font(font, size=15)
        for _ in TXT[callbackQuery.message.chat.id][1:]:
            pdf.multi_cell(200, 10, txt=_, border=0, align="L")
        pdf.output(f"{callbackQuery.message.message_id}.pdf")
        await callbackQuery.message.reply_chat_action("upload_document")
        await processMessage.edit(
            "`بدأ التحميل ..` 🏋️"
        )
        await callbackQuery.message.reply_document(
            file_name="txt2.pdf", quote=True,
            document=open(f"{callbackQuery.message.message_id}.pdf", "rb"),
            thumb=PDF_THUMBNAIL
        )
        await processMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        os.remove(f"{callbackQuery.message.message_id}")
        TXT.remove(callbackQuery.message.chat.id)
    except Exception as e:
        try:
            PROCESS.remove(callbackQuery.message.chat.id)
            await processMessage.edit(f"`ERROR`: __{e}__")
            os.remove(f"{callbackQuery.message.message_id}.pdf")
            TXT.remove(callbackQuery.message.chat.id)
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
