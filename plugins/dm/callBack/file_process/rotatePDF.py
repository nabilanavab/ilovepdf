# fileName : plugins/dm/callBack/file_process/encryptPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/encryptPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def encryptPDF(input_file: str, angle: str, cDIR: str) -> ( bool, str ):
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
