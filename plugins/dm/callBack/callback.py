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
from pyrogram.types  import InlineKeyboardMarkup, InlineKeyboardButton

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
            tTXT, tBTN = await util.translate(button = "PDF_MESSAGE['pdf_button']", order = 22222221, lang_code = lang_code)
            return await callbackQuery.message.edit_reply_markup(tBTN)
        
        data = data.split("|", 1)[1]
        
        if data == "rotate":
            tTXT, tBTN = await util.translate(button = "BUTTONS['rotate']", order = 1221, lang_code = lang_code)
        elif data == "txt":
            tTXT, tBTN = await util.translate(button = "BUTTONS['txt']", order = 1221, lang_code = lang_code)
        elif data == "meta":
            tTXT, tBTN = await util.translate(button = "BUTTONS['meta']", order = 121, lang_code = lang_code)
        elif data == "lock":
            tTXT, tBTN = await util.translate(button = "BUTTONS['lock']", order = 121, lang_code = lang_code)
        elif data == "trim":
            tTXT, tBTN = await util.translate(button = "BUTTONS['trim']", order = 121, lang_code = lang_code)
        elif data == "format":
            tTXT, tBTN = await util.translate(button = "BUTTONS['format']", order = 112211, lang_code = lang_code)
        elif data == "trade":
            tTXT, tBTN = await util.translate(button = "BUTTONS['trade']", order = 121, lang_code = lang_code)
        elif data == "filter":
            tTXT, tBTN = await util.translate(button = "BUTTONS['filter']", order = 1211, lang_code = lang_code)
        elif data == "comocr":
            tTXT, tBTN = await util.translate(button = "BUTTONS['comocr']", order = 121, lang_code = lang_code)
        elif data == "addlt":
            tTXT, tBTN = await util.translate(button = "BUTTONS['addlt']", order = 121, lang_code = lang_code)
        elif data == "T2P":
            tTXT, tBTN = await util.translate(button = "pdf2TXT['font_btn']", order = 12121, lang_code = lang_code)
        
        elif data.startswith("wa"):
            if data == "wa":
                tTXT, tBTN = await util.translate(button = "BUTTONS['type']", order = 131, lang_code = lang_code)
            else:
                typ = data.split("|")[1]
                if "o" not in data:
                    tTXT, tBTN = await util.translate(text = "BUTTONS['op']", lang_code = lang_code)
                    tTXT = await util.editDICT(inDir = tTXT, value = typ, front = f"{typ}".upper())
                    tTXT = await util.createBUTTON(tTXT, "1551")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
                elif "p" not in data:
                    data = data.split("|")[-1]
                    if typ == "txt":
                        tTXT, tBTN = await util.translate(text = "BUTTONS['poTXT']", lang_code = lang_code)
                    else:
                        tTXT, tBTN = await util.translate(text = "BUTTONS['po']", lang_code = lang_code)
                    tTXT = await util.editDICT(inDir = tTXT, value = [typ, data], front = f"{typ}".upper())
                    tTXT = await util.createBUTTON(tTXT, "131")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
                else:
                    data, color = data.split("|")[-2:]
                    tTXT, tBTN = await util.translate(text = "BUTTONS['color']", lang_code = lang_code)
                    tTXT = await util.editDICT(inDir = tTXT, value = [typ, data, color], front = f"{typ}".upper())
                    tTXT = await util.createBUTTON(tTXT, "13331")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
        
        elif data.startswith("img"):
            if data == "img":
                tTXT, tBTN = await util.translate(button="BUTTONS['toImage']", order=1221, lang_code=lang_code)
            else:
                data = data.split("|", 1)[1]
                tTXT, tBTN = await util.translate(text = "BUTTONS['imgRange']", lang_code = lang_code)
                tTXT = await util.editDICT(inDir = tTXT, value = imgg[f"{data}"], front = f"{data}".upper())
                tTXT = await util.createBUTTON(tTXT, "121")
                return await callbackQuery.message.edit_reply_markup(tTXT)
        
        elif data.startswith("stp"):
            if data == "stp":
                tTXT, tBTN = await util.translate(button="BUTTONS['stamp']", order=1112222221, lang_code=lang_code)
            else:
                data = int(data.split("|", 1)[1])
                tTXT, _ = await util.translate(text = "BUTTONS['stampA']", lang_code =lang_code)
                tTXT = await util.editDICT(inDir = tTXT, value = f"{data}", front = f"{annotSet[data]}".upper())
                tTXT = await util.createBUTTON(tTXT, "122221")
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

aio = filters.create(lambda _, __, query: query.data.startswith("aio"))
@ILovePDF.on_callback_query(aio)
async def _aio(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return
        
        await callbackQuery.answer()
        data = callbackQuery.data
        
        if data == "aio":
            tTXT, tBTN = await util.translate(text="AIO['aio']", button = "AIO['aio_button']", order = 121, lang_code = lang_code)
            return await callbackQuery.message.edit(
                text = tTXT.format(callbackQuery.message.reply_to_message.document.file_name, 
                                 await render.gSF(callbackQuery.message.reply_to_message.document.file_size)),
                reply_markup = tBTN
            )
        
        # encrypted input pdf file
        elif data == "aioInput|enc":
            tTXT, tBTN = await util.translate(text = "AIO", order = 1, lang_code = lang_code)
            tBTN = await util.createBUTTON(btn=tTXT['waitPASS'])
            await callbackQuery.message.edit_reply_markup(tBTN)
            input_str = await bot.listen(chat_id = callbackQuery.from_user.id)
            while not input_str.text:
                await input_str.delete()
                input_str = await bot.listen(chat_id = callbackQuery.from_user.id)
            await input_str.delete()
            
            aio_list_btn = []
            for index, (key, value) in enumerate(tTXT['out_button'].items()):
                btn = [InlineKeyboardButton(key, value)]
                try:
                    btn.append(InlineKeyboardButton(tTXT['false'] if tTXT['out_values'][index].endswith("{F}") else tTXT['true'] , tTXT['out_values'][index]))
                except: pass
                aio_list_btn.append(btn)
            return await callbackQuery.message.edit(
                text = tTXT['passMSG'].format(callbackQuery.message.reply_to_message.document.file_name,   #password 300 char limit
                    await render.gSF(callbackQuery.message.reply_to_message.document.file_size), input_str.text[:300], None, None, None ),
                reply_markup = InlineKeyboardMarkup(aio_list_btn)
            )
        # non encrypted input pdf file
        elif data == "aioInput|dec":
            tTXT, tBTN = await util.translate(text = "AIO", order = 1, lang_code = lang_code)
            
            aio_list_btn = []
            for index, (key, value) in enumerate(tTXT['out_button'].items()):
                btn = [InlineKeyboardButton(key, value)]
                try:
                    btn.append(InlineKeyboardButton(tTXT['false'] if tTXT['out_values'][index].endswith("{F}") else tTXT['true'] , tTXT['out_values'][index]))
                except: pass
                aio_list_btn.append(btn)
            return await callbackQuery.message.edit(
                text = tTXT['passMSG'].format(callbackQuery.message.reply_to_message.document.file_name,   #password 300 char limit
                    await render.gSF(callbackQuery.message.reply_to_message.document.file_size), None, None, None, None ),
                reply_markup = InlineKeyboardMarkup(aio_list_btn)
            )
        
        message_data = callbackQuery.message.text.split("•")
        for i in message_data:
            logger.debug(i)
            logger.debug("\n--------------------------------")
        
        # data1 = "meta/enc/form/comp/water/n.." , data2 = "{}/True/False"
        data1, data2 = data.split("|")[1:]
        buttons = callbackQuery.message.reply_markup.inline_keyboard
        callback = [element.callback_data for button in buttons for index, element in enumerate(button, start=1) if index % 2 == 0]
        all_data = [ '{F}' if element.endswith('{F}') else element.split("|")[-1] for element in callback ]
        dataARRANGEMENT = { "met" : 0, "pre" : 1, "txt" : 2, "rot" : 3, "enc" : 4, "for" : 5, "com" : 6, "wat" : 7, "rnm" : 8 }
        
        logger.debug(all_data)
        if data1 in [ "met", "pre", "com" ]:
            data_1 = dataARRANGEMENT.get(data1)
            if isinstance(data_1, int):
                if all_data[data_1] == False: all_data[data_1] = True
                elif all_data[data_1] == True: all_data[data_1] = False
            else: return
            
            tTXT, tBTN = await util.translate(text="AIO", lang_code = lang_code)
            
            aio_list_btn = []
            for index, (key, value) in enumerate(tTXT['out_button'].items()):
                btn = [InlineKeyboardButton(key, value)]
                try: btn.append(InlineKeyboardButton(
                        tTXT['true'] if all_data[index]!="{F}" else tTXT['false'] ,
                        tTXT['out_values'][index].format(F=all_data[index]))
                    )
                except: pass
                aio_list_btn.append(btn)
            return await callbackQuery.message.edit_reply_markup(InlineKeyboardMarkup(aio_list_btn))
        
        elif data1 in [ "enc", "rnm", "wat" ]:
            tTXT, tBTN = await util.translate(text="AIO", lang_code = lang_code)
            tBTN = await util.createBUTTON(btn=tTXT['waitPASS'])
            await callbackQuery.message.edit_reply_markup(tBTN)
            input_str = await bot.listen(chat_id = callbackQuery.from_user.id)
            while not input_str.text:
                await input_str.delete()
                input_str = await bot.listen(chat_id = callbackQuery.from_user.id)
            await input_str.delete()
            
            if input_str.text != "/exit":
                data_1 = dataARRANGEMENT.get(data1)
                if isinstance(data_1, int):
                    if all_data[data_1] == False: all_data[data_1] = True
                    elif all_data[data_1] == True: all_data[data_1] = False
                else: return
            
            aio_list_btn = []
            for index, (key, value) in enumerate(tTXT['out_button'].items()):
                btn = [InlineKeyboardButton(key, value)]
                try: btn.append(InlineKeyboardButton(
                        tTXT['true'] if all_data[index] else tTXT['false'] ,
                        tTXT['out_values'][index].format(F="{T}" if all_data[index] else "{F}"))
                    )
                except: pass
                aio_list_btn.append(btn)
            return await callbackQuery.message.edit_reply_markup(InlineKeyboardMarkup(aio_list_btn))
        
        if data1 in [ "txt", "rot", "form" ]:
            data_1 = dataARRANGEMENT.get(data1)
            if isinstance(data_1, int):
                if all_data[data_1] == False: all_data[data_1] = True
                elif all_data[data_1] == True: all_data[data_1] = False
            else: return
            
            tTXT, tBTN = await util.translate(text="AIO", lang_code = lang_code)
            
            aio_list_btn = []
            for index, (key, value) in enumerate(tTXT['out_button'].items()):
                btn = [InlineKeyboardButton(key, value)]
                try: btn.append(InlineKeyboardButton(
                        tTXT['true'] if all_data[index] else tTXT['false'] ,
                        tTXT['out_values'][index].format(F="{T}" if all_data[index] else "{F}"))
                    )
                except: pass
                aio_list_btn.append(btn)
            return await callbackQuery.message.edit_reply_markup(InlineKeyboardMarkup(aio_list_btn))
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)

# Author: @nabilanavab
