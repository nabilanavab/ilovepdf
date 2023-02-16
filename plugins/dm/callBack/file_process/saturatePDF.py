# fileName : plugins/dm/callBack/file_process/saturatePDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/saturatePDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def saturatePDF(input_file: str, cDIR: str) -> ( bool, str ):
    try:
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:        # empty output PDF
                for pg in range(iNPUT.page_count):
                    iNPUT[pg].get_pixmap().save(f"{cDIR}/temp.png")
                    with Image.open(f"{cDIR}/temp.png") as image:
                        image.convert("L").save(f"{cDIR}/temp.png")
                        rect = iNPUT[pg].rect
                        oUTPUT.new_page(pno = -1, width = rect.width, height = rect.height)
                        oUTPUT[pg].insert_image(rect = rect, filename = f"{cDIR}/temp.png")
                oUTPUT.save(output_path, garbage = 3, deflate = True)
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
