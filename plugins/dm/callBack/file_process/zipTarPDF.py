# fileName : plugins/dm/callBack/file_process/zipTarPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/zipTarPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz, os, shutil
from plugins.utils  import *

async def zipTarPDF(input_file: str, cDIR: str, callbackQuery, dlMSG, imageList: list, text: str) -> ( bool, str):
    """
    
    
    """
    try:
        cancel = await util.createBUTTON(btn=text["_cancelCB"])
        canceled = await util.createBUTTON(btn=text["_canceledCB"])
        completed = await util.createBUTTON(btn=text["_completed"])
        
        fileType = "Zip" if callbackQuery.data.startswith("#p2img|zip") else "Tar"
        
        with fitz.open(input_file) as doc:
            directory = f'{cDIR}/pgs'
            os.mkdir(directory)
            number_of_pages = doc.page_count
            if callbackQuery.data.endswith("A") and number_of_pages <= 50: imageList = list(range(1, number_of_pages+1))
            elif callbackQuery.data.endswith("A"): imageList = list(range(1, 50))
            
            await dlMSG.edit(text=text["_total"].format(len(imageList)), reply_markup=cancel)
            mat = fitz.Matrix(2, 2)
            convertedPages = 0
            
            for i in imageList:
                page = doc.load_page(i-1)
                pix = page.get_pixmap(matrix = mat)
                convertedPages += 1
                if convertedPages % 5 == 0:
                    return await dlMSG.edit(text="`processing {}/{}` 😎".format(convertedPages, len(imageList)), reply_markup=canceled)
                    if not await work(callbackQuery, "check", False):
                        return await dlMSG.edit(text=text["_canceledAT"].format(convertedPages, len(imageList)), reply_markup=canceled)
                with open(f'{cDIR}/pgs/{i}.jpg','wb'):
                    pix.save(f'{cDIR}/pgs/{i}.jpg')
            
            output_path = f'{cDIR}/zipORtar.{fileType.lower()}'
        
            if data in ["zipA", "zipR", "zipS"]:
                shutil.make_archive(output_file, 'zip', directory)
            elif data in ["tarA", "tarR", "tarS"]:
                path = shutil.make_archive(output_file, 'tar', directory) 
        return True, output_path
    
    except Exception as Error:
        shutil.rmtree(f'{cDIR}/pgs')
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
