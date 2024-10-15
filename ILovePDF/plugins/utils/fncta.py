# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab


file_name: str = "ILovePDF/plugins/utils/fncta.py"

from plugins import *
from PIL import Image
from configs.db import *
from pyrogram.enums import ChatType
from hachoir.parser import createParser
from configs.config import settings, images
from hachoir.metadata import extractMetadata

if dataBASE.MONGODB_URI:
    from database import db


# return thumbnail height
async def thumbMeta(thumbPath: str) -> str:
    try:
        metadata = extractMetadata(createParser(thumbPath))
        metadata.get("height", 0)

    except Exception as Error:
        logger.exception("1️⃣: 🐞 %s : %s" % (file_name, Error))


# Converts a local image to a JPEG thumbnail
async def formatThumb(location: str) -> str:
    try:
        height = await thumbMeta(location)
        Image.open(location).convert("RGB").save(location)
        img = Image.open(location)

        # Resize the image while maintaining the aspect ratio
        img.resize((320, height))
        img.save(location, "JPEG")

        return location
    
    except Exception as Error:
        logger.exception("2️⃣: 🐞 %s: %s" % (file_name, Error))


# Returns thumbnail details and file name
async def thumbName(message, fileName: str, getAPI: str = False) -> tuple:
    try:
        chat_type: str = message.chat.type
        chat_id: int = message.chat.id
        fileNm, fileExt = os.path.splitext(fileName)

        if dataBASE.MONGODB_URI:
            info = await db.get_user_data(chat_id)
        
        # Determine the file name based on settings or user data
        if settings.DEFAULT_NAME:
            FILE_NAME = settings.DEFAULT_NAME + fileExt
        elif dataBASE.MONGODB_URI and info and info.get("fname", 0):
            FILE_NAME = info["fname"] + fileExt
        else:
            FILE_NAME = fileName
        
        # Determine the caption based on settings or user data
        if settings.DEFAULT_CAPT:
            FILE_CAPT = settings.DEFAULT_CAPT
        elif dataBASE.MONGODB_URI and info and info.get("capt", 0):
            FILE_CAPT = info["capt"]
        else:
            FILE_CAPT = ""

        # Determine the thumbnail based on chat type and user data
        if dataBASE.MONGODB_URI:
            if chat_type == ChatType.PRIVATE and message.chat.id in CUSTOM_THUMBNAIL_U:
                THUMBNAIL = info["thumb"]
            else:
                THUMBNAIL = images.PDF_THUMBNAIL
        else:
            THUMBNAIL = images.PDF_THUMBNAIL

        return (
            FILE_NAME, FILE_CAPT, THUMBNAIL
        ) if not getAPI else (
            FILE_NAME, FILE_CAPT, THUMBNAIL, info.get("api", 0)
        )

    except Exception as Error:
        logger.exception("3️⃣: 🐞 %s : %s" % (file_name, Error))


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD