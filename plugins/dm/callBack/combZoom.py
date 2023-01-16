# fileName : plugins/dm/callBack/combZoom.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/combZoom.py"

import os, time, fitz 
from logger import logger
from plugins.util import *
from plugins.render import *
from plugins.work import work
from configs.config import images
from plugins.fncta import thumbName, formatThumb
from pyrogram import enums, filters, Client as ILovePDF

CZ = filters.create(lambda _, __, query: query.data.startswith(tuple(["comb", "zoom", "draw"])))

@ILovePDF.on_callback_query(CZ)
async def watermark(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        CHUNK, _ = await translate(text = "comb", button = "comb['cancelCB']", lang_code = lang_code)
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        
        dlMSG = await callbackQuery.message.reply_text(
            CHUNK['download'], reply_markup = _, quote = True
        )
        input_file = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = progress,
            progress_args = (
                callbackQuery.message.reply_to_message.document.file_size,
                dlMSG, time.time()
            )
        )
        # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
        if os.path.getsize(input_file) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work(callbackQuery, "delete", False)
        
        await dlMSG.edit(CHUNK['process'], reply_markup = _)
        if "•" not in callbackQuery.message.text:
            checked, number_of_pages = await checkPdf(input_file, callbackQuery)
            if checked == "encrypted":
                await work(callbackQuery, "delete", False)
                return await dlMSG.delete()
        
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:        # empty output PDF
                if callbackQuery.data == "comb":
                    width, height = fitz.paper_size("a4")
                    r = fitz.Rect(0, 0, width, height)
                    # define the 4 rectangles per page
                    r1 = r / 2 # top left rect
                    r2 = r1 + (r1.width, 0, r1.width, 0) # top right
                    r3 = r1 + (0, r1.height, 0, r1.height) # bottom left
                    r4 = fitz.Rect(r1.br, r.br) # bottom right
                    r_tab = [r1, r2, r3, r4]
                    # now copy input pages to output
                    for pages in iNPUT:
                        if pages.number % 4 == 0: # create new output page
                            page = oUTPUT.new_page(-1, width = width, height = height)
                        # insert input page into the correct rectangle
                        page.show_pdf_page(r_tab[pages.number % 4], iNPUT, pages.number)
                        # by all means, save new file using garbage collection and compression
                
                elif callbackQuery.data == "zoom":
                    for pages in iNPUT:
                        r  = pages.rect
                        d =  fitz.Rect(pages.cropbox_position, pages.cropbox_position)
                        r1 = r / 2 # top left rect
                        r2 = r1 + (r1.width, 0, r1.width, 0) # top right rect
                        r3 = r1 + (0, r1.height, 0, r1.height) # bottom left rect
                        r4 = fitz.Rect(r1.br, r.br) # bottom right rect
                        rect_list = [r1, r2, r3, r4] # put them in a list
                        
                        for rx in rect_list: # run thru rect list
                            rx += d # add the CropBox displacement
                            page = oUTPUT.new_page(-1, width = rx.width, height = rx.height)
                            page.show_pdf_page(page.rect, iNPUT, pages.number, clip = rx)
                
                elif callbackQuery.data == "draw":
                    for page in iNPUT:
                        paths = page.get_drawings()
                        outpage = oUTPUT.new_page(width=page.rect.width, height=page.rect.height)
                        shape = outpage.new_shape()
                        for path in paths:
                            for item in path["items"]: # these are the draw commands
                                if item[0] == "l": # line
                                    shape.draw_line(item[1], item[2])
                                elif item[0] == "re": # rectangle
                                    shape.draw_rect(item[1])
                                elif item[0] == "qu": # quad
                                    shape.draw_quad(item[1])
                                elif item[0] == "c": # curve
                                    shape.draw_bezier(item[1], item[2], item[3], item[4])
                                else:
                                    raise ValueError("unhandled drawing", item)
                            shape.finish(
                                fill = path["fill"], # fill color
                                color = path["color"], # line color
                                dashes = path["dashes"], # line dashing
                                even_odd = path.get("even_odd", True), # control color of overlaps
                                closePath = path["closePath"], # whether to connect last and first point
                                lineJoin = path["lineJoin"], # how line joins should look like
                                lineCap = max(path["lineCap"]), # how line ends should look like
                                width = path["width"], # line width
                                stroke_opacity = path.get("stroke_opacity", 1), # same value for both
                                fill_opacity = path.get("fill_opacity", 1), # opacity parameters
                            )
                    shape.commit()
                
                oUTPUT.save(f"{cDIR}/outPut.pdf", garbage = 3, deflate = True)
        
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
            file_name = FILE_NAME, quote = True, document = f"{cDIR}/outPut.pdf", thumb = THUMBNAIL,
            caption = FILE_CAPT, progress = uploadProgress, progress_args = (dlMSG, time.time()) 
        )
        await dlMSG.delete()
        await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)
        await work(callbackQuery, "delete", False)

#                                                                                             Telegram: @nabilanavab
