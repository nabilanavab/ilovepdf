# fileName : plugins/dm/callBack/pdfFormatter.py
# copyright ©️ 2021 nabilanavab

import os
import time
import fitz
import shutil
from PIL import Image
from time import sleep
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF

#--------------->
#--------> LOCAL VARIABLES
#------------------->

# NB:
#    A4 paper size in pixels with a resolution of 72 PPI is 595 x 842 px.
#    Screens and monitors usually use 72 PPI
#    
#    In a resolution of 300 PPI A4 is 2480 x 3508 px.
#    For printing you often use 200-300 PPI

PDF_THUMBNAIL=Config.PDF_THUMBNAIL

#--------------->
#--------> PDF FORMATTER
#------------------->

a4format=["format", "Kformat"]
formatter=filters.create(lambda _, __, query: query.data.startswith(tuple(a4format)))

@ILovePDF.on_callback_query(formatter)
async def _formatter(bot, callbackQuery):
    try:
        # CHECKS IF BOT DOING ANY WORK
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "Work in progress.. 🙇"
            )
            return
        # CALLBACK DATA
        data=callbackQuery.data
        # DOWNLOAD MESSSAGE
        # IF PDF PAGE MORE THAN 5(PROCESS CANCEL)
        if data[0]=="K":
            _, number_of_pages=callbackQuery.data.split("|")
            if int(number_of_pages) >= 5:
                await callbackQuery.answer("Send Me A File Less Than 5 Pages..🏃")
                return
        # ADD TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        downloadMessage=await callbackQuery.message.reply_text(
            "`Downloding your pdf..` ⏳", quote=True
        )
        input_file=f"{callbackQuery.message.message_id}/unFormated.pdf"
        output_file = f"{callbackQuery.message.message_id}/formatted.pdf"
        file_id=callbackQuery.message.reply_to_message.document.file_id
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        fileNm=callbackQuery.message.reply_to_message.document.file_name
        fileNm, fileExt=os.path.splitext(fileNm)        # seperates name & extension
        
        # STARTED DOWNLOADING
        c_time=time.time()
        downloadLoc=await bot.download_media(
            message=file_id,
            file_name=input_file,
            progress=progress,
            progress_args=(
                fileSize, downloadMessage, c_time
            )
        )
        # CHECKS PDF DOWNLOADED OR NOT
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit("`Started Formatting..` 📖")
        # CHECK PDF OR NOT(HERE compressed, SO PG UNKNOWN)
        if data=="format":
            checked=await checkPdf(input_file, callbackQuery)
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
        unFormated=f'{callbackQuery.message.message_id}/unFormated.jpeg'
        # OPEN INPUT PDF
        r=fitz.Rect(0,0,0,0)
        with fitz.open(input_file) as inPDF:
            # OPENING AN OUTPUT PDF OBJECT
            with fitz.open() as outPDF:
                nOfPages=inPDF.pageCount
                if nOfPages > 5:
                    await downloadMessage.edit(
                        text="__For Some Reason A4 FORMATTING Supports for pdfs with less than 5 Pages__"
                             f"\n\nTotal Pages: {nOfPages} ⭐"
                    )
                    PROCESS.remove(callbackQuery.message.chat.id)
                    shutil.rmtree(f"{callbackQuery.message.message_id}")
                    return
                # ITERATE THROUGH PAGE NUMBERS
                for _ in range(nOfPages):
                    outPDF.new_page(pno=-1, width=595, height=842)
                    # WIDTH AND HEIGH OF PAGE 
                    page=inPDF[_]
                    pix=page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    # SAVE IMAGE AS NEW FILE
                    with open(unFormated,'wb'):
                        pix.save(unFormated)
                    with Image.open(unFormated) as img:
                        imgWidth, imgHeight = img.size
                        if imgWidth == imgHeight:
                            neWidth=595
                            newHeight=neWidth*imgHeight/imgWidth
                            newImage=img.resize((neWidth, int(newHeight)))
                            y0=(842-newHeight)/2; x0=(595-neWidth)/2
                            x1=x0+newHeight; y1=y0+neWidth
                            r=fitz.Rect(x0, y0, x1, y1)
                        elif imgWidth > imgHeight:
                            neWidth=595
                            newHeight=(neWidth*imgHeight)/imgWidth
                            newImage=img.resize((neWidth, int(newHeight)))
                            x0=0; y0=(842-newHeight)/2
                            x1=595; y1=y0+newHeight
                            r=fitz.Rect(x0, y0, x1, y1)
                        else:
                            newHeight=842
                            neWidth=(newHeight*imgWidth)/imgHeight
                            newImage=img.resize((int(neWidth), newHeight))
                            x0=(595-neWidth)/2; y0=0
                            x1=x0+neWidth; y1=842
                            r=fitz.Rect(x0, y0, x1, y1)
                        newImage.save(unFormated)
                    load=outPDF[_]
                    load.insert_image(
                        rect=r, filename=unFormated
                    )
                    os.remove(unFormated)
                outPDF.save(output_file)
        await callbackQuery.message.reply_chat_action("upload_document")
        await downloadMessage.edit("`Started Uploading..` 🏋️")
        await callbackQuery.message.reply_document(
            file_name=f"{fileNm}.pdf", quote=True,
            document=open(output_file, "rb"),
            thumb=PDF_THUMBNAIL, caption="formated PDF (A4)"
        )
        await downloadMessage.delete()
        PROCESS.remove(callbackQuery.message.chat.id)
        shutil.rmtree(f"{callbackQuery.message.message_id}")
    except Exception as e:
        try:
            print("FormatToA4: " , e)
            await downloadMessage.edit(f"ERROR: `{e}`")
            shutil.rmtree(f"{callbackQuery.message.message_id}")
            PROCESS.remove(callbackQuery.message.chat.id)
        except Exception:
            pass

#       ______                                                
#      |      |   _________    __    ___                      
#      |      |  |         |  |  |  |   |                     
#      |  A4  |  |    B    |  |B`|  |___|                     
#      |      |  |_________|  |__|    B``                     
#      |______|                                @ nabilanavab  
#                                                             
#   ° 1st resize image B (large side with rt. A4 sheet)       
#   ° height & width must be in same ratio(pillow)            
#   ° get values for B(x⁰, y⁰, x¹, y¹) on A4                  
#   ° Insert B to A4 (here pymuPdf) fitz                      
#                                                             
#                                                                                  Telegram: @nabilanavab
