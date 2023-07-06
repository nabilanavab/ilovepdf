# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

import fitz
from PIL import Image, ImageOps


async def invertPDF(input_file: str, cDIR: str) -> (bool, str):
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
        with fitz.open(input_file) as iNPUT, fitz.open() as oUTPUT:  # empty output PDF
            for pg in range(iNPUT.page_count):
                iNPUT[pg].get_pixmap().save(f"{cDIR}/temp.png")
                with Image.open(f"{cDIR}/temp.png") as image:
                    ImageOps.invert(image).save(f"{cDIR}/temp.png")
                    oUTPUT.insert_file(infile=f"{cDIR}/temp.png")
            oUTPUT.save(output_path, garbage=3, deflate=True)

        return True, output_path

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
