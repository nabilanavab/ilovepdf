file_name = "plugins/dm/textToPdf/handler.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

import                   os
from plugins.utils       import *
from configs.log         import log
from fpdf                import FPDF
from logger              import logger
from configs.config      import settings, images
from .                   import FONT, COLOR, BACKGROUND, SCALE
from pyrogram            import filters, Client as ILovePDF, enums


async def ask_for_test(callbackQuery, text: str):
    while(text):
        askTEXT = await bot.ask(text=text, chat_id=callbackQuery.message.chat.id,
                               reply_to_message_id=callbackQuery.message.id, filters=None)
        
        if askTEXT.text:
            if askTEXT.text == "/exit":
                return False, askTEXT
            elif askTEXT.text == "/skip":
                return True, None
            return True, askTEXT
        # return isSuccess, result

async def ask_for_bg(callbackQuery, text: str):
    askBG = await bot.ask(text=text, chat_id=callbackQuery.message.chat.id,
                               reply_to_message_id=callbackQuery.message.id, filters=None)
        
    if askBG.photo:
        return askBG.photo
    else:
        return "_"

@ILovePDF.on_callback_query(filters.regex("^t2p.*:$"))
async def text_to_pdf(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            tTXT, _ = await util.translate(text="PROGRESS['workInP']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        await callbackQuery.answer()
        
        CHUNK, _ = await util.translate(text="pdf2TXT", lang_code=lang_code)
        _, scale, h_font, p_font, color, background = callbackQuery.data.split("|")
        logger.debug(f"{SCALE[scale]}/{FONT[h_font]}/{FONT[p_font]}/{COLOR[color]}/{BACKGROUND[background]}")

        if callbackQuery.data.endswith("9:"):
            background = await ask_for_bg(callbackQuery=callbackQuery, text="send me an image")
        
        TXT[callbackQuery.message.chat.id] = []
        
        isSuccess, title = await ask_for_text(callbackQuery=callbackQuery, text=CHUNK['askT'])
        if not isSuccess:
            await title.reply(CHUNK['exit'], quote=True)
            del TXT[callbackQuery.message.chat.id]; return await work(callbackQuery, "delete", False)
        else:
            TXT[callbackQuery.message.chat.id].append(title.text)
        
        nabilanavab = True
        while(nabilanavab):
            isSuccess, paragraph = await ask_for_text(callbackQuery=callbackQuery, text=CHUNK['askC'])
            if not isSuccess:
                await paragraph.reply(CHUNK['exit'], quote=True)
                del TXT[callbackQuery.message.chat.id]; await work(callbackQuery, "delete", False)
            elif isSuccess and paragraph.text == "/create":
                if TXT[callbackQuery.message.chat.id][0] == None and len(TXT[callbackQuery.message.chat.id]) == 1:
                    await askPDF.reply(CHUNK['nothing'], quote=True)
                else:
                    processMessage = await paragraph.reply(CHUNK['start'], quote=True)
                    nabilanavab = False
            else:
                TXT[chat_id].append(f"{paragraph.text}")
        
        pdf = FPDF(orientation=SCALE[scale], format="A4")
        pdf.set_title("NABIL A NAVAB")
        pdf.set_subject("pdf created using nabilanavab open source Telegram Pdf Bot\n\nContact Nabil A Navab: telegram.dog/nabilanavab ❤")
        pdf.set_author("https://github.com/nabilanavab/ilovepdf")
        pdf.set_producer("by nabilanavab@gmail.com")
        
        pdf.set_font(FONT[h_font], "B", size=20)
        if TXT[callbackQuery.message.chat.id][0] != None:
            pdf.cell(200, 20, txt=TXT[callbackQuery.message.chat.id][0], ln=1, align="C")
        pdf.set_font(FONT[_], size=15)
        for _ in TXT[callbackQuery.message.chat.id][1:]:
            pdf.multi_cell(200, 10, txt=_, border=0, align="L")
        pdf.output(f"{cDIR}/out.pdf")
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, f"{callbackQuery.message.chat.id}.pdf")
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(message = THUMBNAIL, file_name = f"{cDIR}/{callbackQuery.message.id}.jpeg")
            THUMBNAIL = await formatThumb(location)
        
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await processMessage.edit(CHUNK['upload'])
        logFile = await callbackQuery.message.reply_document(
            file_name=FILE_NAME, caption=FILE_CAPT, quote=True, thumb=THUMBNAIL,
            document=open(f"{cDIR}/{callbackQuery.message.chat.id}.pdf", "rb")
        )
        await processMessage.delete()
        await log.footer(callbackQuery.message, output=logFile, lang_code=lang_code)
    except Exception as Error:
        logger.exception("PAGE SIZE:CAUSES %s ERROR" %(file_name. Error), exc_info=True)
        await processMessage.edit(f"`ERROR`: __{e}__"); del TXT[callbackQuery.message.chat.id]
    finally:
        del TXT[callbackQuery.message.chat.id]
        await work(callbackQuery, "delete", False)

# SOURCE CODE: "https://github.com/nabilanavab/ilovepdf"
