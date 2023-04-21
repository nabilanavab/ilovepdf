# fileName : plugins/dm/callBack/file_process/invertPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/invertPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import PyPDF2

async def invertPDF(input_file: str, cDIR: str) -> ( bool, str ):
    """
    Using this method, you can easily convert a PDF to invert color
    
    parameter:
        input_file : Here is the path of the file that the user entered
        cDIR       : This is the location of the directory that belongs to the specific user.
        
    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        output_path = f"{cDIR}/outPut.pdf"
        with open(input_file) as iNPUT:
            reader = PyPDF2.PdfFileReader(iNPUT)
            writer = PyPDF2.PdfFileWriter()
            
            for page in range(reader.getNumPages()):
                original_page = reader.getPage(page)
                writer.addPage(original_page)
        
                # Invert the colors of the page
                invert_color_page = original_page
                for content in invert_color_page['/Contents'].getObject():
                    if isinstance(content, PyPDF2.generic.ByteStringObject):
                        invert_color_page['/Contents'].getObject().setData(content.replace(b'/DeviceRGB', b'/DeviceCMYK'))
            
            writer.addPage(invert_color_page)
        
        with open(output_path, "wb") as oUTPUT:
            writer.write(oUTPUT)
            
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
