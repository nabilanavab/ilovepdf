# fileName : plugins/dm/waste.py
# copyright ©️ 2021 nabilanavab

from logger import logger
from plugins.util import *
from configs.config import dm 
from pyrogram import enums, filters
from pyrogram import Client as ILovePDF

# ===========================================| WASTE/DPAMMING MESSAGES |==================================================================================================
@ILovePDF.on_message(filters.private & filters.incoming & ~filters.user(dm.ADMINS))
async def _spam(bot, message):
    try:
        lang_code = await getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        tTXT, tBTN = await translate(text="noHelp", lang_code=lang_code)
        await message.reply_text(tTXT, quote=True)
    except Exception as e:
        logger.exception("plugins/dm/waste: %s" %(e), exc_info=True)

# ======================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
