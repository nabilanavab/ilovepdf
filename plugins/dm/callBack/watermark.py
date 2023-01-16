# fileName : plugins/dm/callBack/watermark.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/watermark.py"

import os, time, fitz
import shutil, asyncio
from plugins.util    import *
from plugins.render  import *
from plugins.work    import work
from PIL             import Image
from logger          import logger
from pyromod         import listen
from configs.config  import images
from pyrogram.types  import ForceReply
from plugins.fncta   import thumbName, formatThumb
from pyrogram        import enums, filters, Client as ILovePDF

wa = filters.create(lambda _, __, query: query.data.startswith("wa"))

@ILovePDF.on_callback_query(wa)
async def watermark(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        CHUNK, _ = await translate(text="wa", button="wa['cancelCB']", lang_code=lang_code)
        data = callbackQuery.data.split("|")    # wa|type|opacity|position
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        nabilanavab = True; i = 0
        while(nabilanavab):
            # REQUEST FOR PG NUMBER (MAX. LIMIT 5)
            if i >= 5:
                await callbackQuery.message.reply(CHUNK['over'])
                break
            i += 1
            askWA = await bot.ask(
                text = CHUNK[data[1]], chat_id = callbackQuery.from_user.id,
                reply_to_message_id = callbackQuery.message.id, filters = None
            )
            # IF /exit PROCESS CANCEL
            if askWA.text == "/exit":
                await askWA.reply(CHUNK['exit'], quote = True)
                break
            elif askWA.document and data[1] == "img":
                if os.path.splitext(askWA.document.file_name)[1].lower() in [".png", ".jpeg", ".jpg"]:
                    waSize = askWA.document.file_size
                    waID = askWA.document.file_id
                    nabilanavab = False
                    break
            elif askWA.photo and data[1] == "img":
                waSize = askWA.photo.file_size
                waID = askWA.document.file_id
                nabilanavab = False
                break
            elif askWA.document and data[1] == "pdf":
                if os.path.splitext(askWA.document.file_name)[1].lower() == ".pdf":
                    waSize = askWA.document.file_size
                    waID = askWA.document.file_id
                    nabilanavab = False
                    break
            elif askWA.text and data[1] == "txt":
                waTXT = askWA.text
                nabilanavab = False
                break
        
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            return await work(callbackQuery, "delete", False)
        
        if nabilanavab == False:
            dlMSG = await callbackQuery.message.reply_text(
                CHUNK['download'], reply_markup = _, quote=True
            )
            input_file = await bot.download_media(
                message = callbackQuery.message.reply_to_message.document.file_id,
                file_name = f"{cDIR}/inPut.pdf", progress = progress,
                progress_args = (
                    callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
                )
            )
            # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
            if os.path.getsize(downloadLoc) != callbackQuery.message.reply_to_message.document.file_size:    
                return await work(callbackQuery, "delete", False)
            
            if "•" not in callbackQuery.message.text:
                checked, number_of_pages = await checkPdf(input_file, callbackQuery)
                if checked == "encrypted":
                    await work(callbackQuery, "delete", False)
                    return await dlMSG.delete()
            
            await dlMSG.edit(CHUNK['waDL'], reply_markup = _)
            if data[1] == "img":
                wa_file = await bot.download_media(
                    message = waID, file_name = f"{cDIR}/watermarkPDF.jpeg", progress = progress,
                    progress_args = (waSize, dlMSG, time.time())
                )
                if wa_file is None:
                    await dlMSG.edit(CHUNK['error'])
                    return await work(callbackQuery, "delete", False)
            
            await dlMSG.edit(CHUNK['add'], reply_markup = _)
            output_pdf = f"{cDIR}/outPut.pdf"
            
            if data[1] == "img":
                # change opacity if needed
                with Image.open(wa_file) as wa:
                    if int(data[2][-2:]) != 10:
                        data = wa.convert("RGBA").getdata()
                        newData = []
                        for item in data:
                            if item[0] in range(200, 255) and item[1] in range(200, 255) and item[2] in range(200, 255):
                                newData.append((255, 255, 255, 0))
                            else:
                                newData.append(item)
                        wa.putdata(newData)
                        wa.save(wa_file, "PNG")
                    imgWidth, imgHeight = wa.size
                
                with fitz.open(input_file) as file_handle:
                    for page in file_handle:
                        r = page.rect
                        page.insert_image(
                            fitz.Rect(r.x0/4, 0, (r.x0/4) + imgHeight, imgWidth),
                            stream = open(wa_file, "rb").read()
                        )
                    file_handle.save(output_pdf)
            
            # Getting thumbnail
            FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(
                callbackQuery.message, callbackQuery.message.reply_to_message.document.file_name
            )
            if images.PDF_THUMBNAIL != THUMBNAIL:
                location = await bot.download_media(
                    message = THUMBNAIL, file_name = f"{cDIR}/thumb.jpeg"
                )
                THUMBNAIL = await formatThumb(location)
            
            await dlMSG.edit(CHUNK['upFile'], reply_markup = _)
            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
            await callbackQuery.message.reply_document(
                file_name = FILE_NAME, quote = True, document = output_pdf, thumb = THUMBNAIL,
                caption = FILE_CAPT, progress = uploadProgress,
                progress_args = (dlMSG, time.time()) 
            )
            await dlMSG.delete()
            await work(callbackQuery, "delete", False)

    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
