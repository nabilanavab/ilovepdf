# fileName : plugins/dm/callBack/file_process/encryptPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/encryptPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def encryptPDF(input_file: str, password: str, cDIR: str) -> Tuple[ bool, str ]:
    try:
        try:
            output_path = f"{cDIR}/outPut.pdf"
            with fitz.open(input_file) as iNPUT:
                number_of_pages = iNPUT.page_count
                iNPUT.save(
                    output_path,
                    encryption = fitz.PDF_ENCRYPT_AES_256, # strongest algorithm
                    owner_pw = "nabil",
                    user_pw = f"{password.text}",
                    permissions = int(
                        fitz.PDF_PERM_ACCESSIBILITY |
                        fitz.PDF_PERM_PRINT |
                        fitz.PDF_PERM_COPY |
                        fitz.PDF_PERM_ANNOTATE
                    )
                )
            return True, output_path
        except Exception as Error:
            return False, Error
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
