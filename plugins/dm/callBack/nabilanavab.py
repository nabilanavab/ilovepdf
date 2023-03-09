# fileName : plugins/dm/callBack/index.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/index.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

from plugins.utils    import *
from pyrogram         import enums, filters, Client as ILovePDF

help = filters.create(lambda _, __, query: query.data.startswith("nabilanavab"))
@ILovePDF.on_callback_query(help)
async def __index__(bot, callbackQuery):
    try:
        data = callbackQuery.data[11:]
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        
        text, _ = await util.translate(text = f"HELP['{data}']", lang_code = lang_code)
        
        await callbackQuery.answer(text, show_alert=True)
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        await work.work(callbackQuery, "delete", False)

# Author: @nabilanavab
