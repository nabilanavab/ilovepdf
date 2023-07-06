# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

import fitz
from plugins.utils import *
from pyrogram import enums


async def metadataPDF(input_file: str, cDIR: str, message) -> (bool, str):
    try:
        with fitz.open(input_file) as iNPUT:
            await message.reply_chat_action(enums.ChatAction.TYPING)
            pdfMetaData = (
                "".join(
                    f"`{i} : {iNPUT.metadata[i]}`\n"
                    for i in iNPUT.metadata
                    if iNPUT.metadata[i] != ""
                )
                if iNPUT.metadata
                else ""
            )
            return (True, pdfMetaData) if pdfMetaData != "" else (False, "")

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
