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
        
        # create a brand new directory to store all of your important user data
        cDIR = await work.work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])
        
        if not callbackQuery.message.reply_to_message and callbackQuery.message.reply_to_message.document:
            await work.work(callbackQuery, "delete", False)
            return await callbackQuery.message.reply_text("#old_queue 💔\n\n`try by sending new file`", reply_markup = _, quote = True)
        
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
        
        for work, work_info in WORKS.items():
            await dlMSG.edit(text = work, reply_markup = _)
            if work == "metadata" and work_info:
                _ , __ = await previewPDF.previewPDF(input_file=input_file, cDIR=cDIR, editMessage=dlMSG, callbackQuery=callbackQuery)
            elif work == "preview" and work_info:
                _ , __ = await previewPDF.previewPDF(input_file=input_file, cDIR=cDIR, editMessage=dlMSG, callbackQuery=callbackQuery)
            elif work == "compress" and work_info:
                _, __ = await compressPDF.compressPDF(input_file=input_file, cDIR=cDIR)
            elif work == "text" and work_info:
                _, __ = await textPDF.textPDF(input_file=input_file, cDIR=cDIR, data=f"text{all_data[3]}")
            elif work == "rotate" and work_info:
                _, __ = await rotatePDF.rotatePDF(input_file=input_file, angle=all_data[4].lower(), cDIR=cDIR)
            elif work == "format" and work_info:
                if work_info == "format1":
                    _, __ = await formatPDF.formatPDF(input_file=input_file, cDIR=cDIR)
                elif work_info == "format2v":
                    _, __ = await twoPagesToOne.twoPagesToOne(input_file=input_file, cDIR=cDIR)
                elif work_info == "format2h":
                    _, __ = await twoPagesToOneH.twoPagesToOneH(input_file=input_file, cDIR=cDIR)
                elif work_info == "format3v":
                    _, __ = await threePagesToOne.threePagesToOne(input_file=input_file, cDIR=cDIR)
                elif work_info == "format3h":
                    _, __ = await threePagesToOneH.threePagesToOneH(input_file=input_file, cDIR=cDIR)
                elif work_info == "format4":
                    _, __ = await combinePages.combinePages(input_file=input_file, cDIR=cDIR)
            elif work == "encrypt" and work_info:
                _, __ = await encryptPDF.encryptPDF(input_file=input_file, password=outPassword, cDIR=cDIR)
            elif work == "watermark" and work_info:
                pass
            elif work == "rename" and work_info:
                pass
            
            if ( _ or _ == "finished" ) and __ != "finished":
                os.remove(f"{cDIR}/inPut.pdf")
                os.rename(__, f"{cDIR}/inPut.pdf")
        await work.work(callbackQuery, "delete", False)
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        await work.work(callbackQuery, "delete", False)

# Author: @nabilanavab
