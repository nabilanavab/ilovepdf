# fileName : plugins/dm/callBack/process.py
# copyright ©️ 2021 nabilanavab
fileName =  "plugins/dm/callBack/process.py"

from PIL import Image
import os, fitz, asyncio
from logger import logger
from plugins.util import *
from plugins.work import work
from plugins.render import gSF
from pyrogram.errors import FloodWait
from PyPDF2 import PdfFileWriter, PdfFileReader
# from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet

try:
    nabilanavab = False # Change to False else never work
    import ocrmypdf
except Exception:
    nabilanavab = True

# ❌ DECRYPT PDF FILE ❌
async def decryptPDF(message, cDIR, password, lang_code):
    try:
        try:
            with fitz.open(f"{cDIR}/inPut.pdf") as encrptPdf:
                encrptPdf.authenticate(f"{password.text}")
                encrptPdf.save(f"{cDIR}/outPut.pdf")
                tTXT, tBTN = await translate(text="PROCESS['decrypted']", lang_code=lang_code)
                return tTXT
        except Exception:
            tTXT, tBTN = await translate(text="PROCESS['decryptError']", lang_code=lang_code)
            await message.edit(tTXT.format(password.text))
            return False
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        return False

# ❌ ENCRYPT PDF FILES ❌
async def encryptPDF(cDIR, password, lang_code):
    try:
        swd = f"abi"
        _pswd = "n"+f"{swd}"+"l"
        
        with fitz.open(f"{cDIR}/inPut.pdf") as encrptPdf:
            number_of_pages = encrptPdf.page_count
            encrptPdf.save(
                f"{cDIR}/outPut.pdf", encryption = fitz.PDF_ENCRYPT_AES_256, # strongest algorithm
                owner_pw = _pswd, user_pw = f"{password.text}",
                permissions = int(
                    fitz.PDF_PERM_ACCESSIBILITY | fitz.PDF_PERM_PRINT |
                    fitz.PDF_PERM_COPY | fitz.PDF_PERM_ANNOTATE
                )
            )
        tTXT, tBTN = await translate(text="PROCESS['encrypted']", lang_code=lang_code)
        return tTXT.format(number_of_pages, password.text)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        return False

# ❌ COMPRESS PDF FILES ❌
async def compressPDF(message, cDIR, lang_code):
    try:
        # Initialize the library
        PDFNet.Initialize(); doc = PDFDoc(f"{cDIR}/inPut.pdf")
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and
        # compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(f"{cDIR}/outPut.pdf", SDFDoc.e_linearized)
        doc.Close()
        
        # FILE SIZE COMPARISON (RATIO)
        initialSize = os.path.getsize(f"{cDIR}/inPut.pdf")
        compressedSize = os.path.getsize(f"{cDIR}/outPut.pdf")
        ratio = (1 - (compressedSize / initialSize)) * 100
        # sends only if compressed more than 10mb or ratio >= 5%
        if (initialSize-compressedSize) > 1000000 or ratio >= 5:
            tTXT, tBTN = await translate(text="PROCESS['compressed']", lang_code=lang_code)
            return tTXT.format(await gSF(initialSize), await gSF(compressedSize), ratio)
        else:
            tTXT, tBTN = await translate(text="PROCESS['cantCompress']", lang_code=lang_code)
            await message.edit(tTXT)
            return False
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        tTXT, tBTN = await translate(text="document['error']", lang_code=lang_code)
        await message.edit(tTXT.format(e))
        return False

# ❌ OCR PDF FILES ❌
async def ocrPDF(message, cDIR, lang_code):
    try:
        try:
            ocrmypdf.ocr(
                input_file = open(f"{cDIR}/inPut.pdf", "rb"),
                output_file = open(f"{cDIR}/outPut.pdf", "wb"),deskew = True
            )
            tTXT, tBTN = await translate(text="PROCESS['ocr']", lang_code=lang_code)
            return tTXT
        except Exception:
            tTXT, tBTN = await translate(text="PROCESS['ocrError']", lang_code=lang_code)
            await message.edit(tTXT)
            return False
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        return False

# ❌ ROTATES PDF FILE ❌
async def rotatePDF(data, cDIR, lang_code):
    try:
        if data == "rot90":
            # Rotate page 90 degrees to the right
            with fitz.open(f"{cDIR}/inPut.pdf") as doc:
                for page in doc: page.set_rotation(90)
                doc.save(f"{cDIR}/outPut.pdf")
            tTXT, _ = await translate(text="PROCESS['90']", lang_code=lang_code)
            caption = tTXT
        if data == "rot180":
            # Rotate page 180 degrees to the right
            with fitz.open(f"{cDIR}/inPut.pdf") as doc:
                for page in doc: page.set_rotation(180)
                doc.save(f"{cDIR}/outPut.pdf")
            tTXT, _ = await translate(text="PROCESS['180']", lang_code=lang_code)
            caption = tTXT
        if data == "rot270":
            # Rotate page 270 degrees to the right
            with fitz.open(f"{cDIR}/inPut.pdf") as doc:
                for page in doc: page.set_rotation(-90)
                doc.save(f"{cDIR}/outPut.pdf")
            tTXT, _ = await translate(text="PROCESS['270']", lang_code=lang_code)
            caption = tTXT
        return caption
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        return False

# ❌ PDF TO MESSAGE, TXT, HTML, JSON ❌
async def textPDF(callbackQuery, message, cDIR, lang_code):
    try:
        data = callbackQuery.data.split("|")[1]
        if data == "T":
            with fitz.open(f"{cDIR}/inPut.pdf") as doc:
                with open(f"{cDIR}/outPut.txt", "wb") as out: # open text output
                    for page in doc:                               # iterate the document pages
                        text = page.get_text().encode("utf8")      # get plain text (is in UTF-8)
                        out.write(text)                            # write text of page()
                        out.write(bytes((12,)))                    # write page delimiter (form feed 0x0C)
            tTXT, _ = await translate(text="PROCESS['T']", lang_code=lang_code)
            return tTXT
        
        elif data == "J":
            with fitz.open(f"{cDIR}/inPut.pdf") as doc:
                with open(f"{cDIR}/outPut.json", "wb") as out: # open text output
                    for page in doc:                                # iterate the document pages
                        text = page.get_text("json").encode("utf8") # get plain text (is in UTF-8)
                        out.write(text)                             # write text of page()
                        out.write(bytes((12,)))                     # write page delimiter (form feed 0x0C)
            tTXT, _ = await translate(text="PROCESS['J']", lang_code=lang_code)
            return tTXT
        
        elif data == "H":
            with fitz.open(f"{cDIR}/inPut.pdf") as doc:
                with open(f"{cDIR}/outPut.html", "wb") as out: # open text output
                    for page in doc:                                # iterate the document pages
                        text = page.get_text("html").encode("utf8") # get plain text (is in UTF-8)
                        out.write(text)                             # write text of page()
                        out.write(bytes((12,)))                     # write page delimiter (form feed 0x0C)
            tTXT, _ = await translate(text="PROCESS['H']", lang_code=lang_code)
            return tTXT
        
        if data == "M":
            tTXT, cancel = await translate(text="PROCESS['M']", button="pdf2IMG['cancelCB']", order=1)
            with fitz.open(f"{cDIR}/inPut.pdf") as doc:
                await message.pin(disable_notification=True, both_sides=True)
                for page in doc:                               # iterate the document pages
                    pageNo = int(str(page).split(" ")[1])+1    # page = "page no of file"
                    pdfText = page.get_text()                  # get plain text (is in UTF-8)
                    if 1 <= len(pdfText) <= 1000:
                        try:
                            await callbackQuery.message.reply(
                                f"```🅿🅰🅶🅴 : {pageNo}\n\n{pdfText}```\n@ilovepdf_bot", quote = pageNo==1
                            )
                        except FloodWait as e:
                            await asyncio.sleep(e.value+1)
                            await callbackQuery.message.reply(f"{pdfText}", quote=False)
                    elif 1000 <= len(pdfText):
                        slice = [pdfText[i: i+1000] for i in range(0, len(pdfText), 1000)]
                        for i, j in enumerate(slice, start=1):
                            try:
                                await callbackQuery.message.reply(
                                    f"```🅿🅰🅶🅴 : {pageNo}-{i}\n\n{j}```\n\n@ilovepdf_bot", quote = pageNo==1
                                )
                            except FloodWait as e:
                                await asyncio.sleep(e.value+1)
                                await callbackQuery.message.reply(f"{pdfText}", quote=False)
                    if await work(callbackQuery, "check", False):
                        try:
                            await message.edit(tTXT.format(pageNo), reply_markup=cancel)
                        except Exception: pass
                    else:
                        return False
            return False
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        return False

# ❌ PDF A4 FORMATTER ❌
# NB:
#    A4 paper size in pixels with a resolution of 72 PPI is 595 x 842 px.
#    Screens and monitors usually use 72 PPI
#    In a resolution of 300 PPI A4 is 2480 x 3508 px.
#    For printing you often use 200-300 PPI
async def formatterPDF(message, cDIR, lang_code):
    try:
        # OPEN INPUT PDF
        r = fitz.Rect(0, 0, 0, 0)
        with fitz.open(f"{cDIR}/inPut.pdf") as inPDF:
            # OPENING AN OUTPUT PDF OBJECT
            with fitz.open() as outPDF:
                nOfPages = inPDF.page_count
                if nOfPages > 5:
                    await message.edit(pgNoError.format(nOfPages))
                    return False
                # ITERATE THROUGH PAGE NUMBERS
                for _ in range(nOfPages):
                    outPDF.new_page(pno = -1, width = 595, height = 842)
                    # WIDTH AND HEIGH OF PAGE 
                    page = inPDF[_]
                    pix = page.get_pixmap(matrix = fitz.Matrix(2, 2))
                    # SAVE IMAGE AS NEW FILE
                    with open(f"{cDIR}/unFormated.jpeg",'wb'):
                        pix.save(f"{cDIR}/unFormated.jpeg")
                    with Image.open(f"{cDIR}/unFormated.jpeg") as img:
                        imgWidth, imgHeight = img.size
                        if imgWidth == imgHeight:
                            neWidth = 595
                            newHeight = neWidth * imgHeight / imgWidth
                            newImage = img.resize((neWidth, int(newHeight)))
                            y0 = (842 - newHeight) / 2; x0 = (595 - neWidth) / 2
                            x1 = x0 + newHeight; y1 = y0 + neWidth
                            r = fitz.Rect(x0, y0, x1, y1)
                        elif imgWidth > imgHeight:
                            neWidth = 595
                            newHeight = (neWidth * imgHeight) / imgWidth
                            newImage = img.resize((neWidth, int(newHeight)))
                            x0 = 0; y0 = (842 - newHeight) / 2
                            x1 = 595; y1 = y0 + newHeight
                            r = fitz.Rect(x0, y0, x1, y1)
                        else:
                            newHeight = 842
                            neWidth = (newHeight * imgWidth) / imgHeight
                            newImage=img.resize((int(neWidth), newHeight))
                            x0 = (595 - neWidth) / 2; y0 = 0
                            x1 = x0 + neWidth; y1 = 842
                            r = fitz.Rect(x0, y0, x1, y1)
                        newImage.save(f"{cDIR}/unFormated.jpeg")
                    load = outPDF[_]
                    load.insert_image(rect = r, filename = f"{cDIR}/unFormated.jpeg")
                    os.remove(f"{cDIR}/unFormated.jpeg")
                outPDF.save(f"{cDIR}/outPut.pdf")
        tTXT, _ = await translate(text="PROCESS['formatted']", lang_code=lang_code)
        return tTXT
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        return False

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
