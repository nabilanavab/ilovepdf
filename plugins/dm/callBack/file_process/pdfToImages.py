# fileName : plugins/dm/callBack/file_process/combinePages.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/combinePages.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz, os, shutil, asyncio
from PIL            import Image
from pyromod        import listen
from pyrogram       import filters
from pyrogram.types import ForceReply
from pdf            import pyTgLovePDF
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
        return (True, my_list) if len(my_list) != 0 else (False, my_list)
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

async def pdfToImages(input_file: str, cDIR: str, callbackQuery, dlMSG, imageList: list) -> ( bool, str):
    """
    
    
    
    """
    try:
        imageType = callbackQuery.data[1:]
        with fitz.open(input_file) as doc:
            number_of_pages = doc.page_count
            mat = fitz.Matrix(2, 2)
            if len(imageList) >= 11:
                await dlMSG.pin(disable_notification = True, both_sides = True)
            #await dlMSG.edit(text = CHUNK["total"], reply_markup = cancel)
            
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
                        if not await work(callbackQuery, "check", False):
                            return #await dlMSG.edit(text="{}/{}".format(cnvrtpg, totalPgList), reply_markup=canceled)
                    with open(f'{cDIR}/pgs/{pageNo}.jpg','wb'):
                        pix.save(f'{cDIR}/pgs/{pageNo}.jpg')
                
                directory = f'{cDIR}/pgs'
                imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                imag.sort(key = os.path.getctime)
                
                media[chat_id] = []
                for file in imag:
                    qualityRate = 95
                    for i in range(200):
                        if os.path.getsize(file) >= 1000000:
                            picture = Image.open(file)
                            picture.save(file, "JPEG", optimize = True,quality = qualityRate)
                            qualityRate -= 5; await asyncio.sleep(0.5)
                        else:
                            if imageType == "#p2img|img":
                                media[chat_id].append(InputMediaPhoto(open(file, "rb")))
                            elif imageType == "#p2img|doc":
                                media[chat_id].append(InputMediaDocument(open(file, "rb")))
                            break
                
                try:
                    pass
                    #await dlMSG.edit(text="{}?{}".format(cnvrtpg, len(totalPgList)), reply_markup = cancel)
                except Exception: pass
                
                if imageType == "p2img|img":
                    await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                elif imageType == "p2img|doc":
                    await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                
                try:
                    await pyTgLovePDF.send_media_group(callbackQuery.message.chat.id, media[callbackQuery.message.chat.id])
                except Exception as e:
                    logger.debug(e)
                    wait = str(e).rsplit(' ', 1)[1]; await asyncio.sleep(int(wait))
                    media[callbackQuery.message.chat.id] = []
                    for file in imag:
                        media[callbackQuery.message.chat.id].append(InputMediaPhoto(open(file, "rb")))
                    await pyTgLovePDF.send_media_group(callbackQuery.message.chat.id, media[callbackQuery.message.chat.id])
                shutil.rmtree(f'{cDIR}/pgs')
            #await dlMSG.edit(text="😁",reply_markup = completed)
            return "finished", "finished"
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error
# Author: @nabilanavab
