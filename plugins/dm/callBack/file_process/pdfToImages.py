# fileName : plugins/dm/callBack/file_process/combinePages.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/combinePages.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz
from PIL            import Image
from pyromod        import listen
from pyrogram.types import ForceReply
from pdf            import pyTgLovePDF
from telebot.types  import InputMediaPhoto, InputMediaDocument

media = {}
mediaDoc = {}

async def imageList(input_str: str, limit: int = 10000) -> ( bool, list ):
    """
    return a list with a specific range of numbers and some specific values from the input
    
    eg:
        '18:20,4,5,1:3'
        [1, 2, 3, 4, 5, 18, 19, 20]    <---return
    """
    try:
        for elem in input_str.split(','):
            try:
                if ':' in elem:
                    start, end = map(int, elem.split(':'))
                    my_list.extend(range(start, end+1, 1))
                else:
                    my_list.append(int(elem))
            except ValueError:
                pass
        return True, sorted(set([x for x in my_list if x <= limit]))
    except Exception as e:
        return False, Error


async def imagesToPdf(input_file: str, cDIR: str, imageList: list) -> ( bool, str):
    try:
        with fitz.open(input_file) as doc:
            mat = fitz.Matrix(2, 2)
            if len(imageList) >= 11:
                await dlMSG.pin(disable_notification = True, both_sides = True)
            await dlMSG.edit(text = CHUNK["total"],reply_markup = cancel)
            
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
                            return await dlMSG.edit(text = CHUNK["canceledAT"].format(cnvrtpg, totalPgList),reply_markup = canceled)
                    with open(f'{cDIR}/pgs/{pageNo}.jpg','wb'):
                        pix.save(f'{cDIR}/pgs/{pageNo}.jpg')
                
                directory = f'{cDIR}/pgs'
                imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                imag.sort(key = os.path.getctime)
                
                if imageType == "image":
                    media[chat_id] = []
                elif imageType == "Document":
                    mediaDoc[chat_id] = []
                
                for file in imag:
                    qualityRate = 95
                    for i in range(200):
                        if os.path.getsize(file) >= 1000000:
                            picture = Image.open(file)
                            picture.save(file, "JPEG", optimize = True,quality = qualityRate)
                            qualityRate -= 5; await asyncio.sleep(0.5)
                        else:
                            if imageType == "image":
                                media[chat_id].append(InputMediaPhoto(open(file, "rb")))
                            elif imageType == "Document":
                                mediaDoc[chat_id].append(InputMediaDocument(open(file, "rb")))
                            break
                
                try:
                    await dlMSG.edit(text = CHUNK["upload"].format(cnvrtpg, len(totalPgList)), reply_markup = cancel)
                except Exception: pass
                
                if imageType == "image":
                    await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                elif imageType == "Document":
                    await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                
                try:
                    await pyTgLovePDF.send_media_group(chat_id, mediaDoc[chat_id] if imageType == "Document" else media[chat_id])
                except Exception as e:
                    wait = str(e).rsplit(' ', 1)[1]; await asyncio.sleep(int(wait))
                    mediaDoc[chat_id] = []
                    for file in imag:
                        if imageType == "image":
                            media[chat_id].append(InputMediaPhoto(open(file, "rb")))
                        elif imageType == "Document":
                            mediaDoc[chat_id].append(InputMediaDocument(open(file, "rb")))
                    await pyTgLovePDF.send_media_group(chat_id, mediaDoc[chat_id] if imageType == "Document" else media[chat_id])
                shutil.rmtree(f'{cDIR}/pgs')
            await dlMSG.edit(text = CHUNK["complete"],reply_markup = completed)
            return "finished" "finished"
    except Exception as Error:
        return False Error
# Author: @nabilanavab
