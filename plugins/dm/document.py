# fileName : plugins/dm/document.py
# copyright ©️ 2021 nabilanavab

import convertapi
from pdf import PDF
from .photo import HD
from PIL import Image
import os, time, fitz
import shutil, asyncio
from pdf import PROCESS
from logger import logger
from plugins.util import *
from configs.log import log
from configs.db import DATA
from plugins.render import *
from pyrogram import filters, enums
from pyrogram import Client as ILovePDF
from configs.config import settings, images
from plugins.thumbName import thumbName, formatThumb

try:
    import aspose.words as word
    wordSupport = True
except Exception:
    wordSupport = False

# ========================================| MAXIMUM FILE SIZE (IF IN config var.) |====================================================================================
if settings.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = int(settings.MAX_FILE_SIZE) * (10 **6 )
else:
    MAX_FILE_SIZE = False

# =============================================================================| FILES TO PDF [SUPPORTED CODECS] |=====================================================
img2pdf = [
    ".jpg", ".jpeg", ".png"
]                                       # Img to pdf file support

pymu2PDF = [
    ".xps", ".oxps",
    ".cbz", ".fb2", ".epub"
]                                      # files to pdf (zero limits)

wordFiles = [
    ".dot", ".bmp", ".gif", ".pcl",
    ".dotx", ".dotm", ".flatOpc", ".html",
    ".mhtml", ".md", ".xps", ".svg", ".tiff",
    ".txt", ".mobi", ".chm", ".emf", ".ps", 
]

cnvrt_api_2PDF = [
    ".csv", ".log", ".mpp", ".mpt", ".odt", ".pot", ".potx", ".pps",
    ".ppsx", ".ppt", ".pptx", ".pub", ".rtf", ".txt", ".vdx", ".vsd",
    ".vsdx", ".vst", ".vstx", ".wpd", ".wps", ".wri", ".xls", ".xlsb",
    ".xlsx", ".xlt", ".xltx", ".xml", ".docx", ".doc"
]                                       # file to pdf (ConvertAPI limit)

# ==================| PYMUPDF FILES TO PDF |===========================================================================================================================
async def pymuConvert2PDF(message, edit, input_file, lang_code):
    try:
        with fitz.open(input_file) as doc:
            with fitz.open("pdf", doc.convert_to_pdf()) as pdf:
                pdf.save(f"{message.id}/outPut.pdf", garbage=4, deflate=True,)
        return True
    except Exception as e:
        tTXT, tBTN = await translate(text="document['error']", lang_code=lang_code)
        await edit.edit(
            text = tTXT.format(e),
            reply_markup = await createBUTTON(btn={"👍" : "try+", "👎" : "try-"})
        )
        return False

# ================================| ConvertAPI FILES TO PDF |=========================================================================================================
async def cvApi2PDF(message, edit, input_file, lang_code, API):
    try:
        convertapi.api_secret = API
        fileNm, fileExt = os.path.splitext(input_file)
        convertapi.convert(
            "pdf", {"File": f"{input_file}"}, from_format = fileExt[1:],
        ).save_files(f"{message.id}/outPut.pdf")
        return True
    except Exception as e:
        tTXT, tBTN = await translate(text="document['error']", lang_code=lang_code)
        await edit.edit(tTXT.format(e))
        return False

# =================================================================================================================================| WORD FILES TO PDF |===============
async def word2PDF(message, edit, input_file, lang_code):
    try:
        doc = word.Document(input_file)
        doc.save(f"{message.id}/outPut.pdf")
        return True
    except Exception as e:
        tTXT, tBTN = await translate(text="document['error']", lang_code=lang_code)
        await edit.edit(tTXT.format(e))
        return False

# ====================================================================================| REPLY TO DOC. FILES |==========================================================
@ILovePDF.on_message(filters.private & filters.incoming & filters.document)
async def documents(bot, message):
    try:
        # refresh causes error ;) so, try
        try: await message.reply_chat_action(enums.ChatAction.TYPING)
        except Exception: pass
        lang_code = await getLang(message.chat.id)
        CHUNK, _ = await translate(text="document", lang_code=lang_code)
        if message.from_user.id in PROCESS:
            tBTN = await createBUTTON(await editDICT(inDir=CHUNK["refresh"], value="refresh"))   # sends refresh msg if any
            return await message.reply_text(CHUNK["inWork"], reply_markup=tBTN, quote=True)   # work exists
        org_file_name = message.document.file_name        # file name
        fileSize = message.document.file_size             # file size
        fileNm, fileExt = os.path.splitext(org_file_name) # seperate name & extension
        
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            tBTN = await createBUTTON(CHUNK["bigCB"])
            return await message.reply_photo(
                photo = images.BIG_FILE, caption = CHUNK["big"].format(MAX_FILE_SIZE, MAX_FILE_SIZE),
                reply_markup = tBTN
            )
        # REPLY TO .PDF FILE EXTENSION
        elif fileExt.lower() == ".pdf":
            pdfMsgId = await message.reply_text(CHUNK["process"] ,quote=True)
            await asyncio.sleep(0.5)
            await pdfMsgId.edit(CHUNK["process"] + ".")
            await asyncio.sleep(0.5)
            tBTN = await createBUTTON(CHUNK["replyCB"])
            await pdfMsgId.edit(
                text = CHUNK["reply"].format(org_file_name, await gSF(fileSize)), reply_markup = tBTN
            )
            logFile = message
        
        # IMAGE AS FILES (ADDS TO PDF FILE)
        elif fileExt.lower() in img2pdf:
            try:
                if message.chat.id in HD:
                    if len(HD[message.chat.id]) >= 16:
                       return
                    HD[message.chat.id].append(message.document.file_id)
                    generateCB = "document['generate']" if settings.DEFAULT_NAME else  "document['generateRN']"
                    tTXT, tBTN = await translate(text="document['imageAdded']", button=generateCB, lang_code=lang_code)
                    return await message.reply_text(tTXT.format(len(HD[message.chat.id])-1, message.chat.id)+" [HD] 🔰", reply_markup = tBTN, quote=True)
                imageDocReply = await message.reply_text(CHUNK["download"], quote=True)
                if not isinstance(PDF.get(message.from_user.id), list):
                    PDF[message.from_user.id] = []
                await message.download(f"{message.from_user.id}/{message.from_user.id}.jpg")
                img = Image.open(
                          f"{message.from_user.id}/{message.from_user.id}.jpg"
                      ).convert("RGB")
                PDF[message.from_user.id].append(img)
                generateCB = "generate" if settings.DEFAULT_NAME else "generateRN"
                tBTN = await createBUTTON(CHUNK[generateCB])
                return await imageDocReply.edit(
                    text = CHUNK["imageAdded"].format(len(PDF[message.from_user.id]), message.from_user.id), reply_markup = tBTN
                )
            except Exception as e:
                return await imageDocReply.edit(CHUNK["error"].format(e))
        
        # FILES TO PDF
        elif (fileExt.lower() in pymu2PDF) or (fileExt.lower() in cnvrt_api_2PDF) or (fileExt.lower() in wordFiles):
            
            if (fileExt.lower() in cnvrt_api_2PDF) and (((not DATA.get(message.chat.id, 0) \
                or (DATA.get(message.chat.id, 0) and not DATA.get(message.chat.id, 0)[0])) \
                and settings.CONVERT_API is False)):
                return await message.reply_text(CHUNK["noAPI"], quote = True)
            
            if (fileExt.lower() in wordFiles) and not wordSupport:
                return await message.reply_text(CHUNK["useDOCKER"], quote = True)
            
            PROCESS.append(message.from_user.id)
            tBTN = await createBUTTON(CHUNK["cancelCB"])
            pdfMsgId = await message.reply_text(CHUNK["download"], reply_markup=tBTN, quote = True)
            input_file = f"{message.id}/input_file{fileExt}"
            # DOWNLOAD PROGRESS
            downloadLoc = await bot.download_media(
                message = message.document.file_id, file_name = input_file, progress = progress,
                progress_args = (message.document.file_size, pdfMsgId, time.time())
            )
            # CHECKS PDF DOWNLOADED OR NOT
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            await pdfMsgId.edit(CHUNK['takeTime'], reply_markup=tBTN)
            
            # WHERE REAL CODEC CONVERSATION OCCURS
            if fileExt.lower() in pymu2PDF:
                FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(message, f"{fileNm}.pdf")
                isError = await pymuConvert2PDF(message, pdfMsgId, input_file, lang_code)
            
            elif fileExt.lower() in cnvrt_api_2PDF:
                FILE_NAME, FILE_CAPT, THUMBNAIL, API = await thumbName(message, f"{fileNm}.pdf", getAPI=True)
                API = API if not(API == False) else settings.CONVERT_API
                isError = await cvApi2PDF(message, pdfMsgId, input_file, lang_code, API)
            
            elif fileExt.lower() in wordFiles:
                FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(message, f"{fileNm}.pdf")
                isError = await word2PDF(message, pdfMsgId, input_file, lang_code)
            
            if not isError:
                PROCESS.remove(message.from_user.id)
                shutil.rmtree(f"{message.id}")
                return
            
            if images.PDF_THUMBNAIL != THUMBNAIL:
                location = await bot.download_media(message = THUMBNAIL, file_name = f"{message.id}.jpeg")
                THUMBNAIL = await formatThumb(location)
            
            await pdfMsgId.edit(CHUNK['upFile'], reply_markup=tBTN)
            await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
            logFile = await message.reply_document(
                file_name = FILE_NAME, document = open(f"{message.id}/outPut.pdf", "rb"),
                thumb = THUMBNAIL, caption = CHUNK["fromFile"].format(fileExt, "pdf") + f"\n\n{FILE_CAPT}",
                quote = True, progress = uploadProgress, progress_args = (pdfMsgId, time.time()),
                reply_markup = await createBUTTON(btn={"👍" : "try+", "👎" : "try-"}) if fileExt.lower() in pymu2PDF else None
            )
            await pdfMsgId.delete(); PROCESS.remove(message.from_user.id); shutil.rmtree(f"{message.id}")
        
        # UNSUPPORTED FILES
        else:
            return await message.reply_text(CHUNK["unsupport"], quote=True)
        
        await log.footer(message, output=logFile, lang_code=lang_code)
    except Exception as e:
        logger.exception("plugins/dm/document: %s" %(e), exc_info=True)
        try: shutil.rmtree(f"{message.id}")
        except Exception:
            try: PROCESS.remove(message.from_user.id)
            except Exception: pass

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
