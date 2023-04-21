# fileName : plugins/dm/callBack/file_process/invertPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/invertPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz
from PIL import Image

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
        with fitz.open(input_file) as iNPUT, fitz.open() as oUTPUT:
            for page_number, page in enumerate(iNPUT):
                # Get the page dimensions
                dimensions = page.MediaBox
                
                # Render the page to a PIL image
                pix = page.getPixmap(matrix=fitz.Matrix(1, 1)).get_data("rgb")
                img = Image.frombytes(mode="RGB", size=(pix.width, pix.height), data=pix)
                
                # Invert the colors of the PIL image
                inverted_img = ImageOps.invert(img)
                
                # Create a new PDF page with the same dimensions as the original
                output_page = output_pdf.new_page(width=dimensions.width, height=dimensions.height)
               
                # Draw the inverted image onto the new PDF page
                output_page.show_pdf_page(output_page.rect, inverted_img.tobytes(), page_number)
            
            # Add the new page to the output PDF
            oUTPUT.insert_pdf(output_page)
            
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
