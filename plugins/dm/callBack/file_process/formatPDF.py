# fileName : plugins/dm/callBack/file_process/formatPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/formatPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def formatPDF(input_file: str, cDIR: str) -> ( bool, str ):
    """
    A4 formatting is a technique for displaying and printing PDF documents, which involves
    aligning all pages of the document within the standard A4 paper size
    
    parameter:
        input_file : Here is the path of the file that the user entered
        cDIR       : This is the location of the directory that belongs to the specific user.
    
    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
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
