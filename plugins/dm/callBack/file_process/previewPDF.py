# fileName : plugins/dm/callBack/file_process/previewPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/previewPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import      fitz
from PIL    import Image

async def previewPDF(input_file: str, cDIR: str) -> ( bool, str ):
    try:
        """
        Using this method, you can easily convert a PDF to black and white pages
        
        parameter:
            input_file : Here is the path of the file that the user entered
            cDIR       : This is the location of the directory that belongs to the specific user.
        
        return:
            bool        : Return True when the request is successful
            output_path : This is the path where the output file can be found.
        """
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            logger.debug(iNPUT.page_count)
            logger.debug(str(iNPUT.page_count)[3:])
            
            if iNPUT.page_count <= 10:
                preview = list(range(iNPUT.page_count + 1))
            elif iNPUT.page_count % 2 == 1:
                pass
                #preview = str(iNPUT.page_count[3:] + [iNPUT.page_count//2:(iNPUT.page_count//2)+2] + iNPUT.page_count[-3:1])
            else:
                pass
                #preview = iNPUT.page_count[3:] + [(iNPUT.page_count//2)-1:(iNPUT.page_count//2)+3] + iNPUT.page_count[-3:1]
            
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
