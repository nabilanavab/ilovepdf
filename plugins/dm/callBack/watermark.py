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

async def get_color_by_name(COLOR_CODE):
    color_codes = {
        'R': (255, 0, 0),
        'G': (0, 255, 0),
        'N': (0, 0, 255),
        'Y': (255, 255, 0),
        'O': (255, 165, 0),
        'V': (238, 130, 238),
        'C': (165, 62, 62),
        'B': (0, 0, 0),
        'W': (255, 255, 255),
    }
    return color_codes.get(COLOR_CODE, (0, 0, 0))

async def get_position(pg_width, pg_height, text_width, position):
    bottomLeft = {
        "T" : [int((pg_width-text_width)/2), int(pg_height/20)],
        "M" : [int((pg_width-text_width)/2), int((pg_height-pg_height/20)/2)],
        "B" : [int((pg_width-text_width)/2), int(pg_height-pg_height/20)]
    }
    return bottomLeft[position][0], bottomLeft[position][1]

async def add_text_watermark(input_file, output_file, watermark_text, opacity, position, color):
    try:
        COLOR_CODE = await get_color_by_name(color)
        # Open PDF file
        with fitz.open(input_file) as pdf:
            for page in pdf:
                
                font = fitz.Font(fontname="tiit")
                text_width = font.text_length(watermark_text, fontsize=int(page.bound().height//20))
                
                tw = fitz.TextWriter(page.rect, opacity = int(opacity)/10, color = COLOR_CODE)
                txt_bottom, txt_left = await get_position(
                    pg_width=page.bound().width, pg_height=page.bound().height, text_width=text_width, position=position[-1]
                )
                
                tw.append((txt_bottom, txt_left), watermark_text, fontsize = int(page.bound().height//20), font = font)
                tw.write_text(page)
                
            pdf.save(output_file)
        return True, output_file
    except Exception as Error:
        logger.exception("1️⃣ 🐞 %s: %s" %(fileName, Error), exc_info = True)
        return False, Error

async def add_image_watermark(input_file, output_file, watermark, opacity, position):
    try:
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
        return True, output_file
    except Exception as Error:
        logger.exception("2️⃣ 🐞 %s: %s" %(fileName, Error), exc_info = True)
        return False, Error

wa = filters.create(lambda _, __, query: query.data.startswith("wa"))

@ILovePDF.on_callback_query(wa)
async def watermark(bot, callbackQuery):
    try:
        """
        callbackQuery.data = wa|type|opacity|position|color{opt.}
        for text:
            wa|type|o07|pM|B
        else:
            wa|type|o07|pM
        """
        lang_code = await getLang(callbackQuery.message.chat.id)
        if await header(bot, callbackQuery, lang_code = lang_code):
            return
        
        CHUNK, _ = await translate(text="wa", button="wa['cancelCB']", lang_code=lang_code)
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        if callbackQuery.data.startswith("wa|txt"):
            # _ & __ are diff.
            __, _type, _opacity, _position, _color = callbackQuery.data.split("|")
        else:
            __, _type, _opacity, _position = callbackQuery.data.split("|")
        
        nabilanavab = True; i = 0
        while(nabilanavab):
            # REQUEST FOR PG NUMBER (MAX. LIMIT 5)
            if i >= 5:
                await callbackQuery.message.reply(CHUNK['over'])
                break
            i += 1
            askWA = await bot.ask(
                text = CHUNK[_type], chat_id = callbackQuery.from_user.id,
                reply_to_message_id = callbackQuery.message.id, filters = None,
                reply_markup = ForceReply(True, "Enter Watermark text.. 🎊")
            )
            # IF /exit PROCESS CANCEL
            if askWA.text == "/exit":
                await askWA.reply(CHUNK['exit'], quote = True)
                break
            elif askWA.document and _type == "img":
                if os.path.splitext(askWA.document.file_name)[1].lower() in [".png", ".jpeg", ".jpg"]:
                    waSize = askWA.document.file_size
                    waID = askWA.document.file_id
                    nabilanavab = False
                    break
            elif askWA.photo and _type == "img":
                waSize = askWA.photo.file_size
                waID = askWA.document.file_id
                nabilanavab = False
                break
            elif askWA.document and _type == "pdf":
                if os.path.splitext(askWA.document.file_name)[1].lower() == ".pdf":
                    waSize = askWA.document.file_size
                    waID = askWA.document.file_id
                    nabilanavab = False
                    break
            elif askWA.text and _type == "txt":
                waTXT = askWA.text
                nabilanavab = False
                break
        
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            return await work(callbackQuery, "delete", False)
        
        if nabilanavab == False:
            dlMSG = await callbackQuery.message.reply_text(CHUNK['download'], reply_markup = _, quote=True)
            input_file = await bot.download_media(
                message = callbackQuery.message.reply_to_message.document.file_id, file_name = f"{cDIR}/inPut.pdf", progress = progress,
                progress_args = (callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time())
            )
            # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
            if os.path.getsize(input_file) != callbackQuery.message.reply_to_message.document.file_size:    
                return await work(callbackQuery, "delete", False)
            
            if "•" not in callbackQuery.message.text:
                checked, number_of_pages = await checkPdf(input_file, callbackQuery)
                if checked == "encrypted":
                    await work(callbackQuery, "delete", False)
                    return await dlMSG.delete()
            
            await dlMSG.edit(CHUNK['waDL'], reply_markup = _)
            if _type == "img":
                wa_file = await bot.download_media(
                    message = waID, file_name = f"{cDIR}/watermarkPDF.jpeg", progress = progress,
                    progress_args = (waSize, dlMSG, time.time())
                )
                if wa_file is None:
                    await dlMSG.edit(CHUNK['error'])
                    return await work(callbackQuery, "delete", False)
            
            await dlMSG.edit(CHUNK['add'], reply_markup = _)
            output_pdf = f"{cDIR}/outPut.pdf"
            
            if _type == "img":
                success, output_file = await add_image_watermark(
                    input_file=input_file, output_file=output_pdf, watermark_text=wa_file, opacity=_opacity, position=_position
                )
            
            if _type == "txt":
                success, output_file = await add_text_watermark(
                    input_file=input_file, output_file=output_pdf, watermark_text=waTXT, opacity=_opacity[-2:], position=_position, color=_color
                )
            
            if not success:
                return await dlMSG.edit(output_file, reply_markup = _)
            
            # Getting thumbnail
            FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(
                callbackQuery.message, callbackQuery.message.reply_to_message.document.file_name
            )
            if images.PDF_THUMBNAIL != THUMBNAIL:
                location = await bot.download_media(message = THUMBNAIL, file_name = f"{cDIR}/thumb.jpeg")
                THUMBNAIL = await formatThumb(location)
            
            await dlMSG.edit(CHUNK['upFile'], reply_markup = _)
            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
            await callbackQuery.message.reply_document(
                file_name = FILE_NAME, quote = True, document = output_pdf, thumb = THUMBNAIL,
                caption = FILE_CAPT, progress = uploadProgress, progress_args = (dlMSG, time.time()) 
            )
            await dlMSG.delete()
            await work(callbackQuery, "delete", False)

    except Exception as e:
        logger.exception("3️⃣ 🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)
