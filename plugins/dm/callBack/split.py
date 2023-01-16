# fileName : plugins/dm/callBack/split.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/split.py"

import os, time
from plugins.util    import *
from plugins.render  import *
from plugins.work    import work
from logger          import logger
from pyromod         import listen
from configs.config  import images
from pyrogram.types  import ForceReply
from plugins.fncta   import thumbName, formatThumb
from PyPDF2          import PdfFileWriter, PdfFileReader
from pyrogram        import enums, filters, Client as ILovePDF

split = filters.create(lambda _, __, query: query.data.startswith("split"))

@ILovePDF.on_callback_query(split)
async def _split(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        CHUNK, _ = await translate(text="split", button="document['cancelCB']", lang_code=lang_code)
        cDIR = await work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer()
        
        data = callbackQuery.data.split("|")[1]
        process = CHUNK["work"][0] if data == "R" else CHUNK["work"][1]
        
        if "•" in callbackQuery.message.text:
            known = True; number_of_pages = int(callbackQuery.message.text.split("•")[1])
        else:
            known = False
        
        nabilanavab = True; i = 0
        while(nabilanavab):
            # REQUEST FOR PG NUMBER (MAX. LIMIT 5)
            if i >= 5:
                await callbackQuery.message.reply(CHUNK["over"])
                break
            i += 1
            needPages = await bot.ask(
                text = CHUNK["pyromodASK_1"], chat_id = callbackQuery.message.chat.id, reply_to_message_id = callbackQuery.message.id,
                filters = filters.text, reply_markup = ForceReply(True, "Eg: 7:86 [start:end] | 7, 8 ,6 [pages]")
            )
            # IF /exit PROCESS CANCEL
            if needPages.text == "/exit":
                await needPages.reply(CHUNK["exit"], quote = True)
                break
            if not (known) and (data == "R"):
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                if len(pageStartAndEnd) > 2:
                    await callbackQuery.message.reply(CHUNK["error_1"])
                elif len(pageStartAndEnd) == 2:
                    start = pageStartAndEnd[0]; end = pageStartAndEnd[1]
                    try:
                        start = int(start); end = int(end)
                    except Exception: pass
                    if type(start) == int and type(end) == int:
                        if (1 <= int(pageStartAndEnd[0])):
                            if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                                nabilanavab = False
                                break
                            else:
                                await callbackQuery.message.reply(CHUNK["error_2"])
                        else:
                            await callbackQuery.message.reply(CHUNK["error_3"])
                    else:
                        await callbackQuery.message.reply(CHUNK["error_4"])
                else:
                    await callbackQuery.message.reply(CHUNK["error_5"])
            elif not (known) and (data == "S"):
                newList = []
                singlePages = list(needPages.text.replace(',',':').split(':'))
                if 1 <= len(singlePages) <= 100:
                    for j in singlePages:
                        try:
                            j = int(j); newList.append(j)
                        except Exception: pass
                    if newList != []:
                         nabilanavab = False
                         break
                    else:
                        await callbackQuery.message.reply(CHUNK["error_6"])
                        continue
                else:
                    await callbackQuery.message.reply()
            elif known and (data == "R"):
                pageStartAndEnd = list(needPages.text.replace('-',':').split(':'))
                if len(pageStartAndEnd)>2:
                    await callbackQuery.message.reply(CHUNK["error_1"])
                elif len(pageStartAndEnd) == 2:
                    start = pageStartAndEnd[0]; end = pageStartAndEnd[1]
                    try:
                        start=int(start); end=int(end)
                        if (int(1) <= int(start) and int(start) < number_of_pages):
                            if (int(start) < int(end) and int(end) <= number_of_pages):
                                nabilanavab = False
                                break
                            else:
                                await callbackQuery.message.reply(CHUNK["error_2"])
                        else:
                            await callbackQuery.message.reply(CHUNK["error_3"])
                    except Exception:
                        await callbackQuery.message.reply(CHUNK["error_4"])
                else:
                    await callbackQuery.message.reply(CHUNK["error_5"])
            elif known and (data == "S"):
                newList = []
                singlePages = list(needPages.text.replace(',',':').split(':'))
                if 1 <= int(len(singlePages)) and int(len(singlePages)) <= 100:
                    for j in singlePages:
                        try: 
                            j=int(j)
                            if j <= number_of_pages:
                                newList.append(j)
                        except Exception: pass
                    if newList == []:
                        await callbackQuery.message.reply(CHUNK["error_8"].format(number_of_pages))
                        continue
                    else:
                        nabilanavab = False
                        break
                else:
                    await callbackQuery.message.reply(CHUNK["error_7"])
        
        # nabilanavab == False [No Error]
        if nabilanavab == True:
            return await work(callbackQuery, "delete", False)
        if nabilanavab == False:
            input_file = f"{cDIR}/inPut.pdf"
            output_file = f"{cDIR}/outPut.pdf"
            
            dlMSG = await callbackQuery.message.reply(CHUNK["download"], reply_markup=_, quote = True)
            downloadLoc = await bot.download_media(
                message = callbackQuery.message.reply_to_message.document.file_id,
                file_name = input_file, progress = progress,
                progress_args = (
                    callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
                )
            )
            if os.path.getsize(downloadLoc) != callbackQuery.message.reply_to_message.document.file_size:    
                return await work(callbackQuery, "delete", False)
            
            await dlMSG.edit(CHUNK["completed"], reply_markup=_)
            if not known:
                checked, number_of_pages = await checkPdf(input_file, callbackQuery)
                if not(checked == "pass"):
                    return await dlMSG.delete()
            splitInputPdf = PdfFileReader(input_file)
            number_of_pages = int(splitInputPdf.getNumPages())
            
            if not known and data == "R":
                if not(int(pageStartAndEnd[1]) <= number_of_pages):
                    await callbackQuery.message.reply(CHUNK["error_9"])
                    return await work(callbackQuery, "delete", False)
            
            splitOutput = PdfFileWriter()
            if not known and data == "R":
                for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                    splitOutput.addPage(
                        splitInputPdf.getPage(i)
                    )
            elif not known and data == "S":
                for i in newList:
                    if int(i) <= number_of_pages:
                        splitOutput.addPage(splitInputPdf.getPage(int(i)-1))
            elif known and data == "R":
                for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                    splitOutput.addPage(splitInputPdf.getPage(i))
            elif known and data == "S":
                for i in newList:
                    if int(i) <= number_of_pages:
                        splitOutput.addPage(splitInputPdf.getPage(int(i)-1))
            
            with open(output_file, "wb") as output_stream:
                splitOutput.write(output_stream)
            
            FILE_NAME, FILE_CAPT, THUMBNAIL = await thumbName(
                callbackQuery.message,
                callbackQuery.message.reply_to_message.document.file_name
            )
            if images.PDF_THUMBNAIL != THUMBNAIL:
                location = await bot.download_media(
                    message = THUMBNAIL, file_name = f"{cDIR}/thumb.jpeg"
                )
                THUMBNAIL = await formatThumb(location)
            
            await dlMSG.edit(CHUNK["upload"], reply_markup = _)
            await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
            if data.startswith("S"):
                caption = f"{newList}"
            else:
                caption = f"from `{pageStartAndEnd[0]}` to `{pageStartAndEnd[1]}`"
            await callbackQuery.message.reply_document(
                file_name = FILE_NAME, thumb = THUMBNAIL, quote = True, document = output_file,
                caption = f"{caption}\n\n{FILE_CAPT}", progress = uploadProgress,
                progress_args = (dlMSG, time.time())
            )
            await dlMSG.delete()
            await work(callbackQuery, "delete", False)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
