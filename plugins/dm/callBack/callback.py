# fileName : plugins/dm/callBack/callback.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/callback.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from plugins.utils   import *
from configs.db      import myID
from logger          import logger
from datetime        import datetime
from lang            import langList
from pyrogram        import Client as ILovePDF, filters

imgg = {
    "img" : "I", "doc" : "D", "zip" : "zip", "tar" : "tar"
}
annotSet = {
    0 : "STAMP_Approved", 1 : "STAMP_AsIs", 2 : "STAMP_Confidential", 3 : "STAMP_Departmental",
    4 : "STAMP_Experimental", 5 : "STAMP_Expired", 6 : "STAMP_Final", 7 : "STAMP_ForComment",
    8 : "STAMP_ForPublicRelease", 9 : "STAMP_NotApproved", 10 : "STAMP_NotForPublicRelease",
    11 : "STAMP_Sold", 12 : "STAMP_TopSecret", 13 : "STAMP_Draft"
}

txt2pdf = {
    "t" : "Times", "c" : "Courier", "h" : "Helvetica (Default)", "s" : "Symbol", "z" : "Zapfdingbats",
}

pdf = filters.create(lambda _, __, query: query.data.startswith("pdf"))

@ILovePDF.on_callback_query(pdf)
async def _pdf(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return
        
        await callbackQuery.answer()
        data = callbackQuery.data
        
        if data == "pdf":
            # pdf : homePage(back2pdfreplyMessage)
            tTXT, tBTN = await util.translate(button = "PDF_MESSAGE['pdf_button']", order = 22222221, lang_code = lang_code)
            return await callbackQuery.message.edit_reply_markup(tBTN)
        
        data = data.split("|", 1)[1]
        
        if data == "rotate":
            tTXT, tBTN = await util.translate(button = "work['rotate']", order = 1221, lang_code = lang_code)
        elif data == "txt":
            tTXT, tBTN = await util.translate(button = "work['txt']", order = 1221, lang_code = lang_code)
        elif data == "split":
            tTXT, tBTN = await util.translate(button = "split['button']", order = 1221, lang_code = lang_code)
        elif data == "T2P":
            tTXT, tBTN = await util.translate(button = "pdf2TXT['font_btn']", order = 12121, lang_code = lang_code)
        
        elif data.startswith("wa"):
            if data == "wa":
                tTXT, tBTN = await util.translate(button = "wa['type']", order = 131, lang_code = lang_code)
            else:
                typ = data.split("|")[1]
                if "o" not in data:
                    tTXT, tBTN = await util.translate(text = "wa['op']", lang_code = lang_code)
                    tTXT = await util.editDICT(inDir = tTXT, value = typ, front = f"{typ}".upper())
                    tTXT = await util.createBUTTON(tTXT, "1551")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
                elif "p" not in data:
                    data = data.split("|")[-1]
                    if typ == "txt":
                        tTXT, tBTN = await util.translate(text = "wa['poTXT']", lang_code = lang_code)
                    else:
                        tTXT, tBTN = await util.translate(text = "wa['po']", lang_code = lang_code)
                    tTXT = await util.editDICT(inDir = tTXT, value = [typ, data], front = f"{typ}".upper())
                    tTXT = await util.createBUTTON(tTXT, "131")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
                else:
                    data, color = data.split("|")[-2:]
                    tTXT, tBTN = await util.translate(text = "wa['color']", lang_code = lang_code)
                    tTXT = await util.editDICT(inDir = tTXT, value = [typ, data, color], front = f"{typ}".upper())
                    tTXT = await util.createBUTTON(tTXT, "13331")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
        
        elif data.startswith("img"):
            if data == "img":
                tTXT, tBTN = await util.translate(button="pdf2IMG['toImage']", order=1221, lang_code=lang_code)
            else:
                data = data.split("|", 1)[1]
                tTXT, tBTN = await util.translate(text = "pdf2IMG['imgRange']", lang_code = lang_code)
                tTXT = await util.editDICT(inDir = tTXT, value = imgg[f"{data}"], front = f"{data}".upper())
                tTXT = await util.createBUTTON(tTXT, "121")
                return await callbackQuery.message.edit_reply_markup(tTXT)
        
        elif data.startswith("stp"):
            if data == "stp":
                tTXT, tBTN = await util.translate(button="stamp['stamp']", order=1112222221, lang_code=lang_code)
            else:
                data = int(data.split("|", 1)[1])
                tTXT, _ = await util.translate(text = "stamp['stampA']", lang_code =lang_code)
                tTXT = await util.editDICT(inDir = tTXT, value = f"{data}", front = f"{annotSet[data]}".upper())
                tTXT = await utilo.createBUTTON(tTXT, "122221")
                return await callbackQuery.message.edit_reply_markup(tTXT)
        
        elif data.startswith("font"):
            data = data.split("|", 1)[1]
            tTXT, _ = await util.translate(text = "pdf2TXT['size_btn']", lang_code = lang_code)
            tTXT = await util.editDICT(inDir = tTXT, value = f"{data}", front = f"{txt2pdf[data]}".upper())
            tTXT = await util.createBUTTON(tTXT, "12121")
            return await callbackQuery.message.edit_reply_markup(tTXT)
        
        # edit button
        return await callbackQuery.message.edit_reply_markup(tBTN)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(file_name, e), exc_info = True)

common = filters.create(lambda _, __, query: query.data.startswith("-|"))

@ILovePDF.on_callback_query(common)
async def _common(bot, callbackQuery):
    try:
        if callbackQuery.data == "-|refresh":
            await callbackQuery.answer("👍")
            BUTTON1, _ = await util.translate(text = "inline_query['TOP']", lang_code = "eng")
            _lang = { langList[lang][1]:f"https://t.me/{myID[0].username}?start=-l{lang}" for lang in langList }
            BUTTON1.update(_lang); BUTTON1.update({"♻" : "-|refresh"})
            BUTTON1 = await util.createBUTTON(
                btn = BUTTON1, order = int(f"1{((len(BUTTON1)-2)//3)*'3'}{(len(BUTTON1)-2)%3}1")
            )
            time = datetime.now()
            
            return await bot.edit_inline_text(
                callbackQuery.inline_message_id,
                text = "set Language: 🌐\n\n"
                       f"i ❤ PDF\nBot: @{myID[0].username}\n"
                       "Update Channel: @ilovepdf_bot\n\n"
                       f"`UPDATED: {time.strftime('%d:%B:%Y, %A')}`\n"
                       f"`TIME: {time.strftime('%I:%M %p')}`",
                reply_markup = BUTTON1
            )
        
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        data = callbackQuery.data.split("|")[1]
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return
        
        if data == "error":
            tTXT, tBTN = await util.translate(text = "cbAns[2]", lang_code = lang_code)
            return await callbackQuery.answer(tTXT)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(file_name, e), exc_info = True)

# Author: @nabilanavab
