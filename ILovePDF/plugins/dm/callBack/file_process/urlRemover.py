# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/file_process/urlRemover.py"

import fitz
from logger import logger

async def urlRemover(input_file: str, cDIR: str) -> (bool, str):
    """
    A URL remover tool is designed to identify and remove URLs (Uniform Resource Locators)
    from PDF documents, images, or text, converting them into plain words.

    parameter:
        input_file : Here is the path of the file that the user entered
        cDIR       : This is the location of the directory that belongs to the specific user.

    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:
                for page in iNPUT:
                    width, height = page.width, page.height
                    pg = oUTPUT.new_page(-1, width=width, height=height)
                    pg.show_pdf_page(pg.rect, iNPUT, page.number)
                oUTPUT.save(output_path, garbage=3, deflate=True)
        return True, output_path

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
