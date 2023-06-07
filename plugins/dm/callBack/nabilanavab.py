# fileName : plugins/dm/callBack/index.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/index.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

from plugins.utils    import *
from pyrogram         import filters, Client as ILovePDF

@ILovePDF.on_callback_query(filters.regex("^nabilanavab"))
async def __index__(bot, callbackQuery):
    try:
        data = callbackQuery.data.split("|", 1)[1]  # "nabilanavab|"
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        
        if data.startswith("aio"):
            text, _ = await util.translate(text = f"_CLICK_RIGHT", lang_code = lang_code)
        else:
            text, _ = await util.translate(text = f"HELP['{data}']", lang_code = lang_code)
        
        await callbackQuery.answer(text, show_alert=True)
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        await work.work(callbackQuery, "delete", False)

# Author: @nabilanavab
