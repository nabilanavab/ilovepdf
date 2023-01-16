# fileName : plugins/group/document.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/group/document.py"

import os, fitz, asyncio
from ..dm.document  import *
from plugins.util   import *
from configs.config import *
from plugins.render import *
from pdf            import PDF
from plugins.work   import work
from PIL            import Image
from logger         import logger
from pyrogram.enums import ChatMemberStatus
from plugins.fncta  import thumbName, formatThumb
from pyrogram       import Client as ILovePDF, filters
from configs.db     import invite_link, myID, BANNED_USR_DB

@ILovePDF.on_message(filters.group & filters.incoming & filters.command(["analyse", "check", "nabilanavab"]))
async def gDOC(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await getLang(message.chat.id)
        CHUNK, _ = await translate(text = "gDocument", lang_code = lang_code)
        
        # CHECKS BOTS RIGHT: ADMIN
        status = await bot.get_chat_member(message.chat.id, myID[0].id)
        if status.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply(CHUNK['admin'], quote = True)
        
        # IF NOT REPLY TO IMAGE OR DOCUMENT
        if (not message.reply_to_message) or not(message.reply_to_message.document or message.reply_to_message.photo):
            return await message.reply(CHUNK['notDOC'], quote = True)
        
        if message.from_user.id in BANNED_USR_DB:
            return await message.reply("Is this some kind of sneaky con job you're trying to pull on us?")
        
        # IF FORCE SUBSCRIPTION
        if len(invite_link) != 0:
            try:
                userStatus = await bot.get_chat_member(
                    str(settings.UPDATE_CHANNEL), message.from_user.id
                )
                # EXCEPTION FOR KICKED USERS 
                if userStatus.status == 'kicked':
                    a = 10 / 0
            except Exception:
                tTXT, tBTN = await translate(
                    text = "BAN['Force']", button = "BAN['ForceCB']",
                    asString = True, lang_code = lang_code
                )
                tBTN = await editDICT(inDir = tBTN, value = [invite_link[0], ""])
                button = await createBUTTON(btn = tBTN, order = "11")
                return await message.reply_photo(
                    photo = images.WELCOME_PIC, quote = True,
                    caption = tTXT.format(message.from_user.first_name, message.from_user.id),
                    reply_markup = button
                )
        # IT ONLT RESPONDS TO BOT ADMIN, GROUP ADMIN AND REQUESTED USERS
        if message.from_user.id in dm.ADMINS:
            pass
        else:
            isAdmin = await bot.get_chat_member(message.chat.id, message.from_user.id)
            if group.ONLY_GROUP_ADMIN and isAdmin.status != ChatMemberStatus.ADMINISTRATOR:
                return await message.reply(CHUNK['Gadmin'], quote = True)
            elif isAdmin.status != ChatMemberStatus.ADMINISTRATOR:
                if message.from_user.id != message.reply_to_message.from_user.id:
                    return await message.reply(CHUNK['adminO'])
        
        try: await message.delete()
        except Exception: pass
        
        logFile = False    # adds logfile if there exists
        # IMAGES TO PDF IN GROUP
        if message.reply_to_message.photo:
            imageReply = await message.reply_to_message.reply_text(CHUNK['dlImage'], quote = True)
            if not isinstance(PDF.get(message.chat.id), list):
                PDF[message.chat.id] = []
            loc = await message.reply_to_message.download(f"work/{message.chat.id}.jpg")
            img = Image.open(loc).convert("RGB")
            PDF[message.chat.id].append(img)
            tBTN = await createBUTTON(CHUNK['generate'])
            return await imageReply.edit(CHUNK['imageAdded'].format(
                len(PDF[message.chat.id]), f'{message.chat.id}')\
                + f"\n\n👤:   {message.from_user.mention}",
                reply_markup = tBTN
            )
        
        # CHECKS MAXIMUM FILE SIZE LIMIT
        fileNm, fileExt = os.path.splitext(message.reply_to_message.document.file_name) # seperate name & extension
        if (message.from_user.id not in dm.ADMINS) and MAX_FILE_SIZE and message.reply_to_message.document.file_size >= int(MAX_FILE_SIZE_IN_kiB):
            tBTN = await createBUTTON(CHUNK["bigCB"])
            return await message.reply_photo(
                photo = images.BIG_FILE,
                caption = CHUNK["big"].format(MAX_FILE_SIZE, MAX_FILE_SIZE) \
                + f"\n\n👤:   {message.from_user.mention}",
                reply_markup = tBTN
            )
        
        # IMAGE AS FILES (ADDS TO PDF FILE)
        elif fileExt.lower() in img2pdf:
            try:
                imageDocReply = await message.reply_to_message.reply_text(CHUNK['dlImage'], quote = True)
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id] = []
                await message.reply_to_message.download(f"work/{message.chat.id}.jpg")
                img = Image.open(
                    f"work/{message.chat.id}.jpg"
                ).convert("RGB")
                PDF[message.chat.id].append(img)
                tBTN = await createBUTTON(CHUNK['generate'])
                await imageDocReply.edit(CHUNK['imageAdded'].format(
                    len(PDF[message.chat.id]), f'{message.chat.id}') \
                    + f"\n\n👤:   {message.from_user.mention}",
                    reply_markup = tBTN
                )
            except Exception as e:
                return await imageDocReply.edit(CHUNK["error"].format(e))
        
        # REPLY TO .PDF FILE EXTENSION
        elif fileExt.lower() == ".pdf":
            logFile = message
            pdfMsgId = await message.reply_to_message.reply_text(CHUNK["process"] ,quote=True)
            await asyncio.sleep(0.5)
            await pdfMsgId.edit(CHUNK["process"] + ".")
            await asyncio.sleep(0.5)
            tBTN = await createBUTTON(CHUNK["replyCB"])
            await pdfMsgId.edit(
                text = CHUNK["reply"].format(
                    message.reply_to_message.document.file_name,
                    await gSF(message.reply_to_message.document.file_size)
                ) + f"\n\n👤:   {message.from_user.mention}",
                reply_markup = tBTN
            )
        
        # IF WORK EXISTS SEND REFRESH BUTTON
        elif await work(message, "check", True):
            tBTN = await createBUTTON(
                await editDICT(inDir = CHUNK["refresh"], value = "refresh")
            )
            return await message.reply_to_message.reply_text(
                CHUNK["inWork"], reply_markup = tBTN, quote = True
            )
        
        # FILES TO PDF
        elif (fileExt.lower() in pymu2PDF) or (fileExt.lower() in cnvrt_api_2PDF) or (fileExt.lower() in wordFiles):
            
            if (fileExt.lower() in cnvrt_api_2PDF) and (((not DATA.get(message.chat.id, 0) \
                or (DATA.get(message.chat.id, 0) and not DATA.get(message.chat.id, 0)[0])) \
                and settings.CONVERT_API is False)):
                return await message.reply_text(CHUNK["noAPI"], quote = True)
            
            if (fileExt.lower() in wordFiles) and not wordSupport:
                return await message.reply_text(CHUNK["useDOCKER"], quote = True)
            
            cDIR = await work(message, "create", True)
            tBTN = await createBUTTON(CHUNK["cancelCB"])
            pdfMsgId = await message.reply_to_message.reply_text(
                CHUNK["download"], reply_markup = tBTN, quote = True
            )
            input_file = f"{cDIR}/input_file{fileExt}"
            # DOWNLOAD PROGRESS
            downloadLoc = await bot.download_media(
                message = message.reply_to_message.document.file_id, file_name = input_file, progress = progress,
                progress_args = (message.reply_to_message.document.file_size, pdfMsgId, time.time())
            )
            # CHECKS PDF DOWNLOADED OR NOT
            if os.path.getsize(downloadLoc) != message.reply_to_message.document.file_size:    
                return await work(message, "delete", True)
            
            await pdfMsgId.edit(CHUNK['takeTime'], reply_markup=tBTN)
            
            # WHERE REAL CODEC CONVERSATION OCCURS
            if fileExt.lower() in pymu2PDF:
                FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(message, f"{fileNm}.pdf")
                isError = await pymuConvert2PDF(cDIR, pdfMsgId, input_file, lang_code)
            
            elif fileExt.lower() in cnvrt_api_2PDF:
                FILE_NAME, FILE_CAPT, THUMBNAIL, API = await thumbName(message, f"{fileNm}.pdf", getAPI=True)
                API = API if not(API == False) else settings.CONVERT_API
                isError = await cvApi2PDF(cDIR, pdfMsgId, input_file, lang_code, API)
            
            elif fileExt.lower() in wordFiles:
                FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(message, f"{fileNm}.pdf")
                isError = await word2PDF(cDIR, pdfMsgId, input_file, lang_code)
            
            if not isError:
                return await work(message, "delete", True)
            
            if images.PDF_THUMBNAIL != THUMBNAIL:
                location = await bot.download_media(message = THUMBNAIL, file_name = f"{cDIR}/THUMB.jpeg")
                THUMBNAIL = await formatThumb(location)
            
            await pdfMsgId.edit(CHUNK['upFile'], reply_markup=tBTN)
            await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
            logFile = await message.reply_to_message.reply_document(
                file_name = FILE_NAME,
                document = open(f"{cDIR}/outPut.pdf", "rb"),
                thumb = THUMBNAIL,
                caption = CHUNK["fromFile"].format(fileExt, "pdf") + f"\n\n{FILE_CAPT}",
                quote = True,
                progress = uploadProgress,
                progress_args = (pdfMsgId, time.time()),
                reply_markup = await createBUTTON(
                    btn = {"👍" : "try+", "👎" : "try-"}
                ) if fileExt.lower() in pymu2PDF else None
            )
            await pdfMsgId.delete()
            await work(message, "delete", True)
        
        # UNSUPPORTED FILES
        else:
            return await message.reply_text(CHUNK["unsupport"], quote = True)
        
        if logFile:
            await log.footer(message, input = logFile, lang_code = lang_code)
        return
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(message, "delete", True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
