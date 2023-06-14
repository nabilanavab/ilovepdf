file_name = "plugins/dm/textToPdf/handler.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

import                   os
from plugins.utils       import *
from configs.log         import log
from fpdf                import FPDF
from logger              import logger
from arabic_reshaper     import reshape
from bidi.algorithm      import get_display
from configs.config      import settings, images
from pyrogram            import filters, Client as ILovePDF, enums
from .                   import FONT, COLOR, BACKGROUND, SCALE, TXT


async def ask_for_text(bot, callbackQuery, text: str, num: int = False):
    while(text):
        askTEXT = await bot.ask(text=text.format(num), chat_id=callbackQuery.message.chat.id,
                               reply_to_message_id=callbackQuery.message.id, filters=None)
        
        if askTEXT.text:
            if askTEXT.text == "/exit":
                return False, askTEXT
            elif askTEXT.text == "/skip":
                return True, None
            return True, askTEXT
        # return isSuccess, result

async def ask_for_bg(bot, callbackQuery, text: str):
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
        
        cDIR = await work.work(callbackQuery, "create", False)
        if not cDIR:
            tTXT, _ = await util.translate(text="_W_I_P", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        await callbackQuery.answer()
        
        CHUNK, _ = await util.translate(text="pdf2TXT", lang_code=lang_code)
        _, scale, h_font, p_font, color, background = [int(i) if i.isdigit() else i for i in callbackQuery.data.split('|')]
        
        logger.debug(f"{SCALE[scale]}/{FONT[h_font]['name']}/{FONT[p_font]}/{COLOR[color]}/{BACKGROUND[int(background[0])]}")

        if callbackQuery.data.endswith("9:"):
            background = await ask_for_bg(bot, callbackQuery=callbackQuery, text="send me an image")
        
        TXT[callbackQuery.message.chat.id] = []
        
        isSuccess, title = await ask_for_text(bot, callbackQuery=callbackQuery, text=CHUNK['askT'])
        if not isSuccess:
            await title.reply(CHUNK['exit'], quote=True)
            del TXT[callbackQuery.message.chat.id]; return await work.work(callbackQuery, "delete", False)
        else:
            TXT[callbackQuery.message.chat.id].append(None if title is None else title.text)
        
        nabilanavab = True
        while(nabilanavab):
            isSuccess, paragraph = await ask_for_text(bot, callbackQuery=callbackQuery, text=CHUNK['askC'],
                                                               num=len(TXT[callbackQuery.message.chat.id]))
            if not isSuccess:
                await paragraph.reply(CHUNK['exit'], quote=True)
                del TXT[callbackQuery.message.chat.id]; return await work.work(callbackQuery, "delete", False)
            elif isSuccess and paragraph.text == "/create":
                if TXT[callbackQuery.message.chat.id][0] == None and len(TXT[callbackQuery.message.chat.id]) == 1:
                    await askPDF.reply(CHUNK['nothing'], quote=True)
                else:
                    processMessage = await paragraph.reply(CHUNK['start'], quote=True)
                    nabilanavab = False
            else:
                TXT[callbackQuery.message.chat.id].append(f"{paragraph.text}")
        
        pdf = FPDF(orientation=SCALE[scale], format="A4")
        pdf.add_page()
        pdf.set_title("NABIL A NAVAB")
        pdf.set_subject("pdf created using nabilanavab open source Telegram Pdf Bot\n\nContact Nabil A Navab: telegram.dog/nabilanavab ❤")
        pdf.set_author("https://github.com/nabilanavab/ilovepdf")
        pdf.set_producer("by nabilanavab@gmail.com")

        if not FONT[h_font]['default']:
            logger.debug(os.getcwd())
            pdf.add_font('NewFont', '', FONT[h_font]['name'], uni=True)
            pdf.set_font('NewFont', "B", size=20)
        else:
            pdf.set_font(FONT[h_font]['name'], "B", size=20)
        if TXT[callbackQuery.message.chat.id][0] != None:
            pdf.cell(200, 20, txt=get_display(reshape(TXT[callbackQuery.message.chat.id][0])), ln=1, align="C")
        
        if not FONT[p_font]['default']:
            logger.debug(os.getcwd())
            pdf.add_font('NewFont', '', FONT[p_font]['name'], uni=True)
            pdf.set_font('NewFont', "B", size=20)
        else:
            pdf.set_font(FONT[p_font]['name'], "B", size=20)
        
        for _ in TXT[callbackQuery.message.chat.id][1:]:
            pdf.multi_cell(200, 10, txt=get_display(reshape(_)), border=0, align="L")
        
        pdf.output(f"{cDIR}/{callbackQuery.message.chat.id}.pdf")
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await fncta.thumbName(callbackQuery.message, f"{callbackQuery.message.chat.id}.pdf")
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
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info=True)
        await processMessage.edit(CHUNK['error'].format(Error))
    finally:
        del TXT[callbackQuery.message.chat.id]
        await work.work(callbackQuery, "delete", False)

# SOURCE CODE: "https://github.com/nabilanavab/ilovepdf"
