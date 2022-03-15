# fileName : Plugins/dm/delete.py
# copyright ©️ 2021 nabilanavab

import os
import shutil
from pdf import PDF
from pyrogram import filters
from pyrogram import Client as ILovePDF

#--------------->
#--------> DELETS CURRENT IMAGES TO PDF QUEUE (/delete)
#------------------->

@ILovePDF.on_message(filters.command(["delete"]))
async def _cancelI2P(bot, message):
    try:
        await message.reply_chat_action("typing")
        del PDF[message.chat.id]
        await message.reply_text("`Queue deleted Successfully..`🤧", quote=True)
        shutil.rmtree(f"{message.chat.id}")
    except Exception:
        await message.reply_text("`No Queue founded..`😲", quote=True)

#                                                                                  Telegram: @nabilanavab
