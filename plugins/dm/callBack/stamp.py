# fileName : plugins/dm/callBack/stamp.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/stamp.py"

import os, time, fitz, shutil

from plugins.util    import *
from plugins.render  import *
from plugins.work    import work
from logger          import logger
from configs.config  import images
from .callback       import annotSet
from plugins.fncta   import thumbName, formatThumb
from pyrogram        import enums, filters, Client as ILovePDF

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
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        CHUNK, _ = await translate(text="stamp", lang_code=lang_code)
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        _, annot, colr = callbackQuery.data.split("|")
        
        dlMSG = await callbackQuery.message.reply_text(CHUNK["download"], quote=True)
        downloadLoc = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = progress,
            progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )
        # COLOR CODE
        color = colorSet.get(f"{colr}", (1, 0, 0))
        annotation = annotSet.get(int(annot), 1)
        # CHECK DOWNLOAD COMPLETED OR CANCELED
        if os.path.getsize(downloadLoc) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        #STAMPING STARTED
        await dlMSG.edit(CHUNK["stamping"])
        if "•" not in callbackQuery.message.text:
            checked, noOfPg = await checkPdf(f"{cDIR}/inPut.pdf", callbackQuery)
            if not(checked == "pass"):
                return await dlMSG.delete()
        r = fitz.Rect(72, 72, 440, 200)
        with fitz.open(f"{cDIR}/inPut.pdf") as doc:
            page = doc.load_page(0)
            annot = page.add_stamp_annot(r, stamp=int(f"{annot}"))
            annot.set_colors(stroke=color)
            annot.set_opacity(0.5)
            annot.update()
            doc.save(f"{cDIR}/outPut.pdf")
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, f"{cDIR}/outPut.pdf")
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(
                message = THUMBNAIL, file_name = f"{cDIR}/thumb.jpeg"
            )
            THUMBNAIL = await formatThumb(location)
        
        await dlMSG.edit(CHUNK["upload"])
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await callbackQuery.message.reply_document(
            file_name = FILE_NAME, document = f"{cDIR}/outPut.pdf", thumb = THUMBNAIL, quote = True,
            caption = CHUNK["caption"].format(color, annotation) + f"\n\n{FILE_CAPT}",
            progress = uploadProgress, progress_args = (dlMSG, time.time())
        )
        await dlMSG.delete()
        await work(callbackQuery, "delete", False)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)
        await dlMSG.delete()

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
