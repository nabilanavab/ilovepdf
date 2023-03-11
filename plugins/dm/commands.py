# fileName : plugins/dm/commands.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/commands.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

import os, shutil
from plugins.utils   import *
from configs.config  import dm 
from pdf             import PDF
from configs.beta    import BETA
from configs.db      import dataBASE
from pyrogram        import Client as ILovePDF, enums, filters

if dataBASE.MONGODB_URI:
    from database import db

# ❌ CANCELS CURRENT PDF TO IMAGES WORK ❌
@ILovePDF.on_message((filters.private | filters.group) & filters.command(["cancel"]) & filters.incoming)
async def cancelP2I(bot, message):
    try:
        await work.work(message, "delete", True)
        return await message.delete()
    except Exception: pass

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message((filters.private | filters.group) & filters.command(["delete"]) & filters.incoming)
async def _cancelI2P(bot, message):
    try:
        lang_code = await util.getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        del PDF[message.chat.id]
        trans_txt, trans_btn = await util.translate( text = "GENERATE['deleteQueue']", lang_code = lang_code)
        await message.reply_text(trans_txt, quote = True)
        shutil.rmtree(f"work/{message.chat.id}")
    except Exception as e:
        logger.exception("🐞 %s : %s" %(file_name, Error))
        trans_txt, trans_btn = await util.translate(text = "GENERATE['noQueue']", lang_code = lang_code)
        await message.reply_text(trans_txt, quote = True)

# ❌ BETA USER (/beta) ❌
@ILovePDF.on_message(filters.private & filters.command(["beta"]) & filters.incoming)
async def _betaMode(bot, message):
    try:
        if message.chat.id in dm.ADMINS:
            logger.debug(f"Beta Users:\n\n{BETA}\n\n")
        if message.chat.id not in BETA:
            await db.set_key(id=message.chat.id, key="beta", value="True")
            BETA.append(message.chat.id)
            return await message.reply_text("`Now you are a beta user..` ☺", quote = True)
        else:
            await db.dlt_key(id=message.chat.id, key="banned")
            BETA.remove(message.chat.id)
            return await message.reply_text("`Now you are not part in beta test..` 😐", quote = True)
    except Exception as Error:
        logger.exception("🐞 %s : %s" %(file_name, Error))

# Author: @nabilanavab
