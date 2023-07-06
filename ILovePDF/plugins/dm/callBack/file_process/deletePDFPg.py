# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/file_process/deletePDFPg.py"

import fitz
from logger import logger

async def deletePDFPg(input_file: str, cDIR: str, imageList: list) -> (bool, str):
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

        dltList = [x - 1 for x in imageList]
        with fitz.open(input_file) as iNPUT:
            del iNPUT[dltList]
            iNPUT.save(output_path)

        return True, output_path

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
