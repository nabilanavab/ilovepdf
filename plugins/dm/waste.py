# fileName : plugins/dm/waste.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/waste.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from plugins.utils  import *
from configs.config import dm 
from logger         import logger
from pyrogram       import Client as ILovePDF, enums, filters

# ==========================| WASTE/DPAMMING MESSAGES |============================
@ILovePDF.on_message(filters.private & filters.incoming & ~filters.user(dm.ADMINS))
async def _spam(bot, message):
    try:
        lang_code = await util.getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        tTXT, tBTN = await util.translate(text = "noHelp", lang_code = lang_code)
        await message.reply_text(tTXT, quote = True)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(file_name, e), exc_info = True)

# Author: @nabilanavab
