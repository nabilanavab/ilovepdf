# fileName : plugins/dm/callBack/file_process/previewPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/previewPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

media = {}

# LOGGING INFO: DEBUG
from logger import logger

import              os, fitz
from pyrogram       import enums
from PIL            import Image
from asyncio        import sleep
from pdf            import pyTgLovePDF
from telebot.types  import InputMediaPhoto

async def previewPDF(input_file: str, cDIR: str, callbackQuery) -> ( bool, str ):
    try:
        """
        This function returns PDF images with their metadata.
        If the PDF has 10 or fewer pages, all pages are included.
        If the PDF has more than 10 pages, the function returns the first three pages,
        the last three pages, and three or four pages from the middle of the document
        depending on whether the document has an odd or even number of pages.
        
        parameter:
            input_file    : Here is the path of the file that the user entered
            cDIR          : This is the location of the directory that belongs to the specific user.
            callbackQuery : callbackQuery message 
        
        return:
            bool          : Return True when the request is successful
            output_path   : This is the path where the output file can be found.
        """
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            
            if iNPUT.page_count <= 10:
                preview = list(range(1, iNPUT.page_count + 1))
            else:
                preview = [0, 1, 2] + list(range(iNPUT.page_count//2 - 1, iNPUT.page_count//2 + 2)) + [-3, -2, -1]
            
            pdfMetaData = "".join(f"`{i} : {iNPUT.metadata[i]}`\n" for i in iNPUT.metadata if iNPUT.metadata[i] != "") if iNPUT.metadata else ""
            
            mat = fitz.Matrix(2, 2)
            os.mkdir(f'{cDIR}/pgs')
            for pageNo in preview:
                pix = iNPUT.load_page(int(pageNo) - 1).get_pixmap(matrix = mat)
                # SAVING PREVIEW IMAGE
                with open(f'{cDIR}/pgs/{pageNo}.jpg','wb'):
                    pix.save(f'{cDIR}/pgs/{pageNo}.jpg')
            
            directory = f'{cDIR}/pgs'
            imag = [os.path.join(directory, file) for file in os.listdir(directory)]
            imag.sort(key = os.path.getctime)
            media[chat_id] = []
            
            for file in imag:
                await sleep(0.5)
                qualityRate = 95
                # print("size: ",file, " ",os.path.getsize(file)) LOG MESSAGE
                # FILES WITH 10MB+ SIZE SHOWS AN ERROR FROM TELEGRAM 
                # SO COMPRESS UNTIL IT COMES LESS THAN 10MB.. :(
                if os.path.getsize(file) >= 1000000:
                    picture = Image.open(file)
                    picture.save(file, "JPEG", optimize = True, quality = qualityRate)
                    qualityRate -= 5
                # ADDING TO GROUP MEDIA IF POSSIBLE
                else:
                    if len(media[callbackQuery.message.chat.id]) == 1:
                        media[callbackQuery.message.chat.id].append(InputMediaPhoto(
                                media = open(file, "rb"), caption = caption, parse_mode = "Markdown"
                                )
                            )
                    else:
                        media[callbackQuery.message.chat.id].append(
                            InputMediaPhoto(media = open(file, "rb"))
                            )
                    break
            
            if await work(callbackQuery, "check", False):
                await dlMSG.edit(CHUNK["upload"], reply_markup = _)
                await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                await pyTgLovePDF.send_media_group(
                    callbackQuery.message.chat.id,
                    media[callbackQuery.message.chat.id],
                    reply_to_message_id = callbackQuery.message.id
                )
            del media[callbackQuery.message.chat.id]
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
