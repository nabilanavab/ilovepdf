# fileName : plugins/dm/callBack/file_process/mergePDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/mergePDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz, os, time
from plugins.utils    import *
from configs.config   import settings

if settings.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * (10 ** 6)
else:
    MAX_FILE_SIZE = False

async def askPDF(bot, callbackQuery, question: str, size: str) -> ( bool, list ):
    """
    return a list of pdf files ID saved on telegram
    """
    try:
        mergeId = [callbackQuery.message.reply_to_message.document.file_id]
        size = callbackQuery.message.reply_to_message.document.file_size
        
        while len(mergeId) <= 10:
            input_file = await bot.ask(
                chat_id = callbackQuery.from_user.id,
                reply_to_message_id = callbackQuery.message.id,
                text = question.format(len(mergeId)), filters = None,
            )
            if input_file.text == "/exit":
                return False, input_file
            elif input_file.text == "/merge" and len(mergeId) >= 2:
                return True, mergeId
            elif input_file.document:
                if (MAX_FILE_SIZE and MAX_FILE_SIZE_IN_kiB <= int(size)) or int(size) >= 2000000000:
                    await callbackQuery.message.reply(
                        size %(MAX_FILE_SIZE if MAX_FILE_SIZE else "1.8Gb")
                    )
                    return True, mergeId
                mergeId.append(input_file.document.file_id)
                size += input_file.document.file_size
        return (True, mergeId) if input_file.text != "/exit" else (False, input_file)
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

async def mergePDF(input_file: str, cDIR: str, mergeId: list, bot, callbackQuery, dlMSG) -> ( bool, str):
    """
    This function helps to merge multiple PDF files into a single PDF file. It takes a list of
    PDF file paths as input and combines them into one output PDF file. This can be useful for
    combining multiple documents into a single file or for creating a single document from
    multiple chapters or sections
    
    parameter:
        input_file    : Here is the path of the file that the user entered
        cDIR          : This is the location of the directory that belongs to the specific user.
        mergeId       : List of pdf files to merge
        
    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        output_path = f"{cDIR}/outPut.pdf"
        
        file_number = 0
        # 1st or imput pdf is already downloaded
        for iD in mergeId[1:]:
            # edit 
            downloadLoc = await bot.download_media(
                message = iD, file_name = f"{cDIR}/{file_number}.pdf", progress = render.progress, 
                progress_args = (mergeId[file_number], dlMSG, time.time())
            )
            checked, noOfPg = await render.checkPdf(f"{cDIR}/{file_number}.pdf", callbackQuery)
            if not(checked == "pass"):
                os.remove(f"{cDIR}/{file_number}.pdf")
        
        directory = f'{cDIR}'
        pdfList = [os.path.join(directory, file) for file in os.listdir(directory)]
        pdfList.sort(key = os.path.getctime)
        
        with fitz.open() as result:
            for pdf in pdfList:
                with fitz.open(pdf) as mfile:
                    result.insert_pdf(mfile)
            result.save(output_path)
            
        return True, output_path
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
