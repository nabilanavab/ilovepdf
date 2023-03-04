# fileName : plugins/dm/callBack/file_process/rotatePDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/rotatePDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def rotatePDF(input_file: str, angle: str, cDIR: str) -> ( bool, str ):
    """
    If a PDF file is rotated incorrectly, rotating it can help to correct the orientation of the pages so that they are displayed properly.
    Rotating a PDF file can also allow you to change the viewing angle of the document, which can be helpful when examining images or graphics.
    
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
            if angle == "rot90":
                for page in doc: page.set_rotation(90)
            elif angle == "rot180":
                for page in doc: page.set_rotation(180)
            elif angle == "rot270":
                for page in doc: page.set_rotation(-90)
            doc.save(output_path)
        return True, output_path
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
