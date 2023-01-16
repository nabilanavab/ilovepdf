# fileName : plugins/dm/callBack/codec.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/codec.py"

# just another way to convert epub files(depending on user satisfraction..)
import os, time
from plugins.util         import *
from plugins.render       import *
from plugins.work         import work
from logger               import logger
from plugins.dm.document  import word2PDF
from pyrogram.enums       import ChatAction
from pyrogram             import Client as ILovePDF, filters

pdf = filters.create(lambda _, __, query: query.data.startswith("try"))

@ILovePDF.on_callback_query(pdf)
async def _pdf(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.from_user.id)
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        if callbackQuery.data == "try+":
            return await callbackQuery.answer("✅")
        
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            tTXT, _ = await translate(text = "PROGRESS['workInP']", lang_code = lang_code)
            return await callbackQuery.answer(tTXT)
        tTXT, _ = await translate(text = "document['process']", lang_code = lang_code)
        await callbackQuery.answer(tTXT)
        
        input_file, output_file = f"{cDIR}/inPut.epub", f"{cDIR}/outPut.pdf"
        
        # DOWNLOAD MESSAGE
        tTXT, tBTN = await translate(text = "PROGRESS['dlFile']", button = "document['cancelCB']", lang_code = lang_code)
        downloadMessage = await callbackQuery.message.reply_text(text = tTXT, reply_markup = tBTN, quote = True)
        
        downloadLoc = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = input_file, progress = progress,
            progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, downloadMessage, time.time()
            )
        )
        if os.path.getsize(downloadLoc) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        tTXT, tBTN = await translate(
            text = "URL['done']", button = "document['cancelCB']", lang_code = lang_code
        )
        await downloadMessage.edit(text = tTXT, reply_markup = tBTN)
        
        await word2PDF(
            cDIR, downloadMessage, input_file, lang_code
        )
        
        await callbackQuery.message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        await callbackQuery.message.reply_to_message.reply_document(
            file_name = f"{callbackQuery.message.reply_to_message.document.file_name[:-5]}.pdf",
            quote = True, document = output_file, progress = uploadProgress,
            progress_args = ( downloadMessage, time.time() )
        )
        await downloadMessage.delete()
        await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)
        tTXT, tBTN = await translate(
            text="document['error']".format(e), button = "document['cancelCB']", lang_code = lang_code
        )
        await downloadMessage.edit(text = tTXT, reply_markup = tBTN)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
