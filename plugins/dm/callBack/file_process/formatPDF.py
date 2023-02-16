# fileName : plugins/dm/callBack/file_process/formatPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/formatPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def formatPDF(input_file: str, cDIR: str) -> tuple[ bool, str ]:
    try:
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:
                width, height = fitz.paper_size("a4")
                for page in iNPUT:
                    pg = oUTPUT.new_page(-1, width = width, height = height)
                    pg.show_pdf_page(pg.rect, iNPUT, page.number)
            oUTPUT.save(output_path, garbage = 3, deflate = True)
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
