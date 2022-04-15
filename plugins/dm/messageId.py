# fileName : Plugins/dm/messageId.py
# copyright ©️ 2021 nabilanavab

from pyrogram import filters
from pyrogram import Client as ILovePDF

#--------------->
#--------> Gets MESSAGE ID
#------------------->

@ILovePDF.on_message(filters.command(["message"]))
async def _cancelI2P(bot, message):
    try:
        await message.reply_chat_action("typing")
        await message.reply_text(f"message_id: `{message.message_id}` 🎭", quote=True)
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
