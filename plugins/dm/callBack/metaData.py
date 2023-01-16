# fileName : plugins/dm/callback/metaData.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callback/metaData.py"

import fitz, time
from logger import logger
from plugins.render import *
from plugins.work import work
from plugins.util import getLang, translate
from pyrogram import filters, Client as ILovePDF

pdfInfo = filters.create(lambda _, __, query: query.data == "metaData")

@ILovePDF.on_callback_query(pdfInfo)
async def _pdfInfo(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        CHUNK, _ = await translate(text = "metaData", button = "comb['cancelCB']", lang_code = lang_code)
        
        if "•" in callbackQuery.message.text:
            return await callbackQuery.answer(CHUNK['read'])
        
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        dlMSG = await callbackQuery.message.reply(
            text = CHUNK["download"], reply_markup = _, quote = True
        )
        downloadLoc = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/pdfInfo.pdf", progress = progress,
            progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )
        if os.path.getsize(downloadLoc) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        checked, number_of_pages = await checkPdf(f"{cDIR}/pdfInfo.pdf", callbackQuery)
        await dlMSG.delete()
        if checked == "pass":
            await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
