# fileName : plugins/dm/callBack/file_process/decryptPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/decryptPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def decryptPDF(input_file: str, password: str, cDIR: str) -> ( bool, str ):
    try:
        """
        Decryption of a PDF file involves removing the encryption that has been applied to the
        file so that it can be read and accessed by an authorized user.
        
        parameter:
            input_file : Here is the path of the file that the user entered
            password   : Password entered by the user for pdf encryption
            cDIR       : This is the location of the directory that belongs to the specific user.
        
        return:
            bool        : Return True when the request is successful
            output_path : This is the path where the output file can be found.
        """
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            iNPUT.authenticate(f"{password}")
            iNPUT.save(output_path)
        return True, output_path
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
