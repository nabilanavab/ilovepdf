# fileName : plugins/dm/callBack/file_process/textPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/textPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def textPDF(input_file: str, cDIR: str, data: str, message = None) -> ( bool, str ):
    try:
        if data == "textT":
            output_path = f"{cDIR}/outPut.txt"
            data = "text"
        elif data == "textH":
            output_path = f"{cDIR}/outPut.html"
            data = "html"
        elif data == "textJ":
            output_path = f"{cDIR}/outPut.json"
            data = "json"
        elif data == "textM":
            data = "message"
        
        with fitz.open(input_file) as iNPUT:
            if data != "message":
                with open(output_path) as oUTPUT:
                    for page in iNPUT:
                        text = page.get_text(data).encode("utf8")
                        oUTPUT.write(text)
                        oUTPUT.write(bytes((12,)))
            else:
                pass
        return True, output_path
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
