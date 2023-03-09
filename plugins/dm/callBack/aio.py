# fileName : plugins/dm/callBack/aio.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/aio.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

aio = filters.create(lambda _, __, query: query.data.startswith("aio"))
@ILovePDF.on_callback_query(aio)
async def _pdf(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return
        
        await callbackQuery.answer()
        data = data.split("|", 1)[1]
        
        if data == "aio":
            tTXT, tBTN = await util.translate(text="AIO['aio']", button = "AIO['aio_button']", order = 22222221, lang_code = lang_code)
            return await callbackQuery.message.edit(
                text=tTXT.format(callbackQuery.message.reply_to_message.document.file_name, 
                                 await render.gSF(callbackQuery.message.reply_to_message.document.file_size)),
                reply_markup = tBTN
            )
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)

# Author: @nabilanavab
