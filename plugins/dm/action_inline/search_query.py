# fileName: plugins/dm/action_inline/search_query.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/action_inline/search_query.py"

from plugins.utils.util   import *
from logger               import logger
from libgenesis           import Libgen
from pyrogram             import Client as ILovePDF
from pyrogram.types       import InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultCachedDocument

@ILovePDF.on_inline_query()
async def inline_query_handler(bot, inline_query):
    try:
        query = inline_query.query.strip()
        results = []
        
        lang_code = await getLang(inline_query.from_user.id)
        trCHUNK, _ = await translate(text="INLINE", lang_code=lang_code)
        
        if len(query) < 2:
            return await inline_query.answer(
                results=[],
                cache_time=0,
                switch_pm_text=trCHUNK['min'],
                switch_pm_parameter="okay",
           )
        else:
            if query:
                result = await Libgen(
                    result_limit=50).search(query=query,
                    return_fields=[
                        'title', 'pages', 'language', 'publisher', 'year', 'author',
                        'extension', 'coverurl', 'volumeinfo', 'mirrors', 'md5'
                    ]
                )
                if result is not None:
                    for id, item in enumerate(result):
                        results.append(
                            InlineQueryResultPhoto(
                                photo_url="https://te.legra.ph/file/8dfa3760df91a218a629c.jpg" if result[item]['coverurl'] is None else result[item]['coverurl'],
                                title=result[item]['title'],
                                id=f"{i}",
                                description=f"Author: {result[item]['author']}\n"
                                            f"Volume: {result[item]['volumeinfo']}   Year: {result[item]['year']}  Pages: {result[item]['pages']}\n"
                                            f"Language: {result[item]['language']}  Extension: {result[item]['extension']}\n"
                                            f"Publisher: {result[item]['publisher']}\n",
                                caption=f"MD5: {result[item]['md5']}\n"
                                        f"Title: **{result[item]['title']}.**\n"
                                        f"Author: **{result[item]['author']}.**",
                                reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(text=trCHUNK['process'], url="https://telegram.dog/ilovepdf_bot")]]
                                )
                            )
                        )
        if results:
            return await inline_query.answer(results=results, cache_time=60, is_personal=False)
        else:
            return await inline_query.answer(
                results=[],
                cache_time=0,
                switch_pm_text=trCHUNK['nothing'].format(query),
                switch_pm_parameter="okay",
            )
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(fileName, Error), exc_info = True)
