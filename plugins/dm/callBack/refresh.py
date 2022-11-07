# fileName : plugins/dm/callBack/refresh.py
# copyright ©️ 2021 nabilanavab 

from pdf import PROCESS
from ..photo import images
from plugins.util import *
from ..document import documents
from configs.db import invite_link
from configs.config import settings
from pyrogram import filters, Client as ILovePDF

refresh = filters.create(lambda _, __, query: query.data == "refresh")
@ILovePDF.on_callback_query(refresh)
async def _refresh(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        if len(invite_link) != 0:
            userStatus = await bot.get_chat_member(str(settings.UPDATE_CHANNEL), callbackQuery.from_user.id)
            if userStatus.status == "kicked":
                await callbackQuery.answer("🤧")
        
        if callbackQuery.message.reply_to_message.text == "/start":
            tTXT, tBTN = await translate(text="HOME['HomeA']", button="HOME['HomeACB']", lang_code=lang_code)
            await callbackQuery.edit_message_caption(caption = tTXT, reply_markup = tBTN)
            return await callbackQuery.message.reply_to_message.delete()
        
        if callbackQuery.from_user.id in PROCESS:
            tTXT, _ = await translate(text="PROGRESS['workInP']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        
        if callbackQuery.message.reply_to_message.document:
            await callbackQuery.message.delete()
            return await documents(bot, callbackQuery.message.reply_to_message)
        
        elif callbackQuery.message.reply_to_message.photo:
            await callbackQuery.message.delete()
            return await images(bot, callbackQuery.message.reply_to_message)
    
    except Exception as e:
        tTXT, _ = await translate(text="BAN['Fool']", lang_code=lang_code)
        return await callbackQuery.answer(tTXT, show_alert=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
