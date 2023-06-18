file_name = "plugins/dm/textToPdf/handler.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

import                    os, re
from plugins.utils        import *
from configs.log          import log
from fpdf                 import FPDF
from PIL                  import Image
from logger               import logger
from arabic_reshaper      import reshape
from pyrogram.types       import ForceReply
from bidi.algorithm       import get_display
from configs.config       import settings, images
from pyrogram             import filters, Client as ILovePDF, enums
from .                    import FONT, COLOR, BACKGROUND_L, BACKGROUND_P, SCALE, TXT


async def ask_for_title(bot, callbackQuery, text: str, num: int = False):
    while(text):
        askTEXT = await bot.ask(text=text.format(num), chat_id=callbackQuery.message.chat.id,
                               reply_to_message_id=callbackQuery.message.id, filters=None,
                               reply_markup = ForceReply(True))
        
        if askTEXT.text:
            if askTEXT.text == "/exit":
                return False, askTEXT.text
            elif askTEXT.text == "/skip":
                return True, None
            return True, askTEXT.text
        # return isSuccess, result

async def ask_for_paragraph(bot, callbackQuery, text: str, num: int = False):
    while(text):
        askTEXT = await bot.ask(text=text.format(num), chat_id=callbackQuery.message.chat.id,
                               reply_to_message_id=callbackQuery.message.id, filters=None,
                               reply_markup = ForceReply(True))
        
        if askTEXT.text:
            if askTEXT.text == "/exit":
                return False, askTEXT.text
            elif askTEXT.text == "/skip":
                return True, None
            return True, askTEXT.text
        elif askTEXT.photo:
            return True, { 'type': 'photo', 'id': askTEXT.photo.file_id,
                          'caption': askTEXT.caption if askTEXT.caption else None}

async def ask_for_bg(bot, callbackQuery, text: str):
    askBG = await bot.ask(text=text, chat_id=callbackQuery.message.chat.id,
                          reply_to_message_id=callbackQuery.message.id, filters=None,
                          reply_markup = ForceReply(True))
        
    if askBG.photo:
        return askBG.photo.file_id
    else:
        return 1

@ILovePDF.on_callback_query(filters.regex("^t2p.*:$"))
async def text_to_pdf(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        
        cDIR = await work.work(callbackQuery, "create", False)
        if not cDIR:
            tTXT, _ = await util.translate(text="_W_I_P", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        await callbackQuery.answer()
        
        CHUNK, _ = await util.translate(text="pdf2TXT", lang_code=lang_code)
        _, scale, h_font, p_font, color, background = [int(i) if i.isdigit() else 1 for i in callbackQuery.data.replace(":", "").split('|')]
        
        if background==9:
            background = await ask_for_bg(bot, callbackQuery=callbackQuery, text="send me an image")
        
        TXT[callbackQuery.message.chat.id] = []
        isSuccess, title = await ask_for_title(bot, callbackQuery=callbackQuery, text=CHUNK['askT'])
        if not isSuccess:
            await callbackQuery.message.reply(CHUNK['exit'], quote=True)
            del TXT[callbackQuery.message.chat.id]; return await work.work(callbackQuery, "delete", False)
        else:
            TXT[callbackQuery.message.chat.id].append(None if title is None else title[:20])
        
        nabilanavab = True
        while(nabilanavab):
            isSuccess, paragraph = await ask_for_paragraph(bot, callbackQuery=callbackQuery, text=CHUNK['askC'],
                                                               num=len(TXT[callbackQuery.message.chat.id]))
            if not isSuccess:
                await callbackQuery.message.reply(CHUNK['exit'], quote=True)
                del TXT[callbackQuery.message.chat.id]; return await work.work(callbackQuery, "delete", False)
            elif isSuccess and isinstance(paragraph, str) and paragraph == "/create":
                if TXT[callbackQuery.message.chat.id][0] == None and len(TXT[callbackQuery.message.chat.id]) == 1:
                    await callbackQuery.message.reply(CHUNK['nothing'], quote=True)
                else:
                    processMessage = await callbackQuery.message.reply(CHUNK['start'], quote=True)
                    nabilanavab = False
            elif isinstance(paragraph, str):
                TXT[callbackQuery.message.chat.id].append(f"{paragraph}")
            elif isinstance(paragraph, dict):
                TXT[callbackQuery.message.chat.id].append(paragraph)
        
        pdf = FPDF(orientation=SCALE[scale], format="A4")
        
        if not BACKGROUND_L.get(background, False):
            background = await bot.download_media(message=background, file_name=f"{cDIR}/")
            pdf.set_page_background(background)
        else:
            pdf.set_page_background(BACKGROUND_L[background]['code'])

        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()
        pdf.set_text_color( *COLOR[color]['code'] )
        
        pdf.set_title("NABIL A NAVAB")
        pdf.set_subject("pdf created using nabilanavab open source Telegram Pdf Bot\n\nContact Nabil A Navab: telegram.dog/nabilanavab ❤")
        pdf.set_author("https://github.com/nabilanavab/ilovepdf")
        pdf.set_producer("by nabilanavab@gmail.com")
        
        pdf.add_font('headFont', '', FONT[h_font], uni=True)
        pdf.set_font('headFont', '', size=30)

        if scale == 1 and BACKGROUND_L.get(background, False):
            POSITION = BACKGROUND_L[background]['position']
        elif scale == 2 and BACKGROUND_P.get(background, False):
            POSITION = BACKGROUND_P[background]['position']
        else:
            POSITION = ['w', 20, 'w', 10]
        
        if TXT[callbackQuery.message.chat.id][0] != None:
            pdf.cell(pdf.w if POSITION[0]=='w' else POSITION[0], POSITION[1],
                     txt=get_display(reshape(TXT[callbackQuery.message.chat.id][0])), ln=True, align="C")
        
        pdf.add_font('paraFont', '', FONT[p_font], uni=True)
        pdf.set_font('paraFont', '', size=20)

        for para in TXT[callbackQuery.message.chat.id][1:]:
            # pdf.set_x(10)
            if isinstance(para, str):
                pdf.multi_cell(pdf.w-20 if POSITION[2]=='w' else POSITION[2], POSITION[3],
                               txt=get_display(reshape(f"     {para}")), ln=True, align="L")
            if isinstance(para, dict):
                if para['type']=='photo':
                    logger.debug(para['caption'])
                    link=para['caption'] if para['caption'] and re.match(r"^(http|https|ftp)://[^\s/$.?#].[^\s]*$", para['caption']) else ''
                    img = await bot.download_media(message=para['id'], file_name=f"{cDIR}/")
                    with Image.open(img) as image, pdf.local_context(blend_mode="Multiply"):
                        image_width, image_height = image.size
                        pdf_width, pdf_height = pdf.w, pdf.h
                        if image_width > pdf_width or image_height > pdf_height:
                            scale_width = pdf_width / image_width
                            scale_height = pdf_height / image_height
                            scale_factor = min(scale_width, scale_height)
                            new_width = int(image_width * scale_factor)
                            new_height = int(image_height * scale_factor)
                            x = (pdf_width - new_width) / 2
                            y = pdf.get_y()
                            if y + new_height > pdf_height:
                                pdf.add_page(); y = pdf.get_y()
                            pdf.image(img, x, y, new_width, new_height, link=link)
                            pdf.ln(new_height+10)
                        else:
                            x = (pdf_width - image_width) / 2
                            y = pdf.get_y()
                            if y + new_height > pdf_height:
                                pdf.add_page(); y = pdf.get_y()
                            pdf.image(img, x, y, image_width, image_height, link=link)
                            pdf.ln(image_height+10)
                
        pdf.output(f"{cDIR}/{callbackQuery.message.chat.id}.pdf")
        
        FILE_NAME, FILE_CAPT, THUMBNAIL = await fncta.thumbName(callbackQuery.message, f"{callbackQuery.message.chat.id}.pdf")
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(message = THUMBNAIL, file_name = f"{cDIR}/{callbackQuery.message.id}.jpeg")
            THUMBNAIL = await formatThumb(location)
        
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await processMessage.edit(CHUNK['upload'])
        logFile = await callbackQuery.message.reply_document(
            file_name=FILE_NAME, caption=FILE_CAPT, quote=True, thumb=THUMBNAIL,
            document=open(f"{cDIR}/{callbackQuery.message.chat.id}.pdf", "rb")
        )
        await processMessage.delete()
        await log.footer(callbackQuery.message, output=logFile, lang_code=lang_code)
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info=True)
        await processMessage.edit(CHUNK['error'].format(Error))
    finally:
        del TXT[callbackQuery.message.chat.id]
        await work.work(callbackQuery, "delete", False)

# SOURCE CODE: "https://github.com/nabilanavab/ilovepdf"
