# fileName: plugins/dm/callBack/inline_query/setLang.py
# copyright ©️ 2021 nabilanavab

from logger          import logger
from lang            import langList
from plugins.util    import *
from configs.config  import images
from pyrogram        import Client as ILovePDF
from pyrogram.types  import (InputTextMessageContent, InlineKeyboardMarkup,
                             InlineKeyboardButton, InlineQueryResultPhoto)

myID = None

@ILovePDF.on_inline_query()
async def setLang(bot, inline_query):
    try:
        global myID
        if not myID:
            myID = await bot.get_me()
        lang_code = await getLang(inline_query.from_user.id)
        CHUNK, _ = await translate(text="inline_query", lang_code=lang_code)
        
        BUTTON1 = CHUNK['TOP']
        _lang = { langList[lang][1]:f"https://t.me/{myID.username}?start=-l{lang}" for lang in langList }
        BUTTON1.update(_lang); BUTTON1.update({"♻" : "-|refresh"})
        BUTTON1 = await createBUTTON(btn=BUTTON1, order=int(f"1{((len(BUTTON1)-2)//3)*'3'}{(len(BUTTON1)-2)%3}1"))
        
        BUTTON2 = CHUNK['TOP']
        __lang = { langList[lang][1]:f"https://t.me/{myID.username}?start=-l{lang}-r{inline_query.from_user.id}" for lang in langList }
        BUTTON2.update(__lang)
        BUTTON2 = await createBUTTON(btn=BUTTON2, order=int(f"1{((len(BUTTON2)-1)//3)*'3'}{(len(BUTTON2)-1)%3}"))
        
        await inline_query.answer(
            results = [
                InlineQueryResultPhoto(
                    photo_url = images.THUMBNAIL_URL, title = "i ❤ PDF", reply_markup = BUTTON1,
                    input_message_content = InputTextMessageContent("set Language 🌐"),
                    caption = CHUNK['capt'], description = CHUNK['des']
                ),
                InlineQueryResultPhoto(
                    photo_url = images.THUMBNAIL_URL, title = "i ❤ PDF | referal", reply_markup = BUTTON2,
                    input_message_content = InputTextMessageContent("set Language: 🌐"),
                    caption = CHUNK['capt'], description = CHUNK['des']
                )
            ]
        )
    except Exception as e:
        logger.debug("Error in inline_query: %s" %(e), exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
