# fileName : plugins/dm/callBack/file_process/textPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/textPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def textPDF(input_file: str, cDIR: str, data: str, message=None) -> Tuple[ bool, str ]:
    try:
        if data != "M":
            return
        
        if data == "T":
            output_path = f"{cDIR}/outPut.pdf"
            data = "text"
        elif data == "H":
            output_path = f"{cDIR}/outPut.pdf"
            data = "html"
        elif data == "J":
            output_path = f"{cDIR}/outPut.pdf"
            data = "json"
        
        with fitz.open(input_file) as iNPUT:
            with open(output_path) as oUTPUT:
                for page in iNPUT:
                    text = page.get_text(data).encode("utf8")
                    oUTPUT.write(text)
                    oUTPUT.write(bytes((12,)))
                
        return True, output_path
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
