# fileName : plugins/dm/action_inline/select_pdf.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/action_inline/select_pdf.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from configs.log     import log
from logger          import logger
from pyrogram        import Client as ILovePDF
from pyrogram.types  import InlineKeyboardButton, InlineKeyboardMarkup

@ILovePDF.on_chosen_inline_result()
async def chosen_inline_result(bot, chosen_inline_result):
    try:
        logger.debug(chosen_inline_result)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)

# Author: @nabilanavab
