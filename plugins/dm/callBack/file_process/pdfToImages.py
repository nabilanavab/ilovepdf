# fileName : plugins/dm/callBack/file_process/pdfToImages.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/pdfToImages.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz, os, shutil, asyncio
from plugins.utils  import *
from PIL            import Image
from pyromod        import listen
from pyrogram.types import ForceReply
from pdf            import pyTgLovePDF
from pyrogram       import filters, enums
from telebot.types  import InputMediaPhoto, InputMediaDocument

media = {}

async def askimageList(bot, callbackQuery, question, limit: int = 1000) -> ( bool, list ):
    """
    return a list with a specific range of numbers and some specific values from the input
    
    eg:
        '18:20,4,5,1:3'
        [1, 2, 3, 4, 5, 18, 19, 20]    <---return
    """
    try:
        input_str = await bot.ask(
            chat_id = callbackQuery.from_user.id,
            reply_to_message_id = callbackQuery.message.id,
            text = question, filters = filters.text,
            reply_markup = ForceReply(True, "Eg: 7:13 [start:end], 2, 3, 21:27..")
        )
        my_list = []
        for elem in input_str.text.split(','):
            try:
                if ':' in elem:
                    start, end = map(int, elem.split(':'))
                    my_list.extend(range(start, end+1, 1))
                else:
                    my_list.append(int(elem))
            except ValueError:
                pass
        my_list = sorted(set([x for x in my_list if isinstance(x, int) and x <= limit]))
        return (True, my_list) if len(my_list) != 0 else (False, input_str)
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

async def pdfToImages(input_file: str, cDIR: str, callbackQuery, dlMSG, imageList: list, text: str) -> ( bool, str):
    """
     function that allows you to fetch pages from a PDF file. Essentially, this means that you can extract specific pages
     from a large PDF document without having to download the entire file. For example, if you only need a few pages from a
     200-page PDF, you can use this function to extract just those pages and save yourself a lot of time and data usage.
     This feature is especially helpful for users who frequently work with large PDF documents and need to extract specific
     information quickly and efficiently.
    
    parameter:
        input_file    : Here is the path of the file that the user entered
        cDIR          : This is the location of the directory that belongs to the specific user.
        imageList     : List of page numbers that the user requires
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
        
        imageType = "Img" if callbackQuery.data.startswith("#p2img|I") else "Doc"
        with fitz.open(input_file) as doc:
            number_of_pages = doc.page_count
            if callbackQuery.data.endswith("A"): imageList = list(range(1, number_of_pages+1))
            mat = fitz.Matrix(2, 2)
            if len(imageList) >= 11:
                await dlMSG.pin(disable_notification = True, both_sides = True)
            await dlMSG.edit(text=text["_total"].format(len(imageList)), reply_markup=cancel)
            
            convertedPages = 0
            for i in range(0, len(imageList), 10):
                pgList = imageList[i:i+10]
                os.mkdir(f'{cDIR}/pgs')
                
                for pageNo in pgList:
                    if int(pageNo) <= int(number_of_pages):
                        page = doc.load_page(int(pageNo)-1)
                        pix = page.get_pixmap(matrix=mat)
                    else:
                        continue
                    convertedPages += 1
                    if convertedPages % 5 == 0:
                        if not await work.work(callbackQuery, "check", False):
                            return await dlMSG.edit(text=text["_canceledAT"].format(convertedPages, len(imageList)), reply_markup=canceled)
                    with open(f'{cDIR}/pgs/{pageNo}.jpg','wb'):
                        pix.save(f'{cDIR}/pgs/{pageNo}.jpg')
                
                directory = f'{cDIR}/pgs'
                imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                imag.sort(key = os.path.getctime)
                
                media[callbackQuery.message.chat.id] = []
                for file in imag:
                    qualityRate = 95
                    for i in range(200):
                        if os.path.getsize(file) >= 1000000:
                            picture = Image.open(file)
                            picture.save(file, "JPEG", optimize = True,quality = qualityRate)
                            qualityRate -= 5; await asyncio.sleep(0.5)
                        else:
                            if imageType == "Img":
                                media[callbackQuery.message.chat.id].append(InputMediaPhoto(open(file, "rb")))
                            elif imageType == "Doc":
                                media[callbackQuery.message.chat.id].append(InputMediaDocument(open(file, "rb")))
                            break
                try:
                    await dlMSG.edit(text=text["_upload"].format(convertedPages, len(imageList)), reply_markup=cancel)
                except Exception: pass
                
                if imageType == "Img":
                    await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                elif imageType == "Doc":
                    await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                
                try:
                    await pyTgLovePDF.send_media_group(callbackQuery.message.chat.id, media[callbackQuery.message.chat.id])
                except Exception as e:
                    wait = str(e).rsplit(' ', 1)[1]; await asyncio.sleep(int(wait))
                    media[callbackQuery.message.chat.id] = []
                    for file in imag:
                        media[callbackQuery.message.chat.id].append(InputMediaPhoto(open(file, "rb")))
                    await pyTgLovePDF.send_media_group(callbackQuery.message.chat.id, media[callbackQuery.message.chat.id])
                shutil.rmtree(f'{cDIR}/pgs')
            await dlMSG.edit(text=text["finished"], reply_markup=completed)
            return "finished", "finished"
    except Exception as Error:
        shutil.rmtree(f'{cDIR}/pgs')
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
