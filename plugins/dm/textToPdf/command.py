file_name = "plugins/dm/textToPdf/command.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

from plugins.utils       import *
from .                   import TXT
from logger              import logger
from pyrogram            import filters, Client as ILovePDF, enums
        
@ILovePDF.on_message(filters.private & filters.command(["txt2pdf"]) & filters.incoming)
async def text2PDF(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await getLang(message.chat.id)
        tTXT, tBTN = await translate(text="pdf2TXT['TEXT']", button="pdf2TXT['font_btn']", order=12121, lang_code=lang_code)
        await message.reply_text(text=tTXT, reply_markup=tBTN)
        await message.delete()
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info=True)

# SOURCE CODE: https://github.com/nabilanavab/ilovepdf
