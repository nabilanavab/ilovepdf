# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/file_process/splitPDF.py"

from logger import logger
from PyPDF2 import PdfWriter, PdfReader


async def splitPDF(input_file: str, cDIR: str, imageList: list) -> (bool, str):
    """
     The function to split a PDF file into smaller PDF files based on the number of pages or a specific
     range of pages is a useful tool for managing large PDF files

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
        splitOutput = PdfWriter()

        for i in imageList:
            if i <= len(splitInputPdf.pages):
                splitOutput.add_page(splitInputPdf.pages[i - 1])

        with open(output_path, "wb") as output_stream:
            splitOutput.write(output_stream)

        return True, output_path

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
