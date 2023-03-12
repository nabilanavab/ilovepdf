# fileName : plugins/dm/callBack/index.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/index.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

import os, time
from plugins.utils    import *
from configs.config   import images
from pyrogram         import enums, filters, Client as ILovePDF

from .file_process import *

index = filters.create(lambda _, __, query: query.data.startswith("^"))
@ILovePDF.on_callback_query(index)
async def __index__(bot, callbackQuery):
    try:
        data = callbackQuery.data[1:]
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        
        if await render.header(bot, callbackQuery, lang_code = lang_code):
            return
        
        CHUNK, _ = await util.translate(text = "INDEX", button = "INDEX['button']", lang_code = lang_code)
        
        if not callbackQuery.message.reply_to_message and callbackQuery.message.reply_to_message.document:
            await work.work(callbackQuery, "delete", False)
            return await callbackQuery.message.reply_text("#old_queue 💔\n\n`try by sending new file`", reply_markup = _, quote = True)
        
        # create a brand new directory to store all of your important user data
        cDIR = await work.work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        dlMSG = await callbackQuery.message.reply_text(CHUNK["download"], reply_markup = _, quote = True)
        
        # download the mentioned PDF file with progress updates
        input_file = await bot.download_media(
            message = callbackQuery.message.reply_to_message.document.file_id,
            file_name = f"{cDIR}/inPut.pdf", progress = render.progress, progress_args = (
                callbackQuery.message.reply_to_message.document.file_size, dlMSG, time.time()
            )
        )
        
        await dlMSG.edit(text = CHUNK["completed"], reply_markup = _)
        
        # The program checks the size of the file and the file on the server to avoid errors when canceling the download
        if os.path.getsize(input_file) != callbackQuery.message.reply_to_message.document.file_size:    
            return await work.work(callbackQuery, "delete", False)
        
        inPassword, outName, watermark, outPassword  = callbackQuery.message.text.split("•")[1::2]
        buttons = callbackQuery.message.reply_markup.inline_keyboard
        callback = [element.callback_data for button in buttons for index, element in enumerate(button, start=1) if index % 2 == 0]
        all_data = [ '{F}' if element.endswith('{F}') else element.split("|")[-1] for element in callback ][:-1]
        
        WORKS = {
            "metadata" : True if all_data[0]=="{T}" else False,
            "preview" : True if all_data[1]=="{T}" else False,
            "compress" : True if all_data[2]=="{T}" else False,
            "text" : all_data[3] if all_data[3]!="{F}" else False,
            "rotate" : all_data[4] if all_data[4]!="{F}" else False,
            "format" : all_data[5] if all_data[5]!="{F}" else False,
            "encrypt" : outPassword if all_data[6]!="{F}" and outPassword!=None else False,
            "watermark" : watermark if all_data[7]!="{F}" and watermark!=None else False,
            "rename" : outName if all_data[8]!="{F}" and outName!=None else False,
        }
        logger.debug(WORKS)
        
        await work.work(callbackQuery, "delete", False)
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        await work.work(callbackQuery, "delete", False)

# Author: @nabilanavab
