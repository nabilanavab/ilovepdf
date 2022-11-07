# fileName : plugins/dm/callBack/images.py
# copyright ©️ 2021 nabilanavab

media = {}
mediaDoc = {}

from PIL import Image
from logger import logger
from pyromod import listen
from plugins.util import *
from plugins.render import *
from configs.config import images
from pdf import PROCESS , pyTgLovePDF
from pyrogram.types import ForceReply
import os, fitz, time, shutil, asyncio
from plugins.thumbName import thumbName, formatThumb
from pyrogram import filters, enums, Client as ILovePDF
from telebot.types import InputMediaPhoto, InputMediaDocument

extract = filters.create(lambda _, __, query: query.data.startswith("p2img"))
@ILovePDF.on_callback_query(extract)
async def _extract(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        CHUNK, _ = await translate(text="pdf2IMG", lang_code=lang_code)
        if await header(bot, callbackQuery):
            return
        chat_id = callbackQuery.from_user.id
        message_id = callbackQuery.message.id
        
        if chat_id in PROCESS:
            return await callbackQuery.answer(CHUNK["inWork"])
        
        PROCESS.append(chat_id)    # ↓ ADD TO PROCESS
        if "•" in callbackQuery.message.text:
            known = True; number_of_pages = int(callbackQuery.message.text.split("•")[1])
        else:
            known = False
        
        data = callbackQuery.data.split("|")[1]
        await callbackQuery.answer(CHUNK["process"])
        if data in ["IA", "DA", "zipA", "tarA"]:
            nabilanavab = False
        elif data in ["IR", "DR", "zipR", "tarR"]:
            nabilanavab = True; i = 0
            while(nabilanavab):    # 5 EXCEPTION, BREAK MERGE PROCESS
                if i >= 5:
                    await callbackQuery.message.reply_text(CHUNK["over"]); break
                i += 1
                needPages = await bot.ask(
                    chat_id = chat_id, text = CHUNK["pyromodASK_1"],
                    reply_to_message_id = message_id, filters = filters.text,
                    reply_markup = ForceReply(True, "Eg: 7:86 [start:end]")
                )   # PYROMOD ADD-ON (PG NO REQUEST)
                if needPages.text == "/exit":    # EXIT PROCESS
                    await needPages.reply_text(CHUNK["exit"], quote = True); break
                # SPLIT STRING TO START & END
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                try:
                    pageStartAndEnd = [ int(x) for x in pageStartAndEnd ]    # make str elements to int
                except: pass
                # IF STRING HAVE MORE THAN 2 LIMITS
                if len(pageStartAndEnd) > 2:
                    await callbackQuery.message.reply_text(CHUNK["error_1"])
                # CORRECT FORMAT
                elif len(pageStartAndEnd) == 2:
                    start, end = pageStartAndEnd[0], pageStartAndEnd[1]
                    if type(start) == int and type(end) == int:
                        if 1 <= start:
                            if (start < end and known and end <= int(number_of_pages)
                                ) or (start < end and not known):
                                    nabilanavab = False
                                    break
                            else:
                                await callbackQuery.message.reply_text(CHUNK["error_2"])
                        else:
                            await callbackQuery.message.reply_text(CHUNK["error_3"])
                    else:
                        await callbackQuery.message.reply_text(CHUNK["error_4"])
                else:
                    await callbackQuery.message.reply_text(CHUNK["error_5"])
        # SINGLE PAGES
        else:
            newList = []
            nabilanavab = True; i = 0
            while(nabilanavab):    # 5 REQUEST LIMIT
                if i >= 5:
                    await callbackQuery.message.reply_text(CHUNK["over"])
                    break
                i += 1
                needPages = await bot.ask(
                    text = CHUNK["pyromodASK_2"], chat_id = chat_id, reply_to_message_id = message_id,
                    filters = filters.text, reply_markup = ForceReply(True, "Eg: 7,8,6 [pages]")
                )
                if needPages.text == "/exit":    # PROCESS CANCEL
                    await needPages.reply(CHUNK["exit"], quote = True)
                    break
                # SPLIT PAGE NUMBERS (,)
                singlePages = list(needPages.text.replace(',',':').split(':'))
                for k in singlePages:
                    try:
                        a = int(k)    # sometimes user enter "pg1, pg2,   pg3"
                        # https://www.geeksforgeeks.org/how-to-replace-values-in-a-list-in-python/
                        singlePages = list(map(lambda x: x.replace(k, a), singlePages))
                    except Exception:
                        singlePages.remove(k)
                singlePages = list(needPages.text.replace(',',':').split(':'))
                # PAGE NUMBER LESS THAN 100
                if 1 <= len(singlePages) <= 100:
                    # CHECK IS PAGE NUMBER A DIGIT(IF ADD TO A NEW LIST)
                    if not known:
                        newList = singlePages
                    else:
                        for j in singlePages:
                            if int(j) <= int(number_of_pages):
                                newList.append(j)
                    if newList != []:
                        nabilanavab = False
                        break
                    # AFTER SORTING (IF NO DIGIT PAGES RETURN)
                    elif newList == []:
                        await callbackQuery.message.reply(CHUNK["error_6"])
                        continue
                else:
                    await callbackQuery.message.reply(CHUNK["error_7"])
        if nabilanavab == True:
            PROCESS.remove(chat_id)
            return
        
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        cancel = await createBUTTON(btn=CHUNK["cancelCB"])
        canceled = await createBUTTON(btn=CHUNK["canceledCB"])
        completed = await createBUTTON(btn=CHUNK["completed"])
        
        if nabilanavab == False:
            # DOWNLOAD MESSAGE
            downloadMessage = await callbackQuery.message.reply(text = CHUNK["download"], quote = True)
            file_id = callbackQuery.message.reply_to_message.document.file_id
            fileSize = callbackQuery.message.reply_to_message.document.file_size
            # DOWNLOAD PROGRESS
            c_time = time.time()
            downloadLoc = await bot.download_media(
                message = file_id, file_name = input_file, progress = progress,
                progress_args = (fileSize, downloadMessage, c_time)
            )
            # CHECK DOWNLOAD COMPLETED/CANCELED
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            # CHECK PDF CODEC, ENCRYPTION..
            if not known:
                checked, number_of_pages = await checkPdf(input_file, callbackQuery)
                if checked != "pass":
                    return await downloadMessage.delete()
            # OPEN PDF WITH FITZ
            with fitz.open(input_file) as doc:
                if data in ["IA", "DA"]:
                    start, end = 1, int(number_of_pages)
                elif data in ["IR", "DR"]:
                    if not(end) <= int(number_of_pages):
                        await downloadMessage.edit(CHUNK["error_8"].format(number_of_pages))
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
                elif data in ["zipA", "tarA"]:
                    if number_of_pages > 50:
                        await downloadMessage.edit(CHUNK["error_10"])
                        await asyncio.sleep(3)
                        start, end = 1, 50
                    else:
                        start, end = 1, int(number_of_pages)
                elif data in ["zipR", "tarR"]:
                    if end - start > 50:
                        await downloadMessage.edit(CHUNK["error_10"])
                        await asyncio.sleep(3)
                        start, end = start, start + 50
                    if not(end) <= int(number_of_pages):
                        await downloadMessage.edit(CHUNK["error_8"].format(number_of_pages))
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
                zoom = 2; mat = fitz.Matrix(zoom, zoom)
                if data in ["IA", "DA", "IR", "DR"]:
                    if int(end+1 - start) >= 11:
                        await downloadMessage.pin(disable_notification = True, both_sides = True)
                    await downloadMessage.edit(
                        text = CHUNK["total"].format(end+1 - start), reply_markup = cancel
                    )
                    totalPgList = range(start, end + 1)
                    cnvrtpg = 0
                    for i in range(0, len(totalPgList), 10):
                        pgList = totalPgList[i:i+10]
                        os.mkdir(f'{message_id}/pgs')
                        for pageNo in pgList:
                            page = doc.load_page(pageNo-1)
                            pix = page.get_pixmap(matrix = mat)
                            cnvrtpg += 1
                            if cnvrtpg % 5 == 0:
                                if chat_id not in PROCESS:
                                    await downloadMessage.edit(text=CHUNK["canceledAT"].format(cnvrtpg, end), reply_markup=canceled)
                                    shutil.rmtree(f'{message_id}')
                                    return
                            with open(f'{message_id}/pgs/{pageNo}.jpg','wb'):
                                pix.save(f'{message_id}/pgs/{pageNo}.jpg')
                        directory = f'{message_id}/pgs'
                        imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                        imag.sort(key = os.path.getctime)
                        if data in ["IA", "IR"]:
                            media[chat_id] = []
                        else:
                            mediaDoc[chat_id] = []
                        for file in imag:
                            qualityRate = 95
                            for i in range(200):
                                if os.path.getsize(file) >= 1000000:
                                    picture = Image.open(file)
                                    picture.save(file, "JPEG", optimize = True, quality = qualityRate)
                                    qualityRate -= 5; await asyncio.sleep(0.5)
                                else:
                                    if data in ["IA", "IR"]:
                                        media[chat_id].append(InputMediaPhoto(open(file, "rb")))
                                    else:
                                        mediaDoc[chat_id].append(InputMediaDocument(open(file, "rb")))
                                    break
                        if chat_id not in PROCESS:
                            await downloadMessage.edit(text=CHUNK["canceledAT"].format(cnvrtpg, end), reply_markup=canceled)
                            shutil.rmtree(f'{message_id}')
                            return
                        try:
                            await downloadMessage.edit(
                                text = CHUNK["upload"].format(cnvrtpg, end+1 - start),
                                reply_markup = cancel
                            )
                        except Exception: pass
                        if data in ["IA", "IR"]:
                            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                            try:
                                await pyTgLovePDF.send_media_group(chat_id, media[chat_id])
                            except Exception as e:
                                wait = str(e).rsplit(' ', 1)[1]; await asyncio.sleep(int(wait))
                                media[chat_id] = []
                                for file in imag:
                                    media[chat_id].append(InputMediaPhoto(open(file, "rb")))
                                await pyTgLovePDF.send_media_group(chat_id, media[chat_id])
                        if data in ["DA", "DR"]:
                            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                            try:
                                await pyTgLovePDF.send_media_group(chat_id, mediaDoc[chat_id])
                            except Exception as e:
                                wait = str(e).rsplit(' ', 1)[1]; await asyncio.sleep(int(wait))
                                mediaDoc[chat_id] = []
                                for file in imag:
                                    mediaDoc[chat_id].append(InputMediaDocument(open(file, "rb")))
                                await pyTgLovePDF.send_media_group(chat_id, mediaDoc[chat_id])
                        shutil.rmtree(f'{message_id}/pgs')
                    await downloadMessage.edit(text=CHUNK["complete"], reply_markup=completed)
                elif data in ["IS", "DS"]:
                    if int(len(newList)) >= 11:
                        await downloadMessage.pin(disable_notification = True, both_sides = True)
                    totalPgList = []
                    for i in newList:
                        if 1 <= int(i) <= int(number_of_pages):
                            totalPgList.append(i)
                    if len(totalPgList) < 1:
                        await downloadMessage.edit(CHUNK["error_8"].format(number_of_pages))
                        PROCESS.remove(chat_id); shutil.rmtree(f'{message_id}')
                        return
                    await downloadMessage.edit(text = CHUNK["total"].format(len(totalPgList)), reply_markup = cancel)
                    cnvrtpg = 0
                    for i in range(0, len(totalPgList), 10):
                        pgList = totalPgList[i:i+10]
                        os.mkdir(f'{message_id}/pgs')
                        for pageNo in pgList:
                            if int(pageNo) <= int(number_of_pages):
                                page = doc.load_page(int(pageNo)-1)
                                pix = page.get_pixmap(matrix=mat)
                            else:
                                continue
                            cnvrtpg += 1
                            if cnvrtpg % 5 == 0:
                                if chat_id not in PROCESS:
                                    await downloadMessage.edit(text=CHUNK["canceledAT"].format(cnvrtpg, totalPgList), reply_markup=canceled)
                                    shutil.rmtree(f'{message_id}')
                                    return
                            with open(
                                f'{message_id}/pgs/{pageNo}.jpg','wb'
                            ):
                                pix.save(f'{message_id}/pgs/{pageNo}.jpg')
                        directory = f'{message_id}/pgs'
                        imag = [os.path.join(directory, file) for file in os.listdir(directory)]
                        imag.sort(key = os.path.getctime)
                        if data == "IS":
                            media[chat_id] = []
                        else:
                            mediaDoc[chat_id] = []
                        for file in imag:
                            qualityRate = 95
                            for i in range(200):
                                if os.path.getsize(file) >= 1000000:
                                    picture = Image.open(file)
                                    picture.save(
                                        file, "JPEG", optimize = True,
                                        quality = qualityRate
                                    )
                                    qualityRate -= 5; await asyncio.sleep(0.5)
                                else:
                                    if data in ["IS", "KIS"]:
                                        media[chat_id].append(InputMediaPhoto(open(file, "rb")))
                                    else:
                                        mediaDoc[chat_id].append(InputMediaDocument(open(file, "rb")))
                                    break
                        try:
                            await downloadMessage.edit(text = CHUNK["upload"].format(cnvrtpg, len(totalPgList)), reply_markup = cancel)
                        except Exception: pass
                        if data in ["IS"]:
                            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                            try:
                                await pyTgLovePDF.send_media_group(chat_id, media[chat_id])
                            except Exception as e:
                                wait = str(e).rsplit(' ', 1)[1]; await asyncio.sleep(int(wait))
                                media[chat_id] = []
                                for file in imag:
                                    media[chat_id].append(InputMediaPhoto(open(file, "rb")))
                                await pyTgLovePDF.send_media_group(chat_id, media[chat_id])
                        if data in ["DS"]:
                            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                            try:
                                await pyTgLovePDF.send_media_group(chat_id, mediaDoc[chat_id])
                            except Exception as e:
                                wait = str(e).rsplit(' ', 1)[1]; await asyncio.sleep(int(wait))
                                mediaDoc[chat_id] = []
                                for file in imag:
                                    mediaDoc[chat_id].append(InputMediaDocument(open(file, "rb")))
                                await pyTgLovePDF.send_media_group(chat_id, mediaDoc[chat_id])
                        shutil.rmtree(f'{message_id}/pgs')
                    await downloadMessage.edit(text=CHUNK["complete"], reply_markup=completed)
                else:
                    if data in ["zipA", "zipR", "tarA", "tarR"]:
                        await downloadMessage.edit(text = f"`Total pages: {end+1 - start}..⏳`", reply_markup=cancel)
                        totalPgList = range(start, end+1)
                    elif data in ["zipS", "tarS"]:
                        totalPgList = []
                        for i in newList:
                            if 1 <= int(i) <= number_of_pages:
                                totalPgList.append(i)
                        if len(totalPgList) < 1:
                            await downloadMessage.edit(CHUNK["error_8"].format(number_of_pages))
                            PROCESS.remove(chat_id); shutil.rmtree(f'{message_id}'); doc.close()
                            return
                        await downloadMessage.edit(text=CHUNK["total"].format({len(totalPgList)}), reply_markup=cancel)
                    cnvrtpg = 0
                    os.mkdir(f'{message_id}/pgs')
                    for i in totalPgList:
                        page = doc.load_page(int(i)-1)
                        pix = page.get_pixmap(matrix = mat)
                        cnvrtpg += 1
                        if cnvrtpg % 5 == 0:
                            await downloadMessage.edit(text=CHUNK["current"].format(cnvrtpg, end+1-start), reply_markup=cancel)
                            if chat_id not in PROCESS:
                                await message.edit(text=CHUNK["canceled"], reply_markup=canceled)
                                shutil.rmtree(f'{message_id}')
                                return
                        with open(f'{message_id}/pgs/{i}.jpg','wb'):
                            pix.save(f'{message_id}/pgs/{i}.jpg')
                    directory = f'{message_id}/pgs'
                    output_file = f'{message_id}/zipORtar'
                    if data in ["zipA", "zipR", "zipS"]:
                        shutil.make_archive(output_file, 'zip', directory)
                    elif data in ["tarA", "tarR", "tarS"]:
                        path = shutil.make_archive(output_file, 'tar', directory) 
                    
                    fileNm = callbackQuery.message.reply_to_message.document.file_name
                    fileNm, fileExt = os.path.splitext(fileNm)        # seperates name & extension
                    fileNm = f"{fileNm}.zip" if data.startswith("zip") else f"{fileNm}.tar"
                    # Getting thumbnail
                    thumbnail, fileName = await thumbName(callbackQuery.message, fileNm)
                    if images.PDF_THUMBNAIL != thumbnail:
                        location = await bot.download_media(
                            message = thumbnail, file_name = f"{callbackQuery.message.message_id}.jpeg"
                        )
                        thumbnail = await formatThumb(location)
                    
                    await downloadMessage.edit(CHUNK["uploadfile"])
                    await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                    await callbackQuery.message.reply_document(
                        file_name = fileName, quote = True, document = open(
                            f"{output_file}.zip" if data.startswith("zip") else f"{output_file}.tar", "rb"
                        ), thumb = thumbnail, caption = "__Zip File__ 🤐" if data.startswith("zip") else "__Tar File__ 🙂",
                        progress = uploadProgress, progress_args = (downloadMessage, time.time())
                    )
                    try:
                        os.remove(location)
                    except Exception: pass
                    await downloadMessage.delete()
                PROCESS.remove(chat_id)
                shutil.rmtree(f'{message_id}')
    except Exception as e:
        logger.exception("plugins/dm/callBack/images: %s" %(e), exc_info=True)
        try:
            PROCESS.remove(chat_id)
            shutil.rmtree(f'{message_id}')
        except Exception: pass

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
