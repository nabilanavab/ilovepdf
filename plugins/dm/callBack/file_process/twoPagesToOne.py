# fileName : plugins/dm/callBack/file_process/twoPagesToOne.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/twoPagesToOne.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def twoPagesToOne(input_file: str, cDIR: str) -> ( bool, str ):
    """
    This function takes a PDF file with two pages per sheet and converts it to a single page per sheet format. 
    The output file will contain all pages from the input file in sequential order, but with each pair of pages 
    combined onto a single sheet. 
    
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
                r1 = fitz.Rect(0, 0, width/2, height)
                r2 = fitz.Rect(width/2, 0, width, height)
                r_tab = [ r1, r2 ]
                for page in iNPUT:
                    pg = oUTPUT.new_page(-1, width = width, height = height)
                    pg.show_pdf_page(r_tab[page.number % 2], iNPUT, page.number)
                oUTPUT.save(output_path, garbage = 3, deflate = True)
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
