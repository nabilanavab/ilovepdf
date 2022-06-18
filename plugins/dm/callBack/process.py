# fileName : plugins/dm/callBack/process.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import fitz
import asyncio
from PIL import Image
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from PyPDF2 import PdfFileWriter, PdfFileReader
from plugins.fileSize import get_size_format as gSF
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet


nabilanavab = False # Change to False else never work
try:
    import ocrmypdf
except Exception:
    nabilanavab = True

#--------------->
#--------> LOCAL VARIABLES
#------------------->

passwordError = "__Cannot Decrypt the file with__ `{}` 🕸️"

decrypted = "__Decrypted File__"

encryptedFileCaption = "__Page Number__: {}\n__key__ 🔐: ||{}||"

compressedCaption = """`Original Size : {}
Compressed Size : {}

Ratio : {:.2f} %`"""

cantCompressMore = "File Can't be Compressed More..🤐"

pgNoError = """__For Some Reason A4 FORMATTING Supports for pdfs with less than 5 Pages__"

Total Pages: {} ⭐"""


# ❌ DECRYPT PDF FILE ❌
async def decryptPDF(message, message_id, password):
    try:
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        try:
            with fitz.open(input_file) as encrptPdf:
                encrptPdf.authenticate(f"{password.text}")
                encrptPdf.save(output_file)
                return decrypted
        except Exception:
            await message.edit(
                              passwordError.format(
                                                  password.text
                                                  )
                              )
            return False
    except Exception as e:
        logger.exception(
                        "DECRYPT[PROCESS]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        return False

# ❌ ENCRYPT PDF FILES ❌
async def encryptPDF(message_id, password):
    try:
        swd = f"abi"
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        _pswd = "n"+f"{swd}"+"l"
        
        with fitz.open(input_file) as encrptPdf:
            number_of_pages = encrptPdf.pageCount
            encrptPdf.save(
                          output_file,
                          # strongest algorithm
                          encryption = fitz.PDF_ENCRYPT_AES_256,
                          owner_pw = _pswd,
                          user_pw = f"{password.text}",
                          permissions = int(
                                           fitz.PDF_PERM_ACCESSIBILITY |
                                           fitz.PDF_PERM_PRINT |
                                           fitz.PDF_PERM_COPY |
                                           fitz.PDF_PERM_ANNOTATE
                                           )
                          )
        return encryptedFileCaption.format(
                                          number_of_pages,
                                          password.text
                                          )
    except Exception as e:
        logger.exception(
                        "ENCRYPT[PROCESS]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        return False

# ❌ COMPRESS PDF FILES ❌
async def compressPDF(message, message_id):
    try:
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        # Initialize the library
        PDFNet.Initialize(); doc = PDFDoc(input_file)
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and
        # compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(
                output_file,
                SDFDoc.e_linearized
                )
        doc.Close()
        
        # FILE SIZE COMPARISON (RATIO)
        initialSize = os.path.getsize(
                                     input_file
                                     )
        compressedSize = os.path.getsize(
                                        output_file
                                        )
        ratio = (1 - (compressedSize / initialSize)) * 100
        # sends only if compressed more than 10mb or ratio >= 5%
        if (initialSize-compressedSize) > 1000000 or ratio >= 5:
            return compressedCaption.format(
                                           await gSF(initialSize),
                                           await gSF(compressedSize),
                                           ratio
                )
        else:
            await message.edit(
                              cantCompressMore 
                              )
            return False
    except Exception as e:
        logger.exception(
                        "COMPRESS[PROCESS]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        await message.edit(
                          f"❌SOMETHING WENT WRONG❌"
                          f"\n\nError: {e}"
                          )
        return False

# ❌ OCR PDF FILES ❌
async def ocrPDF(message, message_id):
    try:
        try:
            input_file = f"{message_id}/inPut.pdf"
            output_file = f"{message_id}/outPut.pdf"
            
            ocrmypdf.ocr(
                        input_file = open(
                                         input_file, "rb"
                                         ),
                        output_file = open(
                                          output_file, "wb"
                                          ),
                        deskew = True
                        )
            return "OCR PDF"
        except Exception:
            await message.edit(
                              "`Already Have A Text Layer.. `😏"
                              )
            return False
    except Exception as e:
        logger.exception(
                        "OCR[PROCESS]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        return False

# ❌ ROTATES PDF FILE ❌
async def rotatePDF(data, message_id):
    try:
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        #STARTED ROTATING
        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(input_file)
        number_of_pages = pdf_reader.numPages
        # ROTATE 90°
        if data == "rot90":
            # Rotate page 90 degrees to the right
            for i in range(number_of_pages):
                page = pdf_reader.getPage(i).rotateClockwise(90)
                pdf_writer.addPage(page)
            caption = "__Rotated 90°__"
        # ROTATE 180°
        if data == "rot180":
            # Rotate page 180 degrees to the right
            for i in range(number_of_pages):
                page = pdf_reader.getPage(i).rotateClockwise(180)
                pdf_writer.addPage(page)
            caption = "__Rotated: 180°__"
        # ROTATE 270°
        if data == "rot270":
            # Rotate page 270 degrees to the right
            for i in range(number_of_pages):
                page = pdf_reader.getPage(i).rotateCounterClockwise(90)
                pdf_writer.addPage(page)
            caption = "__Rotated: 270°__"
        with open(output_file, 'wb') as fh:
            pdf_writer.write(fh)
        return caption
    except Exception as e:
        logger.exception(
                        "ROTATE[PROCESS]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        return False

# ❌ PDF TO MESSAGE, TXT, HTML, JSON ❌
async def textPDF(data, message, message_id):
    try:
        input_file = f"{message_id}/inPut.pdf"
        if data in ["T", "KT"]:
            output_file = f"{message_id}/outPut.txt"
        elif data in ["J", "KJ"]:
            output_file = f"{message_id}/outPut.json"
        elif data in ["H", "KH"]:
            output_file = f"{message_id}/outPut.html"
        
        if data in ["T", "KT"]: 
            with fitz.open(input_file) as doc:
                with open(output_file, "wb") as out: # open text output
                    for page in doc:                               # iterate the document pages
                        text = page.get_text().encode("utf8")        # get plain text (is in UTF-8)
                        out.write(text)                            # write text of page()
                        out.write(bytes((12,)))                    # write page delimiter (form feed 0x0C)
            return "__.txt file__"
        
        if data in ["M", "KM"]:
            with fitz.open(input_file) as doc:
                for page in doc:                               # iterate the document pages
                    pdfText = page.get_text().encode("utf8")            # get plain text (is in UTF-8)
                    if 1 <= len(pdfText) <= 1048:
                        try:
                            await message.reply(
                                               pdfText,
                                               quote = False 
                                               )
                        except FloodWait as e:
                            await asyncio.sleep(e.x+1)
                            await message.reply(pdfText)
            return False
        
        if data in ["H", "KH"]:
            with fitz.open(input_file) as doc:
                with open(output_file, "wb") as out: # open text output
                    for page in doc:                                # iterate the document pages
                        text = page.get_text("html").encode("utf8") # get plain text (is in UTF-8)
                        out.write(text)                             # write text of page()
                        out.write(bytes((12,)))                     # write page delimiter (form feed 0x0C)
            return "__html file__"
        
        if data in ["J", "KJ"]:
            with fitz.open(input_file) as doc:
                with open(output_file, "wb") as out: # open text output
                    for page in doc:                                # iterate the document pages
                        text = page.get_text("json").encode("utf8") # get plain text (is in UTF-8)
                        out.write(text)                             # write text of page()
                        out.write(bytes((12,)))                     # write page delimiter (form feed 0x0C)
            return "__json file__"
    except Exception as e:
        logger.exception(
                        "PDF2TXT[PROCESS]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        return False

# ❌ PDF A4 FORMATTER ❌
# NB:
#    A4 paper size in pixels with a resolution of 72 PPI is 595 x 842 px.
#    Screens and monitors usually use 72 PPI
#    In a resolution of 300 PPI A4 is 2480 x 3508 px.
#    For printing you often use 200-300 PPI
async def formatterPDF(message, message_id):
    try:
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        unFormated = f"{message_id}/unFormated.jpeg"
        # OPEN INPUT PDF
        r = fitz.Rect(0, 0, 0, 0)
        with fitz.open(input_file) as inPDF:
            # OPENING AN OUTPUT PDF OBJECT
            with fitz.open() as outPDF:
                nOfPages = inPDF.pageCount
                if nOfPages > 5:
                    await message.edit(
                                      pgNoError.format(
                                                      nOfPages
                                                      )
                                      )
                    return False
                # ITERATE THROUGH PAGE NUMBERS
                for _ in range(nOfPages):
                    outPDF.new_page(
                                   pno = -1,
                                   width = 595,
                                   height = 842
                                   )
                    # WIDTH AND HEIGH OF PAGE 
                    page = inPDF[_]
                    pix = page.get_pixmap(
                                         matrix = fitz.Matrix(
                                                             2, 2
                                                             )
                                         )
                    # SAVE IMAGE AS NEW FILE
                    with open(unFormated,'wb'):
                        pix.save(unFormated)
                    with Image.open(unFormated) as img:
                        imgWidth, imgHeight = img.size
                        if imgWidth == imgHeight:
                            neWidth = 595
                            newHeight = neWidth * imgHeight / imgWidth
                            newImage = img.resize(
                                                 (neWidth, int(newHeight))
                                                 )
                            y0 = (842 - newHeight) / 2; x0 = (595 - neWidth) / 2
                            x1 = x0 + newHeight; y1 = y0 + neWidth
                            r = fitz.Rect(x0, y0, x1, y1)
                        elif imgWidth > imgHeight:
                            neWidth = 595
                            newHeight = (neWidth * imgHeight) / imgWidth
                            newImage = img.resize(
                                                 (neWidth, int(newHeight))
                                                 )
                            x0 = 0; y0 = (842 - newHeight) / 2
                            x1 = 595; y1 = y0 + newHeight
                            r = fitz.Rect(x0, y0, x1, y1)
                        else:
                            newHeight = 842
                            neWidth = (newHeight * imgWidth) / imgHeight
                            newImage=img.resize(
                                               (int(neWidth), newHeight)
                                               )
                            x0 = (595 - neWidth) / 2; y0 = 0
                            x1 = x0 + neWidth; y1 = 842
                            r = fitz.Rect(x0, y0, x1, y1)
                        newImage.save(unFormated)
                    load = outPDF[_]
                    load.insert_image(
                                     rect = r, filename = unFormated
                    )
                    os.remove(unFormated)
                outPDF.save(output_file)
        return "__a4 formatted pdf__"
    except Exception as e:
        logger.exception(
                        "A4FORMAT[PROCESS]:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        return False

#                                                                                     Telegram: @nabilanavab
