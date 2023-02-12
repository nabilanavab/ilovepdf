# fileName : plugins/dm/url.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/url.py"

import os, re, requests, asyncio
from plugins.util       import *
from configs.log        import log
from plugins.work       import work
from configs.config     import settings, images
from plugins.render     import gSF, cbPRO, header
from plugins.fncta      import thumbName, formatThumb
from pyrogram           import filters, Client as ILovePDF, enums

try:
    import pdfkit
    pattern = re.compile(r'(https?://|www\.)?(www\.)?([a-z0-9-]+)(\..+)?')
    urlSupport = True
except Exception:
    urlSupport = False

if settings.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * (10 **6 )
else:
    MAX_FILE_SIZE = False

# url Example: https://t.me/channel/message
#              https://t.me/nabilanavab/1
links = ["https://telegram.dog/", "https://t.me/", "https://telegram.me/"]

# just a function that returns all urls from a text message
async def urlsFromText(text: str) -> list:
    try:
        urls = re.findall(r'(https?://\S+)', text)
        return urls if not len(urls) == 0 else None
    except Exception:
        return None

@ILovePDF.on_message(filters.private & filters.incoming & filters.text)
async def _url(bot, message):
    try:
        urls = await urlsFromText(message.text)
        if urls is None:
            return
        lang_code = await getLang(message.chat.id)
        
        for url in urls:
            try: await message.reply_chat_action(enums.ChatAction.TYPING)
            except Exception: pass
            
            _, __ = await translate(text = "document['process']", button = "URL['close']", lang_code = lang_code)
            data = await message.reply(text = _, quote = True, reply_markup = __)
            await asyncio.sleep(0.5)
            await data.edit(text = _ + ".", reply_markup = __)
            
            if url.startswith(tuple(links)):
                part = url.split("/")
                message_ids = int(part[-1])
                try:
                    chat_id = int(part[-2])
                    chat_id = int("-100" + f"{chat_id}")
                except Exception:
                    chat_id = part[-2]
                try:
                    file = await bot.get_messages(chat_id = chat_id, message_ids = message_ids)
                except Exception as e:
                    tTXT, _ = await translate(text = "URL['error']", lang_code = lang_code)
                    return await data.edit(text = tTXT.format(e), reply_markup = __)
                await asyncio.sleep(0.5)
                if not file.document:
                    tTXT, _ = await translate(text = "URL['notPDF']", lang_code = lang_code)
                    return await data.edit(tTXT)
                isProtect = "🔒 Protected 🔒" if (
                    (file.sender_chat and file.sender_chat.has_protected_content) or (
                    file.chat and file.chat.has_protected_content)) else "👀 Public 👀"
                tTXT, tBTN = await translate(text = "URL['_get']", button = "URL['get']", lang_code = lang_code)
                await data.edit(
                    text = tTXT.format(
                        url, file.chat.type, file.chat.title, file.chat.username,
                        file.sender_chat.id if file.chat.type == enums.ChatType.CHANNEL else file.chat.id,
                        file.date, file.media, file.document.file_name, await gSF(file.document.file_size), isProtect
                    ),
                    reply_markup = tBTN if file.document.file_name[-4:] == ".pdf" else None,
                    disable_web_page_preview = True
                )
            
            elif url.endswith(".pdf") or bool(urlSupport):
                try:
                    cDIR = await work(message, "create", True)
                    if not cDIR:
                        tTXT, tBTN = await translate(text = 'document["refresh"]', lang_code = lang_code)
                        tBTN = await createBUTTON(await editDICT(inDir = tTXT, value = "refresh"))
                        tTXT, _ = await translate(text = 'document["inWork"]', lang_code = lang_code)
                        return await data.edit(tTXT, reply_markup = tBTN)   # work exists
                    
                    response = requests.get(url)
                    directDlLink = True if "Content-Type" in response.headers and response.headers["Content-Type"]=="application/pdf" else False
                    
                    if not (directDlLink or urlSupport):
                        await data.delete()
                        continue
                    
                    if directDlLink:
                        match = re.match(r".*/([^/]+)/?$", url)
                        outputName = match.group(1) if match.group(1).endswith(".pdf") else f"{match.group(1)}.pdf"
                        
                        response = requests.get(url)
                        total_size = int(response.headers.get("Content-Length", 0))
                        
                        telegramCan = True if total_size < 20000000 else False
                        if not telegramCan:
                            with open(f"{cDIR}/{message.id}.pdf", "wb") as f:
                                f.write(response.content)
                        
                    elif not directDlLink:
                        outputName = pattern.sub(r'\3', url)
                        pdfkit.from_url(url, f"{cDIR}/{message.id}.pdf")
                    
                    tTXT, tBTN = await translate(text = "URL['done']", button = "URL['close']", lang_code = lang_code)
                    await data.edit(tTXT, reply_markup = tBTN)
                    
                    FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(message, f"{outputName}.pdf")
                    if images.PDF_THUMBNAIL != THUMBNAIL:
                        location = await bot.download_media(message = THUMBNAIL, file_name = f"{cDIR}/thumb.jpeg")
                        THUMBNAIL = await formatThumb(location)
                    
                    await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
                    tTXT, _ = await translate(text = "URL['openCB']", lang_code = lang_code)
                    logFile = await message.reply_document(
                        document = url if directDlLink and telegramCan else f"{cDIR}/{message.id}.pdf",
                        file_name = FILE_NAME.replace("+", " "), caption = f"Url: `{url}`\n\n{FILE_CAPT}",
                        reply_markup = await createBUTTON(await editDICT(inDir = tTXT, value = url)),
                        thumb = THUMBNAIL, progress = cbPRO, progress_args = (data, 0, "UPLOADED", True), quote = True
                    )
                    await data.delete()
                    await log.footer(message, output = logFile, lang_code = lang_code)
                except Exception as e:
                    logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
                    tTXT, tBTN = await translate(text = "URL['_error']", button="URL['close']", lang_code=lang_code)
                    await data.edit(tTXT.format(e), reply_markup=tBTN)
            await work(message, "delete", True)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(message, "delete", True)
        tTXT, tBTN = await translate(text = "URL['error']", button = "URL['close']", lang_code = lang_code)
        return await data.edit(text = tTXT.format(e), reply_markup = tBTN)

getFile = filters.create(lambda _, __, query: query.data == "getFile")
@ILovePDF.on_callback_query(getFile)
async def _getFile(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        url = callbackQuery.message.reply_to_message.text
        part = url.split("/")
        message_ids = int(part[-1])
        try:
            chat_id = int(part[-2])
            chat_id = int("-100" + f"{chat_id}")
        except Exception:
            chat_id = part[-2]
        # bot.get_messages
        file = await bot.get_messages(chat_id=chat_id, message_ids=message_ids)
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and file.document.file_size >= int(MAX_FILE_SIZE_IN_kiB):
            tTXT, _ = await translate(text="getFILE['big']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT.format(MAX_FILE_SIZE))
        
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            _, __ = await translate(text="getFILE['inWork']", lang_code=lang_code)
            return await callbackQuery.answer(_)
        
        _, __ = await translate(text="getFILE['wait']", lang_code=lang_code)
        await callbackQuery.answer(_)
        # if not a protected channel/group [just forward]
        if not (
            (file.sender_chat and file.sender_chat.has_protected_content) or (
                file.chat and file.chat.has_protected_content)
        ):
            await work(callbackQuery, "delete", False)
            return await file.copy(
                chat_id = callbackQuery.message.chat.id, caption = file.caption
            )
        
        _, __ = await translate(button = "getFILE['dl']", lang_code = lang_code)
        await callbackQuery.edit_message_reply_markup(__)
        location = await bot.download_media(
            message = file.document.file_id, file_name = f"{cDIR}/{file.document.file_name}", progress = cbPRO,
            progress_args = (callbackQuery.message, file.document.file_size, "DOWNLOADED", True)
        )
        _, __ = await translate(button = "getFILE['up']", lang_code = lang_code)
        await callbackQuery.edit_message_reply_markup(__)
        logFile = await callbackQuery.message.reply_document(
            document = location, caption = file.caption, progress = cbPRO,
            progress_args = (callbackQuery.message, 0, "UPLOADED", True)
        )
        _, __ = await translate(button = "getFILE['complete']", lang_code = lang_code)
        await callbackQuery.edit_message_reply_markup(__)
        await work(callbackQuery, "delete", False)
        await log.footer(callbackQuery.message, output = logFile, lang_code = lang_code)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "create", False)
