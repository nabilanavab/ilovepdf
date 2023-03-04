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
                for pg in range(iNPUT.page_count):
                    iNPUT[pg].get_pixmap().save(f"{cDIR}/temp.png")
                    with Image.open(f"{cDIR}/temp.png") as image:
                        rect = iNPUT[pg].rect
                        oUTPUT.new_page(pno = -1, width = rect.width, height = rect.height)
                        oUTPUT[pg].insert_image(rect = rect, filename = f"{cDIR}/temp.png")
                oUTPUT.save(output_path, garbage = 3, deflate = True)
        
        # FILE SIZE COMPARISON (RATIO)
        initialSize = os.path.getsize(input_file)
        compressedSize = os.path.getsize(output_path)
        ratio = (1 - (compressedSize / initialSize)) * 100
        
        #if (initialSize - compressedSize) > 1000000 or ratio >= 5:
        #    return await render.gSF(initialSize), await render.gSF(compressedSize), ratio
        #else:
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
