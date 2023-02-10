# fileName: plugins/dm/callBack/inline_query/query.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/inline_query/query.py"

from logger          import logger
from configs.db      import myID
from pyrogram.types  import (InputTextMessageContent, InlineKeyboardMarkup,
                             InlineKeyboardButton, InlineQueryResultPhoto)

async def create_result(datas, query):
    """This function will sort the data for inline query search results"""
    # datas = id, href, alt, thumb, title
    
    results = [
        InlineQueryResultPhoto(
            photo_url = f"{datas[i]['thumb']}",
            title = f"{datas[i]['title']}",
            description = f"{datas[i]['span']}",
            id = f"{i}",
            caption = f"**ID**: __{datas[i]['id']}__\n"
                      f"**TITLE** : __{datas[i]['title']}__",
            reply_markup = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        text = "⚙️ Processing.. ",
                        callback_data = f"nabilanavab"
                    ),
                ]]
            )
        ) for i, data in enumerate(datas.items(), start=1)
    ]
    
    return results
    
