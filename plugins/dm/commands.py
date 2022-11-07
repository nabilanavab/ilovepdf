# fileName : plugins/dm/commands.py
# copyright ©️ 2021 nabilanavab

import os, shutil
from pdf import PDF
from pdf import PROCESS
from asyncio import sleep
from logger import logger
from pyrogram import enums
from pyrogram import filters
from configs.config import dm, settings
from pyrogram import Client as ILovePDF
from plugins.util import getLang, translate

# ❌ CANCELS CURRENT PDF TO IMAGES WORK ❌
@ILovePDF.on_message((filters.private | filters.group) & filters.command(["cancel"]) & filters.incoming)
async def cancelP2I(bot, message):
    try:
        PROCESS.remove(message.from_user.id)
        await message.delete()          # delete /cancel if process canceled
    except Exception:
        try:
            await message.reply_chat_action(enums.ChatAction.TYPING)
            await message.reply_text('🤔', quote=True)
        except Exception: pass

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message((filters.private | filters.group) & filters.command(["delete"]) & filters.incoming)
async def _cancelI2P(bot, message):
    try:
        lang_code = await getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        del PDF[message.chat.id]
        trans_txt, trans_btn = await translate( text="GENERATE['deleteQueue']", lang_code=lang_code)
        await message.reply_text(trans_txt,quote=True)
        shutil.rmtree(f"{message.chat.id}")
    except Exception:
        trans_txt, trans_btn = await translate( text="GENERATE['noQueue']", lang_code=lang_code)
        await message.reply_text(trans_txt, quote=True)

@ILovePDF.on_message((filters.private | filters.group) & filters.command("help") & filters.incoming)
async def _help(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await getLang(message.chat.id)
        trans_txt, trans_btn = await translate(text="document['process']", lang_code=lang_code)
        helpMsg = await message.reply(trans_txt ,quote=True)
        await sleep(1)
        userHELP, CB = await translate(text="HELP_CMD['userHELP']", button="HELP_CMD['CB']", lang_code=lang_code)
        HELP = userHELP
        await helpMsg.edit(HELP, reply_markup=CB)
        if message.from_user.id in dm.ADMINS:
            adminHelp, _ = await translate(text="HELP_CMD['adminHelp']", lang_code=lang_code)
            await sleep(2)
            HELP = userHELP + adminHelp
            await helpMsg.edit(HELP, reply_markup=CB)
        await sleep(1)
        footer, _footer = await translate(text="HELP_CMD['footerHelp']", lang_code=lang_code)
        HELP += footer
        await helpMsg.edit(HELP, reply_markup=CB, disable_web_page_preview=True)
    except Exception as e:
        logger.exception("/HELP:CAUSES %(e)s ERROR", exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
