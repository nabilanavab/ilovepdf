# fileName : plugins/dm/callBack/file_process/ocrPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/ocrPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

try:
    nabilanavab = False # Change to False else never work
    import ocrmypdf
except Exception:
    nabilanavab = True

async def ocrPDF(input_file: str, cDIR: str) -> ( bool, str ):
    try:
        output_path = f"{cDIR}/outPut.pdf"
        ocrmypdf.ocr(
            input_file = open(input_file, "rb"),
            output_file = open(output_path, "wb"),
            deskew = True
        )
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
