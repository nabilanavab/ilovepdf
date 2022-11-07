# fileName : plugins/render.py
# copyright ©️ 2021 nabilanavab

from pdf import PROCESS
from logger import logger
from plugins.util import *
from configs.config import dm
import fitz, shutil, time, math
from pyrogram.types import Message
from pyrogram import Client, filters, enums

#======================================= CHECKS CALLBACKQUERY USER ====================================================================================================
async def header(bot, callbackQuery):
    # callBack Message delete if User Deletes pdf
    try:
        fileExist = callbackQuery.message.reply_to_message
        
        if (callbackQuery.message.chat.type != enums.ChatType.PRIVATE and 
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id and 
            callbackQuery.from_user.id not in dm.ADMINS
        ):
            userStat = await bot.get_chat_member(callbackQuery.message.chat.id, callbackQuery.from_user.id)
            if userStat.status not in ["administrator", "creator"]:
                await callbackQuery.answer("Message Not For You.. :(")
                return True
        return False
    except Exception as e:
        logger.exception("plugins/render/header: %s" %(e), exc_info=True)
        await callbackQuery.message.delete()
        return "delete"

#======================================================================================== SIZE FORMATER (TO HUMAN READABLE FORM) ======================================
async def gSF(b, factor=2**10, suffix="B"):    # get_size_format
    try:
        for unit in ["", "K", "M", "G", "T"]:                 # Scale bytes to its proper byte format
            if b < factor:                                    # e.g: 1253656 => '1.20MB'
                return f"{b:.2f}{unit}{suffix}"               #      1253656678 => '1.17GB'
            b /= factor
        return f"{b:.2f}Y{suffix}"
    except Exception: pass

#====================== CHECKS PDF CODEC, IS ENCRYPTED OR NOT =========================================================================================================
async def checkPdf(file_path, callbackQuery):
    try:
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.id
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        lang_code = await getLang(chat_id)
        CHUNK, _ = await translate(text="checkPdf", lang_code=lang_code)
        
        with fitz.open(file_path) as doc:
            isEncrypted = doc.is_encrypted
            number_of_pages = doc.page_count
            metaData = doc.metadata
            if metaData != None:
                pdfMetaData = ""
                for i in metaData:
                    if metaData[i] != "":
                        pdfMetaData += f"`{i} : {metaData[i]}`\n"
            if isEncrypted:
                pdfMetaData = ""
                try:
                    await callbackQuery.edit_message_text(
                        text = CHUNK["encrypt"].format(fileName, await gSF(fileSize)) + "\n\n"
                             + CHUNK["pg"].format(number_of_pages) + "\n\n" + pdfMetaData,
                        reply_markup = await createBUTTON(CHUNK["encryptCB"])
                    )
                except Exception: pass
                if callbackQuery.data != "work|decrypt":
                    PROCESS.remove(chat_id)
                    # try Coz(at the time of merge there is no such dir but checking)
                    try:
                        shutil.rmtree(f'{message_id}')
                    except Exception: pass
                return "encrypted", number_of_pages
            else:
                if callbackQuery.data != "merge":
                    await callbackQuery.edit_message_text(
                        text = CHUNK["pdf"].format(fileName, await gSF(fileSize)) + "\n\n"
                             + CHUNK["pg"].format(number_of_pages) + "\n\n" + pdfMetaData,
                        reply_markup = await createBUTTON(CHUNK["pdfCB"])
                    )
                return "pass", number_of_pages
    # CODEC ERROR
    except Exception as e:
        logger.debug(e)
        await callbackQuery.edit_message_text(
            text = CHUNK["error"],
            reply_markup = await createBUTTON(CHUNK["errorCB"], order=11)
        )
        PROCESS.remove(chat_id)
        # try Coz(at the time of merge there is no such dir but checking)
        try:
            shutil.rmtree(f'{message_id}')
        except Exception: pass
        return "notPdf", "🚫"

#=================================================================================== DOC. DOWNLOAD PROGRESS ===========================================================
# Here t = 0; cauz downloading using bot.downlod_media cant fetch
# total file size, so sharing file_size as function para.
async def progress(current, t, total, message, start):
    now = time.time(); diff = now - start
    
    if round(diff % 10) in [0, 8] or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current)/speed)*1000
        progress="[{0}{1}] \n".format(
            ''.join(["●" for _ in range(math.floor(percentage / 5))]),
            ''.join(["○" for _ in range(20 - math.floor(percentage / 5))])
        )
        estimated_total_time = TimeFormatter(time_to_completion)
        lang_code = await getLang(message.chat.id)
        tTXT, tBTN = await translate(text="PROGRESS['progress']", button="document['cancelCB']", lang_code=lang_code)
        tmp = progress + tTXT.format(
            await gSF(current), await gSF(total), await gSF(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        await message.edit_text(text="DOWNLOADING.. 📥\n{}".format(tmp), reply_markup=tBTN)

#========================================================================================================================== DOC. UPLOADING PROGRESS ===================
async def uploadProgress(current, total, message, start):
    now = time.time(); diff = now - start
    
    if round(diff % 10) in [0, 8] or current == total:
        await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current)/speed)*1000
        progress="[{0}{1}] \n".format(
            ''.join(["●" for _ in range(math.floor(percentage / 5))]),
            ''.join(["○" for _ in range(20 - math.floor(percentage / 5))])
        )
        estimated_total_time = TimeFormatter(time_to_completion)
        lang_code = await getLang(message.chat.id)
        tTXT, tBTN = await translate(text="PROGRESS['progress']", button="document['cancelCB']", lang_code=lang_code)
        tmp = progress + tTXT.format(
            await gSF(current), await gSF(total), await gSF(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        await message.edit_text(text="UPLOADING.. 📤\n{}".format(tmp), reply_markup=tBTN)

#======================================================================================================================================================================
def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds=divmod(int(milliseconds), 1000)
    minutes, seconds=divmod(seconds, 60)
    hours, minutes=divmod(minutes, 60)
    days, hours=divmod(hours, 24)
    tmp=((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

#======================================================================================================================================================================
async def cbPRO(current, t, message, total=0, typ="DOWNLOADED", cancel=False):
    lang_code = await getLang(message.chat.id)
    if t != 0:
        total = t
    
    if typ == "DOWNLOADED":
        tTXT, _ = await translate(text="PROGRESS['cbPRO_D']", lang_code=lang_code)
    else:
        tTXT, _ = await translate(text="PROGRESS['cbPRO_U']", lang_code=lang_code)
    percentage = current * 100 / total
    if cancel:
        await message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(tTXT[0].format(percentage), callback_data="nabilanavab")]
                 ,[InlineKeyboardButton(tTXT[1].format(percentage), callback_data="close|all")]]
            ))
    else:
        await message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(tTXT[0].format(percentage), callback_data="close|all")]]
            ))

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
