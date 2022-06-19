# fileName : plugins/thumbName.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: INFO [!= DEBUG COZ LOTS OF PIL SERVICE MSG]
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.INFO,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
from PIL import Image
from pyrogram import Client
from pyrogram.types import Message
from configs.db import isMONGOexist
from configs.images import DEFAULT_NAME    # DEFAULT NAME
from configs.images import PDF_THUMBNAIL   # DEFAULT THUMBNAIL
from configs.images import CUSTOM_THUMBNAIL_U, CUSTOM_THUMBNAIL_C

# THUMBNAIL METADATA
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

if isMONGOexist:
    from database import db

changeNAME = False
if DEFAULT_NAME:
   changeNAME = True

# return thumbnail height
async def thumbMeta(thumbPath: str):
    try:
        metadata = extractMetadata(createParser(thumbPath))
        if metadata.has("height"):
            return metadata.get("height")
        else:
            return 0
    except Exception as e:
        logger.exception(
                        "THUMB_META:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

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
        logger.exception(
                        "LOCAL_THUMB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# return thumbnail and fileName
async def thumbName(message, fileName):
    try:
        chat_type = message.chat.type
        fileNm, fileExt = os.path.splitext(fileName)
        if changeNAME:
            SET_DEFAULT_NAME = DEFAULT_NAME + fileExt
        
        # if no mongoDB return False [default thumbnail ]
        if not isMONGOexist:
            # id no DEFAULT_NAME, use current file name 
            if changeNAME:
                return PDF_THUMBNAIL, SET_DEFAULT_NAME
            else:
                return PDF_THUMBNAIL, fileName
        
        # user with thumbnail
        if chat_type == "private" and message.chat.id in CUSTOM_THUMBNAIL_U:
            thumbnail = await db.get_thumbnail(message.chat.id)
        elif chat_type in ["group", "supergroup"] and message.chat.id in CUSTOM_THUMBNAIL_C:
            thumbnail = await db.get_group_thumb(message.chat.id)
        else:
            thumbnail = PDF_THUMBNAIL
        
        if changeNAME:
            return thumbnail, SET_DEFAULT_NAME
        else:
            return thumbnail, fileName
    
    except Exception as e:
        logger.exception(
                        "THUMB_NAME:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                         Telegram: @nabilanavab
