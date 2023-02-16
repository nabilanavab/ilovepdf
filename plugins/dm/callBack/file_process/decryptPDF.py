# fileName : plugins/dm/callBack/file_process/decryptPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/decryptPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def decryptPDF(input_file: str, password: str, cDIR: str) -> Tuple[ bool, str ]:
    try:
        try:
            output_path = f"{cDIR}/outPut.pdf"
                with fitz.open(input_file) as iNPUT:
                iNPUT.authenticate(f"{password.text}")
                iNPUT.save(output_path)
            return True, output_path
        except Exception as Error:
            return False, Error
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
