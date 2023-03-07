# fileName : plugins/dm/callBack/file_process/splitPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/splitPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

from PyPDF2          import PdfFileWriter, PdfFileReader

async def splitPDF(input_file: str, cDIR: str, imageList: list) -> ( bool, str):
    """
     function that allows you to fetch pages from a PDF file. Essentially, this means that you can extract specific pages
     from a large PDF document without having to download the entire file. For example, if you only need a few pages from a
     200-page PDF, you can use this function to extract just those pages and save yourself a lot of time and data usage.
     This feature is especially helpful for users who frequently work with large PDF documents and need to extract specific
     information quickly and efficiently.
    
    parameter:
        input_file    : Here is the path of the file that the user entered
        cDIR          : This is the location of the directory that belongs to the specific user.
        imageList     : List of page numbers that the user requires
        
    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        output_path = f"{cDIR}/outPut.pdf"
        splitInputPdf = PdfReader(input_file)
        number_of_pages = int(splitInputPdf.getNumPages())
        
        splitOutput = PdfWriter()
        
        for i in imageList:
            if int(i) <= number_of_pages:
                splitOutput.addPage(splitInputPdf.getPage(int(i)-1))
        
        with open(output_path, "wb") as output_stream:
            splitOutput.write(output_stream)
        
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
