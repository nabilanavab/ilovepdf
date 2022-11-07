# fileName : plugins/dm/generate.py
# copyright ©️ 2021 nabilanavab

from pdf import PDF
from .photo import HD
from logger import logger
from pyromod import listen
from configs.log import log
import asyncio, os, shutil, fitz
from pyrogram.types import ForceReply
from configs.config import images as im
from plugins.render import header, cbPRO
from plugins.thumbName import thumbName, formatThumb
from pyrogram import enums, filters, Client as ILovePDF
from plugins.util import getLang, translate, createBUTTON

# ========================================================================| GENERATE PDF FROM IMAGES |=================================================================
GEN = filters.create(lambda _, __, query: query.data.startswith("generate"))
@ILovePDF.on_callback_query(GEN)
async def _GEN(bot, callbackQuery):
    try:
        chat_id = callbackQuery.from_user.id
        lang_code = await getLang(chat_id)
        
        images = PDF.get(chat_id)
        if isinstance(PDF.get(chat_id), list):
            pgnmbr = len(PDF[chat_id])
            del PDF[chat_id]
        
        if (not(images) and chat_id not in HD) or (chat_id in HD and len(HD[chat_id]) == 1):
            tTXT, tBTN = await translate(text="GENERATE['noImages']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        await callbackQuery.answer()
        
        if callbackQuery.data[-3:] == "REN":
            tTXT, tBTN = await translate(text="GENERATE['getFileNm']", lang_code=lang_code)
            fileName = await bot.ask(
                chat_id = chat_id, reply_to_message_id = callbackQuery.message.id,
                text = tTXT, reply_markup = ForceReply(True)
            )
            if (not fileName.text) or len(fileName.text)>50:
                fileName = f"{chat_id}.pdf"
            else:
                if fileName.text[-4:].lower() != ".pdf":
                    fileName = fileName.text + ".pdf"
                else:
                    fileName = fileName.text
        else:
            fileName = f"{chat_id}.pdf"
        
        tTXT, tBTN = await translate(text="GENERATE['geting']", button="GENERATE['getingCB']", lang_code=lang_code)
        if not images:
            pgnmbr = len(HD[chat_id])-1
        gen = await callbackQuery.message.reply_text(
            tTXT.format(fileName, pgnmbr), reply_markup=tBTN, quote=False
        )
        
        filePath = f"{chat_id}/{callbackQuery.message.id}.pdf"
        if chat_id not in HD:
            images[0].save(filePath, save_all=True, append_images=images[1:])
        else:
            tTXT, tBTN = await translate(text="GENERATE['currDL']", button="GENERATE['getingCB']", lang_code=lang_code)
            for i, ID in enumerate(HD[chat_id]):
                if i == 0:
                    continue    # HD mode shift: messageID
                await gen.edit(tTXT.format(i, len(HD[chat_id])), reply_markup=tBTN)
                await bot.download_media(message=ID, file_name=f"{chat_id}/{i}.jpg")
                
            imgList = [os.path.join(f"{chat_id}", file) for file in os.listdir(f"{chat_id}")]
            imgList.sort(key = os.path.getctime)
            
            tTXT, tBTN = await translate(text="GENERATE['geting']", button="GENERATE['getingCB']", lang_code=lang_code)
            await gen.edit(tTXT.format(fileName, pgnmbr), reply_markup=tBTN)
            
            with fitz.open() as doc:
                for img in imgList:
                    try:
                        with fitz.open(img) as hdIMG:
                            rect = hdIMG[0].rect
                            pdfbytes = hdIMG.convert_to_pdf()
                            imgPDF = fitz.open("pdf", pdfbytes)
                            page = doc.new_page(width=rect.width, height=rect.height)
                            page.show_pdf_page(rect, imgPDF, 0)
                    except Exception: pass
                try: await bot.delete_messages(chat_id=chat_id, message_ids=HD[chat_id][0])
                except Exception: pass
                doc.save(filePath, deflate_images=True)
                del HD[chat_id]
        
        # Getting thumbnail
        FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(callbackQuery.message, fileName)
        if im.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(
                message = THUMBNAIL,
                file_name = f"{callbackQuery.message.id}.jpeg"
            )
            THUMBNAIL = await formatThumb(location)
        
        tTXT, tBTN = await translate(button="PROGRESS['upFileCB']", lang_code=lang_code)
        await gen.edit_reply_markup(tBTN)
        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        tTXT, tBTN = await translate(text="GENERATE['geting']", lang_code=lang_code)
        logFile = await callbackQuery.message.reply_document(
            document = filePath, caption = f"{tTXT.format(fileName, pgnmbr)}\n\n{FILE_CAPT}",
            file_name = FILE_NAME, thumb = THUMBNAIL, progress = cbPRO,
            progress_args = (gen, 0, "UPLOADED", True)
        )
        await gen.delete(); shutil.rmtree(f"{chat_id}")
        try: os.remove(location)
        except Exception: pass
        await log.footer(callbackQuery.message, output=logFile, lang_code=lang_code)
    except Exception as e:
        tTXT, tBTN = await translate(text="document['error']", button="checkPdf['errorCB']", lang_code=lang_code)
        await gen.edit(tTXT.format(e), reply_markup=tBTN)
        try: shutil.rmtree(f"{chat_id}"); del HD[chat_id]
        except Exception: pass

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
