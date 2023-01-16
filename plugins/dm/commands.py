# fileName : plugins/dm/commands.py
# copyright ©️ 2021 nabilanavab

import os, shutil
from pdf import PDF
from asyncio import sleep
from logger import logger
from pyrogram import enums
from pyrogram import filters
from plugins.work import work
from configs.config import dm, settings
from pyrogram import Client as ILovePDF
from plugins.util import getLang, translate

# ❌ CANCELS CURRENT PDF TO IMAGES WORK ❌
@ILovePDF.on_message((filters.private | filters.group) & filters.command(["cancel"]) & filters.incoming)
async def cancelP2I(bot, message):
    try:
        await work(message, "delete", True)
        return await message.delete()
    except Exception: pass

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message((filters.private | filters.group) & filters.command(["delete"]) & filters.incoming)
async def _cancelI2P(bot, message):
    try:
        lang_code = await getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        del PDF[message.chat.id]
        trans_txt, trans_btn = await translate( text = "GENERATE['deleteQueue']", lang_code = lang_code)
        await message.reply_text(trans_txt, quote = True)
        shutil.rmtree(f"work/{message.chat.id}")
    except Exception:
        trans_txt, trans_btn = await translate(text = "GENERATE['noQueue']", lang_code = lang_code)
        await message.reply_text(trans_txt, quote = True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
