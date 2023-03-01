# fileName : plugins/dm/callBack/file_process/compressPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/compressPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import os, fitz
from plugins.utils               import *

async def compressPDF(input_file: str, cDIR: str) -> ( bool, str ):
    try:
        output_path = f"{cDIR}/outPut.pdf"
        
        with fitz.open(input_file) as inPut:
            with fitz.open() as outPut:
                for page in inPut:
                    logger.debug(page)
                    outPage = outPut.new_page(-1, width=page.rect.width, height=page.rect.height)
                    outPage.show_pdf_page(outPage.rect, inPut, pages.number)
                outPut.save(output_path)
        
        # FILE SIZE COMPARISON (RATIO)
        initialSize = os.path.getsize(input_file)
        compressedSize = os.path.getsize(output_path)
        ratio = (1 - (compressedSize / initialSize)) * 100
        
        if (initialSize - compressedSize) > 1000000 or ratio >= 5:
            return await render.gSF(initialSize), await render.gSF(compressedSize), ratio
        else:
            return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
