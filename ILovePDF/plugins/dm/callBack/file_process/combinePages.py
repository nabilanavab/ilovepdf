# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/file_process/combinePages.py"

import fitz
from logger import logger

async def combinePages(input_file: str, cDIR: str) -> (bool, str):
    """
    Combining PDF files allows you to merge multiple PDF documents into a single file.
    This can be useful for organizing and streamlining your PDF files, as well as for making it easier to share and store them.

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
            with fitz.open() as oUTPUT:  # empty output PDF
                width, height = fitz.paper_size("a4")
                r = fitz.Rect(0, 0, width, height)
                # define the 4 rectangles per page
                r1 = r / 2  # top left rect
                r2 = r1 + (r1.width, 0, r1.width, 0)  # top right
                r3 = r1 + (0, r1.height, 0, r1.height)  # bottom left
                r4 = fitz.Rect(r1.br, r.br)  # bottom right
                r_tab = [r1, r2, r3, r4]
                # now copy input pages to output
                for pages in iNPUT:
                    if pages.number % 4 == 0:  # create new output page
                        page = oUTPUT.new_page(-1, width=width, height=height)
                    # insert input page into the correct rectangle
                    page.show_pdf_page(r_tab[pages.number % 4], iNPUT, pages.number)
                    # by all means, save new file using garbage collection and compression
                oUTPUT.save(output_path, garbage=3, deflate=True)
        return True, output_path

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
