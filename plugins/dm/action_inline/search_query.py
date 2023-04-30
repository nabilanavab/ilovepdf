# fileName: plugins/dm/action_inline/search_query.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/action_inline/search_query.py"


from libgenesis      import Libgen
from pyrogram        import Client as ILovePDF


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
            query = query.split(':')[1].strip()
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
        else:
            if query:
                result = await Libgen(result_limit=50
                                      ).search(query=q,
                                           return_fields=[
                                               'title', 'pages', 'language',
                                               'publisher', 'year', 'author',
                                               'extension', 'coverurl',
                                               'volumeinfo', 'mirrors', 'md5'
                                           ])
                if result is not None:
                    for item in result:
                        results.append(
                            InlineQueryResultArticle(
                                title=result[item]['title'],
                                description=f"Author: {result[item]['author']}\n"
                                f"Volume: {result[item]['volumeinfo']}   Year: {result[item]['year']}  Pages: {result[item]['pages']}\n"
                                f"Language: {result[item]['language']}  Extension: {result[item]['extension']}\n"
                                f"Publisher: {result[item]['publisher']}\n",
                                thumb_url="https://te.legra.ph/file/8dfa3760df91a218a629c.jpg" if result[item]['coverurl'] is None else result[item]['coverurl'],
                                input_message_content=InputTextMessageContent(
                                    message_text=f"MD5: {result[item]['md5']}\n"
                                    f"Title: **{result[item]['title']}.**\n"
                                    f"Author: **{result[item]['author']}.**"),
                                    reply_markup=None
                                )
                            )

        if results:
            return await inline_query.answer(results=results, cache_time=60, is_personal=False)
        else:
            return await inline_query.answer(
                results=[],
                cache_time=0,
                switch_pm_text=f'{emoji.CROSS_MARK} No results for "{query}"',
                switch_pm_parameter="okay",
            )
        
    except Exception as Error:
        logger.debug(Error)
