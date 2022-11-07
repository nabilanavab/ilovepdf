# fileName : plugins/dm/callBack/stamp.py
# copyright ©️ 2021 nabilanavab

from pdf import PROCESS
from logger import logger
from plugins.util import *
from plugins.render import *
import os, time, fitz, shutil
from .callback import annotSet
from configs.config import images
from plugins.thumbName import thumbName, formatThumb
from pyrogram import enums, filters, Client as ILovePDF

# COLOR: [RGB] r = red, g = green, b = blue
colorSet = {
    "r" : (1, 0, 0), "b" : (0, 0, 1),
    "g" : (0, 1, 0), "c1" : (1, 1, 0),
    "c2" : (1, 0, 1), "c3": (0, 1, 1),
    "c4" : (1, 1, 1), "c5" : (0, 0, 0)
}

stamp = filters.create(lambda _, __, query: query.data.startswith("spP"))
@ILovePDF.on_callback_query(stamp)
async def _stamp(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        CHUNK, _ = await translate(text="stamp", lang_code=lang_code)
        
        if await header(bot, callbackQuery):
            return
        
        data = callbackQuery.data
        chat_id = callbackQuery.message.chat.id; message_id = callbackQuery.message.id
        
        # CHECK IF USER IN PROCESS
        if chat_id in PROCESS:
            return await callbackQuery.answer(CHUNK["inWork"])
        _, annot, colr = callbackQuery.data.split("|")
        await callbackQuery.answer(CHUNK["process"])
        PROCESS.append(chat_id)
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        downloadMessage = await callbackQuery.message.reply_text(CHUNK["download"], quote=True)
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        fileNm = callbackQuery.message.reply_to_message.document.file_name
        # DOWNLOAD PROGRESS
        c_time = time.time()
        downloadLoc = await bot.download_media(
            message = file_id, file_name = input_file, progress = progress,
            progress_args = (fileSize, downloadMessage, c_time)
        )
        # COLOR CODE
        color = colorSet.get(f"{colr}", (1, 0, 0))
        annotation = annotSet.get(int(annot), 1)
        # CHECK DOWNLOAD COMPLETED OR CANCELED
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        #STAMPING STARTED
        await downloadMessage.edit(CHUNK["stamping"])
        if "•" not in callbackQuery.message.text:
            checked, noOfPg = await checkPdf(input_file, callbackQuery)
            if not(checked == "pass"):
                return await downloadMessage.delete()
        r = fitz.Rect(72, 72, 440, 200)
        with fitz.open(input_file) as doc:
            page = doc.load_page(0)
            annot = page.add_stamp_annot(r, stamp=int(f"{annot}"))
            annot.set_colors(stroke=color)
            annot.set_opacity(0.5)
            annot.update()
            doc.save(output_file)
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, output_file)
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(message = THUMBNAIL, file_name = f"{callbackQuery.message.id}.jpeg")
            THUMBNAIL = await formatThumb(location)
        
        await downloadMessage.edit(CHUNK["upload"])
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await callbackQuery.message.reply_document(
            file_name = FILE_NAME, document = output_file, thumb = THUMBNAIL, quote = True,
            caption = CHUNK["caption"].format(color, annotation) + f"\n\n{FILE_CAPT}",
            progress = uploadProgress, progress_args = (downloadMessage, time.time())
        )
        await downloadMessage.delete()
        try:
            os.remove(location)
        except Exception: pass
        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
    except Exception as e:
        logger.exception("plugins/dm/callBack/stamp %s" %(e), exc_info=True)
        try:
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
            await downloadMessage.delete()
        except Exception:
            pass

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
