# fileName : plugins/dm/callBack/file_process/messagePDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/messagePDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz
from plugins.utils         import *
from pyrogram.errors       import FloodWait

async def messagePDF(input_file: str, cDIR: str, callbackQuery, dlMSG, text: str) -> ( bool, str):
    """
    Function that allows you to fetch pages from a PDF file. Essentially, this means that you can extract specific pages
    from a large PDF document without having to download the entire file. For example, if you only need a few pages from a
    200-page PDF, you can use this function to extract just those pages and save yourself a lot of time and data usage.
    This feature is especially helpful for users who frequently work with large PDF documents and need to extract specific
    information quickly and efficiently.
    
    parameter:
        input_file    : Here is the path of the file that the user entered
        cDIR          : This is the location of the directory that belongs to the specific user.
        dlMSG         : Edit Message progress bar
        text          : Edit Message Content [progress]
        callbackQuery : CallbackQuery 
        
    return:
        "finished"    : Return finished when the request is successful
        "finished"    : Return finished when the request is successful
    """
    try:
        cancel = await util.createBUTTON(btn=text["_cancelCB"])
        canceled = await util.createBUTTON(btn=text["_canceledCB"])
        completed = await util.createBUTTON(btn=text["_completed"])
        
        with fitz.open(input_file) as doc:
            if doc.page_count >= 3:
                await dlMSG.pin(disable_notification=True, both_sides=True)
            for page in doc:
                pageNo = int(str(page).split(" ")[1])+1
                pdfText = page.get_text()
                if 1 <= len(pdfText) <= 1000:
                    try:
                        await callbackQuery.message.reply(f"```🅿🅰🅶🅴 : {pageNo}\n\n{pdfText}```\n@ilovepdf_bot", quote=pageNo==1)
                    except FloodWait as e:
                        await asyncio.sleep(e.value+1)
                        await callbackQuery.message.reply(f"{pdfText}", quote=False)
                elif 1000 <= len(pdfText):
                    slice = [pdfText[i: i+1000] for i in range(0, len(pdfText), 1000)]
                    for i, j in enumerate(slice, start=1):
                        try:
                            await callbackQuery.message.reply(f"```🅿🅰🅶🅴 : {pageNo}-{i}\n\n{j}```\n\n@ilovepdf_bot", quote=pageNo==1)
                        except FloodWait as e:
                            await asyncio.sleep(e.value+1)
                            await callbackQuery.message.reply(f"{pdfText}", quote=False)
                if await work.work(callbackQuery, "check", False):
                    try:
                        await dlMSG.edit("------- {}".format(pageNo), reply_markup=cancel)
                    except Exception: pass
        return "finished", "finished"
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
