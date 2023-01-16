# fileName : plugins/dm/callBack/refresh.py
# copyright ©️ 2021 nabilanavab 
fileName = "plugins/dm/callBack/refresh.py"

from plugins.util              import *
from configs.db                import myID
from plugins.work              import work
from plugins.group.document    import gDOC
from .link                     import decode
from ..photo                   import images
from plugins.render            import header
from configs.config            import settings
from ..document                import documents
from configs.db                import invite_link
from pyrogram                  import filters, Client as ILovePDF

refresh = filters.create(lambda _, __, query: query.data.startswith("refresh"))

@ILovePDF.on_callback_query(refresh)
async def _refresh(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        if await header(bot, callbackQuery, lang_code=lang_code):
            return
        
        if len(invite_link) != 0:
            userStatus = await bot.get_chat_member(
                str(settings.UPDATE_CHANNEL), callbackQuery.from_user.id
            )
            if userStatus.status == "kicked":
                await callbackQuery.answer("🤧")
        
        if callbackQuery.data.startswith("refresh-g"):    # this means "refresh-g{code}
            await decode(bot, callbackQuery.data[7:], [callbackQuery.message, "message"], lang_code)
            return await callbackQuery.message.delete()
        
        elif callbackQuery.message.reply_to_message.text == "/start":
            tTXT, tBTN = await translate(
                text = "HOME['HomeA']", button = "HOME['HomeACB']", lang_code = lang_code, order = 2121
            )
            await callbackQuery.edit_message_caption(
                caption = tTXT.format(
                    callbackQuery.from_user.mention, myID[0].mention
                ),
                reply_markup = tBTN
            )
            return await callbackQuery.message.reply_to_message.delete()
        
        elif await work(callbackQuery, "check", False):
            tTXT, _ = await translate(text = "PROGRESS['workInP']", lang_code = lang_code)
            return await callbackQuery.answer(tTXT)
        
        elif callbackQuery.message.reply_to_message.document:
            await callbackQuery.message.delete()
            return await documents(bot, callbackQuery.message.reply_to_message)
        
        elif callbackQuery.message.reply_to_message.photo:
            await callbackQuery.message.delete()
            return await images(bot, callbackQuery.message.reply_to_message)
        
        elif callbackQuery.message.reply_to_message.text.startswith("/"):
            await callbackQuery.message.delete()
            return await gDOC(bot, callbackQuery.message.reply_to_message)
        
        elif callbackQuery.message.reply_to_message.text:
            await callbackQuery.message.delete()
            return await _url(bot, callbackQuery.message.reply_to_message)
    
    except Exception as e:
        logger.debug(f"{callbackQuery.from_user.id} : {e}")
        tTXT, _ = await translate(text = "BAN['Fool']", lang_code = lang_code)
        return await callbackQuery.answer(tTXT, show_alert = True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
