file_name = "plugins/dm/textToPdf/callBack.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

import                   os
from plugins.utils       import *
from configs.log         import log
from fpdf                import FPDF
from configs.config      import settings, images
from .                   import FONT, COLOR, PAGE_SIZE
from pyrogram            import filters, Client as ILovePDF, enums

@ILovePDF.on_callback_query(filters.regex("^t2p.*:$"))
async def text_to_pdf(bot, callbackQuery):
    try:
        chat_id = callbackQuery.message.chat.id
        await callbackQuery.answer(); lang_code = await getLang(chat_id)
        
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            tTXT, _ = await translate(text="PROGRESS['workInP']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        
        CHUNK, _ = await translate(text="pdf2TXT", lang_code=lang_code)
        bla, _, __ = callbackQuery.data.split("|")
        
        TXT[chat_id] = []; nabilanavab=True
        while(nabilanavab):
            # 1st value will be pdf title
            askPDF = await bot.ask(text=CHUNK['askT'] ,chat_id=chat_id, reply_to_message_id=callbackQuery.message.id, filters=None)
            if askPDF.text == "/exit":
                await askPDF.reply(CHUNK['exit'], quote=True)
                await work(callbackQuery, "delete", False)
                del TXT[chat_id]; break
            elif askPDF.text == "/skip":
                TXT[chat_id].append(None); nabilanavab=False
            elif askPDF.text:
                TXT[chat_id].append(f"{askPDF.text}"); nabilanavab=False
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            await work(callbackQuery, "delete", False)
            del TXT[chat_id]; return
        nabilanavab = True
        while(nabilanavab):
            # other value will be pdf para
            askPDF = await bot.ask(text=CHUNK['askC'].format(len(TXT[chat_id])-1), chat_id=chat_id, reply_to_message_id=callbackQuery.message.id, filters=None)
            if askPDF.text == "/exit":
                await askPDF.reply(CHUNK['exit'], quote=True)
                await work(callbackQuery, "delete", False)
                del TXT[chat_id]; break
            elif askPDF.text == "/create":
                if TXT[chat_id][0] == None and len(TXT[chat_id]) == 1:
                    await askPDF.reply(CHUNK['nothing'], quote=True)
                else:
                    processMessage = await askPDF.reply(CHUNK['start'], quote=True)
                    nabilanavab = False
            elif askPDF.text:
                TXT[chat_id].append(f"{askPDF.text}")
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            await work(callbackQuery, "delete", False)
            del TXT[chat_id]
            return
        
        pdf = FPDF()
        pdf.add_page(orientation = __)
        pdf.set_font(FONT[_], "B", size = 20)
        if TXT[chat_id][0] != None:
            pdf.cell(200, 20, txt = TXT[chat_id][0], ln = 1, align = "C")
        pdf.set_font(FONT[_], size = 15)
        for _ in TXT[chat_id][1:]:
            pdf.multi_cell(200, 10, txt = _, border = 0, align = "L")
        pdf.output(f"{cDIR}/out.pdf")
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, f"out.pdf")
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(
                message = THUMBNAIL,
                file_name = f"{cDIR}/{callbackQuery.message.id}.jpeg"
            )
            THUMBNAIL = await formatThumb(location)
        
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await processMessage.edit(CHUNK['upload'])
        logFile = await callbackQuery.message.reply_document(
            file_name = FILE_NAME, caption = FILE_CAPT,
            quote = True, document = open(f"{cDIR}/out.pdf", "rb"), thumb = THUMBNAIL
        )
        await processMessage.delete(); del TXT[chat_id]
        await work(callbackQuery, "delete", False)
        await log.footer(callbackQuery.message, output = logFile, lang_code = lang_code)
    except Exception as e:
        logger.exception("PAGE SIZE:CAUSES %s ERROR" %(e), exc_info=True)
        await work(callbackQuery, "delete", False)
        await processMessage.edit(f"`ERROR`: __{e}__"); del TXT[chat_id]
