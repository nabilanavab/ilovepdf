# fileName : plugins/dm/callBack/file_process/zipTarPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/zipTarPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz, os, shutil

async def pdfToImages(input_file: str, cDIR: str, imageList: list, text: str) -> ( bool, str):
    """
    
    
    """
    try:
        os.mkdir(f'{cDIR}/pgs')
        for i in imageList:
            page = doc.load_page(int(i)-1)
            pix = page.get_pixmap(matrix = mat)
            cnvrtpg += 1
            if cnvrtpg % 5 == 0:
                #edit
                if not await work(callbackQuery, "check", False):
                    #edit cancel
            with open(f'{cDIR}/pgs/{i}.jpg','wb'):
            pix.save(f'{cDIR}/pgs/{i}.jpg')
        directory = f'{cDIR}/pgs'
        
        output_path = f'{cDIR}/zipORtar'
        
        if data in ["zipA", "zipR", "zipS"]:
            shutil.make_archive(output_file, 'zip', directory)
        elif data in ["tarA", "tarR", "tarS"]:
            path = shutil.make_archive(output_file, 'tar', directory) 
        
        output_path += ".zip" if data == "zip" else "."tar"
    except Exception as Error:
        pass
        
