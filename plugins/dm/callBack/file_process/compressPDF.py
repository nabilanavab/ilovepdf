# fileName : plugins/dm/callBack/file_process/compressPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/compressPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import os, subprocess #, fitz
from PIL    import Image
# from PyPDF2 import PdfReader, PdfWriter

async def compressPDF(input_file: str, cDIR: str) -> ( bool, str ):
    """
    Compressing a PDF file can significantly reduce its file size, making it
    easier to share and store. This can be especially useful when sending files over
    the internet, as smaller file sizes can lead to faster uploading and downloading times.
    
    parameter:
        input_file : Here is the path of the file that the user entered
        cDIR       : This is the location of the directory that belongs to the specific user.
    
    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        """
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:
                for pg in range(iNPUT.page_count):
                    iNPUT[pg].get_pixmap().save(f"{cDIR}/temp.png")
                    with Image.open(f"{cDIR}/temp.png") as image:
                        rect = iNPUT[pg].rect
                        oUTPUT.new_page(pno = -1, width = rect.width, height = rect.height)
                        oUTPUT[pg].insert_image(rect = rect, filename = f"{cDIR}/temp.png")
                oUTPUT.save(output_path, garbage = 3, deflate = True)
        
        
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.compress_content_streams()  # This is CPU intensive!
            writer.add_page(page)
        writer.remove_images()
        with open(output_path, "wb") as f:
            writer.write(f)
        """
        output_path = f"{cDIR}/outPut.pdf"
        
        # Set the Ghostscript command and options to compress the PDF
        gs_command = 'gs'
        gs_options = ['-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS=/screen', '-dNOPAUSE', '-dQUIET', '-dBATCH', '-sOutputFile={}'.format(output_path), input_file]
        
        # Call Ghostscript to compress the PDF
        subprocess.call([gs_command] + gs_options)
        
        # FILE SIZE COMPARISON (RATIO)
        initialSize = os.path.getsize(input_file)
        compressedSize = os.path.getsize(output_path)
        ratio = (1 - (compressedSize / initialSize)) * 100
        
        #if (initialSize - compressedSize) > 1000000 or ratio >= 5:
        #    return await render.gSF(initialSize), await render.gSF(compressedSize), ratio
        #else:
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
