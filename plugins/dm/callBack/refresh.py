# fileName : plugins/dm/callBack/refresh.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/refresh.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from plugins.utils             import *
from configs.db                import myID
from plugins.group.document    import gDOC
from ..photo                   import images
from .file_process.link        import decode
from logger                    import logger
from configs.config            import settings
from ..action_inline.in_bot    import openInBot
from ..document                import documents
from configs.db                import invite_link
from pyrogram                  import filters, Client as ILovePDF

@ILovePDF.on_callback_query(filters.regex("^refresh"))
async def _refresh(bot, callbackQuery):
    try:
        logger.debug(callbackQuery.data[7:])
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return
        
        if invite_link:
            userStatus = await bot.get_chat_member(str(settings.UPDATE_CHANNEL), callbackQuery.from_user.id)
            if userStatus.status == "kicked":
                await callbackQuery.answer("🤧")
        
        logger.debug(callbackQuery.data[7:])
        if callbackQuery.data.startswith("refresh-g"):    # this means "refresh-g{code}
            await decode(bot, callbackQuery.data[9:], callbackQuery.message, lang_code, cb=True)
            return await callbackQuery.message.delete()
        
        elif callbackQuery.data.startswith("refresh-m"):    # this means "refresh-g{code}
            await openInBot(bot, callbackQuery.message, callbackQuery.data.split("-m"))
            return await callbackQuery.message.delete()
        
        elif callbackQuery.message.reply_to_message.text == "/start":
            tTXT, tBTN = await util.translate(text="HOME['HomeA']", button="HOME['HomeACB']", lang_code=lang_code, order=2121)
            await callbackQuery.edit_message_caption(
                caption=tTXT.format(callbackQuery.from_user.mention, myID[0].mention), reply_markup=tBTN
            )
            return await callbackQuery.message.reply_to_message.delete()
        
        elif await work.work(callbackQuery, "check", False):
            tTXT, _ = await util.translate(text = "PROGRESS['workInP']", lang_code = lang_code)
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
        tTXT, _ = await util.translate(text="BAN['Fool']", lang_code=lang_code)
        return await callbackQuery.answer(tTXT, show_alert=True)
