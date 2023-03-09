# fileName : plugins/dm/callBack/file_process/deletePDFPg.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/deletePDFPg.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def deletePDFPg(input_file: str, cDIR: str, imageList: list) -> ( bool, str):
    """
     Delete specified pages from a PDF file and save the modified PDF to a new file.
    
    parameter:
        input_file    : Here is the path of the file that the user entered
        cDIR          : This is the location of the directory that belongs to the specific user.
        imageList     : List of page numbers that the user want to delete
        
    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        output_path = f"{cDIR}/outPut.pdf"
        
        dltList = [x-1 for x in imageList]
        with fitz.open(input_file) as iNPUT:
            del iNPUT[dltList]
            iNPUT.save(output_path)
        
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
