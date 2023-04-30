# fileName: plugins/dm/action_inline/search_query.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/action_inline/search_query.py"

from logger          import logger
from libgenesis      import Libgen
from pyrogram        import Client as ILovePDF
from pyrogram.types  import InlineQueryResultPhoto, InputTextMessageContent, InlineQueryResultCachedDocument

@ILovePDF.on_inline_query()
async def inline_query_handler(bot, inline_query):
    try:
        query = inline_query.query.strip()
        results = []
        
        if len(query) < 2:
            return await inline_query.answer(
                results=[],
                cache_time=0,
                switch_pm_text='You must enter at least 2 characters to search',
                switch_pm_parameter="okay",
           )
        
        elif query.startswith("dl:"):
            """query = query.split(':')[1].strip()
            q_res_data = await BookdlFiles().get_file_by_name(query, 50)
            if q_res_data:
                for file in q_res_data:
                    results.append(
                        InlineQueryResultCachedDocument(
                            id=str(file['_id']),
                            document_file_id=file['file_id'],
                            caption=file['title'],
                            title=file['title'],
                            description=f"File Name: {file['file_name']}\n"
                            f"File Type: {file['file_type']}",
                        )
                    )
            """
        else:
            if query:
                result = await Libgen(result_limit=50
                                      ).search(query=query,
                                           return_fields=[
                                               'title', 'pages', 'language',
                                               'publisher', 'year', 'author',
                                               'extension', 'coverurl',
                                               'volumeinfo', 'mirrors', 'md5'
                                           ])
                if result is not None:
                    for item in result:
                        results.append(
                            InlineQueryResultPhoto(
                                title=result[item]['title'],
                                description=f"Author: {result[item]['author']}\n"
                                f"Volume: {result[item]['volumeinfo']}   Year: {result[item]['year']}  Pages: {result[item]['pages']}\n"
                                f"Language: {result[item]['language']}  Extension: {result[item]['extension']}\n"
                                f"Publisher: {result[item]['publisher']}\n",
                                caption=message_text=f"MD5: {result[item]['md5']}\n"
                                        f"Title: **{result[item]['title']}.**\n"
                                        f"Author: **{result[item]['author']}.**"),
                                photo_url="https://te.legra.ph/file/8dfa3760df91a218a629c.jpg" if result[item]['coverurl'] is None else result[item]['coverurl'],
                                reply_markup = InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(text="⚙️ Processing.. ", callback_data=f"nabilanavab")]]
                                )
                            )

        if results:
            return await inline_query.answer(results=results, cache_time=60, is_personal=False)
        else:
            return await inline_query.answer(
                results=[],
                cache_time=0,
                switch_pm_text=f'🤐 No results for "{query}"',
                switch_pm_parameter="okay",
            )
        
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(fileName, Error), exc_info = True)
