# fileName : plugins/utilsfncta.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/utils/fncta.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

import os
from configs.db     import *
from PIL            import Image
from pyrogram.enums import ChatType
from configs.config import settings, images

# THUMBNAIL METADATA
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

if dataBASE.MONGODB_URI:
    from database import db

# return thumbnail height
async def thumbMeta(thumbPath: str):
    try:
        metadata = extractMetadata(createParser(thumbPath))
        if metadata.has("height"):
            return metadata.get("height")
        else:
            return 0
    except Exception as e:
        logger.exception("1️⃣: 🐞 %s /close: %s" %(file_name, e))

# photo_id -> local image
async def formatThumb(location):
    try:
        height = await thumbMeta(location)
        Image.open(location).convert("RGB").save(location)
        img = Image.open(location)
        img.resize((320, height))
        img.save(location, "JPEG")
        return location
    except Exception as e:
        logger.exception("2️⃣: 🐞 %s /close: %s" %(file_name, e))

# return thumbnail and fileName
async def thumbName(message, fileName, getAPI=False):
    try:
        chat_type = message.chat.type; chat_id = message.chat.id
        fileNm, fileExt = os.path.splitext(fileName)
        
        if (dataBASE.MONGODB_URI):
            info = await db.get_user_data(chat_id)
        
        if settings.DEFAULT_NAME:
            FILE_NAME = settings.DEFAULT_NAME + fileExt
        elif dataBASE.MONGODB_URI and info and info.get('fname', 0):
            FILE_NAME = info["fname"] + fileExt
        else:
            FILE_NAME = fileName
        
        if settings.DEFAULT_CAPT:
            FILE_CAPT = settings.DEFAULT_CAPT
        elif dataBASE.MONGODB_URI and info and info.get('capt', 0):
            FILE_CAPT = info["capt"]
        else:
            FILE_CAPT = ""
        
        if dataBASE.MONGODB_URI:
            if chat_type == ChatType.PRIVATE and message.chat.id in CUSTOM_THUMBNAIL_U:
                THUMBNAIL = info["thumb"]
            else:
                 THUMBNAIL = images.PDF_THUMBNAIL
        else:
            THUMBNAIL = images.PDF_THUMBNAIL
        
        if not getAPI:
             return FILE_NAME, FILE_CAPT, THUMBNAIL
        else:
            return FILE_NAME, FILE_CAPT, THUMBNAIL, info.get('api', 0)
        
    except Exception as Error:
        logger.exception("3️⃣: 🐞 %s /close: %s" %(file_name, Error))

# Author: @nabilanavab
