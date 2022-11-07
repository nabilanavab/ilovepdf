# fileName : plugins/dm/callback/metaData.py
# copyright ©️ 2021 nabilanavab

from pdf import PROCESS
import fitz, time, shutil
from logger import logger
from plugins.render import *
from plugins.util import getLang, translate
from pyrogram import filters, Client as ILovePDF

pdfInfo = filters.create(lambda _, __, query: query.data == "metaData")
@ILovePDF.on_callback_query(pdfInfo)
async def _pdfInfo(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        CHUNK, _ = await translate(text="metaData", lang_code=lang_code)
        
        if "•" in callbackQuery.message.text:
            return await callbackQuery.answer(CHUNK['read'])
        await callbackQuery.answer(CHUNK["process"])
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.id
        
        if chat_id in PROCESS:
            return await callbackQuery.answer(CHUNK["inWork"])
        if await header(bot, callbackQuery):
            return
        
        PROCESS.append(chat_id)
        downloadMessage = await callbackQuery.message.reply(text=CHUNK["download"], quote=True)
        pdf_path = f"{message_id}/pdfInfo.pdf"
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        downloadLoc = await bot.download_media(
            message = file_id, file_name = pdf_path, progress = progress,
            progress_args = (fileSize, downloadMessage, time.time())
        )
        if downloadLoc is None:    
            PROCESS.remove(chat_id)
            return
        
        checked, number_of_pages = await checkPdf(pdf_path, callbackQuery)
        await downloadMessage.delete()
        if checked == "pass":
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
    
    except Exception as e:
        logger.exception("plugins/dm/callBack/metaData: %s" %(e), exc_info=True)
        PROCESS.remove(chat_id)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
