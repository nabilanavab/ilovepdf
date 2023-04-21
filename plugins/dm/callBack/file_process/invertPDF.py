# fileName : plugins/dm/callBack/file_process/invertPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/invertPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def invertPDF(input_file: str, cDIR: str) -> ( bool, str ):
    """
    Using this method, you can easily convert a PDF to invert color
    
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
                for page in iNPUT:
                    pix = page.get_pixmap()
                    pixmap_invert = fitz.Pixmap(pix)
                    pixmap_invert.invert()
                    page_pixmap_invert = fitz.Pixmap(pixmap_invert, 0)
                    inv_page = new_doc.newPage(width = page_pixmap_invert.width, height = page_pixmap_invert.height)
                    inv_page.showPDFpage(page.rect, page)
                    inv_page.insertImage(page_pixmap_invert)
                    new_doc.insertPDF(inv_page)
                oUTPUT.save(output_path)
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
