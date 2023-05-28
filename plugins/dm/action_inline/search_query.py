# fileName: plugins/dm/action_inline/search_query.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/action_inline/search_query.py"

from plugins.utils.util   import *
from configs.log          import log
from .                    import DATA
from logger               import logger
from libgenesis           import Libgen
from default              import default_ans
from plugins.utils.util   import getLang, translate
from pyrogram             import Client as ILovePDF, errors
from pyrogram.types       import InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultCachedDocument

@ILovePDF.on_inline_query()
async def inline_query_handler(bot, inline_query):
    try:
        query = inline_query.query.strip()
        results = []
        
        lang_code = await getLang(inline_query.from_user.id)
        trCHUNK, _ = await translate(text="INLINE", lang_code=lang_code)
        
        # Inline feature will not work if there is no log channel set up.
        if not log.LOG_CHANNEL:
            return await inline_query.answer(
                results=[],
                cache_time=0,
                switch_pm_text=trCHUNK['noDB'],
                switch_pm_parameter="okay",
           )
        
        if len(query) < 2:
            result = await default_ans(inline_query)
            return await inline_query.answer(
                results=result,
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
                    DATA[inline_query.from_user.id] = {}
                    for id, item in enumerate(result, start=1):
                        results.append(
                            InlineQueryResultPhoto(
                                photo_url="https://te.legra.ph/file/8dfa3760df91a218a629c.jpg" if result[item]['coverurl'] is None else result[item]['coverurl'],
                                title=result[item]['title'],
                                id=f"{id}",
                                description=trCHUNK['description'].format(
                                    result[item]['author'], result[item]['volumeinfo'], result[item]['year'], result[item]['pages'],
                                    result[item]['language'], result[item]['extension'], result[item]['publisher']
                                ),
                                caption=trCHUNK['caption'].format(
                                    result[item]['md5'], result[item]['title'], result[item]['author'], result[item]['volumeinfo'], result[item]['year'],
                                    result[item]['pages'], result[item]['language'], result[item]['publisher']
                                ),
                                reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(text=trCHUNK['process'], url="https://telegram.dog/ilovepdf_bot")]]
                                )
                            )
                        )
                        DATA[inline_query.from_user.id][id] = {
                            'thumb':"https://te.legra.ph/file/8dfa3760df91a218a629c.jpg" if result[item]['coverurl'] is None else result[item]['coverurl'],
                            'caption':f"MD5: {result[item]['md5']}\n"
                                      f"Title: **{result[item]['title']}.**\n"
                                      f"Author: **{result[item]['author']}.**"
                        }
        if results:
            return await inline_query.answer(results=results, cache_time=60, is_personal=False)
        else:
            return await inline_query.answer(
                results=[],
                cache_time=0,
                switch_pm_text=trCHUNK['nothing'].format(query),
                switch_pm_parameter="okay",
            )
    
    except errors.QueryIdInvalid:
        pass
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(fileName, Error), exc_info = True)
