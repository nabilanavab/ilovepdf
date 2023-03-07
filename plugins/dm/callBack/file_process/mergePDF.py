# fileName : plugins/dm/callBack/file_process/mergePDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/mergePDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

async def mergePDF(input_file: str, cDIR: str, imageList: list) -> ( bool, str):
    try:
        output_path = f"{cDIR}/outPut.pdf"
        
        
        
        return True, output_path
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
