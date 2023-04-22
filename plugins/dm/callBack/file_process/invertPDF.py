# fileName : plugins/dm/callBack/file_process/invertPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/invertPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz
from PIL import Image, ImageOps

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
            for i in range(iNPUT.page_count):
                page = iNPUT[i]
                
                # Convert the page to PNG and invert colors
                pix = page.get_pixmap(alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = ImageOps.invert(img)
                
                # Convert the inverted image back to Pixmap
                pix = fitz.Pixmap(img.tobytes(), 0)
                
                # Replace the original page with the inverted Pixmap
                page.set_pixmap(pix)
            
            iNPUT.save(output_path)
            
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
