# fileName : plugins/dm/callBack/file_process/metadataPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/metadataPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger


import fitz
from plugins.utils  import *
from pyrogram       import enums

async def metadataPDF(input_file: str, cDIR: str, message) -> ( bool, str ):
    try:
        with fitz.open(input_file) as iNPUT:
            await message.reply_chat_action(enums.ChatAction.TYPING)
            pdfMetaData = "".join(f"`{i} : {iNPUT.metadata[i]}`\n" for i in iNPUT.metadata if iNPUT.metadata[i] != "") if iNPUT.metadata else ""
            return (True, pdfMetaData) if pdfMetaData!="" else (False, "") 
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
