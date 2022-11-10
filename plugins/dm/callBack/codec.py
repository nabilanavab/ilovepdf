# fileName : plugins/dm/callBack/codec.py
# copyright ©️ 2021 nabilanavab

# just another way to convert epub files(depending on user satisfraction..)
import time
from pdf import PROCESS
from logger import logger
from plugins.util import *
from plugins.render import *
from plugins.dm.document import word2PDF
from pyrogram import Client as ILovePDF, filters

pdf = filters.create(lambda _, __, query: query.data.startswith("try"))
@ILovePDF.on_callback_query(pdf)
async def _pdf(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.from_user.id
        message_id = callbackQuery.message.id
        
        if callbackQuery.data == "try+":
            return await callbackQuery.answer("✅")
        
        if callbackQuery.message.chat.id in PROCESS:
            tTXT, _ = await translate(text="PROGRESS['workInP']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        
        tTXT, _ = await translate(text="document['process']", lang_code=lang_code)
        await callbackQuery.answer(tTXT)
        PROCESS.append(callbackQuery.message.chat.id)
        
        input_file = f"{callbackQuery.message.id}/inPut.epub"
        output_file = f"{callbackQuery.message.id}/outPut.pdf"
        
        # DOWNLOAD MESSAGE
        tTXT, tBTN = await translate(text="PROGRESS['dlFile']", button="document['cancelCB']", lang_code=lang_code)
        downloadMessage = await callbackQuery.message.reply_text(text=tTXT, reply_markup=tBTN, quote=True)
        
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
        downloadLoc = await bot.download_media(
             message = file_id, file_name = input_file, progress = progress,
             progress_args = (fileSize, downloadMessage, time.time())
        )
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        
        tTXT, tBTN = await translate(text="URL['done']", button="document['cancelCB']", lang_code=lang_code)
        await downloadMessage.edit(text=tTXT, reply_markup=tBTN)
        
        await word2PDF(callbackQuery.message, downloadMessage, input_file, lang_code)
        
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        with open(output_file, "rb") as outPut:
            await callbackQuery.message.reply_to_message.reply_document(
                file_name = f"{callbackQuery.message.reply_to_message.document.file_name[:-5]}.pdf",
                quote = True, document = outPut, progress = uploadProgress,
                progress_args = ( downloadMessage, time.time() )
            )
        
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f'{callbackQuery.message.id}')
    except Exception as e:
        logger.debug(f"plugins/dm/callBack/callback/codec : {e}", exc_info=True)
        try:
            tTXT, tBTN = await translate(text="document['error']".format(e), button="document['cancelCB']", lang_code=lang_code)
            await downloadMessage.edit(text=tTXT, reply_markup=tBTN)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f'{callbackQuery.message.id}')
        except Exception:
            pass

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
